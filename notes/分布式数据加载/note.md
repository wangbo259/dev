# 直接分布式读取csv为pandas.dataframe
```
import pandas as pd
from dask import dataframe as dd
import time

# 普通方法：约4.5min
start = time.time()
d = pd.read_csv(filepath)
end = time.time()
print(f'共花费{round((end-start)/60,3)}min')

# 分布式方法：约1.8min
start = time.time()
# 使用Dask的read_csv函数导入CSV文件
ddf = dd.read_csv(filepath)

df = ddf.compute()
end = time.time()
print(f'共花费{round((end-start)/60,3)}min')
```