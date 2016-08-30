from pandas import DataFrame
import pandas as pd

"""
Descripe:
    使用 python pandas module 作為讀取 excel 檔案方法。
    讀取的資料返回格式有兩種：DataFrame, Series

Usage:
    read excel data
    >>> xlsx_factory = connect_to('bm-v23.xlsx')
    
    select the format(.parsed_data or .parsed_seriesdata)
    >>> xlsx_data = xlsx_factory.parsed_data
    >>> xlsx_data_s = xlsx_factory.parsed_seriesdata
"""


class XLSconnector:
    """xlsx data structure is pandas"""

    def __init__(self, filepath, sheetname):
        if getattr(self, 'FATP', True):
            sheetname = 'FATP'
        #self.data = pd.read_excel(filepath, sheetname, index_col=None, na_values=['NA'])
        self.data = pd.read_excel(filepath, sheetname)
    
    @property    
    def parsed_data(self):
        return self.data

    @property
    def parsed_seriesdata(self):
        return pd.Series([range(len(self.data.index))], index=self.data)
    

def connection_factory(filepath, sheetname):
    if filepath.endswith('xlsx'):
        connector = XLSconnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector(filepath, sheetname)


def connect_to(filepath, sheetname='FATP'):
    """if not setting sheet name the defautl is FATP"""
    factory = None
    try:
        factory = connection_factory(filepath, sheetname)
    except Exception as e:
        print('error:', e)
    return factory


def main():
    xlsx_factory = connect_to('bm-v23.xlsx')
    xlsx_data = xlsx_factory.parsed_data
    xlsx_data_s = xlsx_factory.parsed_seriesdata


if __name__ == '__main__':
    main()



    
