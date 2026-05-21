import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Instead of Beautiful soup, let's extract sections and their following scripts (if any) as chunks
# We can find sections by searching for <section id="XYZ" ...>...</section>
# Actually, the user's HTML is small enough to split and join manually or with a simple Python script.

def extract_block(text, start_marker, end_marker):
    start = text.find(start_marker)
    if start == -1: return "", text
    end = text.find(end_marker, start)
    if end == -1: return "", text
    end += len(end_marker)
    block = text[start:end]
    rest = text[:start] + text[end:]
    return block, rest

# Let's write a robust script to extract the body content and reorder sections.
# But looking at the HTML, the sections are simple.
# Wait, <section id="ukazky"> is followed by a <script> block.
