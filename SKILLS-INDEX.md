# SKILLS-INDEX — 个人技能索引表

> 本仓库托管 `~/.workbuddy/skills/` 下的个人沉淀技能。用途与调用方式一览如下。

| 技能 | 用途（一句话） | 怎么调用 | 关键依赖 |
|---|---|---|---|
| **[a-share-headline-earnings](./a-share-headline-earnings/SKILL.md)** | A股 98 家头部企业半年报/年报批量跟踪：下载 PDF → 解析财务 → wiki 入库 → 行业深度分析 → 全景预测 | 对话：披露季说「开始 A 股头部半年报跟踪」；或已配置的 8/25、8/31 定时自动化任务 | 工作区 `Claw/` 下 `all_a_head_*.py` 脚本；巨潮接口；wiki-knowledge |
| **[cninfo-financial-reports](./cninfo-financial-reports/SKILL.md)** | 巨潮资讯批量下载科创板/创业板财报 PDF → 解析关键财务数据 → llm-wiki 入库（增量更新） | 对话：「批量抓取科创板半年报」「增量更新财报」；脚本：`starboard_h1/00_run_incremental.py` | `Claw/starboard_h1/` 管线（01~07）；PyMuPDF；巨潮接口 |
| **[fin-statement-bridge](./fin-statement-bridge/SKILL.md)** | 高研发公司净利润 Bridge 拆解：净利增速与收入背离、股份支付(SBC)扭曲利润、净利率归因 | 对话：分析海光/寒武纪/摩尔线程/沐曦等财报时说「拆解净利增速为什么背离」 | 半年报利润表 + 费用/股份支付附注；有效所得税率反推 |
| **[llm-wiki](./llm-wiki/SKILL.md)** | 用 LLM 增量构建维护个人知识库 wiki（非 RAG）：ingest → 交叉引用 → 综合 → 定期 lint | 对话：所有涉及 wiki 的读写/入库/提问；默认库 `~/.workbuddy/wiki-knowledge/`（另有 wiki-life） | WIKI-SCHEMA.md 约定；index/log 维护；git 同步 |
| **[tencent-news](./tencent-news/SKILL.md)** | 7×24 腾讯新闻搜索：热榜、早报/晚报、实时资讯、领域新闻、天气 | 对话：「看今天热点」「早报」「财经新闻」；底层 CLI：`scripts/run-cli.sh help`（Windows 用 `.ps1`） | `tencent-news-cli` + API Key；需先 `cli-state` 检查环境 |
| **[wiki-life-plan-authoring](./wiki-life-plan-authoring/SKILL.md)** | 编撰/年审 20 年期方向性人生规划：从 wiki-life 库建真实画像 → 方向层主文档 + 论证层附录双文件 → 逐轮先判推翻什么再联动改，数字名义/实际口径校验，审定后按 WIKI-SCHEMA 入库 | 对话：「整理/修订二十年人生规划」「给条新事实重估」「每年 9 月校准 / 五年复盘」；给 wiki-life 路径或自动探测 | `~/.workbuddy/wiki-life/` 库；llm-wiki 的 WIKI-SCHEMA 约定；WebSearch 核政策/价格；私有库 git 同步 |

---

## 详细说明

### 1. a-share-headline-earnings — A股头部企业财报跟踪
- **干什么**：98 家 A 股头部（18 行业）半年报/年报披露季分批次跟踪，产出「半年报全景分析与产业预测」报告（景气矩阵 + AI 产业链传导 + 产业预测）。
- **管线**：`all_a_head_fetch.py`（下载 PDF）→ `all_a_head_process.py`（解析 + 生成 wiki 页 + 聚焦清单）。
- **数据文件**：`all_a_head_manifest.json`（清单）/ `all_a_head_data.json`（财务数据）/ `all_a_head_focus.json`（行业重点）。
- **已踩坑**：字段名带单位后缀、跨行单位声明、保险/银行报表特例、目录页干扰。

### 2. cninfo-financial-reports — 巨潮财报批量入库
- **干什么**：批量下载科创板/沪深定期报告到 `~/.workbuddy/wiki-knowledge/`，生成每公司「财报关键信息页」并与投资概念双向链接。
- **管线**：`starboard_h1/` 下 01_fetch_orgids → 02_fetch_links → 03/05_extract → 04/06_gen_wiki → 07_gen_deep；`00_run_incremental.py` 一键增量。
- **产出**：`wiki/papers/2026-H1-{code}-{name}-半年报.md` + 综合页景气矩阵 + index/log 更新。

### 3. fin-statement-bridge — 财报净利 Bridge 拆解
- **干什么**：回答「扣股份支付后净利增速为何 > 收入增速」「净利率提升由哪些因素贡献」。核心：SBC 藏在研发费用 → 研发付现费用率下降 = 真实经营杠杆。
- **用法**：取利润表 + 费用/股份支付附注 → 算税后 SBC 影响 → 净利率 Bridge 归因 → 专项检查清单 → 输出模板。
- **2026H1 案例数据**：海光（收入 +66.5%、扣SBC后归母 +82.3%、SBC 占研发 21.3%）、寒武纪（收入 +108%）。

### 4. llm-wiki — 个人知识库模式
- **干什么**：Karpathy LLM-Wiki 模式——LLM 增量编译、交叉引用、维护持久化结构化 wiki。三层架构：raw（不可变源）→ wiki（LLM 写）→ schema。
- **三个操作**：Ingest（新源入库）/ Query（带引用作答，好答案回写为页）/ Lint（健康检查：矛盾、孤立页、缺失链接）。
- **默认位置**：`~/.workbuddy/wiki-knowledge/`（宏观/投资）+ `~/.workbuddy/wiki-life/`（人生系统）。

### 5. tencent-news — 腾讯新闻搜索
- **干什么**：7×24 新闻/热榜/早晚报/领域新闻/天气查询，聚焦国内与国际热点。
- **环境就绪**：`cli-state` 检查 CLI 与 API Key → 缺失时安装/配置（Key 从 news.qq.com/exchange 获取）。
- **核心约束**：所有调用走 `run-cli` 脚本，先读 `help` 不硬编码；CLI 失败不降级到 WebSearch。

### 6. wiki-life-plan-authoring — 长期人生规划编撰与年审
- **干什么**：基于 `~/.workbuddy/wiki-life/`（人生系统库）编撰或年度复核一份 20 年期方向性人生规划。核心不是一次写完，而是「建真实画像 → 定规格 → 分层产出 → 逐条校对 → 先审后入库」。
- **产出结构**：主文档＝方向层（终局视角、阶段划分、触发器而非日历、失败清单、五要素速览、事实确认状态、近期衔接）；附录＝论证层（通胀/财务测算、保险精析、政策与尾部风险、口径推导）。两文件用 §编号互指，命名 `<跨度>人生规划-<起年>-<止年>`。
- **关键纪律**：新事实先判定推翻了什么再逐处 grep 联动改；金额/年龄换算并显式声明**名义 vs 实际**口径；政策/价格等客观事实一律 WebSearch 核实并标时点；隐私数字**「只留线不留账」**（方向层只留阈值与带宽，明细留附录）；**未审定绝不写库**。
- **入库**：用户点头后按 WIKI-SCHEMA 落 `framework/`＋`synthesis/`，补双链、更新 index、在 log 追加、git commit；远程为私有库才 push。
- **依赖/关联**：复用 llm-wiki 的三层架构与 WIKI-SCHEMA 约定；只操作内在库 wiki-life，与对外研报库 wiki-knowledge 不混。
- **已踩坑（写进 SKILL 的 Pitfalls）**：换轮后 Edit 报 "File has not been read yet"→先整文件 Read；old_string 失配→Grep 取精确原文再替换；成段替换后检查重复残留；版本标记三处联动；数字联动清单（改一处先 Grep 找齐）。

---

## 备注
- **westock（腾讯自选股 MCP）**：属第三方 connector 技能（`~/.workbuddy/connectors/skills/connector-westock-mcp/`），由连接器更新维护，不入本仓库。查询行情/自选/模拟交易时使用。
- **内置技能**：3D 模型、PPT、Excel、文档等 WorkBuddy 内置技能位于插件缓存目录，随产品更新，不入本仓库。
- **定时自动化**：a-share-headline-earnings 已配置 8/25（下载+行业分析）与 8/31（补全+全景预测）两个任务；automation 的 cwds 会被指向独立目录，prompt 里需显式 `cd C:/Users/sealin/WorkBuddy/Claw`。
