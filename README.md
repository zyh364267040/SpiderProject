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
| `xuetiger_exam_question_spider/` | 学虎网在线题库题目采集案例，按题号请求题目、选项和答案并保存为文本 |
| `freepik_image_downloader/` | Freepik 图片下载案例，从搜索页解析图片地址并保存到本地目录 |
| `glassdoor_review_interview_spider/` | Glassdoor 公司评论与面试经验采集案例，包含 Reviews 和 Interviews 两类页面解析脚本 |
| `ydl_expert_info_spider/` | ydl.com 专家信息采集案例，解析专家列表页和详情页并导出咨询、评价、价格等字段 |
| `csres_dl_standard_spider/` | 中国标准服务网 DL 电力行业标准信息采集案例，解析标准编号、名称、状态和替代情况等字段 |
| `google_patents_link_spider/` | Google Patents 专利搜索结果链接采集案例，按关键词和语言条件批量提取专利详情页链接 |
| `us_census_zipcode_data_spider/` | 美国 Census ZIP Code 就业与收入公开数据采集案例，按邮政编码提取 ACS 统计字段 |
| `samr_national_standard_spider/` | 国家标准信息公共服务平台采集案例，按关键词检索国家标准并解析标准号、类别及日期等字段 |
| `phenoscanner_snp_gwas_spider/` | PhenoScanner SNP/GWAS 关联数据采集案例，批量查询 SNP 并提取 Trait、PMID、Beta、P 等字段 |
| `haodf_doctor_spider/` | 好大夫在线医生公开职业信息采集案例，按地区采集医生、医院、公开电话、地址和门诊时间 |
| `focus2career_occupation_spider/` | Focus 2 Career 职业信息采集案例，解析职业概述、任务、技能、价值观、教育要求等字段 |
| `cnas_laboratory_spider/` | CNAS 实验室公开信息采集案例，按地区查询实验室并解析名称、联系人、公开电话、网址和地址 |
| `ti_product_inventory_spider/` | TI 产品型号与库存信息采集案例，支持产品清单读取、库存解析、进度去重和表格转换 |
| `drug_information_spider/` | 多来源药品公开信息采集案例，整合 RxList、DrugFuture 和药智网的药品说明、规格及企业字段 |

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

### 9. 在线题库题目采集：xuetiger_exam_question_spider

`xuetiger_exam_question_spider` 案例用于按题号请求在线题库页面，解析题目、选项和正确答案，并将结果保存为文本文件。原始历史登录凭据已删除，保留的是题库页面请求、XPath 解析和文本落地的代码结构。

这个案例体现了：

- 在线题库接口请求
- HTML 页面 XPath 解析
- 题目、选项、答案字段提取
- 文本文件追加保存
- 历史登录凭据清理后的代码归档方式

### 10. Freepik 图片下载：freepik_image_downloader

`freepik_image_downloader` 案例用于从 Freepik 搜索结果页解析图片地址，并将图片下载到本地目录。整理入库时只保留核心代码，未提交历史下载图片和 HTML 缓存，避免把第三方图片素材上传到代码仓库。

这个案例体现了：

- 搜索结果页请求
- 图片 `data-src` 地址解析
- 图片 URL 清洗
- 本地目录创建与二进制图片保存
- 第三方素材不入库的代码整理原则

### 11. Glassdoor 评论与面试经验采集：glassdoor_review_interview_spider

`glassdoor_review_interview_spider` 案例用于采集 Glassdoor 公司 Reviews 评论和 Interviews 面试经验页面。整理时只保留两个核心脚本，历史 URL 列表和采集结果数据未提交到仓库。

这个案例体现了：

- Selenium 浏览器自动化采集
- BeautifulSoup 页面解析
- Reviews 评论字段提取
- Interviews 面试经验字段提取
- 多线程任务分发与批量 URL 处理思路

### 12. ydl 专家信息采集：ydl_expert_info_spider

`ydl_expert_info_spider` 案例用于采集 ydl.com 专家列表页和详情页信息，提取专家姓名、性别、咨询数、在线帮助人数、服务时长、起价、好评率、评价数量、星级、从业年限等字段，并写入 Excel。整理时只保留核心代码，历史 Excel 结果和历史登录凭据未提交到仓库。

这个案例体现了：

- 列表页与详情页联动采集
- PC 页面和移动页面字段互补解析
- XPath 多字段提取
- openpyxl 写入 Excel
- 历史访问凭据清理后的代码归档方式

### 13. CSRES 电力行业标准采集：csres_dl_standard_spider

`csres_dl_standard_spider` 案例用于采集中国标准服务网 CSRES 中 DL 电力行业标准信息，提取标准编号、标准名称、发布部门、实施日期、状态、替代情况等字段，并写入 Excel。整理时只保留核心代码，历史 Excel 结果、HTML 缓存和临时测试脚本未提交到仓库。

这个案例体现了：

- 行业标准列表页分页采集
- 标准详情页链接拼接与请求
- 替代情况字段解析
- openpyxl 写入 Excel
- 断点续爬思路

### 14. Google Patents 专利链接采集：google_patents_link_spider

`google_patents_link_spider` 案例用于请求 Google Patents 搜索接口，按关键词、语言和页码条件批量提取专利详情页链接，并保存为文本。整理时只保留核心代码，历史链接结果文件未提交到仓库。

这个案例体现了：

- Google Patents 搜索接口请求
- 翻页采集
- JSON 响应字段解析
- 专利详情 URL 拼接
- 搜索结果链接落地保存

### 15. 美国 Census ZIP Code 数据采集：us_census_zipcode_data_spider

`us_census_zipcode_data_spider` 案例用于根据 ZIP Code 从美国 Census ACS 公开数据接口采集就业、劳动者类型和家庭收入区间等统计字段，并写入 Excel。整理时只保留核心代码，历史输入和结果文件未提交到仓库，历史 API Key 已删除。

这个案例体现了：

- Census ACS 公开数据接口请求
- ZIP Code 筛选与剩余任务保存
- 就业和家庭收入多字段提取
- openpyxl 写入 Excel
- 中断后继续处理的思路

### 16. SAMR 国家标准信息采集：samr_national_standard_spider

`samr_national_standard_spider` 案例用于从国家标准信息公共服务平台按关键词分页检索国家标准，提取标准 ID 后进入详情页，采集标准号、标准名称、标准类别、批准日期和实施日期，并写入 Excel。

这个案例体现了：

- 国家标准搜索结果分页采集
- 标准 ID 提取与详情页请求
- XPath 多字段解析
- openpyxl 写入 Excel
- 请求间隔与随机 User-Agent

### 17. PhenoScanner SNP/GWAS 数据采集：phenoscanner_snp_gwas_spider

`phenoscanner_snp_gwas_spider` 案例用于从 CSV 批量读取 SNP 编号，查询 PhenoScanner GWAS 页面，提取 SNP、Trait、PMID、Beta 和 P 值并保存为 CSV。整理时只保留核心代码，客户输入、历史结果、HTML 缓存和历史访问会话信息未提交到仓库。

这个案例体现了：

- CSV 批量读取与 SNP 任务生成
- PhenoScanner GWAS 页面请求
- XPath 表格字段解析
- 关联结果 CSV 保存
- 请求重试与访问间隔控制

### 18. 好大夫在线医生信息采集：haodf_doctor_spider

`haodf_doctor_spider` 案例用于按地区分页采集好大夫在线妇产科医生的公开职业信息，包括姓名、性别、职称、医院名称、医院公开联系电话、地址和门诊时间。整理时只保留核心代码，历史结果和含具体医院排班数据的测试脚本未提交到仓库。

这个案例体现了：

- 医生列表页分页采集
- 医生详情页和门诊页联动请求
- XPath 与正则表达式组合解析
- 失败链接记录和请求重试
- 公开职业信息采集合规意识

### 19. Focus 2 Career 职业信息采集：focus2career_occupation_spider

`focus2career_occupation_spider` 案例用于解析职业分类、职业名称、概述、工作任务、兴趣画像、技能、价值观、工作环境、教育要求、晋升发展和专业协会等字段，并将综合职业信息或拆分后的技能、价值观写入 Excel。整理时只保留核心代码，历史结果、历史登录会话信息和调试数据示例未提交到仓库。

这个案例体现了：

- 职业分类与职业详情页联动采集
- 多模块职业信息解析
- 技能与价值观条目结构化
- openpyxl 写入多类 Excel 结果
- 受限页面凭据清理与合规说明

### 20. CNAS 实验室信息采集：cnas_laboratory_spider

`cnas_laboratory_spider` 案例用于从 CNAS 实验室查询页面按地区检索获认可实验室，解析实验室名称、联系人、公开电话、网址和地址，并将结果写入 Excel。整理时保留接口测试和 Selenium 采集两个版本，历史结果、调试页面、验证码图片和历史会话信息未提交到仓库。

这个案例体现了：

- 验证码辅助查询流程
- Selenium 查询、翻页和页面源码获取
- 实验室详情页 XPath 解析
- openpyxl 写入 Excel
- 联系方式数据最小化与历史会话凭据清理

### 21. TI 产品库存信息采集：ti_product_inventory_spider

`ti_product_inventory_spider` 案例用于批量读取德州仪器产品型号，请求产品及库存接口，解析子型号和库存数量，并通过已完成记录实现去重和继续处理。整理时保留三个采集版本、型号表格转换工具和浏览器辅助脚本，历史 Cookie、产品清单、结果文件及缓存未提交到仓库。

这个案例体现了：

- 产品型号清单批量读取
- 产品详情与库存接口请求
- 子型号及库存数量结构化解析
- CSV / Excel 数据转换与进度去重
- 历史 Cookie 清理和桌面自动化副作用说明

### 22. 多来源药品信息采集：drug_information_spider

`drug_information_spider` 案例从 RxList 获取软胶囊类药品条目和详情说明，再结合 DrugFuture 与药智网补充药品规格及生产企业，并将药品名称、说明内容、规格和企业信息保存为 CSV。整理时只保留核心代码，历史采集结果和失败记录未提交到仓库。

这个案例体现了：

- 多网站药品信息联动查询
- 搜索页、详情页和表单请求组合
- XPath 多字段解析
- CSV 结构化结果保存
- 失败链接追加记录与医疗信息用途说明

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
├── bilibili_comment_spider/
│   └── bilibili_comment_spider.py
├── cnas_laboratory_spider/
│   ├── README.md
│   ├── cnas_laboratory_spider_1.py
│   └── cnas_laboratory_spider_2.py
├── ti_product_inventory_spider/
│   ├── README.md
│   ├── browser_cookie_refresh_helper.py
│   ├── product_model_csv_to_excel.py
│   ├── ti_product_inventory_spider_1.py
│   ├── ti_product_inventory_spider_2.py
│   └── ti_product_inventory_spider_3.py
└── drug_information_spider/
    ├── README.md
    └── drug_information_spider.py
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

