import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("/home/mango3/Downloads/Pump Log File.csv", index_col=0)
print(df)
fig, ax = plt.subplots()
ax.bar(df["Date"],df["RT"])
plt.show()
