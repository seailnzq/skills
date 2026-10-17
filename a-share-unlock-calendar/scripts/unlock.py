#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股限售解禁日历批量查询（东方财富数据中心 RPT_LIFT_STAGE）。

用法:
  uv run unlock.py 688041 688981 688702 --months 24 --out lift_out.json
  uv run unlock.py 688820 --days 365

设计要点:
  - 仅标准库（urllib），无第三方依赖，uv run 或 python 均可执行。
  - stdout 只打印 ASCII 日志（规避 Git Bash GBK 乱码）；含中文的结果写入 UTF-8 JSON，
    由调用方用 Read 工具读取。
  - 服务端拿全量后客户端过滤: 今日 <= FREE_DATE <= 窗口末。
  - 单位: LIFT_MARKET_CAP=万元(脚本已换算为亿元), CURRENT_FREE_SHARES/ABLE_FREE_SHARES=万股,
    FREE_RATIO/TOTAL_RATIO=小数(脚本已 x100 转成百分数字段 *_pct)。
"""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://datacenter-web.eastmoney.com/api/data/v1/get"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://data.eastmoney.com/",
}


def fetch_page(code: str, page: int, timeout: int = 20):
    """拉取一个分页。返回 (rows, total_pages)。"""
    params = {
        "sortColumns": "FREE_DATE",
        "sortTypes": "1",
        "pageSize": "50",
        "pageNumber": str(page),
        "reportName": "RPT_LIFT_STAGE",
        "columns": "ALL",
        "filter": '(SECURITY_CODE="%s")' % code,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    result = payload.get("result") or {}
    return result.get("data") or [], int(result.get("pages") or 1)


def get_num(item: dict, *keys):
    """按候选键名取数值字段（兼容 TOTAL_RATIO / TOTALSHARES_RATIO 等差异）。"""
    for k in keys:
        v = item.get(k)
        if isinstance(v, (int, float)):
            return v
    return None


def window_end(today: datetime.date, months: int, days=None) -> datetime.date:
    if days:
        return today + datetime.timedelta(days=days)
    total = today.month - 1 + months
    year = today.year + total // 12
    month = total % 12 + 1
    day = min(today.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
                          else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime.date(year, month, day)


def collect(code: str, start_iso: str, end_iso: str):
    """抓取单个代码窗口内的未来解禁记录。"""
    items, page, retries = [], 1, 0
    while True:
        try:
            rows, pages = fetch_page(code, page)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            if retries == 0:
                retries = 1
                print("[retry] %s page %d: %s" % (code, page, exc.__class__.__name__))
                continue
            print("[err] %s page %d failed: %s" % (code, page, exc.__class__.__name__))
            break
        for row in rows:
            date_str = (row.get("FREE_DATE") or "")[:10]
            if not date_str or date_str < start_iso or date_str > end_iso:
                continue
            cap_wan = get_num(row, "LIFT_MARKET_CAP")
            shares_wan = get_num(row, "CURRENT_FREE_SHARES")
            able_wan = get_num(row, "ABLE_FREE_SHARES")
            free_ratio = get_num(row, "FREE_RATIO")
            total_ratio = get_num(row, "TOTAL_RATIO", "TOTALSHARES_RATIO")
            items.append({
                "code": code,
                "name": row.get("SECURITY_NAME_ABBR"),
                "free_date": date_str,
                "type": row.get("FREE_SHARES_TYPE"),
                "holder_num": row.get("BATCH_HOLDER_NUM"),
                "lift_market_cap_yi": round(cap_wan / 10000.0, 2) if cap_wan is not None else None,
                "current_free_shares_wan": shares_wan,
                "current_free_shares_yi": round(shares_wan / 10000.0, 3) if shares_wan is not None else None,
                "able_free_shares_wan": able_wan,
                "free_ratio_pct": round(free_ratio * 100, 4) if free_ratio is not None else None,
                "total_ratio_pct": round(total_ratio * 100, 4) if total_ratio is not None else None,
                "ref_price": row.get("NEW"),
                "raw": row,
            })
        if page >= pages:
            break
        page += 1
    return items


def main():
    parser = argparse.ArgumentParser(description="A股限售解禁日历查询 (RPT_LIFT_STAGE)")
    parser.add_argument("codes", nargs="+", help="6位A股代码，可多个")
    parser.add_argument("--months", type=int, default=12, help="未来窗口月数，默认12")
    parser.add_argument("--days", type=int, help="未来窗口天数（优先于 --months）")
    parser.add_argument("--out", default="lift_out.json", help="UTF-8 JSON 输出路径")
    args = parser.parse_args()

    today = datetime.date.today()
    end = window_end(today, args.months, args.days)
    start_iso, end_iso = today.isoformat(), end.isoformat()

    all_items, missing = [], []
    for code in args.codes:
        if len(code) != 6 or not code.isdigit():
            print("[skip] invalid code: %s" % code)
            missing.append(code)
            continue
        items = collect(code, start_iso, end_iso)
        all_items.extend(items)
        print("[ok] %s: %d future unlock rows" % (code, len(items)))

    all_items.sort(key=lambda x: (x["free_date"], -(x["lift_market_cap_yi"] or 0)))

    doc = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "eastmoney datacenter RPT_LIFT_STAGE",
        "window": {"start": start_iso, "end": end_iso},
        "codes": args.codes,
        "missing_or_invalid": missing,
        "count": len(all_items),
        "units": {
            "lift_market_cap_yi": "亿元 (converted from 万元)",
            "current_free_shares_wan": "万股",
            "free_ratio_pct": "% of current float (raw API value is decimal fraction, script x100), may exceed 100",
            "total_ratio_pct": "% of total shares (script x100)",
            "holder_num": "解禁户数 BATCH_HOLDER_NUM",
        },
        "items": all_items,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
    print("[done] wrote %s with %d rows" % (args.out, len(all_items)))


if __name__ == "__main__":
    sys.exit(main())
