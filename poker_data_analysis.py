# %% [markdown]
# # Poker data analysis

# %% [markdown]
# ## Initial imports

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
filename = "poker_results_long.csv"

# %%
df = pd.read_csv(filename)
df.head()

# %%
df["Date"] = pd.to_datetime(df["Date"])

# %%
df.info()

# %%
df.head()

# %%
sns.set_theme()
sns.set_style("white")

# %%
g = sns.displot(data=df, kind="hist", col="Player", y="Position", height=6, aspect=0.4, binwidth=1, binrange=[1, 13])
for ax in g.axes.ravel():
    ax.set_yticks(list(range(1, 13)))
    ax.set_xticks(list(range(0, 16, 2)))

# %%
