"""Builds a static preview of the site without Django.

Renders the same templates and content as the Django project (parish/routes.py)
with Jinja2, which reads the template tags this site uses the same way.
Usage: python build_preview.py [output_dir]
"""
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from parish.routes import ROUTES  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "preview")
if out.exists():
    shutil.rmtree(out)
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True, undefined=Undefined)
for url, template, build in ROUTES:
    html = env.get_template(template).render(**build())
    target = out / url / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
shutil.copytree(ROOT / "static", out / "static")
print(f"Built {len(ROUTES)} pages into {out}")
