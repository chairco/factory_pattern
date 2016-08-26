import pandas as pd


class XLSconnector:
    def __init__(self, filepath):
        self.data = pd.read_excel(filepath)
        #self.data = dict()
        #with open(filepath, mode='r', encoding='utf-8') as f:
        #    self.data = pd.read_excel(f)

    @property    
    def parsed_data(self):
        return self.data


def connection_factory(filepath):
    if filepath.endswith('xlsx'):
        connector = XLSconnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector(filepath)


def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except Exception as e:
        print('error:', e)
    return factory


def main():
    xlsx_factory = connect_to('test.xlsx')
    xlsx_data = xlsx_factory.parsed_data
    print(xlsx_data)


if __name__ == '__main__':
    main()



    
