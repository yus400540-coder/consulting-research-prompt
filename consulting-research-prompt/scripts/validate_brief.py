"""Validate review-only consulting research briefs without external side effects."""

import argparse
import json
from pathlib import Path
import re
from typing import Any, Dict, List


REQUIRED_TOP_LEVEL_FIELDS = (
    "schema_version", "status", "generated_at", "input", "identity", "classification",
    "decision", "scope", "issue_tree", "hypotheses", "source_plan", "client_requests",
    "deliverables", "risks", "open_questions", "execution_prompt", "review",
)
ALLOWED_STATUSES = {"draft", "needs-review"}
ALLOWED_SOURCE_ROUTES = {
    "public-available", "public-partial", "client-required", "proxy-available", "unknown",
}
HYPOTHESIS_FIELDS = ("id", "statement", "priority", "kill_test", "required_evidence")
CLIENT_REQUEST_FIELDS = (
    "priority", "item", "period", "granularity", "reason", "decision_affected",
    "sensitivity", "substitute", "consequence_if_missing",
)
REQUIRED_PROMPT_SECTIONS = (
    "Review warning",
    "Client and decision",
    "Verified identity plus assumptions",
    "Scope/exclusions",
    "MECE issue tree",
    "Hypotheses/kill tests",
    "Public source plan",
    "Client request list",
    "Analysis sequence",
    "Deliverables",
    "Full research-to-obsidian Vault rules",
    "Scope/evidence/publication gates",
    "Retrieval and audit acceptance",
)


def _has_content(value: Any) -> bool:
    """Return whether a required text or collection field has usable content."""
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict, set)):
        return bool(value)
    return False


def _prompt_sections(prompt: str):
    """Return non-empty required Markdown sections, or None for a bad contract."""
    comparable = prompt.replace("`", "")
    matches = []
    for number, title in enumerate(REQUIRED_PROMPT_SECTIONS, 1):
        match = re.search(
            rf"(?m)^#{{1,6}}\s+{number}\.\s+{re.escape(title)}\s*$",
            comparable,
        )
        if match is None:
            return None
        matches.append((title, match))
    if [match.start() for _, match in matches] != sorted(match.start() for _, match in matches):
        return None
    sections = {}
    for index, (title, match) in enumerate(matches):
        end = matches[index + 1][1].start() if index + 1 < len(matches) else len(comparable)
        body = comparable[match.end():end].strip()
        if not body:
            return None
        sections[title] = body
    return sections


def validate_brief(data: dict) -> List[str]:
    """Return stable validation errors for a review brief without changing *data*."""
    if not isinstance(data, dict):
        return ["brief must be a JSON object"]

    errors = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"missing top-level field: {field}")

    if "schema_version" in data and not (
        type(data["schema_version"]) is int and data["schema_version"] == 1
    ):
        errors.append("schema_version must equal 1")
    if "status" in data and (
        not isinstance(data["status"], str) or data["status"] not in ALLOWED_STATUSES
    ):
        errors.append("status must be draft or needs-review")

    input_data = data.get("input")
    if "input" in data:
        if not isinstance(input_data, dict):
            errors.append("input must be an object")
        else:
            if not _has_content(input_data.get("company")):
                errors.append("input.company must be non-empty")
            if not _has_content(input_data.get("question")):
                errors.append("input.question must be non-empty")

    review = data.get("review")
    if "review" in data:
        if not isinstance(review, dict):
            errors.append("review must be an object")
        elif "status" in data and review.get("status") != data.get("status"):
            errors.append("review.status must match status")

    source_plan = data.get("source_plan")
    if "source_plan" in data:
        if not isinstance(source_plan, list):
            errors.append("source_plan must be a list")
        else:
            for index, source in enumerate(source_plan):
                route = source.get("route") if isinstance(source, dict) else None
                if not isinstance(route, str) or route not in ALLOWED_SOURCE_ROUTES:
                    errors.append(f"source_plan[{index}].route is invalid")

    hypotheses = data.get("hypotheses")
    if "hypotheses" in data:
        if not isinstance(hypotheses, list):
            errors.append("hypotheses must be a list")
        else:
            for index, hypothesis in enumerate(hypotheses):
                for field in HYPOTHESIS_FIELDS:
                    value = hypothesis.get(field) if isinstance(hypothesis, dict) else None
                    has_content = (
                        isinstance(value, list) and bool(value)
                        if field == "required_evidence"
                        else _has_content(value)
                    )
                    if not has_content:
                        errors.append(f"hypotheses[{index}].{field} must be non-empty")

    client_requests = data.get("client_requests")
    if "client_requests" in data:
        if not isinstance(client_requests, list):
            errors.append("client_requests must be a list")
        else:
            for index, request in enumerate(client_requests):
                for field in CLIENT_REQUEST_FIELDS:
                    value = request.get(field) if isinstance(request, dict) else None
                    if not _has_content(value):
                        errors.append(f"client_requests[{index}].{field} must be non-empty")

    prompt = data.get("execution_prompt")
    prompt_text = prompt.lower() if isinstance(prompt, str) else ""
    if "人工审核" not in prompt_text and "human review" not in prompt_text:
        errors.append("execution_prompt must require human review")
    if "范围确认" not in prompt_text and "scope gate" not in prompt_text:
        errors.append("execution_prompt must require the scope gate")
    has_review_gate = "人工审核" in prompt_text or "human review" in prompt_text
    has_scope_gate = "范围确认" in prompt_text or "scope gate" in prompt_text
    has_required_controls = (
        "research-to-obsidian" in prompt_text
        and ("financial-health report" in prompt_text or "财务健康报告" in prompt_text)
        and ("no auto execution" in prompt_text or "不得自动执行" in prompt_text)
    )
    if has_review_gate and has_scope_gate:
        sections = _prompt_sections(prompt) if isinstance(prompt, str) else None
        contract_invalid = sections is None or not has_required_controls
        if sections is not None:
            route_text = sections["Public source plan"] + " " + sections["Client request list"]
            routes = {
                source.get("route") for source in (source_plan if isinstance(source_plan, list) else [])
                if isinstance(source, dict)
                and isinstance(source.get("route"), str)
                and source.get("route") in ALLOWED_SOURCE_ROUTES
            }
            priorities = {
                request.get("priority") for request in (client_requests if isinstance(client_requests, list) else [])
                if isinstance(request, dict) and isinstance(request.get("priority"), str)
            }
            contract_invalid = contract_invalid or any(route not in route_text for route in routes)
            contract_invalid = contract_invalid or any(
                priority not in sections["Client request list"] for priority in priorities
            )
            analysis = sections["Analysis sequence"].lower()
            financial_positions = [
                position for marker in ("financial-health report", "财务健康报告", "财务健康")
                if (position := analysis.find(marker)) >= 0
            ]
            valuation_positions = [
                position for marker in ("valuation", "估值")
                if (position := analysis.find(marker)) >= 0
            ]
            contract_invalid = contract_invalid or not financial_positions
            contract_invalid = contract_invalid or (
                bool(valuation_positions) and min(financial_positions) > min(valuation_positions)
            )
        if contract_invalid:
            errors.append("execution_prompt must include required sections in order")

    return errors


def load_brief(path: Path) -> Dict[str, Any]:
    """Load a UTF-8 JSON brief and raise one ValueError for schema violations."""
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    errors = validate_brief(data)
    if errors:
        raise ValueError("; ".join(errors))
    return data


def _result_payload(status: str, **fields: Any) -> str:
    """Serialize a CLI response deterministically for machine consumers."""
    return json.dumps({"status": status, **fields}, ensure_ascii=False)


def main(argv=None) -> int:
    """Run validation for one file and return a shell-compatible exit status."""
    parser = argparse.ArgumentParser(description="Validate a consulting review brief.")
    parser.add_argument("--brief", required=True, type=Path, help="UTF-8 JSON brief path")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args(argv)

    path = args.brief.expanduser().resolve()
    try:
        load_brief(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors = str(error).split("; ")
        if args.json:
            print(_result_payload("invalid", errors=errors))
        else:
            for item in errors:
                print(item)
        return 1

    if args.json:
        print(_result_payload("valid", brief=str(path)))
    else:
        print(f"valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
