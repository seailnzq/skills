# SKILLS-INDEX — 个人技能索引表

> 本仓库托管 `~/.qwenworkcn/skills/` 下的个人沉淀技能。用途与调用方式一览如下。
> 2026-10-17 增量同步：新增 12 个自研技能（投资/审计/宏观/研报采集/wiki 入库/工具向），下表加粗行为本次新增。官方内置技能与 `dingtalk-*`（DWS 市场安装）不入本库。

| 技能 | 用途（一句话） | 怎么调用 | 关键依赖 |
|---|---|---|---|
| **[a-share-headline-earnings](./a-share-headline-earnings/SKILL.md)** | A股 98 家头部企业半年报/年报批量跟踪：下载 PDF → 解析财务 → wiki 入库 → 行业深度分析 → 全景预测 | 对话：披露季说「开始 A 股头部半年报跟踪」；或已配置的 8/25、8/31 定时自动化任务 | 工作区 `Claw/` 下 `all_a_head_*.py` 脚本；巨潮接口；wiki-knowledge |
| **[cninfo-financial-reports](./cninfo-financial-reports/SKILL.md)** | 巨潮资讯批量下载科创板/创业板财报 PDF → 解析关键财务数据 → llm-wiki 入库（增量更新） | 对话：「批量抓取科创板半年报」「增量更新财报」；脚本：`starboard_h1/00_run_incremental.py` | `Claw/starboard_h1/` 管线（01~07）；PyMuPDF；巨潮接口 |
| **[fin-statement-bridge](./fin-statement-bridge/SKILL.md)** | 高研发公司净利润 Bridge 拆解：净利增速与收入背离、股份支付(SBC)扭曲利润、净利率归因 | 对话：分析海光/寒武纪/摩尔线程/沐曦等财报时说「拆解净利增速为什么背离」 | 半年报利润表 + 费用/股份支付附注；有效所得税率反推 |
| **[llm-wiki](./llm-wiki/SKILL.md)** | 用 LLM 增量构建维护个人知识库 wiki（非 RAG）：ingest → 交叉引用 → 综合 → 定期 lint | 对话：所有涉及 wiki 的读写/入库/提问；默认库 `~/.workbuddy/wiki-knowledge/`（另有 wiki-life） | WIKI-SCHEMA.md 约定；index/log 维护；git 同步 |
| **[tencent-news](./tencent-news/SKILL.md)** | 7×24 腾讯新闻搜索：热榜、早报/晚报、实时资讯、领域新闻、天气 | 对话：「看今天热点」「早报」「财经新闻」；底层 CLI：`scripts/run-cli.sh help`（Windows 用 `.ps1`） | `tencent-news-cli` + API Key；需先 `cli-state` 检查环境 |
| **[wiki-life-plan-authoring](./wiki-life-plan-authoring/SKILL.md)** | 编撰/年审 20 年期方向性人生规划：从 wiki-life 库建真实画像 → 方向层主文档 + 论证层附录双文件 → 逐轮先判推翻什么再联动改，数字名义/实际口径校验，审定后按 WIKI-SCHEMA 入库 | 对话：「整理/修订二十年人生规划」「给条新事实重估」「每年 9 月校准 / 五年复盘」；给 wiki-life 路径或自动探测 | `~/.workbuddy/wiki-life/` 库；llm-wiki 的 WIKI-SCHEMA 约定；WebSearch 核政策/价格；私有库 git 同步 |
| **[jin-guantao-cybernetics](./jin-guantao-cybernetics/SKILL.md)** | 《控制论与科学方法论》（金观涛/华国凡）知识库技能：可能性空间、控制能力 M/m、共轭控制、负反馈、滤波七法、相对孤立系统、稳态结构、超稳定、自组织、突变理论（飞跃/渐变判据）、黑箱认识论五部位排查 | 对话：说「用 jin-guantao-cybernetics 讲 X」/「ch04 飞跃判据」；用于决策、系统分析、认识失灵排查时引用作者框架 | book-to-skill 生成（扫描版视觉 OCR）；SKILL.md+5 章节文件+术语表+patterns+cheatsheet |
| **[earnings-guidance-incremental-analysis](./earnings-guidance-incremental-analysis/SKILL.md)** | A 股业绩预告/快报「增量信息」拆解：与上次披露 diff 措辞与数字 → 拆表观 vs 调整后口径 → 反推单季与增速剪刀差 → 列预告未披露的验证项 → 同业镜像表分「行业共性 vs 公司独有」→ 每个数字标注推算/未核实 | 对话：拿到某公司业绩预告后说「拆增量信息」「这是行业共性还是公司独有」「反推单季」 | 公告原文 + 上一次同主体披露（中报预告/中报/快报）；`qwenwork_web_search` 核数 |
| **[a-share-unlock-calendar](./a-share-unlock-calendar/SKILL.md)** | A 股限售解禁日历批量查询与抛压提示（东财 RPT_LIFT_STAGE）：解禁市值/占总股本比/相对流通盘倍数，按日期排表可接持仓兑现窗口 | 对话：「XX 什么时候解禁」「批量查持仓解禁日历」 | 东方财富数据中心 API；接持仓/估值兑现窗口 |
| **[a-stock-realtime](./a-stock-realtime/SKILL.md)** | A 股实时行情快查 + 个人持仓盈亏管理 + 当日分时量能异常信号（早盘/尾盘放量、主力抢筹/出货） | 对话：「XX 现在多少钱」「看我的持仓/加一只到持仓」 | 财经行情接口；`scripts/portfolio.py`（持仓为运行时外部文件，不写死金额） |
| **[fab-capacity-five-ring-audit](./fab-capacity-five-ring-audit/SKILL.md)** | 晶圆代工厂季度财报「五环核查」增量分析 + 跨公司同口径对比（12 英寸约当 wpm 归一）+ 来源三级分级 + 在建产能时间表 | 财报季对话：「核查中芯/华虹季报」「扩产体量/同口径多了多少」「先进产能怎么跟踪」 | 财报实数；五环顺序＝设备到账→有效产能→良率→单位成本毛利→收入；**2026-10 加环④-F：Fabless 设计厂八层利润表环比、利润总额/所得税/少数股东只准公告实数相减、禁净利率反推、归母+少数=净利勾稽归零锁死** |
| **[fed-rate-pricing-check](./fed-rate-pricing-check/SKILL.md)** | 美联储利率路径的市场定价核查固定流水线：决议事实→会后期货定价→四方对照→口径校验→回写 wiki 月度利率跟踪页 | 对话：「XX 已被市场定价吗」；FOMC 决议日/月度利率 cron | 四级降级链采集；点阵图 vs 期货 vs 机构预期 |
| **[macro-news-incremental-brief](./macro-news-incremental-brief/SKILL.md)** | 宏观/产业新闻「增量信息」五步分析骨架：校准口径→拆增量→辨机制→映射持仓主线→回写 wiki 并挂核查提醒 | 对话：抛一条宏观/产业新闻问「怎么看/对持仓意味什么」 | 持仓映射（盈利兑现×估值扩张）；区别于 fed-rate-pricing-check |
| **[multi-line-distress-four-paper-audit](./multi-line-distress-four-paper-audit/SKILL.md)** | 投资/子女/工作（+配偶父母背景）多线同时「不对劲」时的五线分诊 + 逐张纸四行审计 + 领域专用审点 + 合并收口到一个最小身体/关系动作 | 对话：「最近什么都不顺」「投资/孩子/工作同时出问题」「帮我拆这几件事」 | 与 portfolio-drawdown-narrative-audit 配套（后者做投资深水区） |
| **[portfolio-drawdown-narrative-audit](./portfolio-drawdown-narrative-audit/SKILL.md)** | A 股组合回撤叙事四步审计：四行纸/叙事语言漂移检测/终局尺子证伪/回撤 ABC 分类 + 隐含 beta 校准 + 最坏值锚定 | 对话：「又跌了怎么办」「回撤怎么自处」「心神不宁扛不住」「三张纸审计」 | jin-guantao 框架 + 用户认知尺子（叙事过剩、钱是约束） |
| **[user-profile-doc-fetch](./user-profile-doc-fetch/SKILL.md)** | 跨历史会话 outputs 与 wiki-life 定位并交付「认知/画像于我」文档（按 mtime 取权威版），再用最新记忆决策审计其时效并报告待裁决项 | 对话：「你对我的认知」「调出画像」「你多了解我」「更新画像文档」 | 历史 outputs 目录 + wiki-life；mtime 定权威版 |
| **[wechat-report-mirror-fetch](./wechat-report-mirror-fetch/SKILL.md)** | 中文卖方研报/公众号文章当日采集流水线：金山收藏判当日新增→频道/镜像降级链取全文→并行提炼→固定五要素输出（论点/带日期论据/定价含义/来源URL/未核实项） | 对话：「抓今天新收藏」「郭磊今天写什么」「研报打不开找镜像」 | 金山收藏助手；Reportify 频道；多镜像站降级链 |
| **[wiki-research-sync](./wiki-research-sync/SKILL.md)** | 深度研究主题归档进 wiki-knowledge 的闭环：外部检索+库内引用→按 WIKI-SCHEMA 建 synthesis 综合页（双向链接）→更新 index/log→校验链接→commit/push；处理代理未开与 vault backup 冲突 | 对话：「深研某主题并入库」「回写综合页」「对已有综合页追加章节深化」 | wiki-knowledge git；WIKI-SCHEMA；双库同步 |
| **[win-desktop-xlsx-safe-edit](./win-desktop-xlsx-safe-edit/SKILL.md)** | Windows 桌面（或用户目录）已有 .xlsx 的安全端到端编辑：备份→openpyxl 保格式编辑→UTF-8 JSON 校验（避 GBK 乱码）→~$ 锁检查，被占用先出 outputs 再回写 | 对话：「修改桌面上已有中文 xlsx」「改投标参数表/明细表」 | 与 xlsx 技能叠加（规范看 xlsx、文件安全看本技能）；openpyxl |
| **[industry-research](./industry-research/SKILL.md)** | 面向特定行业/赛道的系统性深度研究：定义/市场规模/竞争格局/技术趋势/政策/投融资多维全面调研，输出结构化行业研究报告 | 对话：「深度研究 XX 行业/赛道」「这块市场多大、格局如何」 | 多来源检索 + 结构化报告模板 |
| **[awareness-git-sync](./awareness-git-sync/SKILL.md)** | 记忆(awareness)+自研技能 与 GitHub 私有库(seailnzq/*) 的**双向同步与换机恢复**（本用户此主题默认技能）：上传=刷 md→只纳人读文件→扫真凭据→push(被 vault backup 拒则 rebase 保留双方)；还原=clone 四库→bootstrap(dry-run→-Apply)→补凭据/重建 cron；含两轴隐私(私有库可留金额明文、本机 DLP 才是红线、凭据永不入库) | 对话：「同步记忆/技能到 git」「备份自研技能」=上传；「同步 git 到本地」「从 git 拉回本机」「换机恢复」=还原；或 /awareness-git-sync | 四私有库(wiki-life/wiki-knowledge/skills/awareness)；fine-grained PAT 需含各库白名单；`reference/migration-package.md` 有五件套模板 |

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
- **关键纪律**：新事实先判定推翻了什么再逐处 grep 联动改；**财务口径四查**（①名义 vs 实际折现——跨期对比先折现到同一口径，实踩坑"A 缺口 1240 实为 2860"；②结构通胀分化——综合 CPI 锚之外医疗照护 5–8% 等分项单列；③高方差项按低/中/高三档给区间不写单点值；④可逆/不可逆窗口——商业保险可保期等"过窗永久关闭"动作给 deadline）；用户要求"再审视/找盲区"时按**审视报告五分法**输出（客观硬伤/方差低估/结构性盲区/框架可商榷点/内容性缺席），只改客观规律可校验部分、价值判断声明不动；政策/价格等客观事实一律 WebSearch 核实并标时点；隐私数字**「只留线不留账」**（方向层只留阈值与带宽，明细留附录）；**未审定绝不写库**。（以上四查与五分法为 v1.3.0 增补）
- **入库**：用户点头后按 WIKI-SCHEMA 落 `framework/`＋`synthesis/`，补双链、更新 index、在 log 追加、git commit；远程为私有库才 push。
- **依赖/关联**：复用 llm-wiki 的三层架构与 WIKI-SCHEMA 约定；只操作内在库 wiki-life，与对外研报库 wiki-knowledge 不混。
- **已踩坑（写进 SKILL 的 Pitfalls）**：换轮后 Edit 报 "File has not been read yet"→先整文件 Read；old_string 失配→Grep 取精确原文再替换；成段替换后检查重复残留；版本标记三处联动；数字联动清单（改一处先 Grep 找齐）。

### 7. earnings-guidance-incremental-analysis — 业绩预告增量分析
- **干什么**：把「公司写了什么」翻译成「市场该重新定价什么」。核心不是复述预告数字，而是找**相对上一次披露的边际变化**、拆口径、反推单季、列未验证项、用同业镜像区分共性与独有。
- **七步**：①锚定预告口径（自愿/强制、是否审计）→ ②与上一披露逐条 diff（归因**措辞质变** > 新量化项 > 口径变化）→ ③表观 vs 调整后拆口径（**先查 SBC 的同比基数增量**，别默认剪刀差主因是股权激励，常在毛利率）→ ④累计−上半年=单季反推 + 营收/归母/扣非剪刀差（pct，看上上期是否收敛）→ ⑤列预告未披露的验证项（**合同负债、经营现金流/净现比**通常比存货金额更具决策价值）→ ⑥同业镜像表统一口径分「行业共性 vs 公司独有」→ ⑦每个数字标 `公告/推算/卖方/未核实`。
- **判定纪律**：孤例不得升格为「行业共性」；扭亏/低基数公司表观增速可能名义无解，看扣非绝对额占表观比；AI 聚合站/自媒体测算需交叉验证或弃用。
- **重叠提示**：与 `fin-statement-bridge` 在「SBC 扭曲、净利 vs 营收背离、海光/寒武纪/摩尔线程/沐曦同业」有交叉；本技能更宽（预告专属：增量 diff、单季反推、前瞻验证清单、未披露项），`fin-statement-bridge` 更聚焦利润表 Bridge 归因，两者互补。
- **关联**：常与 `cninfo-financial-reports`（取公告）、`a-share-headline-earnings`（行业全景）、`fin-statement-bridge`（深度 Bridge）串联。

---

## 备注
- **westock（腾讯自选股 MCP）**：属第三方 connector 技能（`~/.workbuddy/connectors/skills/connector-westock-mcp/`），由连接器更新维护，不入本仓库。查询行情/自选/模拟交易时使用。
- **内置技能**：3D 模型、PPT、Excel、文档等 WorkBuddy 内置技能位于插件缓存目录，随产品更新，不入本仓库。
- **定时自动化**：a-share-headline-earnings 已配置 8/25（下载+行业分析）与 8/31（补全+全景预测）两个任务；automation 的 cwds 会被指向独立目录，prompt 里需显式 `cd C:/Users/sealin/WorkBuddy/Claw`。
