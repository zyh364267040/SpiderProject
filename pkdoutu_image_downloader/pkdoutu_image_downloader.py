# -*- coding: utf-8 -*-
# @Time: 2022/9/17 19:33
"""
皮卡斗图图片下载脚本

功能：
1. 爬取 https://www.pkdoutu.com/photo/list/ 的表情包图片地址
2. 自动创建 img 文件夹
3. 支持多页采集
4. 使用线程池并发下载
5. 自动去重，避免重复下载
6. 下载失败时给出提示，不中断整体任务
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests
from lxml import etree


BASE_URL = "https://www.pkdoutu.com/photo/list/"
OUTPUT_DIR = "img"
START_PAGE = 1
END_PAGE = 4
MAX_WORKERS = 10
TIMEOUT = 15

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/105.0.0.0 Safari/537.36"
    )
}


def get_page_html(page):
    """请求列表页 HTML。"""
    url = f"{BASE_URL}?page={page}"
    print(f"正在请求第 {page} 页：{url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"第 {page} 页请求失败：{error}")
        return ""


def parse_image_urls(html):
    """从列表页 HTML 中提取图片地址。"""
    if not html:
        return []

    tree = etree.HTML(html)
    if tree is None:
        return []

    img_urls = tree.xpath('//li[@class="list-group-item"]//img/@data-original')

    # 兼容部分图片使用 src，而不是 data-original
    if not img_urls:
        img_urls = tree.xpath('//li[@class="list-group-item"]//img/@src')

    result = []
    for img_url in img_urls:
        if not img_url:
            continue
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        if img_url.startswith("http") and img_url not in result:
            result.append(img_url)

    return result


def collect_image_urls(start_page=START_PAGE, end_page=END_PAGE):
    """采集多页图片地址并去重。"""
    all_img_urls = []

    for page in range(start_page, end_page + 1):
        html = get_page_html(page)
        img_urls = parse_image_urls(html)
        print(f"第 {page} 页提取到 {len(img_urls)} 张图片")

        for img_url in img_urls:
            if img_url not in all_img_urls:
                all_img_urls.append(img_url)

        time.sleep(1)

    print(f"共采集到 {len(all_img_urls)} 张不重复图片")
    return all_img_urls


def build_filename(img_url):
    """根据图片 URL 生成本地文件名。"""
    path = urlparse(img_url).path
    filename = os.path.basename(path)

    if not filename:
        filename = "image.jpg"

    return filename


def download_image(img_url, output_dir=OUTPUT_DIR):
    """下载单张图片。"""
    os.makedirs(output_dir, exist_ok=True)

    filename = build_filename(img_url)
    save_path = os.path.join(output_dir, filename)

    if os.path.exists(save_path):
        print(f"已存在，跳过：{filename}")
        return save_path

    try:
        response = requests.get(img_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        with open(save_path, "wb") as file:
            file.write(response.content)

        print(f"下载成功：{filename}")
        return save_path
    except requests.RequestException as error:
        print(f"下载失败：{img_url}，原因：{error}")
        return None


def download_images(img_urls, output_dir=OUTPUT_DIR, max_workers=MAX_WORKERS):
    """使用线程池批量下载图片。"""
    if not img_urls:
        print("没有可下载的图片")
        return []

    success_files = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tasks = [
            executor.submit(download_image, img_url, output_dir)
            for img_url in img_urls
        ]

        for future in as_completed(future_tasks):
            save_path = future.result()
            if save_path:
                success_files.append(save_path)

    print(f"下载完成，成功 {len(success_files)} 张")
    return success_files


def main():
    """主入口。"""
    img_urls = collect_image_urls(start_page=START_PAGE, end_page=END_PAGE)
    download_images(img_urls, output_dir=OUTPUT_DIR, max_workers=MAX_WORKERS)


if __name__ == "__main__":
    main()
