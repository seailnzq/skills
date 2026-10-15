---
name: earnings-guidance-incremental-analysis
name_en: Earnings Guidance Incremental Analysis
name_zh: 业绩预告增量分析
description: Incremental-information framework for dissecting A-share earnings pre-announcements and flash reports. Compares wording and figures against the prior disclosure, splits reported vs adjusted calibers, back-derives the marginal single quarter and the revenue-profit growth "scissors gap", lists items the guidance omits that need the full report to verify, and builds a same-caliber peer table to separate industry-common from company-specific drivers, honestly labeling estimates and unverified items. Use when the user asks about 业绩预告, 业绩快报, 财报增量信息, 财报拆解, 表观 vs 调整后, 增速剪刀差, 单季反推, or whether a problem is 行业共性 or 公司独有.
description_en: Incremental-information framework for dissecting A-share earnings pre-announcements and flash reports. Use when analyzing 业绩预告 / 业绩快报, reported vs adjusted calibers, growth scissors gap, single-quarter backout, or peer-based industry vs company attribution.
description_zh: 拆解 A 股业绩预告与业绩快报的"增量信息"方法论——与上次披露逐条比对措辞与数字、拆分表观与调整后口径、反推单季与增速剪刀差、列出预告未披露的验证项、用统一口径同业可比表区分"行业共性 vs 公司独有"，并诚实标注推算与未核实项。用于用户问业绩预告、业绩快报、财报增量信息、财报拆解、表观 vs 调整后、增速剪刀差、单季反推、行业共性还是公司独有。
argument-hint: 给出股票代码/公司名与预告期（如"海光信息 688041 2026年前三季度业绩预告 增量信息"），并说明是否需要同业对比
argument-hint-en: Provide the ticker/company and guidance period, and whether a peer comparison is wanted
argument-hint-zh: 给出股票代码/公司名与预告期（如"海光信息 688041 2026年前三季度业绩预告 增量信息"），并说明是否需要同业对比
user-invocable: true
---

# 业绩预告增量分析

一套把"公司写了什么"翻译成"市场该重新定价什么"的可复用流程。核心不是复述预告数字，而是找**相对上一次披露的边际变化**、拆**口径**、反推**单季**、列**未验证项**、用**同业镜像**区分共性与独有，并且**诚实区分事实与推算**。

## 适用与前置

- 面向 A 股业绩预告、业绩快报、自愿性/强制披露、单季或累计口径的财务预告拆解。
- 动手前先拿到两样东西：①本次**公告原文**（含归因文字），②**上一次同主体披露**（中报预告 / 中报 / 快报 / 上年同期）。两者缺一，"增量"无从谈起。
- 时效性数据一律用 `qwenwork_web_search` 核实，不凭记忆填数；优先第一手公告，AI 聚合站/自媒体数字需交叉验证。

## 工作流（7 步）

按顺序执行；详细公式、模板与陷阱见 [reference.md](reference.md)。

1. **锚定预告**：记下公告时间、自愿/强制、是否审计（"未经审计，以正式季报为准"）。抽取披露口径表——营收 / 归母 / 扣非 / 调整后（如扣股份支付）× 上年同期 × 同比。
2. **增量视角（最重要）**：与上一披露逐条 diff。重点抓三样——**归因措辞质变**（如"政策驱动"→"市场驱动"）、**新量化项**（首次给出某金额/比例）、**口径变化**。措辞质变往往比数字更值钱。
3. **表观 vs 调整后**：把报表直接口径（归母、扣非，=表观/headline）与剔除一次性或非现金项后的调整口径分开列。量化两者差额。**关键**：不要用"利润增速低于营收增速=股权激励拖累"直接下结论——先查该项**同比基数增量**，很多剪刀差主因是毛利率而非费用项。
4. **单季反推 + 剪刀差**：用"累计 − 上半年 = 单季"反推边际季度；算单季 YoY、QoQ、隐含净利率；算"营收增速 − 归母/扣非增速"剪刀差（以百分点 pct 计），并与**上一期剪刀差对比**看是否收敛/扩大。
5. **未披露验证项（前瞻清单）**：显式列出预告**没给、但决定下季定价**的科目——合同负债/在手订单、经营现金流与净现比、存货、预付款、关联交易、毛利率、费用率。明确标注"待季报确认"。合同负债与经营现金流的决策价值通常高于存货金额本身。
6. **同业可比表（镜像）**：先统一口径（都按同一累计区间、都取各自公告），再列每家"营收—归母—扣非"三方增速与剪刀差；据此把本次结论逐条归因为**行业共性**还是**公司独有**。行业共性看产业链/成本/节奏，公司独有才是需要警惕的经营信号。
7. **诚实标注**：全文对每个数字标 `公告直接披露 / 推算值 / 未核实来源`；估值、目标价、全年预测等市场数据注明是卖方口径；绝不把推算当事实陈述。

## 输出模板

用分节结构（骨架见 reference.md）：
1. 预告口径表 → 2. 相对上次披露的增量（分条，标注重要性）→ 3. 表观 vs 调整后拆解 → 4. 单季反推与剪刀差（标推算值）→ 5. 未披露验证项清单 → 6.（若需要）同业镜像表 + 共性/独有归因 → 7. 一句话结论 + 需提示的不确定项。

## 关键陷阱

- 累计 ≠ 单季：反推单季必须减掉已披露的更早区间，别把累计增速当单季。
- 剪刀差归因要先查基数：SBC/一次性项同比增量可能很小，主因常在毛利率。
- 同业必须同口径同区间，否则表不可比。
- 扭亏/低基数公司：表观增速可能"名义无解"，要看扣非绝对额占表观的比例。
- 不轻信二手源：AI 生成聚合页、过时预测、自媒体测算需交叉验证或弃用。

## 附加资源

- 公式、口径表模板、同业镜像表模板、验证项完整清单、worked example：见 [reference.md](reference.md)。
