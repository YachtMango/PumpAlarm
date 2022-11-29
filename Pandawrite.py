import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("/home/mango3/Downloads/Pump Log File Epoch DT.csv", index_col=1)
print(df)
fig, ax = plt.subplots()
ax.bar(df["Timestamp"],df["RT"])
plt.show()
