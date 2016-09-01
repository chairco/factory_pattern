"""
Descripe:
    專為 Nimbus Build Matrix 做的 filter 工具，可以找出 main table 與 sub table 座標位置
    並且轉為二維的表格。

    對於 build matrix 分為兩個表格 main, sub table. 
    main table 需要三個座標判斷從第幾行 row 的 column 開始，因此為 row start, column start, row end 
    sub table 需要四個座標，因為要在切兩個表格並且建立一個新的表格 row start, column segmentation(1,2), row end
    這幾個值做定義：
    main table:
        - row start: m_row_s
        - column start: m_col_s
        - row end: row_e
    sub table:
        - row start: s_row_s
        - column segmentation 1: s_col_seg1(=m_col_s)
        - column segmentation 2: s_col_seg2(=m_col_s+1)
        - row end: row_e
    total:
        - 3 position


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

    def __init__(self, content, filter_type=None, filepath=None):
        self.content = content
        self.filter_type = filter_type

    @property
    def datatype(self):
        return isinstance(self.content, pd.DataFrame)

    def position(self):
        if self.filter_type is None:
            return None #TODO 這裡怪怪傳 None ??
        else:
            return self.filter_type(self)

    @property
    def main_table(self):
        self.df = self.content
        position = self.position()

        row_s, row_e = position['row_s'], position['row_e'] - 1
        col_s = position['col_s']
        self.df = self.df.iloc[row_s:row_e, col_s:].copy() #根據座標切割資料
        self.df = self.df.T #轉正資料
        return self.df

    @property
    def sub_table(self):
        pass
    

    def __repr__(self):
        fmt = '<Content position: {}, type: {}>'
        return fmt.format(self.position(), self.datatype) 


def bm_filter(NimbusBM):
    """This is filter method for Nimbus Build Matrix"""
    init = True
    m_row_s, m_col_s = None, None
    for row in range(0, len(NimbusBM.content.values)):
        for col in range(0, len(NimbusBM.content.values[row])):
            if (str(NimbusBM.content.values[row][col]).upper() == "Configs".upper() and
                init):
                if init: m_row_s, m_col_s = row, col
                init = False
        if (isinstance(NimbusBM.content.values[row][0], str) and 
            not NimbusBM.content.isnull().values[row].any()):
            return {'m_row_s': m_row_s,
                    'm_col_s': m_col_s,
                    's_row_s': row,
                    'row_e': len(NimbusBM.content.values[row])}


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
            return {'head_s': row_s,
                    'head_e': row_e,
                    'row_s': row + 1,
                    'row_e': len(NimbusBM.content.values[row])}


#process: 讀入資料 parse data -> 根據 filter strategy 取得 position(但這邊要建立一個容器儲存(4座標)) -> 再用 nimbusbmdata 轉出適合格式
def main():
    xlsx_factory = bm.connect_to('bm-v23.xlsx')
    xlsx_data = xlsx_factory.parsed_data
    #print(NimbusBM(xlsx_data, main_filter))
    #print(NimbusBM(xlsx_data, bm_filter))

    # main_table() other
    df = NimbusBM(xlsx_data, main_filter).main_table
    #df.to_csv(datetime.now().strftime("%y%m%d_%H%M")+'.csv', header=False, index=False) #寫入 csv


'''
    # sub_table() 
    #TODO(yichihe)here should modify new format
    """處理流程:
    取得座標，一行一行處理補齊 item, compoment, sku(configs)
    補完之後重新建立一個新的 DataFrame（header 要增加一欄位）接著儲存。"""

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
    '''
    

if __name__ == '__main__':
    main()

