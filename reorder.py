from bs4 import BeautifulSoup
import copy

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

body = soup.find('body')

# Find all direct children of body that are <header> or <section> or <footer> or <script> or other stuff
children = list(body.children)

# The sections we care about
sections_dict = {}
for child in children:
    if child.name in ['header', 'section']:
        sec_id = child.get('id')
        if sec_id:
            sections_dict[sec_id] = child

# Desired order based on user prompt
# 1. Hero (id="top")
# 2. Rotující reference (id="reference")
# 3. Proměny zahrad (id="ukazky")
# 4. Naše služby (id="sluzby")
# 5. Proč si vybrat nás (id="proc-nas")
# 6. Ceník (id="cenik")
# 7. FAQ (id="faq")
# 8. Kontakt (id="kontakt")

# What about the others?
# Current ones: top, proc-nas, ukazky, sluzby, cenik, reference, rady, spoluprace, faq, onas, kontakt, seo-text
# I will output them in this order:
# top
# reference
# ukazky
# sluzby
# proc-nas
# cenik
# rady
# spoluprace
# faq
# onas
# kontakt
# seo-text

order = [
    'top',
    'reference',
    'ukazky',
    'sluzby',
    'proc-nas',
    'cenik',
    'rady',
    'spoluprace',
    'faq',
    'onas',
    'kontakt',
    'seo-text'
]

# We also need to preserve the scripts that are placed directly after the sections in the body.
# Wait, let's just do it manually with regex or string replacement, BeautifulSoup might mess up the formatting/indentation.
