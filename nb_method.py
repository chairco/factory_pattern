import json
import openpyxl
import pandas as pd


class XLSconnector:

    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = pd.read_csv(f)


    @property
    def parsed_data(self):
        return self.data


def connection_factory(filepath):
    if filepath.endswith('xlsx'):
        connection = XLSconnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connection(filepath)


def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except Exception as e:
        print(e)
    return factory


def main():
    pass


if __name__ == '__main__':
    main()



    
