# focus2career_occupation_spider

Focus 2 Career 职业信息采集脚本整理版。

## 文件说明

- `focus2career_occupation_spider_1.py`：采集职业分类、名称、概述、工作任务、兴趣画像、技能、价值观、工作环境、教育要求、晋升发展和专业协会，并写入 Excel。
- `focus2career_occupation_spider_2.py`：将职业技能和价值观条目拆分为独立结构，并分别写入 Excel。

## 整理说明

整理时只保留核心代码，没有迁移历史 Excel 结果。两个脚本中的历史登录会话信息已删除，第一版中用于调试的大段采集结果示例也已清理。

代码仍引用 Focus 2 Career 的登录后页面路径，但仓库不提供任何登录凭据或平台数据。重新运行前，使用者应取得合法访问授权，并根据当前页面结构调整入口地址和 XPath；同时遵守平台服务规则、内容版权和数据使用要求。
