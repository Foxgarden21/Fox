import re
import os

with open("live_index.html", "r") as f:
    html = f.read()

# Already saved via curl earlier, let's just make sure it's copied to index.html
with open("index.html", "w") as f:
    f.write(html)
