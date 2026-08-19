---
name: cninfo-financial-reports
title: 巨潮资讯财报批量抓取与知识库入库
description: 从巨潮资讯网批量下载上市公司定期报告（年报/半年报/季报）PDF，解析关键财务数据，生成 llm-wiki 知识库页面并增量更新。适用于批量跟踪科创板/创业板公司财报、生成财报概览与投资框架链接。
agent_created: true
tags: [财报, 巨潮, 爬虫, PDF解析, 知识库]
---

# 巨潮资讯财报批量抓取与知识库入库

## 适用场景
- 批量下载科创板/沪深公司定期报告（年报/半年报/季报）到 llm-wiki 知识库
- 生成每家公司「财报关键信息页」并与投资概念（高成长叙事/半导体周期等）双向链接
- 按周/按月增量更新（只处理新披露公司）

## 关键接口（巨潮资讯 cninfo）
1. **搜索公司 orgId**：`POST http://www.cninfo.com.cn/new/information/topSearch/query`
   - body: `keyWord={代码}&maxNum=10`，Content-Type: application/x-www-form-urlencoded
   - 返回 JSON 数组，匹配 `code` 且 `category=='A股'` 的项的 `orgId`（科创板 688 开头；CDR 如 689009 无标准 orgId）
2. **查公告列表**：`POST http://www.cninfo.com.cn/new/hisAnnouncement/query`
   - body: `pageNum=1&pageSize=30&column=sse&tabName=fulltext&plate=sh&stock={code},{orgId}&seDate=2026-07-01~2026-08-31&isHLtitle=true`
   - 返回 `announcements[]`，含 `announcementTitle`、`adjunctUrl`、`announcementTime`
   - 半年报标题含「半年度报告」；区分全文（无「摘要」）与摘要（含「摘要」）
3. **下载 PDF**：`http://static.cninfo.com.cn{adjunctUrl}`，必须带 `User-Agent` + `Referer: http://www.cninfo.com.cn/`
   - 校验：文件头 `%PDF` 且 >5KB 才算成功
   - Windows Git Bash 下 /tmp 映射异常，用工作区相对目录

## PDF 解析要点（PyMuPDF）
- 半年报摘要 PDF「主要财务数据」表格提取后为**逐行文本**（字段名/本期/上期/同比各占一行），需用"字段名→后续行"序列解析，不能用单行正则
- 全文 PDF 定位正文：搜索「报告期内主要经营情况」「行业格局和趋势」，跳过目录行（关键词后跟省略号/点+页码）
- 财务字段模式（完整示例见实现）：
  - 营业收入/营业总收入、归属于上市公司股东的净利润、扣除非经常性损益、经营活动产生的现金流量净额、总资产、归属于上市公司股东的净资产、加权平均净资产收益率、研发投入占营业收入的比例

## 知识库入库规范（llm-wiki）
- PDF → `~/.workbuddy/wiki-knowledge/raw/{年份}/半年报/科创板/{code}-{name}/`（本地归档，**.gitignore 排除**，610 家全文约 1.2GB 不入 git）
- 每公司一页：`wiki/papers/2026-H1-{code}-{name}-半年报.md`，frontmatter 含 source 指向 PDF
- 页面结构：一句话总结 / 关键财务数据表 / 核心内容提示 / 与投资知识的关系（[[concepts/xxx]] 双向链接）/ 我的批注
- 行业→概念映射（sealin 框架）：半导体→[[concepts/半导体周期]]、[[concepts/端侧算力]]；通信设备→[[concepts/高成长叙事]]；电池/光伏→[[concepts/反内卷]]
- 综合页：`wiki/synthesis/2026-科创板半年报-总览.md`（景气矩阵表，随披露滚动更新）
- 每次入库后更新 `wiki/index.md`（分类新增行）+ `wiki/log.md`（ingest 记录），然后 git commit + push

## 完整管线（参考实现）
`C:/Users/sealin/WorkBuddy/Claw/starboard_h1/`：
- 01_fetch_orgids.py（批量 orgId，610 家约 3min）
- 02_fetch_links.py（查公告+下载 PDF，增量跳过已存在）
- 03_extract.py（摘要财务数据提取）
- 05_extract_full.py（全文经营/行业/风险/毛利率提取）
- 04_gen_wiki.py（生成 L1 自动页）+ 06_merge_full.py（合并全文要点）
- 07_gen_deep.py（重点公司深度页模板）
- 00_run_incremental.py（一键增量主控：02→06 + 输出新披露清单）

## 增量更新流程（每周）
1. 跑 `00_run_incremental.py` 发现新披露公司并自动入库（L1 页）
2. 精读重点公司（半导体/AI算力/光通信/医药等），升级深度页（07 模式）
3. 更新综合页景气矩阵 + index + log → commit + push

## 注意事项
- 单日请求频率控制：orgId 查询间隔 0.15s，公告查询间隔 0.1s
- 披露高峰期（如科创板半年报 8/25-8/31 约 70% 集中披露）单次可能新增几十家，先批量入库 L1 页，再分批升级深度页
- 数据以 PDF 原文为准，提取失败时检查 `text_sample` 确认表格格式再调正则
