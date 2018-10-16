class PimsRebuildXls(object):
  def __init__(self, fn_in):
    self.fn_in = fn_in

  def to_csv(self, fn_out_df, fn_out_desc):
    df, desc = self.read_excel()
    df.to_csv(fn_out_df, index=True) # can save index now since it is set to family/code
    with open(fn_out_desc, 'w') as fh:
      fh.write(desc)      

  def read_excel(self):
    import pandas as pd
    df=pd.read_excel(self.fn_in, header=None)
    df=df[pd.notnull(df[0])]

    # check that columns are ok
    if ~(df[0]=='code').any():
      raise ValueError("Wrong format. Missing row containing 'code'")

    cols_actual = df[df[0]=='code'].iloc[0].values
    cols_expected = ["code", "description", "quantity", "unit cost", "sub-total"]
    cols_diff = set(cols_actual) - set(cols_expected)
    if len(cols_diff)>0:
      raise ValueError("Unexpected/missing columns: %s"%(", ".join(list(cols_diff))))

    # get file description
    # string, e.g. 'detailed by item\nevaluated as per Thursday 11 October 2018\nquantity on hand printed\nexclude items with zero quantities\nat Average cost, in USD\n'
    desc = df[df[0].str.startswith("detailed by item")].iloc[0]
    desc = desc[0]

    # make machine-readable
    df=df[~df[0].str.startswith("detailed by item")]
    df=df[~df[0].str.startswith("VAT ")] # e.g. "VAT 123456-789,"
    df=df[~df[0].str.startswith("PIMS2 ")] # e.g. "PIMS2 1901-1115131206 - AKikiEng akikeng"
    df=df[~df[0].isin(["Akiki Engineering", "code", "Report inventory valuation by department", ])]

    # extract totals rows
    # Note that this is not the same as the total of sub-total per family
    # since I compared them below (check "assert totals same as manual calculation" below)
    # totals = df[ df[0].str.startswith('total for')]
    df     = df[~df[0].str.startswith('total for')]

    # set columns
    df.columns = cols_expected

    # set family
    df['family'] = df.apply(lambda row: row['code'] if pd.isnull(row['description']) else None, axis=1)
    df['family'] = df['family'].fillna(method='ffill')
    df = df[pd.notnull(df['description'])]

    # negatives
    negatives = df[ (df['sub-total'].map(str)+df['quantity']).str.contains('\\(')]
    df        = df[~(df['sub-total'].map(str)+df['quantity']).str.contains('\\(')]

    # split qty unit from value
    df[['qty_val', 'qty_unit']] = df['quantity'].str.split(' ', n=1, expand=True)
    del df['quantity']

    # set numeric type
    # import re
    for fx in ['unit cost', 'sub-total', 'qty_val']:
      # df[fx] = df[fx].apply(lambda v: re.sub("\((.*)\)", "-\\1", v)) # convert (12.34) to -12.34
      df[fx] = df[fx].astype('float')

    # assert totals same as manual calculation (compare to "totals" variable above)
    # df.groupby('family')['sub-total'].sum().head()

    # set index and sort
    df = df.set_index(['family', 'code']).sort_index(ascending=True)

    return df, desc


def test_pimsRebuildXls_read_excel():
  import os
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  fn_in = os.path.join(BASE_DIR, "test_fixture-stock_rebuild.xls")
  prx = PimsRebuildXls(fn_in)
  df, desc = prx.read_excel()
  # assert totals.shape[0]==34
  assert 'Thursday 11 October 2018' in desc
  assert df.shape[0] == 4 # 1517 # > 1000


if __name__ == '__main__':
  # https://github.com/google/python-fire/blob/master/docs/guide.md#version-3-firefireobject
  import fire
  fire.Fire(PimsRebuildXls)
