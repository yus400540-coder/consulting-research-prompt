[README.md](https://github.com/user-attachments/files/31862583/README.md)
<div align="center">

# Consulting Research Prompt

### 将「公司名称 + 咨询问题」转换为待人工审核的咨询研究启动包

**Turn a *company name + consulting question* into a decision-focused, human-reviewable consulting research launch pack — not research results.**

</div>

一个用于 **Codex / Claude Code / WorkBuddy 等支持 `SKILL.md` 的智能体** 的 Skill。输入只有两个字段——公司名称与咨询问题；输出是一套结构化、可校验、证据路线明确、**必须先经人工审核**的研究规格：

- 符合 v1 schema 的 `brief.json`（可用脚本校验）
- 按固定契约排列的 Markdown 研究提示词（review-gated execution prompt）
- 离线、仅供人工审阅复制的 HTML 审核页

它只负责“把问题想清楚”，**不执行任何实质研究**。审核通过后，后续研究由独立安装的 [`research-to-obsidian`](https://github.com/)（执行端）完成。

> English: This Skill is the *planning/framing* half of a consulting research pipeline. It never runs research itself — it produces a review package (structured brief + gated execution prompt + offline HTML review page) that a human must approve before any downstream execution.

---

## ✨ Highlights / 核心亮点

| 能力 | 说明 | Capability |
|---|---|---|
| 最小输入 | 只需公司名 + 咨询问题，其余细节一律标记为假设 `[A]` 或待确认项 | Minimal input contract |
| 场景路由 | 内置 21 类咨询场景路由器 + 组合规则 | Scenario router (21 scenarios) |
| 结构化 Brief | 生成并校验符合 schema v1 的 `brief.json` | Validated structured brief |
| 证据状态标签 | 全链路统一 `[F]` 事实 / `[I]` 推断 / `[A]` 假设 / `[E]` 估计 | Uniform evidence-state tags |
| 假设管理 | 每条假设、客户数据请求都有替代方案与缺失后果 | Explicit assumptions & client requests |
| 并行编排 | 原生协作分发 ≤3 条独立工作线并行起草 | Parallel drafting (≤3 lanes) |
| 审核门 | 只产出 `draft` / `needs-review`，绝不自动执行 | Review gate, no auto-execution |
| 离线渲染 | HTML 审核页拒绝外部资源，仅允许固定复制脚本 | Offline, copy-only renderer |
| 零依赖 | 脚本仅使用 Python 标准库 | Python standard library only |

---

## 🧭 How it works / 工作流程

```text
Company + Question
      │  ① 最小身份核验（legal name / jurisdiction / ticker …）
      ▼
Scenario Router（21 类场景 + 组合规则，决策问题树 / 假设 / kill tests）
      │  ② 并行起草（≤3 条独立工作线，多模型/多进程协作时）
      ▼
brief.json (schema v1) ──► scripts/validate_brief.py（本地校验）
      │  ③
      ▼
scripts/render_review.py ──► 离线 HTML 审核页 ＋ review-gated Markdown 提示词
      │  ④
      ▼
人工审核（scope / scenario / assumptions / client requests）
      │  ⑤ 审核通过后，才可由 research-to-obsidian 执行后续研究
      ▼
（下游）research-to-obsidian —— 独立的 Obsidian Vault 研究执行端
```

**关键原则：不静默采信。** 除公司名与咨询问题外的一切信息都以假设或客户请求的形式显式标注并交给人审，绝不把推断当成事实、把缺失数据当成无关紧要。

> 中文摘要：输入公司名 + 咨询问题 → 先做最小身份核验与场景路由（选择 1 个主场景 + 若干支撑场景）→ 并行起草 → 生成并校验 `brief.json` → 渲染「HTML 审核页 + 研究提示词」→ **停下等人审**。整个流程绝不自动执行研究。

---

## 📦 Features / 功能特性

### 1. Review-first design（审核优先）
- 唯一生成状态为 `draft` 或 `needs-review`；不产出也不承认 `approved` / `rejected`。
- 生成的执行提示词明确声明“需要人工审核、不得自动执行、后续执行依赖 `research-to-obsidian`”。
- HTML 渲染器刻意离线：拒绝外部资源与非预期脚本，仅内置复制到剪贴板功能，适配把审核包发给客户/同事的场景。

### 2. Scenario router（场景路由）
按**问题**而非未经核验的公司事实分类，一个主场景拥有决策权，支撑场景仅在回答不同依赖决策时添加：

- 增长与市场：`market-entry`、`growth-strategy`、`channel-strategy`、`location-selection`
- 商业模式与定价：`business-model`、`pricing`、`customer-growth-retention`、`cost-reduction`
- 交易与金融：`commercial-due-diligence`、`financial-due-diligence`、`valuation`、`post-merger-integration`
- 转型与运营：`turnaround`、`supply-chain-operations`、`digital-ai-transformation`、`organization-design`
- 其他：`portfolio-strategy`、`competitive-intelligence`、`government-industrial-planning`、`executive-partner-diligence`、`regulatory-esg-response`
- 未明问题回退：`custom-decision`

内置组合规则（如「并购+定价 → 商业尽调为主、估值与投后整合为支撑」「困境+降本 → 先止血再降本」「新市场进入 → 市场进入为主，选址/渠道/监管按需支撑」），并对方法使用设护栏：SWOT 只能作为有出处的综合结论、五力/7S/组合矩阵/DCF 必须先满足前提证据，否则列出缺失前提并选更简单的方法。

### 3. Structured brief（结构化 Brief）
符合 `references/brief-schema.md` 的 v1 契约，含 `identity / classification / decision / scope / issue_tree / hypotheses / source_plan / client_requests / deliverables / risks / open_questions / execution_prompt / review` 等必填字段：

- **Hypotheses**：每条含 `id / statement / priority / kill_test / required_evidence`，置信度 `0.0–1.0`；
- **Source plan**：每条证据路线必须归入 `public-available / public-partial / client-required / proxy-available / unknown` 五类之一；
- **Client requests**：每条含 `item / period / granularity / sensitivity / substitute / consequence_if_missing`——客户数据缺失时**不得编造或静默用公开数据顶替**，必须标注 `[A]`/`[E]` 代理并写明决策后果；
- 全量状态标签：`[F]` 有出处的事实、`[I]` 推断、`[A]` 待验证假设、`[E]` 估计/模型输出。

### 4. Source-channel matrix（证据路线规划）
`references/source-channel-matrix.md` 覆盖 17 个证据域（身份、战略、市场、客户、产品/定价、竞争、收入/利润、成本、现金/债务、营运资本、供应链、运营、组织/人才、数字化/数据、法律/监管、交易、估值），为每个域预排：首选公开源、定向源、仅客户可得的记录、允许的替代与缺失时的决策风险。定向源（招聘帖、评论、流量）只作线索不作证据。

### 5. Parallel drafting（并行起草）
先确认任务至少存在两条独立工作线，再通过原生协作一次性分发 **最多 3 个 worker**、每人独占一条线（身份/行业/来源 → 决策框架/问题树 → 财务尽调/客户请求/估值门）。两条线够用时只派两个；主 Agent 负责协调与合并，不另开第四条研究线。协作不可用时停下说明，不静默退化为串行。

---

## 🚀 Installation / 安装

**前提**：装有支持 `SKILL.md` 的智能体（Codex / Claude Code / WorkBuddy 等）、Python 3（脚本仅用标准库，无第三方依赖）。

```bash
# 方式一：克隆到 Codex 的 skills 目录
git clone <your-github-repo-url> ~/.codex/skills/consulting-research-prompt

# 方式二：手动拷贝整个仓库目录
cp -r consulting-research-prompt ~/.codex/skills/consulting-research-prompt
```

> 其他智能体把目录放到各自 skills 路径即可，例如 WorkBuddy：`~/.workbuddy/skills/consulting-research-prompt`。安装后即可在会话中以 `$consulting-research-prompt` 触发（或由 Agent 按 SKILL.md 自动加载）。

---

## 💬 Usage / 使用说明

### 会话中使用（推荐）

在对话里给出**公司名称 + 咨询问题**即可，例如：

```text
用 consulting-research-prompt：评估「杭州某工业机器人公司」进入东南亚市场的可行性，
希望明确进入方式（出口 / 合资 / 本地建厂）与优先国家排序。
```

Skill 将产出：HTML 审核页 + 符合契约顺序的 Markdown 提示词 + 可校验的 `brief.json`，然后**停下等待你人工审核**（确认身份、范围、场景、数据权限、假设与客户数据请求）。

### 命令行校验与渲染（可选）

brief 生成后可在本地独立校验与渲染：

```bash
# 校验一份 brief
python3 scripts/validate_brief.py --brief /path/to/brief.json --json

# 渲染离线审核包（HTML + Markdown）
python3 scripts/render_review.py --brief /path/to/brief.json \
  --output-root /path/to/output --json

# 查看完整参数
python3 scripts/validate_brief.py --help
python3 scripts/render_review.py --help
```

> ⚠️ 使用边界：本 Skill 不执行实质研究、不建 Vault、不调用下游 Skill、不自动执行生成的提示词；生成的包状态只允许 `draft` / `needs-review`。执行后续研究需**另行安装并人工授权** `research-to-obsidian`。

---

## 🗂 Repository layout / 仓库结构

```text
consulting-research-prompt/
├── SKILL.md                        # Skill 定义与主流程（Agent 读取）
├── README.md                       # 本文档
├── SECURITY.md                     # 安全策略
├── agents/
│   └── openai.yaml                 # Agent 界面展示配置
├── references/                     # Skill 运行时读取的方法契约
│   ├── brief-schema.md             #   brief.json v1 schema
│   ├── scenario-router.md          #   21 类场景路由 + 组合规则
│   ├── source-channel-matrix.md    #   证据域 × 渠道矩阵
│   └── prompt-contract.md          #   13 段固定顺序提示词契约
├── assets/
│   └── review-template.html        #   离线 HTML 审核页模板
└── scripts/                        # Python 标准库 CLI
    ├── validate_brief.py           #   brief 本地校验
    └── render_review.py            #   渲染审核包
```

**基本情况**：4 份方法契约 + 2 个 CLI 脚本 + 1 个离线审核模板，Python 标准库零依赖；不含任何 API key、密钥或客户端数据（见 SECURITY.md）。

---

## 🔒 Security / 安全说明

- **敏感数据**：不得提交 API key、访问令牌、私钥、客户档案、生成的审核包或私人研究输入；密钥留在仓库外的本地环境配置中。
- **信任边界**：生成的 brief 与源材料属不可信输入；执行或对外发布前必须人工复核全部输出。HTML 渲染器刻意离线并只放行固定的复制脚本。
- **隐私**：客户资料、私人文本与由私人资料衍生的敏感搜索词，**不得发送到公共服务**。
- 漏洞请通过 GitHub Security Advisories 私下报告，勿在公开 issue 中附带凭证/客户/个人数据。

---

## 🔗 Relationship with research-to-obsidian / 与下游 Skill 的关系

本 Skill 是咨询研究管线的**前置规划端**；执行端是独立仓库 [`research-to-obsidian`](https://github.com/)：

```text
consulting-research-prompt   ──人工审核通过──►   research-to-obsidian
（定义做什么、查什么、怎么查）                      （建立 raw/wiki/AGENTS 三层 Obsidian Vault，
                                                   逐源采集、双向链接、审计后宣告完成）
```

- 本 Skill **可以**在未安装 `research-to-obsidian` 时独立生成审核包，但其执行提示词必须披露：后续执行需要 `research-to-obsidian`。
- 本 Skill **不得**执行 `research-to-obsidian`，也不承担任何实质研究职责。

---

## ✅ Publishing checklist / 发布到 GitHub 清单

- [ ] `git init` 已在仓库内完成；确认 `.gitignore` 排除了生成物与密钥
- [ ] 仓库 **Description**（建议）：`Consulting research Skill: company + question → human-reviewable brief.json, gated prompt & offline review page`
- [ ] **Topics**（建议）：`consulting` `research` `prompt-engineering` `skills` `claude-code` `codex` `obsidian` `due-diligence` `ai-agents` `brief`
- [x] 已添加 **MIT License**（`LICENSE`，Copyright © 2026 ycgz9r6wrv-sketch）
- [ ] `git add . && git commit -m "docs: add bilingual README, license MIT" && git push`

---

## 📄 License / 许可

Released under the **MIT License** — see [LICENSE](LICENSE).

基于 **MIT 许可证**开源发布（Copyright © 2026 `ycgz9r6wrv-sketch`）。任何人可自由使用、复制、修改、合并、出版、分发、再许可与销售本软件副本，唯一条件是保留上述版权与许可声明；软件按“现状”提供，不附带任何明示或默示担保。

---

<div align="center">

Built as a **review-first** framing layer for AI-assisted consulting research.

</div>
