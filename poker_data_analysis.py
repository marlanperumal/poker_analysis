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
sns.set_palette("bright")

# %%
g = sns.displot(data=df, kind="hist", col="Player", y="Position", hue="Position", palette=sns.color_palette("hls", 12), height=6, aspect=0.4, binwidth=1, binrange=[1, 13])
for ax in g.axes.ravel():
    ax.set_yticks(list(range(1, 13)))
    ax.set_xticks(list(range(0, 16, 2)))

# %%
df.head()

# %% [markdown]
# ## Add in additional info columns
# - No ghost position (take the first elimination only)
# - Final order (ignore all previous eliminations - take the last eliminated position only)
# - Mark ghost plays (flag positions occupied as a ghost)
# - Game table
# - Scoring table

# %%
df["EliminationRank"] = df.groupby(["Date", "Player"])["Position"].rank(ascending=False).astype("int64")
df["ReverseEliminationRank"] = df.groupby(["Date", "Player"])["Position"].rank().astype("int64")

# %%
df.loc[df["EliminationRank"] == 1, "NoGhostFlag"] = True
df.loc[df["ReverseEliminationRank"] == 1, "FinalPositionFlag"] = True

# %%
df.loc[df["NoGhostFlag"].isna(), "NoGhostFlag"] = False
df.loc[df["FinalPositionFlag"].isna(), "FinalPositionFlag"] = False

# %%
df["NoGhostFlag"] = df["NoGhostFlag"].astype(bool)
df["FinalPositionFlag"] = df["FinalPositionFlag"].astype(bool)

# %%
df[~df["NoGhostFlag"]]

# %%
df[~df["FinalPositionFlag"]]

# %%
df.loc[df["NoGhostFlag"], "NoGhostPosition"] = df[df["NoGhostFlag"]].groupby("Date")["Position"].rank(method="min")
df.loc[df["FinalPositionFlag"], "FinalPosition"] = df[df["FinalPositionFlag"]].groupby("Date")["Position"].rank(method="min")

# %%
df.loc[df["NoGhostFlag"]]

# %%
df.loc[df["FinalPositionFlag"]]

# %%
df.loc[~df["NoGhostFlag"], :].groupby(["Player"])["Date"].count()

# %%
df[df["NoGhostFlag"]].info()

# %%
g = sns.displot(data=df[df["Player"]!="Peter"].loc[df["NoGhostFlag"], :], kind="hist", col="Player", y="NoGhostPosition", hue="NoGhostPosition", palette=sns.color_palette("hls", 9), height=6, aspect=0.4, binwidth=1, binrange=[1, 10])
for ax in g.axes.ravel():
    ax.set_yticks(list(range(1, 10)))
    ax.set_xticks(list(range(0, 14, 2)))

# %%
g = sns.displot(data=df[df["Player"]!="Peter"].loc[df["FinalPositionFlag"], :], kind="hist", col="Player", y="FinalPosition", hue="FinalPosition", palette=sns.color_palette("hls", 9), height=6, aspect=0.4, binwidth=1, binrange=[1, 10])
for ax in g.axes.ravel():
    ax.set_yticks(list(range(1, 10)))
    ax.set_xticks(list(range(0, 14, 2)))

# %%
df[(~df["NoGhostFlag"]) & (df["Position"] == 1)]

# %%
scoring_filename = "scoring.csv"

# %%
scoring_df = pd.read_csv(scoring_filename)
scoring_df

# %%
df.merge(scoring_df, how="inner", left_on="FinalPosition", right_on="Position").groupby("Player")["F1score"].sum().sort_values(ascending=False)

# %%
df.merge(scoring_df, how="inner", left_on="NoGhostPosition", right_on="Position").groupby("Player")["F1score"].sum().sort_values(ascending=False)

# %%
(df.merge(scoring_df, how="inner", left_on="FinalPosition", right_on="Position").groupby("Player")["F1score"].sum() - df.merge(scoring_df, how="inner", left_on="NoGhostPosition", right_on="Position").groupby("Player")["F1score"].sum()).sort_values(ascending=False)

# %%
df[~df["FinalPosition"].isna()].groupby("Player")["Date"].count()

# %%
sns.relplot(df[df["FinalPositionFlag"]], kind="line", x="Date", y="FinalPosition", hue="Player", palette="hls", height=8, aspect=4)

# %%
no_ghost_results_df = pd.pivot_table(df, index="Date", columns="Player", values="NoGhostPosition")
final_results_df = pd.pivot_table(df, index="Date", columns="Player", values="FinalPosition")

no_ghost_results_df.to_csv("no_ghost_results.csv")
final_results_df.to_csv("final_results.csv")

# %%
no_ghost_results_df

# %%
g = sns.heatmap(no_ghost_results_df.reset_index().drop(columns="Peter").assign(Date=no_ghost_results_df.reset_index()["Date"].apply(lambda x: x.strftime("%Y-%m-%d"))).set_index("Date"), cmap="viridis")

# %%
g = sns.heatmap(final_results_df.reset_index().drop(columns="Peter").assign(Date=final_results_df.reset_index()["Date"].apply(lambda x: x.strftime("%Y-%m-%d"))).set_index("Date"), cmap="viridis")

# %%
no_ghost_results_df.corr()

# %%
sns.heatmap(no_ghost_results_df.drop(columns="Peter").corr(), vmin=-0.45, vmax=0.45, center=0, cmap="vlag", annot=True, fmt=".2f", annot_kws={"fontsize": 8})

# %%
sns.heatmap(final_results_df.drop(columns="Peter").corr(), vmin=-0.45, vmax=0.45, center=0, cmap="vlag", annot=True, fmt=".2f", annot_kws={"fontsize": 8})

# %%
no_ghost_results_df - final_results_df

# %%
(no_ghost_results_df - final_results_df).sum()

# %%
{row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}

# %%
no_ghost_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill()

# %%
sns.relplot(no_ghost_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill(), kind="line", dashes=False, aspect=2)

# %%
sns.relplot(final_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill(), kind="line", dashes=False, aspect=2)

# %%
no_ghost_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill().rank(axis=1, ascending=False, method="min")

# %%
g = sns.relplot(no_ghost_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill().rank(axis=1, ascending=False, method="min"), kind="line", dashes=False, aspect=2)
for ax in g.axes[0]:
    ax.invert_yaxis()

# %%
g = sns.relplot(final_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill().rank(axis=1, ascending=False, method="min"), kind="line", dashes=False, aspect=2)
for ax in g.axes[0]:
    ax.invert_yaxis()

# %%
(
    final_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill()
    - no_ghost_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill()
)

# %%
sns.relplot(
    final_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill()
    - no_ghost_results_df.drop(columns="Peter").replace({row["Position"]: row["F1score"] for _, row in scoring_df.iterrows()}).cumsum().ffill(),
    kind="line", dashes=False, aspect=2
)

# %%
