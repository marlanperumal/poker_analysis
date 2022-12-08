# %% [markdown]
# # Poker data cleanup

# %% [markdown]
# This notebook analyses the results of a weekly poker game of a nominal nine players. Not all players are available every week. The results of the final finishing positions of each player has been recorded. It's possible for 2 or more players to be eliminated in the same round, thereby tying in position. There is also a house rule for *ghost players*. This allows players who have previously been eliminated to return to the game and either go out again or potentially even win. If a play does come back in via the ghost player rule, then each of their finishing positions is recorded.

# %% [markdown]
# The objective of this notebook is to clean up the original data to make available for subsequent analysis

# %% [markdown]
# ## Initial imports

# %%
import pandas as pd

# %% [markdown]
# ## Read in and inspect raw data

# %%
raw_filename = "raw_poker_results.csv"

# %%
raw_df = pd.read_csv(raw_filename)
raw_df.head()

# %% [markdown]
# ## Extract and process just the results data

# %% [markdown]
# Only keep the date and result columns

# %%
results_df = raw_df.drop(columns=["Host", "Notes", "Unavailable"])
results_df.head()

# %% [markdown]
# Convert the Date column to a proper date data type

# %%
results_df["Date"] = pd.to_datetime(results_df["Date"])
results_df.head()

# %% [markdown]
# Transform the position data from wide format to long

# %%
results_df = results_df.melt(id_vars=["Date"], var_name="Position", value_name="Player").dropna()
results_df["Position"] = pd.to_numeric(results_df["Position"])
results_df = results_df.sort_values(["Date", "Position"])
results_df

# %% [markdown]
# Some of the cells contain comma separated lists of players where they went out together and shared a position. Convert these to separate records for each player and clean up the resultant player names

# %%
results_df = results_df.assign(Player=results_df["Player"].str.split(",")).explode("Player")
results_df["Player"] = results_df["Player"].str.strip()
results_df

# %%
results_df = results_df.reset_index().drop(columns="index")
results_df

# %% [markdown]
# There is some inconsistency in how the position of the next player following any tied players is recorded. Convert this to a standard min rank.

# %%
results_df["Position"] = results_df.groupby("Date")["Position"].rank(method="min").astype("Int64")
results_df

# %% [markdown]
# Convert the clean data back to the original wide format and output to csv

# %%
clean_raw_df = pd.pivot_table(results_df, index="Date", columns="Position", values="Player", aggfunc=lambda x: ", ".join(x))
clean_raw_df

# %%
clean_raw_df.to_csv("clean_poker_results.csv")

# %% [markdown]
# Consider the pivot of players and finishing positions. Rename the columns so it's a regular data frame and sort by finishing position.

# %%
results_pivot = pd.pivot_table(results_df, index="Player", columns="Position", aggfunc="count").astype("Int64").reset_index()
results_pivot

# %%
results_pivot.columns = [col[0] if not col[1] else col[1] for col in results_pivot.columns]
results_pivot

# %%
results_pivot = results_pivot.sort_values(list(range(1, 13)), ascending=False).reset_index().drop(columns="index")
results_pivot

# %% [markdown]
# Output both the lnog format dataframe and the pivot table to csv

# %%
results_df.to_csv("poker_results_long.csv", index=False)

# %%
results_pivot.to_csv("poker_results_pivot.csv", index=False)

# %%
