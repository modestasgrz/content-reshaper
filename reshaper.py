import argparse
import asyncio
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv
from google import genai
from loguru import logger
from youtube_transcript_api import YouTubeTranscriptApi

from prompts.blog_post import PROMPT as BLOG_POST
from prompts.email_newsletter import PROMPT as EMAIL_NEWSLETTER
from prompts.linkedin_post import PROMPT as LINKEDIN_POST
from prompts.summary import PROMPT as SUMMARY
from prompts.twitter_thread import PROMPT as TWITTER_THREAD

MODEL = "gemini-3-flash-preview"


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query)["v"][0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
    raise ValueError(f"Cannot extract video ID from URL: {url}")


def fetch_transcript(video_id: str) -> str:
    logger.info(f"Fetching transcript for {video_id}...")
    entries = YouTubeTranscriptApi.get_transcript(video_id)  # type: ignore[attr-defined]
    return " ".join(entry["text"] for entry in entries)


async def generate(client: genai.Client, prompt: str, transcript: str) -> str:
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=f"{prompt}\n\n{transcript}",
    )
    assert response.text is not None
    return response.text


def build_markdown(video_id: str, results: dict[str, str]) -> str:
    sections = [
        ("Blog Post", results["blog_post"]),
        ("Twitter Thread", results["twitter_thread"]),
        ("LinkedIn Post", results["linkedin_post"]),
        ("Email Newsletter", results["email_newsletter"]),
        ("Summary", results["summary"]),
    ]
    header = f"# Repurposed Content — `{video_id}`\n"
    body = "\n\n---\n\n".join(f"## {title}\n\n{content}" for title, content in sections)
    return f"{header}\n{body}\n"


async def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Repurpose a YouTube video into 5 content formats."
    )
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise OSError(
            "GEMINI_API_KEY not set — copy .env.example to .env and fill it in."
        )

    client = genai.Client(api_key=api_key)
    video_id = extract_video_id(args.url)
    transcript = fetch_transcript(video_id)

    logger.info("Generating content with Gemini (parallel)...")
    (
        blog_post,
        twitter_thread,
        linkedin_post,
        email_newsletter,
        summary,
    ) = await asyncio.gather(
        generate(client, BLOG_POST, transcript),
        generate(client, TWITTER_THREAD, transcript),
        generate(client, LINKEDIN_POST, transcript),
        generate(client, EMAIL_NEWSLETTER, transcript),
        generate(client, SUMMARY, transcript),
    )

    results = {
        "blog_post": blog_post,
        "twitter_thread": twitter_thread,
        "linkedin_post": linkedin_post,
        "email_newsletter": email_newsletter,
        "summary": summary,
    }

    output_path = Path("output") / f"{video_id}.md"
    output_path.write_text(build_markdown(video_id, results), encoding="utf-8")
    logger.info(f"Done — output saved to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
