# content-reshaper

Give it a YouTube URL, get back 5 ready-to-publish content pieces: a blog post, Twitter thread, LinkedIn post, email newsletter, and a summary.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A [Gemini API key](https://aistudio.google.com/apikey)

## Setup

```bash
git clone https://github.com/yourusername/content-reshaper
cd content-reshaper
uv sync
cp .env.example .env  # then fill in your GEMINI_API_KEY
```

## Usage

```bash
uv run reshaper.py <youtube-url>
```

Output is saved to `output/<video-id>.md`.

## Example

```bash
uv run reshaper.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```
output/dQw4w9WgXcQ.md
```

The file contains all 5 formats separated by section headers, ready to copy-paste.
