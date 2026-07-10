# phenoscanner_snp_gwas_spider

PhenoScanner SNP/GWAS 关联数据采集脚本整理版。

## 文件说明

- `phenoscanner_snp_gwas_spider.py`：从 CSV 输入文件读取 SNP 编号，逐条查询 PhenoScanner GWAS 页面，提取关联结果并保存为 CSV。

## 采集字段

- SNP
- Trait
- PMID
- Beta
- P

## 整理说明

整理时只保留核心代码，没有迁移客户输入 CSV、历史采集结果、HTML 缓存和重复备份。原代码中的历史访问会话信息已删除，并修正了 `requests.get()` 的请求头参数写法。

如需重新运行，需要准备包含 `SNP` 列的输入 CSV，并根据 PhenoScanner 当前页面结构核对查询参数和 XPath。涉及医学遗传学数据时，应遵守数据来源、授权和隐私要求。
