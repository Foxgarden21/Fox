import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's locate the sections by line numbers or index
# Since there are not many sections, let's just do a string split/regex approach.

blocks = {}

# Match <header ... id="top"> ... </header>
hero_match = re.search(r'<header class="hero" id="top">.*?</header>\s+', html, flags=re.DOTALL)
if hero_match:
    blocks['top'] = hero_match.group(0)

def extract_section(id_name, extract_script=False):
    # Find section
    pattern = r'(<section id="' + id_name + r'".*?</section>\s+)'
    if extract_script:
        pattern = r'(<section id="' + id_name + r'".*?</section>\s+<script>.*?</script>\s+)'

    match = re.search(pattern, html, flags=re.DOTALL)
    if match:
        return match.group(0)
    return ""

blocks['proc-nas'] = extract_section('proc-nas')
blocks['ukazky'] = extract_section('ukazky', extract_script=True)
blocks['sluzby'] = extract_section('sluzby')
blocks['cenik'] = extract_section('cenik')
blocks['reference'] = extract_section('reference')
blocks['rady'] = extract_section('rady')
blocks['spoluprace'] = extract_section('spoluprace')
blocks['faq'] = extract_section('faq')
blocks['onas'] = extract_section('onas')
blocks['kontakt'] = extract_section('kontakt')
blocks['seo-text'] = extract_section('seo-text')

for k, v in blocks.items():
    if not v:
        print(f"Failed to find {k}")

# Reorder them according to the requested plan:
# 1. Hero
# 2. Rotující reference
# 3. Proměny zahrad (ukazky)
# 4. Naše služby (sluzby)
# 5. Proč si vybrat nás (proc-nas)
# 6. Ceník (cenik)
# 7. FAQ (faq)
# 8. Kontakt (kontakt)
# Keeping rady, spoluprace, onas, seo-text in reasonable places.
# Let's place:
# Hero -> Reference -> Ukázky -> Služby -> Proč nás -> Ceník -> Rady -> Spolupráce -> FAQ -> O nás -> Kontakt -> SEO text

new_body_content = "".join([
    blocks['top'],
    blocks['reference'],
    blocks['ukazky'],
    blocks['sluzby'],
    blocks['proc-nas'],
    blocks['cenik'],
    blocks['rady'],
    blocks['spoluprace'],
    blocks['faq'],
    blocks['onas'],
    blocks['kontakt'],
    blocks['seo-text']
])

# Replace the original sections in the HTML.
# Find the start of the first block (Hero) and the end of the last block in original HTML
start_match = re.search(r'<header class="hero" id="top">', html)
end_match = re.search(r'</section>\s+<footer>', html)

if start_match and end_match:
    start_idx = start_match.start()
    # The end_match matches the </section> of the seo-text
    end_idx = end_match.start() + len('</section>\n')

    # Wait, end_match matches exactly the end of the seo-text section.

    # We should also capture anything between the last section and the footer

    with open("index_reordered.html", "w", encoding="utf-8") as f:
        f.write(html[:start_idx])
        f.write(new_body_content)
        # We need to output the rest of the HTML starting from <footer>
        footer_idx = html.find('<footer>')
        f.write(html[footer_idx:])

    print("Reordered successfully.")
else:
    print("Could not find start/end markers")
