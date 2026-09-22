# Image Comparison API: Score Image Similarity and Find Duplicate Images

Compare images by visual similarity and catch exact and near-duplicates, over a plain HTTP API. Give it one source image and a list of targets, and it returns one row per comparison with a similarity score, a duplicate verdict, and perceptual hash distances.

Runs on the [Image Similarity API](https://apify.com/johnvc/image-similarity-api?fpr=9n7kx3) Actor on Apify. This repo shows two ways to call it: a Python quick start, and MCP install steps for five clients.

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/hqdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Text walkthrough

This image comparison API answers one question: how alike are these two pictures? You pass a `sourceImage` URL and a `targetImages` list, and every target comes back with a `similarityScore` between 0 and 1, an `isSimilar` flag measured against your `threshold`, and a plain-language `verdict`. Under the hood it runs two independent methods: a CLIP vision embedding, which understands content and still matches a photo that has been cropped, recoloured, or re-encoded, and perceptual hashing (pHash and dHash), which is cheap and catches byte-level near-duplicates. Set `comparisonMode` to `embedding`, `phash`, or `both` depending on which signal you want to pay for. The duplicate-detection path is what most people come for: point it at a list of URLs to find duplicate images online without downloading anything yourself. It is also the fastest way to compare two images for similarity when you need a number rather than an eyeball judgement, for example to compare screenshots against a baseline and flag a layout change.

## Quick start

```bash
uv sync
cp .env.example .env      # paste your Apify token into .env
uv run image-similarity-api-example.py
```

Get a free Apify API token at https://apify.com?fpr=9n7kx3 (Console, then Settings, then API & Integrations).

The example keeps every run small, one source against two or three targets, so your first run costs almost nothing. The Actor accepts up to 500 targets per run.

## Recipes

Each of these is a published, ready-to-run example on the Apify Store. Open one, press Start, and read the output before you write any code.

- [Compare Images via API, Similarity Scores as JSON](https://apify.com/johnvc/image-similarity-api/examples/compare-images-api-similarity-scores?fpr=9n7kx3)
- [Compare Two Images for Similarity, Percentage Verdict](https://apify.com/johnvc/image-similarity-api/examples/compare-two-images-for-similarity?fpr=9n7kx3)
- [Find Duplicate Images Online Across a List of URLs](https://apify.com/johnvc/image-similarity-api/examples/find-duplicate-images-online?fpr=9n7kx3)
- [Bulk Image Hash Check with pHash and dHash](https://apify.com/johnvc/image-similarity-api/examples/bulk-image-hash-check-phash?fpr=9n7kx3)
- [Compare Screenshots to a Baseline, Flag Changes](https://apify.com/johnvc/image-similarity-api/examples/compare-screenshots-to-a-baseline?fpr=9n7kx3)

The first three are implemented as functions in `image-similarity-api-example.py`, so you can run them locally as well.

**Schedule tip:** to watch for reuse of your own photography, save a run as a task with your image as `sourceImage`, then schedule it. Each run appends fresh comparison rows, so you get a dated trail rather than a single snapshot.

## Input parameters

| Parameter | Type | What it does |
|---|---|---|
| `sourceImage` | string | URL of the image everything is compared against. |
| `sourceImageUpload` | array | Upload a source image instead of linking one. |
| `targetImages` | array | The image URLs to compare against the source, up to 500. |
| `comparisonMode` | string | `embedding`, `phash`, or `both`. Controls which signals run. |
| `threshold` | number | Score above which `isSimilar` becomes true. |
| `phashThreshold` | integer | Maximum hash distance still counted as a near-duplicate. |
| `sourceImageId` | string | Your own identifier for the source, echoed back on every row. |
| `customId` | string | Free-form label echoed on every row, handy for batch jobs. |
| `headers` | object | Extra request headers, for images behind a referer check. |
| `proxyConfiguration` | object | Proxy settings for hosts that block datacentre traffic. |

## Output fields

One row per comparison.

| Field | What it holds |
|---|---|
| `resultType` | Row kind, so you can separate comparisons from errors. |
| `targetIndex` | Position of this target in your input list. |
| `sourceImage`, `targetImage` | The two images compared. |
| `sourceImageId`, `customId` | Your identifiers, echoed back. |
| `similarityScore` | Embedding similarity, 0 to 1. |
| `isSimilar` | Whether the score cleared your `threshold`. |
| `phashDistance`, `dhashDistance` | Perceptual hash distances, lower is closer. |
| `isNearDuplicate` | Whether hash distance cleared `phashThreshold`. |
| `verdict` | Plain-language summary of the match. |
| `comparisonMode`, `embeddingModel` | Which signals ran, and the model used. |
| `errorMessage` | Why a target could not be compared. |
| `processedAt` | Timestamp for the comparison. |

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the image comparison API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings > Connectors** (or **Settings > Developer > Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the image comparison API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

---

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the image comparison API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

---

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings > Connectors > Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/image-similarity-api`.
3. In any chat, open **+ > Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api`, using OAuth when prompted.
5. Ask Claude to run the image comparison API.

Open Claude on the web: https://claude.ai

---

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor > Settings > MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the image comparison API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

---

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/image-similarity-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

## FAQ

**How do I compare two images for similarity?**
Pass one `sourceImage` and one entry in `targetImages`, then read `similarityScore`. It is a number between 0 and 1, so 0.97 means the pair is almost certainly the same picture. Set `threshold` to the cut-off you want and the Actor sets `isSimilar` for you.

**What is the difference between the embedding score and pHash?**
The embedding is a CLIP vision model: it compares what is in the picture, so it still matches after a crop, a resize, a recolour, or a re-encode. Perceptual hashing compares the visual fingerprint of the pixels and is very cheap, but a heavy edit will break it. Running `both` gives you a semantic score and a duplicate distance in the same row.

**How do I find duplicate images online across a list of URLs?**
Put the image you care about in `sourceImage`, put the candidates in `targetImages`, and run in `both` mode. Rows where `isNearDuplicate` is true are byte-level copies; rows with a high `similarityScore` but a large hash distance are edited or re-encoded copies.

**Can I use this as an image copyright checker?**
You can use it for the matching half of that job. Give it your original photo and a list of pages where you suspect the image was reused, and it will tell you which of those images match and how closely. It does not make a legal determination, and it does not search the web for you; you supply the candidate URLs.

**Does it work for comparing screenshots?**
Yes, and that is a common use. Keep a baseline screenshot as the source, compare each new capture against it, and alert when the score drops below your threshold. Hash distance is usually the more sensitive signal for small layout shifts.

**What is perceptual hashing?**
A perceptual hash reduces an image to a short fingerprint so that visually similar images produce similar fingerprints. You compare two hashes by counting how many bits differ, which is the distance this Actor returns as `phashDistance` and `dhashDistance`. Unlike a checksum, one changed pixel does not change the answer completely.

**What happens if an image will not load?**
That target comes back as its own row with an `errorMessage`, and the rest of the run continues. A dead URL never fails the whole job.

**How much does a run cost?**
Pricing is on the [Actor page](https://apify.com/johnvc/image-similarity-api?fpr=9n7kx3) and bills per comparison, so ten targets is ten units. Hash-only mode is the cheaper path when you do not need the model score. Check live pricing there rather than a number copied into a README.

## People also search for

image comparison api, image similarity api, find duplicate images, duplicate image finder, compare two images for similarity, phash, perceptual hashing, image copyright checker, compare screenshots, image deduplication, ai image comparison, find duplicate photos, image hash check, visual similarity search

## More

- Actor on the Apify Store: https://apify.com/johnvc/image-similarity-api?fpr=9n7kx3
- Free Apify account: https://apify.com?fpr=9n7kx3
- Apify Python client docs: https://docs.apify.com/api/client/python/
- Apify MCP docs: https://docs.apify.com/platform/integrations/mcp
- uv: https://docs.astral.sh/uv/

Last Updated: 2026.09.22
