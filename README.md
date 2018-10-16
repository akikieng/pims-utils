# pims-utils

Utility tools to read/convert files exported from PIMS

- PimsRebuildXls: Convert PIMS exported "stock rebuild" excel file (.xls) to pair of csv file and a description txt file


## Installation

```
pip install -U -e git@github.com/akikieng/pims-utils.git#egg=PimsUtils
```

or

```
git clone git@github.com/akikieng/pims-utils.git
pip install -U -e pims-utils
```


## Usage

To use CLI:
```
PimsRebuildXls.py \
    --fn_in="test_fixture-stock_rebuild.xls" \
    to_csv --fn_out_df="stock.csv" \
           --fn_out_desc="stock.desc.txt"
```


## Dev notes

### Requirements

```
pip install pandas xlrd pytest
```


### Run tests

```
pytest PimsUtils/PimsRebuildXls.py
```


