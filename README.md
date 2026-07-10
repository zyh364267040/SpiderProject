<div align="center">

# SpiderProject

Python 爬虫学习与实战项目集合

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Crawler](https://img.shields.io/badge/Web%20Crawler-Requests%20%7C%20Selenium-green)
![Data](https://img.shields.io/badge/Data-Excel%20%7C%20CSV%20%7C%20Docx-orange)
![Status](https://img.shields.io/badge/Status-Learning%20Project-lightgrey)

</div>

## 项目简介

SpiderProject 是一个 Python 爬虫学习与实战项目仓库，记录了我在网页数据采集、自动化脚本、结构化解析和数据落地过程中的练习案例。

这个仓库不是单一产品，而是多个独立爬虫案例的集合，覆盖了新闻文章采集、企业信息查询、商品数据抓取、航班信息采集、海外网站信息解析等场景。项目主要用于学习 Python 网络请求、XPath / 正则解析、Selenium 浏览器自动化、Excel / CSV / Word 文件生成等能力。

## 项目亮点

- 使用 `requests` 完成网页请求、接口请求和数据获取
- 使用 `lxml`、XPath、正则表达式解析网页结构与接口返回内容
- 使用 `Selenium` 处理需要浏览器自动化或登录态的网站
- 使用 `openpyxl`、`pandas`、`csv`、`python-docx` 等工具保存结构化数据
- 包含多个真实网站场景，便于理解爬虫项目从“请求 → 解析 → 清洗 → 保存”的完整流程
- 项目按案例分目录组织，适合作为 Python 爬虫学习记录与作品集素材

## 技术栈

| 类别 | 技术 |
| --- | --- |
| 编程语言 | Python |
| 网络请求 | requests |
| 页面解析 | lxml / XPath / re |
| 浏览器自动化 | Selenium |
| 数据处理 | pandas / csv / json |
| 文件生成 | openpyxl / python-docx |
| 数据格式 | Excel / CSV / TXT / DOCX / JSON |

## 目录说明

| 目录 | 内容说明 |
| --- | --- |
| `arcteryx/` | 户外品牌商品数据采集与商品信息整理，包含 TXT 转 Excel 的数据处理脚本 |
| `glassdoor/` | 使用 Selenium 登录并采集 Glassdoor 公司评论数据，支持保存为 Excel |
| `lusha_linkedin/` | 从 Lusha 页面获取公司信息，并进一步解析 LinkedIn 页面中的网站与公司介绍 |
| `sunwing/` | 航班与机场信息采集案例，包含航线、国家代码、票务信息等解析逻辑 |
| `tianyancha/` | 天眼查企业信息采集案例，解析公司主营业务、行业、A 股代码等信息 |
| `xzxw/` | 新闻搜索结果采集案例，根据关键词抓取文章并保存为 Word 文档 |
| `reservoir_wiki_spider/` | 中国大型水库公开信息采集案例，从 Wiki 页面解析水库字段并整理为表格数据 |
| `pkdoutu_image_downloader/` | 皮卡斗图表情包图片下载器，支持多页采集、图片地址去重和线程池并发下载 |
| `bilibili_comment_spider/` | B 站视频评论采集案例，解析评论接口并导出评论内容、用户、时间、点赞数等字段 |

## 代表案例

### 1. 新闻文章采集：xzxw

`xzxw` 案例围绕关键词搜索新闻内容，通过接口请求获取搜索结果，再进一步提取文章正文、来源、日期等字段，最后按年份目录保存为 Word 文档。

这个案例体现了：

- POST 请求参数构造
- 分页采集逻辑
- JSON 数据解析
- 文章正文提取
- Word 文档自动生成

### 2. 企业信息采集：tianyancha

`tianyancha` 案例通过搜索企业名称，解析企业详情页链接，再请求接口获取公司基础信息。

这个案例体现了：

- 搜索页解析
- 详情页 ID 提取
- 接口数据请求
- 企业字段结构化输出

### 3. 浏览器自动化采集：glassdoor

`glassdoor` 案例使用 Selenium 处理登录流程和页面访问，再解析公司评论数据并保存到 Excel。

这个案例体现了：

- Selenium 浏览器驱动配置
- 登录表单自动填写
- 页面源码获取
- 评论数据解析
- Excel 文件写入

### 4. 航班信息采集：sunwing

`sunwing` 案例通过接口和网页解析获取航班、机场、国家代码等信息，并判断国内 / 国际航线。

这个案例体现了：

- API 数据请求
- JSON 数据遍历
- 多接口组合调用
- Excel 表格生成

### 5. 商品数据采集：arcteryx

`arcteryx` 案例采集商品链接、商品基础信息、价格、图片等内容，并配套 TXT 转 Excel 脚本，便于后续整理商品数据。

这个案例体现了：

- 商品列表解析
- 商品详情字段提取
- 图片链接处理
- 批量数据保存
- 电商数据表格化整理

### 6. 水库公开信息采集：reservoir_wiki_spider

`reservoir_wiki_spider` 案例面向中国大陆大型水库公开信息页面，采集水库名称、坐标、位置、库容、坝高、装机容量等字段，并整理为可表格化处理的数据。

这个案例体现了：

- Wiki / HTML 表格页面解析
- 详情页链接提取与拼接
- 多字段字典映射
- Excel 表格写入
- 与水利行业背景相关的数据采集思路

### 7. 表情包图片下载：pkdoutu_image_downloader

`pkdoutu_image_downloader` 案例用于从皮卡斗图列表页采集表情包图片地址，并批量下载到本地目录。脚本经过整理后支持多页采集、自动创建保存目录、图片地址去重、异常处理和线程池并发下载。

这个案例体现了：

- 图片列表页解析
- `data-original` / `src` 图片地址提取
- 图片 URL 去重与文件名处理
- 线程池并发下载
- 下载失败跳过与日志提示

### 8. B 站评论采集：bilibili_comment_spider

`bilibili_comment_spider` 案例用于采集 B 站视频评论数据，解析评论接口返回内容，提取评论 ID、评论内容、发布时间、点赞数、用户名、性别、用户 ID 等字段，并保存为 Excel 文件。

这个案例体现了：

- B 站评论接口请求
- JSON / JSONP 返回内容解析
- 评论字段结构化提取
- 分页采集与请求间隔控制
- pandas 去重与 Excel 导出

## 项目结构

```text
SpiderProject/
├── README.md
├── arcteryx/
│   ├── arcteryx.py
│   └── txt_to_excel.py
├── glassdoor/
│   ├── glassdoor_selenium.py
│   ├── settings.py
│   └── company_info.txt
├── lusha_linkedin/
│   └── lusha_linkedin.py
├── sunwing/
│   ├── hangban.py
│   └── ticket.py
├── tianyancha/
│   └── tianyancha.py
├── xzxw/
│   └── xzxw.py
├── reservoir_wiki_spider/
│   ├── reservoir_wiki_spider_1.py
│   └── reservoir_wiki_spider_2.py
├── pkdoutu_image_downloader/
│   └── pkdoutu_image_downloader.py
└── bilibili_comment_spider/
    └── bilibili_comment_spider.py
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zyh364267040/SpiderProject.git
cd SpiderProject
```

### 2. 安装常用依赖

```bash
pip install requests lxml selenium openpyxl pandas python-docx
```

### 3. 运行单个案例

进入对应目录后运行脚本，例如：

```bash
cd tianyancha
python tianyancha.py
```

不同案例依赖的网站结构、接口状态、登录状态和浏览器驱动配置可能不同，运行前需要根据实际情况调整参数。

## 注意事项

- 本仓库主要用于 Python 爬虫学习、代码练习和技术复盘。
- 部分网站结构可能已经更新，旧脚本不保证可以直接运行。
- 部分案例涉及登录、验证码、Cookie 或浏览器驱动配置，需要自行按当前环境调整。
- 请遵守目标网站的 robots 协议、服务条款和当地法律法规。
- 请控制请求频率，不要对目标网站造成压力。
- 本项目不提供任何绕过权限、批量滥用或非法采集的用途支持。

## 学习收获

通过这个项目，我主要练习了：

- Python 网络请求基础
- 网页结构分析与 XPath 定位
- 正则表达式在网页解析中的使用
- Selenium 自动化浏览器操作
- JSON / CSV / Excel / Word 等多种数据保存方式
- 多页面、多接口、多字段的数据采集流程设计
- 将非结构化网页内容整理为结构化数据的基本思路

## 后续计划

- 整理每个案例的运行说明和参数配置
- 补充 `requirements.txt`
- 为典型案例增加流程图和字段说明
- 将旧脚本逐步重构为更清晰的模块化结构
- 增加异常处理、日志记录和配置文件管理

## 免责声明

本仓库代码仅用于 Python 编程学习、网络数据采集原理研究和个人技术记录。请勿将本项目用于任何违反法律法规、侵犯隐私、违反网站服务条款或影响网站正常运行的行为。由使用者不当使用造成的任何后果，与本仓库作者无关。

