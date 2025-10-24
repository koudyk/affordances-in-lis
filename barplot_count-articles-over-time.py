from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

filepath = Path(__file__).resolve().parent / "ebsco-search-results.csv"
df = pd.read_csv(filepath)

cols = ["publicationDate", "subjects", "source"]
df = df[cols]
df["datetime"] = pd.to_datetime(df["publicationDate"], format="%Y%m%d")
df["year"] = df["datetime"].dt.year
# counts_df = df.groupby(["year", "source"]).size().reset_index(name="count")

fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(data=df, x="year")

labels = ax.get_xticklabels()
new_labels = [label if i % 2 == 0 else "" for i, label in enumerate(labels)]
ax.set_xticklabels(new_labels)

ax.set_ylabel("Number of peer-reviewed journal articles")
ax.set_xlabel("Publication year")

plt.tight_layout()
destination = Path(__file__).resolve().parent / "barplot_count-articles-over-time.png"
plt.savefig(destination)


d = 1
