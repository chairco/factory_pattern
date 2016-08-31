"""
Descripe:
    專為 Nimbus Build Matrix 做的 filter 工具，可以找出 main table 與 sub table 座標位置
    並且轉為二維的表格

Usage:
    >>> xlsx_factory = bm.connect_to('bm-v23.xlsx')
    >>> xlsx_data = xlsx_factory.parsed_data
    >>> print(NimbusBM(xlsx_data, main_filter))
    <Content position: {'row_s': 2, 'col_e': 70, 'col_s': 54, 'row_e': 44}, type: True>
    >>> print(NimbusBM(xlsx_data, sub_filter))
    <Content position: {'head_e': 54, 'head_s': 45, 'row_s': 46, 'row_e': 70}, type: True>

"""

import json
import pandas as pd
from datetime import datetime

import bm_method as bm


class NimbusBM:

    def __init__(self, content, filter_type=None):
        self.content = content
        self.filter_type = filter_type

    @property
    def datatype(self):
        return isinstance(self.content, pd.DataFrame)

    def position(self):
        if self.filter_type is None:
            return 0 #TODO 這裡怪怪傳 0 ??
        else:
            return self.filter_type(self)

    def __repr__(self):
        fmt = '<Content position: {}, type: {}>'
        return fmt.format(self.position(), self.datatype) 


class NimbusbmData:

    def __init__(self, df, position, filepath=None):
        self.df = df
        self.position = position
        self.filepath = filepath

    def main_table(self):
        pass

    def sub_table(self):
        row_s, row_e = self.position['row_s'], self.position['row_e']
        col_s = self.position['col_s']
        self.df = self.df.iloc[row_s:row_e, col_s:].copy() #根據座標切割資料
        self.df = self.df.T #轉正資料
        return self.df


def main_filter(NimbusBM):
    """This is filter method for main table"""
    init = True
    row_s = None
    row_e = None
    for row in range(0, len(NimbusBM.content.values)):
        for col in range(0, len(NimbusBM.content.values[row])):
            if (str(NimbusBM.content.values[row][col]).upper() == "Configs".upper() and
                init):
                init = False
                row_s, row_e = row, col
        if (isinstance(NimbusBM.content.values[row][0], str) and 
            not NimbusBM.content.isnull().values[row].any()):
            return {'row_s': row_s,
                    'row_e': row - 1,
                    'col_s': row_e,
                    'col_e': len(NimbusBM.content.values[row])}


def sub_filter(NimbusBM):
    """This is filter method for sub table"""
    init = True
    row_e = None
    for row in range(0, len(NimbusBM.content.values)):
        for col in range(0, len(NimbusBM.content.values[row])):
            if (str(NimbusBM.content.values[row][col]).upper() == "Configs".upper() and
                init):
                init = False
                row_e = col
        if (isinstance(NimbusBM.content.values[row][0], str) and 
            not NimbusBM.content.isnull().values[row].any()):
            return {'head_s': row,
                    'head_e': row_e,
                    'row_s': row + 1,
                    'row_e': len(NimbusBM.content.values[row])}


def main():
    xlsx_factory = bm.connect_to('bm-v23.xlsx')
    xlsx_data = xlsx_factory.parsed_data
    print(NimbusBM(xlsx_data, sub_filter))
    
    # main_table()
    position = NimbusBM(xlsx_data, main_filter).position()
    df = NimbusbmData(xlsx_data, position, 'test.csv').sub_table()
    df.to_csv(datetime.now().strftime("%y%m%d_%H%M")+'.csv', header=False, index=False) #寫入 csv

    #TODO(yichihe)
    # sub_table() here should modify new format
    """處理流程:
    取得座標，一行一行處理補齊 item, compoment, sku(configs)
    補完之後重新建立一個新的 DataFrame（header 要增加一欄位）接著儲存。
    """
    sub = NimbusBM(xlsx_data, sub_filter).position()
    header = list() # save header
    for r in range(sub['head_s'], sub['head_s']+1):
        for c in range(0, sub['head_e']):
            header.append(xlsx_data.values[r][c])
    header.append('configs')

    content = list() # save content
    item, comp = None, None
    for r in range(sub['row_s'], len(xlsx_data.index)):
        if isinstance(xlsx_data.values[r][0], str):
            item = xlsx_data.values[r][0]
        elif isinstance(xlsx_data.values[r][1], str):
            comp = xlsx_data.values[r][1]
        else:
            xlsx_data.values[r][0] = item
            xlsx_data.values[r][1] = comp
            content.append(xlsx_data.values[r][:sub['head_e']])
        for c in range(sub['head_e']+1, sub['row_e']):
            if xlsx_data.notnull().values[r][c]:
                print(xlsx_data.values[sub['row_s']-1][c])
    df_content = xlsx_data[46:48].copy()
    print(df_content)
    

if __name__ == '__main__':
    main()

