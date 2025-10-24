from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

filepath = Path(__file__).resolve().parent / "ebsco-search-results.csv"
df = pd.read_csv(filepath)

cols = ["publicationDate", "subjects"]
df = df[cols]
df["datetime"] = pd.to_datetime(df["publicationDate"], format="%Y%m%d")
df["year"] = df["datetime"].dt.year
counts_df = df.groupby(["year"]).size().reset_index(name="count")

intervals = [
    range(1998, 2005),  # - 2004
    range(2005, 2010),  # 2005-2009
    range(2010, 2015),  # 2010-2014
    range(2015, 2020),  # 2015-2019
    range(2020, 2025),  # 2020-2024
]

fig, axs = plt.subplots(len(intervals), 1, figsize=(5, 15))
for i_plot, interval in enumerate(intervals):
    rows = df[df["year"].isin(interval)]
    subjects_rows = rows["subjects"].str.cat(sep="; ")
    wc = WordCloud(
        width=800, height=400, background_color="white", stopwords=STOPWORDS
    ).generate(subjects_rows)
    axs[i_plot].imshow(wc, interpolation="bilinear")
    axs[i_plot].axis("off")
    axs[i_plot].set_title(f"{interval[0]} - {interval[-1]}", fontsize=18)


plt.tight_layout()
destination = Path(__file__).resolve().parent / "wordcloud_article-subjects.png"
plt.savefig(destination)


d = 1
