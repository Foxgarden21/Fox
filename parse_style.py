with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_idx = html.find('</style>')
if start_idx != -1:
    print("Found </style>")
