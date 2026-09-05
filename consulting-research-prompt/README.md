# Consulting Research Prompt

将“公司名称 + 咨询问题”转换为待人工审核的咨询研究提示词、结构化 `brief.json` 和离线 HTML 审核页。

## 安装

将本仓库复制到 Codex skills 目录：

```text
~/.codex/skills/consulting-research-prompt/
```

随后在 Codex 中使用 `$consulting-research-prompt`。

## 设计边界

- 本 Skill 只生成 `draft` 或 `needs-review` 审核包，不执行实质研究。
- 后续研究需要单独安装并人工授权 `research-to-obsidian`。
- HTML 审核页为离线、复制专用页面；渲染器会拒绝外部资源和非预期脚本。
- 客户资料、私人文本和由私人资料衍生的敏感搜索词不得发送到公共服务。

## 本地校验

```bash
python3 scripts/validate_brief.py --brief /path/to/brief.json --json
python3 scripts/render_review.py --brief /path/to/brief.json --output-root /path/to/output --json
```

代码仅使用 Python 标准库。

## 许可

本仓库当前未附带开源许可证。除非权利人另行授权，默认保留全部权利。
