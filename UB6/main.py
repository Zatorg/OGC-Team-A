import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("population.csv")
print("\n2. Classifier Ranges:")
print("center_1:\t", df["center_1"].min(), " - ", df["center_1"].max())
print("spread_1:\t", df["spread_1"].min(), " - ", df["spread_1"].max())
print("center_2:\t", df["center_2"].min(), " - ", df["center_2"].max())
print("spread_2:\t", df["spread_2"].min(), " - ", df["spread_2"].max())

print("\n3. Anzahl maximal erlaubter Classifier:")
print("as:")
print("mean", df['as'].mean())
print("max", df["as"].max())
print("min", df['as'].min())

unique_actions = df['action'].unique()
print("\n4. Actionspace:")
print(unique_actions)

print()
dfg = df[['ID', 'num']].groupby(by="num")
s=0
for i, group in dfg:
    s += i*len(group)

print("num rules without aggregatin:", s)

dfg = df.groupby(["action"])[["p"]].idxmax()
dfg = dfg.reset_index()
for i, row in dfg.iterrows():
    x = row["p"]
    print(df.iloc[x])

r_x = 100
r_y = 100

plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams["figure.dpi"] = 600
plt.gca().set_aspect('equal', adjustable='box')
plt.gca().invert_yaxis()

df_mask = df["p"]==1000
df_f = df[df_mask]

for x in range(r_x):
    for y in range(r_y):
        x_n = x/r_x
        y_n = y/r_y
        print("\n \nx", x_n)
        print("y", y_n)
        df_mask = ((df_f["center_1"] + df_f["spread_1"]) > x_n) & ((df_f["center_1"] - df_f["spread_1"]) <= x_n)
        df_fx = df_f[df_mask]
        df_mask = ((df_fx["center_2"] + df_fx["spread_2"]) > y_n) & ((df_fx["center_2"] - df_fx["spread_2"]) <= y_n)
        df_fxy = df_fx[df_mask]
        df_fxy = df_fxy.reset_index()
        df_fxy = df_fxy.groupby(["action"])
        color_list = list(df_fxy.groups.keys())
        for color in color_list:
            print(color)
            plt.plot(y_n, x_n, color=color, alpha=0.5, linestyle='solid', linewidth=1,
                     marker='.', markersize=1)
plt.show()