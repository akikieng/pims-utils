# pims-utils

Convert PIMS exported "stock rebuild" excel file (.xls) to pair of csv file and a description txt file


## Requirements

```
pip install pandas xlrd pytest
```


## Run tests

```
pytest PimsRebuildXls.py
```


## Usage

To use CLI:
```
 python PimsRebuildXls.py \
        --fn_in="test_fixture-stock_rebuild.xls" \
        to_csv --fn_out_df="stock.csv" \
               --fn_out_desc="stock.desc.txt"
```
