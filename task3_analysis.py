import pandas as pd
import numpy as np
import os

# File path
FILE_PATH = "data/trends_clean.csv"

# 1 — Load and Explore
if not os.path.exists(FILE_PATH):
    print("Clean CSV not found. Run Task 2 first.")
    exit()

df = pd.read_csv(FILE_PATH)

# Print basic info
print(f"Loaded data: {df.shape}\n")

print("First 5 rows:")
print(df.head())

# Average values using pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# 2 — Basic Analysis with NumPy

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, Median, Std
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# Max and Min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_index = np.argmax(comments)
top_story = df.iloc[max_comments_index]

print(f'\nMost commented story: "{top_story["title"]}" — {top_story["num_comments"]} comments')

# 3 — Add New Columns

# Engagement: comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular flag
df["is_popular"] = df["score"] > avg_score

# 4 — Save the Result
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")