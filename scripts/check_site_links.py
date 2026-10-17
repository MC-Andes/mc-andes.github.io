"""Check local HTML links, fragment identifiers and media in a built MkDocs site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs = set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.refs.append((tag, key, attrs[key]))


def check(root):
    pages = {p.resolve(): Page(p.read_text()) for p in root.rglob("*.html")}
    errors = []
    count = 0
    for path, page in pages.items():
        for tag, key, ref in page.refs:
            u = urlsplit(ref)
            if u.netloc or u.scheme:
                continue
            if not u.path and not u.fragment:
                continue
            target = ((root / unquote(u.path).lstrip("/")) if u.path.startswith("/")
                      else path.parent / unquote(u.path)) if u.path else path
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            count += 1
            if not target.exists():
                errors.append(f"{path.relative_to(root)}: missing {ref}")
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(root)}: missing fragment {ref}")
    if not pages:
        errors.append("No HTML pages found; run mkdocs build --strict first")
    for error in errors:
        print(error)
    print(f"Checked {len(pages)} HTML pages and {count} local references; {len(errors)} errors")
    return bool(errors)

if __name__ == "__main__":
    sys.exit(check(Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()))
