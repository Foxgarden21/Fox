with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_idx = html.find('<section id="reference">')
end_idx = html.find('</section>', start_idx) + len('</section>')

print(html[start_idx:end_idx])
