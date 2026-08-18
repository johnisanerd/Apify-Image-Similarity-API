"""
Image comparison API on Apify: score how similar two images are, and find
duplicate images across a list of URLs.

Actor:  https://apify.com/johnvc/image-similarity-api?fpr=9n7kx3
Token:  get a free Apify API key at https://apify.com?fpr=9n7kx3

Setup:
    uv sync
    cp .env.example .env      # then paste your token into .env
    uv run image-similarity-api-example.py

Every run input below is deliberately small (one source image against two or
three targets) so your first run costs almost nothing. The Actor accepts up to
500 targets per run; raise the list once you have seen the output shape.
"""

import json
import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR = "johnvc/image-similarity-api"

TOKEN = os.getenv("APIFY_TOKEN")
if not TOKEN:
    raise SystemExit(
        "Set APIFY_TOKEN in .env first. Free key: https://apify.com?fpr=9n7kx3"
    )

client = ApifyClient(TOKEN)

# The same public demo images the Actor prefills in the Apify Console, so these
# URLs are known to load. CAT_SMALL is the same photo as CAT at a smaller size,
# which is why it scores as a duplicate rather than merely related.
WIKI = "https://upload.wikimedia.org/wikipedia/commons"
CAT = f"{WIKI}/thumb/3/3a/Cat03.jpg/960px-Cat03.jpg"
CAT_SMALL = f"{WIKI}/thumb/3/3a/Cat03.jpg/250px-Cat03.jpg"
OTHER_CAT = f"{WIKI}/thumb/2/25/Siam_lilacpoint.jpg/960px-Siam_lilacpoint.jpg"
DOG = f"{WIKI}/thumb/9/90/Labrador_Retriever_portrait.jpg/960px-Labrador_Retriever_portrait.jpg"


def run_actor(run_input: dict) -> list[dict]:
    """Start the Actor, wait for it to finish, return the dataset rows."""
    run = client.actor(ACTOR).call(run_input=run_input)
    dataset_id = run.default_dataset_id
    return list(client.dataset(dataset_id).iterate_items())


def show(rows: list[dict], limit: int = 5) -> None:
    """Print a short, readable summary of what came back."""
    results = [r for r in rows if r.get("resultType") == "comparison"]
    errors = [r for r in rows if r.get("errorMessage")]

    print(f"  {len(results)} comparisons, {len(errors)} error rows")

    for row in results[:limit]:
        score = row.get("similarityScore")
        score_text = f"{score:.4f}" if isinstance(score, (int, float)) else "n/a"
        print(f"  - target #{row.get('targetIndex')}: {row.get('targetImage')}")
        print(f"      similarity:     {score_text}  (similar: {row.get('isSimilar')})")
        print(f"      verdict:        {row.get('verdict')}")
        print(f"      phash distance: {row.get('phashDistance')}")
        print(f"      dhash distance: {row.get('dhashDistance')}")
        print(f"      near duplicate: {row.get('isNearDuplicate')}")
        print(f"      mode:           {row.get('comparisonMode')}")
        print(f"      model:          {row.get('embeddingModel')}")

    for row in errors[:2]:
        print(f"  ! {row.get('targetImage')}: {row.get('errorMessage')}")


def compare_two_images_for_similarity() -> list[dict]:
    """Recipe: compare two images for similarity and read the percentage verdict.

    Mirrors the published task "Compare Two Images for Similarity, Percentage
    Verdict". Uses both modes so you see the model score and the hash distance
    side by side.
    """
    return run_actor(
        {
            "sourceImage": CAT,
            "targetImages": [CAT_SMALL],
            "comparisonMode": "both",
            "threshold": 0.85,
        }
    )


def find_duplicate_images_online() -> list[dict]:
    """Recipe: find duplicate images across a list of URLs.

    Mirrors the published task "Find Duplicate Images Online Across a List of
    URLs". One source, several targets, one row per comparison.
    """
    return run_actor(
        {
            "sourceImage": CAT,
            "targetImages": [CAT_SMALL, OTHER_CAT, DOG],
            "comparisonMode": "both",
            "threshold": 0.9,
            "phashThreshold": 8,
        }
    )


def bulk_image_hash_check() -> list[dict]:
    """Recipe: bulk hash check with pHash and dHash, no embedding model.

    Mirrors the published task "Bulk Image Hash Check with pHash and dHash".
    Hash-only mode is the cheapest way to catch exact and near-duplicates.
    """
    return run_actor(
        {
            "sourceImage": CAT,
            "targetImages": [CAT_SMALL, OTHER_CAT, DOG],
            "comparisonMode": "phash",
            "phashThreshold": 10,
        }
    )


if __name__ == "__main__":
    print("1. Compare two images for similarity")
    rows = compare_two_images_for_similarity()
    show(rows)

    print("\n2. Find duplicate images across a list of URLs")
    show(find_duplicate_images_online())

    print("\n3. Bulk image hash check (pHash and dHash only)")
    show(bulk_image_hash_check())

    print("\nFull first row:")
    print(json.dumps(rows[0] if rows else {}, indent=2)[:1200])
