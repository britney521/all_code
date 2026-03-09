import pandas as pd

df = pd.read_csv('酷派.csv')
datas = df.iloc[:,0].tolist()
print(datas)