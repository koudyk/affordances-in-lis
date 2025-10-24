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

plot_labels = ["A)", "B)", "C)", "D)", "E)"]


# Define a simple color function that returns a fixed color (e.g., black)
def fixed_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    return "tab:blue"  # You can change this to any color like "grey", "blue", etc.


fig, axs = plt.subplots(len(intervals), 1, figsize=(5, 15))
for (i_plot, interval), plot_label in zip(enumerate(intervals), plot_labels):
    rows = df[df["year"].isin(interval)]
    subjects_rows = rows["subjects"].str.cat(sep="; ")
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=STOPWORDS,
        color_func=fixed_color_func,
    ).generate(subjects_rows)
    axs[i_plot].imshow(wc, interpolation="bilinear")
    axs[i_plot].axis("off")
    axs[i_plot].set_title(
        f"\n{plot_label}   {interval[0]} - {interval[-1]}\n", fontsize=18, loc="left"
    )


plt.tight_layout()
destination = Path(__file__).resolve().parent / "wordcloud_article-subjects.png"
plt.savefig(destination)

destination = Path(__file__).resolve().parent / "wordcloud_article-subjects.svg"
plt.savefig(destination)


d = 1
