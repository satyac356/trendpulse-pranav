import pandas as pd
import matplotlib.pyplot as plt
import os

# File path
FILE_PATH = "data/trends_analysed.csv"

# 1 — Setup
if not os.path.exists(FILE_PATH):
    print("Analysed CSV not found. Run Task 3 first.")
    exit()

df = pd.read_csv(FILE_PATH)

# Create outputs folder if it doesn't exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Helper function to shorten long titles
def shorten_title(title, max_length=50):
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title

# -----------------------------
# Chart 1 — Top 10 Stories by Score
# -----------------------------
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Apply title shortening
titles = [shorten_title(t) for t in top_stories["title"]]

plt.figure()
plt.barh(titles, top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # Highest score on top

plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -----------------------------
# Chart 2 — Stories per Category
# -----------------------------
category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.close()

# -----------------------------
# Chart 3 — Score vs Comments
# -----------------------------
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -----------------------------
# Bonus — Dashboard
# -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axes[0].barh(titles, top_stories["score"])
axes[0].set_title("Top Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Categories")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")

# Chart 3 in dashboard
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

# Overall title
fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts saved in outputs/ folder")