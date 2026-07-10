# us_census_zipcode_data_spider

美国人口普查局 Census ZIP Code 就业与收入数据采集脚本整理版。

## 文件说明

- `us_census_zipcode_data_spider.py`：根据 ZIP Code 从美国 Census ACS 公开数据接口采集就业、劳动者类型和家庭收入区间等统计信息，并写入 Excel。

## 主要字段

- ZIP Code
- 就业与失业人数
- 16 岁及以上劳动者
- 居家办公人数
- 私营、政府、个体经营和无薪家庭劳动者
- 家庭收入分段
- 家庭收入中位数和平均数

## 整理说明

整理时只保留核心代码，没有迁移历史输入文件、待处理 ZIP Code 列表和 Excel 结果。原代码中的历史 Census API Key 已删除，`eval()` 已替换为更安全的 `ast.literal_eval()`，并修复了 `$100,000 to $149,999` 列写入变量错误。

代码依赖 2020 年 ACS 接口和旧版返回数据下标。后续重新运行前，应核对 Census 当前接口、字段定义和返回结构。
