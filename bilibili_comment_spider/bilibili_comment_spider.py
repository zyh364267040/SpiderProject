# -*- coding: utf-8 -*-
"""
Bilibili 评论采集脚本

功能：
1. 请求 B 站评论接口
2. 解析 JSON / JSONP 返回数据
3. 提取评论 ID、评论内容、发布时间、点赞数、用户名、性别、用户 ID
4. 自动分页采集
5. 去重后保存为 Excel

说明：
- OID 是 B 站视频的 aid，不是 BV 号。
- 旧接口可能随 B 站调整而失效，运行前需要根据当前页面接口更新参数。
"""

import json
import math
import re
import time
from datetime import datetime

import pandas as pd
import requests


API_URL = "https://api.bilibili.com/x/v2/reply/main"
VIDEO_OID = 338896747
REFERER = "https://www.bilibili.com/video/BV1HR4y1775Z"
OUTPUT_FILE = "bilibili_comments.xlsx"
PAGE_SIZE = 20
REQUEST_DELAY = 1
TIMEOUT = 15

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": REFERER,
}


def parse_json_response(text):
    """兼容 JSON 和 JSONP 两种返回格式。"""
    text = text.strip()
    if text.startswith("{"):
        return json.loads(text)

    match = re.search(r"\(({.*})\)", text)
    if not match:
        raise ValueError("接口返回内容不是有效 JSON/JSONP")

    return json.loads(match.group(1))


def get_comment_page(page, oid=VIDEO_OID):
    """获取指定页评论数据。"""
    params = {
        "next": page,
        "type": 1,
        "oid": oid,
        "mode": 2,
        "plat": 1,
    }

    response = requests.get(API_URL, headers=HEADERS, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return parse_json_response(response.text)


def parse_replies(json_data):
    """从接口数据中解析评论列表。"""
    replies = json_data.get("data", {}).get("replies") or []
    rows = []

    for reply in replies:
        member = reply.get("member", {})
        content = reply.get("content", {})
        ctime = reply.get("ctime")

        rows.append({
            "id": reply.get("rpid"),
            "content": content.get("message", ""),
            "ctime": datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S") if ctime else "",
            "like": reply.get("like", 0),
            "uname": member.get("uname", ""),
            "sex": member.get("sex", ""),
            "mid": member.get("mid", ""),
        })

    return rows


def get_total_pages(first_page_data):
    """根据第一页数据计算总页数。"""
    total = first_page_data.get("data", {}).get("cursor", {}).get("all_count", 0)
    if not total:
        return 1
    return max(1, math.ceil(total / PAGE_SIZE))


def collect_comments(oid=VIDEO_OID, max_pages=None):
    """采集指定视频评论。"""
    print(f"开始采集视频评论，oid={oid}")
    first_page_data = get_comment_page(1, oid=oid)
    total_pages = get_total_pages(first_page_data)

    if max_pages:
        total_pages = min(total_pages, max_pages)

    print(f"预计采集 {total_pages} 页")
    all_rows = parse_replies(first_page_data)

    for page in range(2, total_pages + 1):
        print(f"正在采集第 {page}/{total_pages} 页")
        try:
            page_data = get_comment_page(page, oid=oid)
            all_rows.extend(parse_replies(page_data))
            time.sleep(REQUEST_DELAY)
        except requests.RequestException as error:
            print(f"第 {page} 页请求失败：{error}")
        except Exception as error:
            print(f"第 {page} 页解析失败：{error}")

    return all_rows


def save_to_excel(rows, output_file=OUTPUT_FILE):
    """保存评论数据到 Excel。"""
    if not rows:
        print("没有采集到评论数据")
        return None

    df = pd.DataFrame(rows)
    df.drop_duplicates(subset=["id"], inplace=True)
    df.to_excel(output_file, index=False)
    print(f"已保存 {len(df)} 条评论到：{output_file}")
    return output_file


def main():
    rows = collect_comments(oid=VIDEO_OID)
    save_to_excel(rows, output_file=OUTPUT_FILE)


if __name__ == "__main__":
    main()
