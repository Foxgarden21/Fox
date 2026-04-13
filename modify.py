import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace alt="Logo FOX Garden" with alt=""
content = content.replace('alt="Logo FOX Garden"', 'alt=""')

# Change root variables
content = content.replace('--orange: #f97316;', '--orange: #f97316;\n            --primary-btn: #2E7D32;\n            --primary-btn-hover: #4CAF50;')

# Update .btn-primary
content = re.sub(
    r'\.btn-primary\s*\{[^}]*\}',
    '.btn-primary {\n            background: var(--primary-btn);\n            color: var(--white);\n            box-shadow: 0 6px 20px rgba(46, 125, 50, 0.25);\n        }',
    content
)

content = re.sub(
    r'\.btn-primary:hover\s*\{[^}]*\}',
    '.btn-primary:hover {\n            background: var(--primary-btn-hover);\n            transform: translateY(-3px);\n            box-shadow: 0 10px 25px rgba(76, 175, 80, 0.35);\n            color: var(--white);\n        }',
    content
)

# Update nav-cta
content = re.sub(
    r'\.hero-nav a\.nav-cta\s*\{[^}]*\}',
    '.hero-nav a.nav-cta {\n            background: var(--primary-btn);\n            color: var(--white);\n            border-color: var(--primary-btn);\n        }',
    content
)
content = re.sub(
    r'\.hero-nav a\.nav-cta:hover\s*\{[^}]*\}',
    '.hero-nav a.nav-cta:hover {\n            background: var(--primary-btn-hover);\n            border-color: var(--primary-btn-hover);\n        }',
    content
)

# Update .micro color to var(--green)
content = re.sub(
    r'\.micro\s*\{([^}]*)color:\s*var\(--orange\);([^}]*)\}',
    r'.micro {\1color: var(--green);\2}',
    content
)

# Update .price-card p color
content = re.sub(
    r'\.price-card p\s*\{([^}]*)color:\s*var\(--orange\);([^}]*)\}',
    r'.price-card p {\1color: var(--green);\2}',
    content
)

# Update .float-btn
content = re.sub(
    r'\.float-btn\s*\{([^}]*)background:\s*var\(--orange\);([^}]*)box-shadow:\s*0 10px 25px rgba\(249, 115, 22, 0\.4\);([^}]*)\}',
    r'.float-btn {\1background: var(--primary-btn);\2box-shadow: 0 10px 25px rgba(46, 125, 50, 0.4);\3}',
    content
)

content = re.sub(
    r'\.float-btn:hover\s*\{([^}]*)background:\s*var\(--orange-hover\);([^}]*)box-shadow:\s*0 15px 30px rgba\(249, 115, 22, 0\.5\);([^}]*)\}',
    r'.float-btn:hover {\1background: var(--primary-btn-hover);\2box-shadow: 0 15px 30px rgba(76, 175, 80, 0.5);\3}',
    content
)

# O nas text - fix "Nejsme nejlevnejsi"
content = re.sub(
    r'color:\s*var\(--orange\);\s*(margin-bottom:\s*32px;\s*>\s*Nejsme nejlevnější)',
    r'color: var(--green); \1',
    content
)
content = content.replace('color: var(--orange); margin-bottom: 32px;">Nejsme nejlevnější', 'color: var(--green); margin-bottom: 32px;">Nejsme nejlevnější')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Modifications applied successfully.")
