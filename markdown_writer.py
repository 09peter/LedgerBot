import os
import re
import datetime
import yaml
from utils import slugify

class MarkdownWriter:
    def __init__(self, out_dir="reports"):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def build(self, message):
        # 1) Prepare front-matter fields
        date = message.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        # Use first line (up to 8 words) as title fallback
        title_raw = message.content.strip().split("\n", 1)[0]
        title = " ".join(title_raw.split()[:8]) or f"Report {date}"
        slug = slugify(title)
        author = message.author.display_name

        # Build the YAML front-matter
        fm = {
            "title": title,
            "date": date,
            "author": author,
        }

        # 2) Assemble the Markdown body
        body = message.content
        md_lines = [
            "---",
            yaml.dump(fm, sort_keys=False).strip(),
            "---",
            "",
            body,
            ""
        ]
        full_md = "\n".join(md_lines)

        # 3) Write to file: YYYY-MM-DD-slug.md
        fname = f"{message.created_at.strftime('%Y-%m-%d')}-{slug}.md"
        path = os.path.join(self.out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_md)

        return path  # Return the path for logging/confirmation
