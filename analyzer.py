import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

ids = [x.split(".")[0] for x in os.listdir("reviews")]
# print(*ids, sep = "\n")

# id = input("Enter the product ID: ")
id = 138536499
max_score = 5

dataframe = pd.read_json(f"reviews/{id}.json")

dataframe["stars"] = (dataframe["score"] * max_score).round(1)

review_count = dataframe.shape[0]
pros_count = dataframe["pros"].astype(bool).sum()
cons_count = dataframe["cons"].astype(bool).sum()
average_score = (dataframe["stars"].mean() * max_score).round(2)

print(f"""For the selected product (id: {id})
the review count is {review_count}, of which
{pros_count} have one or more advantage(s) and
{cons_count} have one or more disadvantage(s) listed.

The average score for this product is {average_score}/{max_score}.""")

if not os.path.exists("charts"):
    os.mkdir("charts")

recommendations = dataframe["recommendation"].value_counts(dropna = False).reindex([True, False, np.nan], fill_value = 0)
recommendations.plot.pie(
    label = "",
    labels = ["Recommended", "Not recommended", "Neutral"],
    colors = ["#44ee44", "#ee4444", "#999999"],
    autopct = lambda p: "{:.1f}%".format(round(p)) if p > 0 else ''
)

plt.title(f"Recommendations for product {id}")
plt.savefig(f"./charts/{id}_pie.svg")
plt.close()

stars = dataframe["stars"].value_counts().reindex(list(np.arange(0.0, 5.5, 0.5)), fill_value = 0)
stars.plot.bar(color = "#4444ee")

plt.title(f"Star count for product {id}")
plt.ylim(0, max(stars) + 15)
plt.xlabel("Star count")
plt.ylabel("Review count")
plt.xticks(rotation = 0)
plt.grid(axis = "y", linestyle = "--", linewidth = 0.5)

for index, value in enumerate(stars):
    plt.text(index, value + 1.5, str(value), ha = "center")

plt.savefig(f"./charts/{id}_bar.svg")
plt.close()