"""Render validated consulting review briefs into offline review packages."""

import argparse
from datetime import date
import html
import importlib.util
import json
import os
from pathlib import Path
import re
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "consulting_prompt_validator", SCRIPT_DIR / "validate_brief.py"
)
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)

COPY_SCRIPT = """document.getElementById('copy-prompt').addEventListener('click', function () {
        navigator.clipboard.writeText(document.getElementById('execution-prompt').textContent);
      });"""
UNSAFE_TEMPLATE_PATTERNS = (
    r"(?i)<[^>]+\bsrc\s*=",
    r"(?i)<[^>]+\b(?:xlink:)?href\s*=",
    r"(?i)<(?:link|img|iframe|audio|video|source|embed|object|base)\b",
    r"(?i)<form\b|\bformaction\s*=",
    r"(?i)@import\b|url\s*\(",
    r"(?i)\bfetch\s*\(|\bxmlhttprequest\b|\bwebsocket\b",
    r"(?i)\b(?:https?:)?//|\bhttp-equiv\s*=",
    r"(?i)\son\w+\s*=|javascript:|data:",
)


def safe_slug(value: str) -> str:
    """Return a stable filename-safe slug while retaining Unicode letters."""
    slug = re.sub(r"[^\w]+", "-", str(value).strip().lower(), flags=re.UNICODE)
    slug = slug.strip("-_")
    return slug or "untitled"


def choose_output_dir(root: Path, company: str, scenario: str, generated_at: str) -> Path:
    """Choose an unused package directory without changing the filesystem."""
    try:
        day = date.fromisoformat(str(generated_at)[:10]).isoformat()
    except ValueError as error:
        raise ValueError("generated_at must start with YYYY-MM-DD") from error
    base = f"{day}-{safe_slug(company)}-{safe_slug(scenario)}"
    candidate = Path(root) / base
    suffix = 2
    while os.path.lexists(candidate):
        candidate = Path(root) / f"{base}-{suffix}"
        suffix += 1
    return candidate


def _escape(value: Any) -> str:
    """Escape every dynamic value before it is inserted into HTML."""
    return html.escape(str(value), quote=True)


def _value(data: dict, key: str, default: str = "—") -> Any:
    """Return a display value for an optional structured field."""
    value = data.get(key, default) if isinstance(data, dict) else default
    return default if value in (None, "") else value


def _items(values: Any) -> str:
    """Render a sequence as safe list items, including an explicit empty value."""
    if not isinstance(values, list) or not values:
        return "<li>—</li>"
    return "".join(f"<li>{_escape(value)}</li>" for value in values)


def _table(headers: tuple, rows: Any, fields: tuple) -> str:
    """Render structured table rows with escaped cells."""
    heading = "".join(f"<th scope=\"col\">{_escape(header)}</th>" for header in headers)
    if not isinstance(rows, list) or not rows:
        body = f"<tr><td colspan=\"{len(headers)}\">—</td></tr>"
    else:
        body = "".join(
            "<tr>" + "".join(f"<td>{_escape(_value(row, field))}</td>" for field in fields) + "</tr>"
            for row in rows
        )
    return f"<table><thead><tr>{heading}</tr></thead><tbody>{body}</tbody></table>"


def _joined(value: Any) -> str:
    """Render a list in a single escaped-ready display string."""
    return ", ".join(map(str, value)) if isinstance(value, list) else str(value)


def _review_content(data: dict) -> str:
    """Build all human-readable review sections from structured brief fields."""
    input_data = data["input"]
    identity = data["identity"]
    classification = data["classification"]
    decision = data["decision"]
    scope = data["scope"]
    source_rows = [
        {"route": _value(source, "route"), "channels": _value(source, "channels"), "limitations": _value(source, "limitations")}
        for source in data["source_plan"]
    ]
    sections = [
        ("咨询问题", f"<p><strong>公司：</strong>{_escape(input_data['company'])}</p><p><strong>问题：</strong>{_escape(input_data['question'])}</p>"),
        ("主体识别", "".join((
            f"<p><strong>状态：</strong>{_escape(_value(identity, 'verification_status'))}</p>",
            f"<p><strong>规范名称：</strong>{_escape(_value(identity, 'canonical_name', _value(identity, 'name')))}</p>",
            f"<p><strong>行业：</strong>{_escape(_value(identity, 'industry', _value(identity, 'sector')))}</p>",
            f"<p><strong>置信度：</strong>{_escape(_value(identity, 'confidence'))}</p>",
            f"<p><strong>来源：</strong>{_escape(_joined(_value(identity, 'sources', [])))}</p>",
            f"<p><strong>歧义：</strong>{_escape(_joined(_value(identity, 'ambiguities', [])))}</p>",
        ))),
        ("情景判断", f"<p><strong>主情景：</strong>{_escape(_value(classification, 'primary'))}</p><p><strong>支持情景：</strong>{_escape(_joined(_value(classification, 'supporting', [])))}</p><p><strong>理由：</strong>{_escape(_value(classification, 'rationale'))}</p>"),
        ("决策", "".join((
            f"<p><strong>决策陈述：</strong>{_escape(_value(decision, 'statement'))}</p>",
            f"<p><strong>决策者：</strong>{_escape(_value(decision, 'maker'))}</p>",
            f"<p><strong>截止日期：</strong>{_escape(_value(decision, 'deadline'))}</p>",
            f"<p><strong>成功指标：</strong>{_escape(_joined(_value(decision, 'success_metrics', [])))}</p>",
            f"<p><strong>终止条件：</strong>{_escape(_joined(_value(decision, 'kill_conditions', [])))}</p>",
        ))),
        ("范围、假设与排除项", "".join((
            f"<p><strong>范围：</strong>{_escape(json.dumps(scope, ensure_ascii=False, sort_keys=True))}</p>",
            f"<p><strong>假设：</strong>{_escape(_joined(_value(data, 'assumptions', [])))}</p>",
            f"<p><strong>排除项：</strong>{_escape(_joined(_value(data, 'exclusions', [])))}</p>",
        ))),
        ("问题树", _table(("分支", "问题"), data["issue_tree"], ("branch", "question"))),
        ("假设", _table(("编号", "假设", "优先级", "终止测试", "所需证据"), data["hypotheses"], ("id", "statement", "priority", "kill_test", "required_evidence"))),
        ("来源计划", _table(("获取路径", "渠道", "限制"), source_rows, ("route", "channels", "limitations"))),
        ("客户资料请求", _table(("优先级", "资料", "期间", "颗粒度", "原因", "受影响决策", "敏感度", "替代方案", "缺失后果"), data["client_requests"], ("priority", "item", "period", "granularity", "reason", "decision_affected", "sensitivity", "substitute", "consequence_if_missing"))),
        ("交付物", f"<ul>{_items(data['deliverables'])}</ul>"),
        ("风险", f"<ul>{_items(data['risks'])}</ul>"),
        ("待澄清问题", f"<ul>{_items(data['open_questions'])}</ul>"),
    ]
    return "".join(f"<section><h2>{_escape(title)}</h2>{content}</section>" for title, content in sections)


def render_markdown(data: dict) -> str:
    """Return a human-review-only Markdown prompt without changing prompt text."""
    return "\n".join((
        "> [!WARNING] 需要人工审核",
        "> 此生成提示必须经人工审核，且不得自动执行。",
        "",
        "# 研究执行提示（待审核）",
        "",
        data["execution_prompt"],
    ))


def _validate_template(template: str) -> None:
    """Reject templates that could break the offline, copy-only review boundary."""
    for pattern in UNSAFE_TEMPLATE_PATTERNS:
        if re.search(pattern, template):
            raise ValueError("template contains a prohibited active or external resource")
    scripts = re.findall(r"(?is)<script\b[^>]*>(.*?)</script\s*>", template)
    if len(scripts) != 1 or scripts[0].strip() != COPY_SCRIPT.strip():
        raise ValueError("template must contain only the copy-only execution-prompt script")
    if template.count('id="copy-prompt"') != 1 or template.count('id="execution-prompt"') != 1:
        raise ValueError("template must contain one copy button and one execution prompt element")


def _required_package_fields(data: dict) -> tuple[str, str, str]:
    """Validate fields used for filesystem paths before any output is created."""
    classification = data.get("classification")
    if not isinstance(classification, dict) or not isinstance(classification.get("primary"), str) or not classification["primary"].strip():
        raise ValueError("classification.primary must be non-empty")
    generated_at = data.get("generated_at")
    if not isinstance(generated_at, str):
        raise ValueError("generated_at must start with YYYY-MM-DD")
    try:
        date.fromisoformat(generated_at[:10])
    except ValueError as error:
        raise ValueError("generated_at must start with YYYY-MM-DD") from error
    input_data = data.get("input")
    if not isinstance(input_data, dict) or not isinstance(input_data.get("company"), str) or not input_data["company"].strip():
        raise ValueError("input.company must be non-empty")
    return input_data["company"], classification["primary"], generated_at


def render_html(data: dict, template: str) -> str:
    """Populate a local template once per placeholder and reject incomplete output."""
    _validate_template(template)
    replacements = {
        "{{TITLE}}": _escape(f"{data['input']['company']} — 咨询研究提示审核"),
        "{{REVIEW_CONTENT}}": _review_content(data),
        "{{EXECUTION_PROMPT}}": _escape(data["execution_prompt"]),
    }
    rendered = template
    for token, value in replacements.items():
        if template.count(token) != 1:
            raise ValueError(f"template must contain {token} exactly once")
        rendered = rendered.replace(token, value, 1)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError("template contains unresolved double-brace token")
    return rendered


def _write_exclusive(path: Path, content: str) -> None:
    """Write UTF-8 content while refusing to replace an existing review artifact."""
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def write_review_package(data: dict, output_root: Path, template_path: Path) -> dict[str, str]:
    """Validate then create a fresh three-file human-review package."""
    errors = VALIDATOR.validate_brief(data)
    if errors:
        raise ValueError("; ".join(errors))
    company, scenario, generated_at = _required_package_fields(data)
    template = Path(template_path).read_text(encoding="utf-8")
    markdown = render_markdown(data)
    rendered_html = render_html(data, template)
    brief_json = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    root = Path(output_root).expanduser().resolve()
    output_dir = choose_output_dir(root, company, scenario, generated_at)
    root.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            output_dir.mkdir()
            break
        except FileExistsError:
            output_dir = choose_output_dir(root, company, scenario, generated_at)
    paths = {"brief": output_dir / "brief.json", "html": output_dir / "review.html", "prompt": output_dir / "research-prompt.md"}
    _write_exclusive(paths["brief"], brief_json)
    _write_exclusive(paths["html"], rendered_html)
    _write_exclusive(paths["prompt"], markdown)
    return {
        "status": "generated", "review_status": data["status"], "output_dir": str(output_dir.resolve()),
        **{key: str(path.resolve()) for key, path in paths.items()},
    }


def main(argv=None) -> int:
    """Render a review package and return a shell-compatible exit status."""
    parser = argparse.ArgumentParser(description="Render a consulting review package.")
    parser.add_argument("--brief", required=True, type=Path, help="validated UTF-8 JSON brief")
    parser.add_argument("--output-root", required=True, type=Path, help="directory for review packages")
    parser.add_argument("--template", type=Path, help="optional local review HTML template")
    parser.add_argument("--json", action="store_true", help="emit JSON paths")
    args = parser.parse_args(argv)
    template_path = args.template or SCRIPT_DIR.parent / "assets" / "review-template.html"
    try:
        data = VALIDATOR.load_brief(args.brief.expanduser().resolve())
        result = write_review_package(data, args.output_root, template_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        if args.json:
            print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False))
        else:
            print(f"error: {error}")
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"generated: {result['output_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
