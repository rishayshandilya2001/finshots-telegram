"""
Fetch the latest Finshots post and send it to a Telegram chat.

Why each part exists:
- Finshots runs on Ghost CMS, which auto-generates an RSS feed at /rss/.
  That feed always lists the newest post first, so we don't need to
  scrape the HTML — RSS is stable and won't break if their site design changes.
- We track the last-sent post's link in sent_log.txt so that if this
  script accidentally runs twice in a day (e.g. a manual re-run),
  it won't spam you with the same story twice.
- Telegram's Bot API just needs a bot token + chat id — no approval,
  no expiry, unlike WhatsApp's Sandbox/Cloud API.
"""

import os
import sys
import feedparser
import requests

FEED_URL = "https://finshots.in/rss/"
SENT_LOG = "sent_log.txt"


def get_latest_post():
    """Pull the newest entry from the Finshots RSS feed."""
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        raise RuntimeError("Finshots RSS feed returned no entries — feed may be down or URL changed.")
    latest = feed.entries[0]
    return {
        "title": latest.title,
        "link": latest.link,
        "summary": getattr(latest, "summary", "").strip(),
        "published": getattr(latest, "published", ""),
    }


def already_sent(link: str) -> bool:
    """Check our log so we don't send the same post twice."""
    if not os.path.exists(SENT_LOG):
        return False
    with open(SENT_LOG, "r", encoding="utf-8") as f:
        return link.strip() in {line.strip() for line in f}


def mark_sent(link: str) -> None:
    with open(SENT_LOG, "a", encoding="utf-8") as f:
        f.write(link.strip() + "\n")


def send_to_telegram(bot_token: str, chat_id: str, post: dict) -> None:
    """Send the post as a formatted Telegram message."""
    # Telegram caps messages at 4096 chars; Finshots summaries are short so this is safe,
    # but we trim defensively in case a post ever has a long RSS summary.
    summary = post["summary"]
    if len(summary) > 500:
        summary = summary[:500].rsplit(" ", 1)[0] + "..."

    text = (
        f"📊 *Finshots Daily*\n\n"
        f"*{post['title']}*\n\n"
        f"{summary}\n\n"
        f"🔗 {post['link']}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    resp = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        },
        timeout=15,
    )
    resp.raise_for_status()


def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables.")
        sys.exit(1)

    post = get_latest_post()

    if already_sent(post["link"]):
        print(f"Already sent today's post: {post['title']}")
        return

    send_to_telegram(bot_token, chat_id, post)
    mark_sent(post["link"])
    print(f"Sent: {post['title']}")


if __name__ == "__main__":
    main()
