# WideTable
Python script to convert a pandas dataframe with many columns into a number of subtables output as LaTeX script.
Use the wide_table function:
```python
Table = wide_table(table=df, no_cols=16, landscape=True, center=True, midrules=[4, 6])
```
This will produce a number of subtables with 16 columns, orient them landscape, center them on the page, and insert midrules on rows 4 and 6.

Note. The format of each cell will be reproduced as written e.g., if numbers are defined as float32 the LaTeX table will contain all significant figures.
