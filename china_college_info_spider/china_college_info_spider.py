# -*- coding: utf-8 -*-
"""中国高校公开信息异步采集脚本。

从中国教育在线公开数据接口读取高校基础信息、排名、地区和招生办公开联系方式，
支持限制并发、失败重试、断点续采和统一写入 CSV。
"""

import asyncio
from pathlib import Path
from typing import Any

import aiohttp
import pandas as pd
from tqdm import tqdm

BASE_URL = "https://static-data.eol.cn/www/2.0/school/{school_id}/info.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "college_info.csv"
MAX_SCHOOL_ID = 5000
CONCURRENCY = 20
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

COLUMNS = [
    "学校id",
    "学校名称",
    "学校层次",
    "软科排名",
    "校友会排名",
    "武书连排名",
    "QS世界排名",
    "US世界排名",
    "学校类型",
    "省份",
    "城市",
    "所处地区",
    "招生办电话",
    "招生办官网",
]


def load_completed_ids(output_file: Path = OUTPUT_FILE) -> set[int]:
    """读取历史结果中的学校 ID，用于断点续采。"""
    if not output_file.exists():
        return set()

    try:
        dataframe = pd.read_csv(output_file, usecols=["学校id"])
        return set(dataframe["学校id"].dropna().astype(int).tolist())
    except (ValueError, KeyError, pd.errors.EmptyDataError) as exc:
        print(f"⚠️ 无法读取历史进度，将重新采集：{exc}")
        return set()


def build_school_ids(max_school_id: int, completed_ids: set[int]) -> list[int]:
    """生成尚未完成的学校 ID 列表。"""
    return [school_id for school_id in range(max_school_id) if school_id not in completed_ids]


def parse_school_info(data: dict[str, Any]) -> dict[str, Any]:
    """将接口返回的学校信息转换为稳定的表格字段。"""
    rank = data.get("rank") or {}

    if str(data.get("f985", "")) == "1" and str(data.get("f211", "")) == "1":
        level = "985 211"
    elif str(data.get("f211", "")) == "1":
        level = "211"
    else:
        level = data.get("level_name", "")

    return {
        "学校id": data.get("school_id", ""),
        "学校名称": data.get("name", ""),
        "学校层次": level,
        "软科排名": rank.get("ruanke_rank", ""),
        "校友会排名": rank.get("xyh_rank", ""),
        "武书连排名": rank.get("wsl_rank", ""),
        "QS世界排名": rank.get("qs_world", ""),
        "US世界排名": rank.get("us_rank", ""),
        "学校类型": data.get("type_name", ""),
        "省份": data.get("province_name", ""),
        "城市": data.get("city_name", ""),
        "所处地区": data.get("town_name", ""),
        "招生办电话": data.get("phone", ""),
        "招生办官网": data.get("site", ""),
    }


async def fetch_school(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    school_id: int,
) -> dict[str, Any] | None:
    """请求一所学校的信息；失败时按配置重试。"""
    url = BASE_URL.format(school_id=school_id)

    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with session.get(url) as response:
                    if response.status == 404:
                        return None
                    response.raise_for_status()
                    payload = await response.json(content_type=None)
                    data = payload.get("data") if isinstance(payload, dict) else None
                    return parse_school_info(data) if isinstance(data, dict) and data else None
            except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as exc:
                if attempt == MAX_RETRIES:
                    print(f"⚠️ 学校 ID {school_id} 请求失败：{exc}")
                    return None
                await asyncio.sleep(attempt)

    return None


def save_results(results: list[dict[str, Any]], output_file: Path = OUTPUT_FILE) -> None:
    """将本轮结果统一追加到 CSV，避免多个协程同时写文件。"""
    if not results:
        print("ℹ️ 本轮没有新增学校数据")
        return

    dataframe = pd.DataFrame(results, columns=COLUMNS)
    dataframe.drop_duplicates(subset=["学校id"], inplace=True)
    dataframe.to_csv(
        output_file,
        index=False,
        mode="a",
        header=not output_file.exists(),
        encoding="utf-8-sig",
    )
    print(f"✅ 新增 {len(dataframe)} 所学校，结果已保存：{output_file}")


async def main() -> None:
    """运行高校信息采集任务。"""
    completed_ids = load_completed_ids()
    school_ids = build_school_ids(MAX_SCHOOL_ID, completed_ids)
    print(f"📚 已完成 {len(completed_ids)} 所，待检查 {len(school_ids)} 个学校 ID")

    semaphore = asyncio.Semaphore(CONCURRENCY)
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        )
    }

    async with aiohttp.ClientSession(timeout=timeout, headers=headers, trust_env=True) as session:
        tasks = [asyncio.create_task(fetch_school(session, semaphore, school_id)) for school_id in school_ids]
        results = []
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="采集高校"):
            result = await task
            if result:
                results.append(result)

    save_results(results)


if __name__ == "__main__":
    asyncio.run(main())
