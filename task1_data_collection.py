import requests
import json
import time
import os
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None  # Ignore if no category matches


def main():
    try:
        # Step 1: Fetch top story IDs
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        story_ids = response.json()[:500]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return

    collected_stories = []

    # Keep track of how many stories per category
    category_count = {cat: 0 for cat in CATEGORIES}

    # Step 2: Fetch each story
    for story_id in story_ids:
        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            res.raise_for_status()
            story = res.json()

            if not story or "title" not in story:
                continue

            category = get_category(story["title"])

            # Skip if no category match
            if not category:
                continue

            # Skip if already collected 25 for this category
            if category_count[category] >= 25:
                continue

            # Extract required fields
            story_data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_stories.append(story_data)
            category_count[category] += 1

            # Stop if all categories are filled
            if all(count >= 25 for count in category_count.values()):
                break

        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

    # Sleep 2 seconds per category loop (as required)
    for _ in CATEGORIES:
        time.sleep(2)

    # Step 3: Save to JSON file
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()