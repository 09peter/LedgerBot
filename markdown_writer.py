import os
import re
import datetime
import yaml
from utils import slugify

class MarkdownWriter:
    def __init__(self, out_dir="reports"):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def _extract_tags(self, content: str):
        # find [tag:xyz] patterns
        tags = re.findall(r"\[tag:([^\]]+)\]", content)
        return list({tag.strip() for tag in tags})

    def _build_toc(self, content: str):
        # scan for markdown headings: lines starting with ## or ### etc.
        lines = content.splitlines()
        toc = []
        for line in lines:
            m = re.match(r"^(#{2,6})\s+(.*)$", line)
            if m:
                level = len(m.group(1)) - 1  # TOC indent level
                title = m.group(2).strip()
                slug = slugify(title)
                toc.append(f"{'  ' * (level-1)}- [{title}](#{slug})")
        return "\n".join(toc)

    def build(self, message):
        # Prepare front-matter
        date = message.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        # Use first 5–8 words or fallback to timestamp
        title_raw = message.content.strip().split("\n", 1)[0]
        title = " ".join(title_raw.split()[:8]) or f"Report {date}"
        slug = slugify(title)
        tags = self._extract_tags(message.content)

        fm = {
            "title": title,
            "date": date,
        }
        if tags:
            fm["tags"] = tags

        # Build body
        body = message.content

        # Assemble full markdown
        md = [
            "---",
            yaml.dump(fm, sort_keys=False).strip(),
            "---",
            "",
            "<!-- TOC -->",
            "",
            self._build_toc(body),
            "",
            "<!-- /TOC -->",
            "",
            body,
            ""
        ]
        full = "\n".join(md)

        # Filename: YYYY-MM-DD-slug.md
        fname = f"{message.created_at.strftime('%Y-%m-%d')}-{slug}.md"
        path = os.path.join(self.out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(full)

        return path  # so you know where it landed