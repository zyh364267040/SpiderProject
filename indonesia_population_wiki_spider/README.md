# indonesia_population_wiki_spider

英文 Wikipedia 印度尼西亚行政区与人口公开信息采集案例。项目从印度尼西亚县市列表出发，访问各行政区详情页，解析省、市/县、下级地区及不同年份的人口数据，并保存为 Excel。

## 文件说明

- `indonesia_population_wiki_spider_1.py`：早期人口表格解析和断点续采版本。
- `indonesia_population_wiki_spider_2.py`：采集市、县名称及总人口的简化版本。
- `indonesia_population_wiki_spider_3.py`：按省、市/县、下级地区三级结构采集人口的完整版本。

## 技术栈

- `requests`：Wikipedia 页面请求
- `lxml` / XPath：行政区列表和人口表格解析
- `urllib.parse.urljoin`：详情页链接拼接
- `openpyxl`：人口数据写入 Excel

## 整理说明

本目录只保留三个核心代码版本，没有迁移历史 Excel、失败链接、缓存文件或 `.DS_Store`。历史 Cookie 已删除，请求参数写法已修正，失败链接调整为追加记录。

该项目属于历史学习案例。Wikipedia 页面结构、行政区划和人口年份可能已经变化，重新运行前应核对当前页面结构与数据口径，并控制请求频率。
