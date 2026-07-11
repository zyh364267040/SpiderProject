# cnas_laboratory_spider

CNAS 实验室公开信息采集案例，按地区查询获认可实验室，并解析实验室名称、联系人、公开电话、网址和地址等字段。

## 文件说明

- `cnas_laboratory_spider_1.py`：验证码与查询接口测试版本，历史会话信息已删除。
- `cnas_laboratory_spider_2.py`：Selenium 浏览器采集版本，支持查询、翻页、详情解析和 Excel 保存。

## 整理说明

本目录只保留核心代码。历史 Excel 结果、调试 HTML、验证码图片、`.DS_Store` 和浏览器会话信息未迁移。旧版代码依赖 Selenium 和本地 ChromeDriver，重新运行前需要按照当前 Selenium 版本调整驱动初始化方式和页面定位规则。

请仅采集依法公开且确有合理用途的信息，遵守 CNAS 网站服务规则，控制访问频率，并妥善处理联系人和电话号码等个人信息。
