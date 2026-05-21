import re
import sys

def main():
    with open("prompt.txt", "r") as f:
        content = f.read()

    # Extract the first HTML block
    match = re.search(r'<!DOCTYPE html>.*?</html>', content, re.DOTALL)
    if match:
        html = match.group(0)
        with open("index.html", "w") as out:
            out.write(html)
        print("Successfully saved index.html")
    else:
        print("Could not find HTML in prompt.txt")

if __name__ == "__main__":
    main()
