# %%
import pandas as pd
from datetime import date

# %%
raw_filename = "raw_poker_results.csv"

# %%
raw_df = pd.read_csv(raw_filename)
raw_df.head()

# %%
results_df = raw_df.drop(columns=["Host", "Notes", "Unavailable"])
results_df.head()

# %%
results_df["Date"] = pd.to_datetime(results_df["Date"])
results_df.head()

# %%
results_df = results_df.melt(id_vars=["Date"], var_name="Position", value_name="Player").dropna()
results_df["Position"] = pd.to_numeric(results_df["Position"])
results_df = results_df.sort_values(["Date", "Position"])
results_df

# %%
results_df = results_df.assign(Player=results_df["Player"].str.split(",")).explode("Player")
results_df["Player"] = results_df["Player"].str.strip()
results_df

# %%
results_df = results_df.reset_index().drop(columns="index")
results_df

# %%
results_df["Position"] = results_df.groupby("Date")["Position"].rank(method="min").astype("Int64")
results_df

# %%
clean_raw_df = pd.pivot_table(results_df, index="Date", columns="Position", values="Player", aggfunc=lambda x: ", ".join(x))
clean_raw_df

# %%
clean_raw_df.to_csv("clean_poker_results.csv")

# %%
results_pivot = pd.pivot_table(results_df, index="Player", columns="Position", aggfunc="count").astype("Int64").reset_index()
results_pivot

# %%
results_pivot.columns = [col[0] if not col[1] else col[1] for col in results_pivot.columns]
results_pivot

# %%
results_pivot = results_pivot.sort_values(list(range(1, 13)), ascending=False).reset_index().drop(columns="index")
results_pivot

# %%
results_df.to_csv("poker_results_long.csv", index=False)

# %%
results_pivot.to_csv("poker_results_pivot.csv", index=False)

# %%
