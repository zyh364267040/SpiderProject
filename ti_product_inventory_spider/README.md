# ti_product_inventory_spider

德州仪器（Texas Instruments，TI）产品型号与库存信息采集案例。项目读取产品型号列表，请求 TI 产品接口，解析子型号及库存数量，并支持结果保存和已完成型号去重。

## 文件说明

- `ti_product_inventory_spider_1.py`：早期产品详情与库存采集版本。
- `ti_product_inventory_spider_2.py`：第二版采集脚本。
- `ti_product_inventory_spider_3.py`：按产品清单采集库存并通过 `done.csv` 记录进度的简化版本；Cookie 仅在运行时输入。
- `product_model_csv_to_excel.py`：产品型号 CSV 去重并转换为 Excel。
- `browser_cookie_refresh_helper.py`：旧版基于固定屏幕坐标的浏览器辅助操作脚本，仅作历史实现参考。

## 整理说明

历史硬编码 Cookie 已删除。本目录未迁移产品清单、历史 CSV/Excel 结果、失败记录、缓存文件和 `.DS_Store`。重新运行前，需要自行准备合法来源的产品型号清单，并根据 TI 当前接口和访问规则调整参数。

浏览器辅助脚本依赖固定屏幕坐标，可能直接操作鼠标和键盘，不能在不了解代码行为时运行。使用采集脚本时请遵守 TI 网站服务规则并控制请求频率。
