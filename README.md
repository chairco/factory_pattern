# factory_pattern
嘗試使用 Factory Pattern 來處理 xlsx 資料。
流程主要為讀入、轉成 data set、然後再給負責處理資料 format 的 api 接手。
 

## How to use

Read .xlsx file:

```python
import pandas as pd
import bm_method as bm_method

xlsx_factory = bm.connect_to('bm-v23.xlsx')

# select the format(.parsed_data or .parsed_seriesdata)
xlsx_data = xlsx_factory.parsed_data
xlsx_data_s = xlsx_factory.parsed_seriesdata

```

Select the position:

```python
import pandas as pd

import bm_method as bm_method

import filter as f


xlsx_factory = bm.connect_to('bm-v23.xlsx')
xlsx_data = xlsx_factory.parsed_data

# main_table()
position = f.NimbusBM(xlsx_data, f.main_filter).position()
df = f.NimbusBM(xlsx_data, f.main_filter).main_table

```