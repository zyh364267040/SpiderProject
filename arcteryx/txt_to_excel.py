# -*- coding = utf-8 -*-
# @Time: 2022/11/3 20:01
import openpyxl


def read_txt():
    data_list = []
    with open('clothes.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            data_list.append(line.strip())
    return data_list


def save_data():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'ID'
    sheet['B1'] = '类型'
    sheet['C1'] = 'SKU'
    sheet['D1'] = '名称'
    sheet['E1'] = '已发布'
    sheet['F1'] = '是推荐产品？'
    sheet['G1'] = '在列表页可见'
    sheet['H1'] = '简短描述'
    sheet['I1'] = '描述'
    sheet['J1'] = '促销开始日期'
    sheet['K1'] = '促销截止日期'
    sheet['L1'] = '税状态'
    sheet['M1'] = '税类'
    sheet['N1'] = '有货？'
    sheet['O1'] = '库存'
    sheet['P1'] = '库存不足'
    sheet['Q1'] = '允许缺货下单？'
    sheet['R1'] = '单独出售？'
    sheet['S1'] = '重量(kg)'
    sheet['T1'] = '长度(cm)'
    sheet['U1'] = '宽度 (cm)'
    sheet['V1'] = '高度 (cm)'
    sheet['W1'] = '允许客户评价？'
    sheet['X1'] = '购物备注'
    sheet['Y1'] = '促销价格'
    sheet['Z1'] = '常规售价'
    sheet['AA1'] = '分类'
    sheet['AB1'] = '标签'
    sheet['AC1'] = '运费类'
    sheet['AD1'] = '图片'
    sheet['AE1'] = '下载限制'
    sheet['AF1'] = '下载的过期天数'
    sheet['AG1'] = '父级'
    sheet['AH1'] = '分组产品'
    sheet['AI1'] = '交叉销售'
    sheet['AJ1'] = '交叉销售'
    sheet['AK1'] = '外部链接'
    sheet['AL1'] = '按钮文本'
    sheet['AM1'] = '位置'
    sheet['AN1'] = '属性1名称'
    sheet['AO1'] = '属性1值'
    sheet['AP1'] = '属性1可见'
    sheet['AQ1'] = '属性1的全局'
    data_list = read_txt()
    for data in data_list:
        page_data = data.split('@')


def main():
    pass


if __name__ == '__main__':
    main()
