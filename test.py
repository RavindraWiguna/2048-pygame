import numpy as np
import pandas as pd

exdata = np.full((4, 4), 4, np.uint16)
a = np.array([exdata.ravel()])


print(exdata)
print("===")
print(a)
exdata[0][0] = 12
print(exdata)
print("===")
print(a)
# for item in a:
#     print(type(item))

newdata = np.full((4, 4), 8, np.uint16)
# a = np.append(a, [newdata.ravel()])
# print(a)
# a = np.insert(a, )
# print(a)
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning) 

a = np.concatenate((a, [newdata.ravel()]), axis=0)

print("===")
print(a)
# print(a.shape)

df = pd.DataFrame(a, columns = [i for i in range(16)])
# print(df)
df['move'] = [False*1, True*1]
print(df)

df.to_csv('data01.csv')