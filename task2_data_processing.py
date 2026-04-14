import pandas as pd
import os

# File path (make sure your Task 1 JSON exists in data/ folder)
DATA_FOLDER = "data"

# Find the latest JSON file automatically
json_files = [f for f in os.listdir(DATA_FOLDER) if f.startswith("trends_") and f.endswith(".json")]

if not json_files:
    print("No JSON file found in data/ folder. Run Task 1 first.")
    exit()

# Pick the latest file
json_files.sort(reverse=True)
latest_file = os.path.join(DATA_FOLDER, json_files[0])

# 1 — Load JSON file
df = pd.read_json(latest_file)

print(f"Loaded {len(df)} stories from {latest_file}")

# 2 — Clean the data

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Drop rows with missing essential fields
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Ensure correct data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Strip whitespace from title
df["title"] = df["title"].str.strip()

# 3 — Save cleaned data to CSV
output_file = os.path.join(DATA_FOLDER, "trends_clean.csv")
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Print summary: stories per category
print("\nStories per category:")
print(df["category"].value_counts())

drop_duplicates(subset="post_id")

dropna(subset=["post_id", "title", "score"])

astype(int)

df[df["score"] >= 5]

str.strip()