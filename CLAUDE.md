# Notes for Claude: St. Elizabeth the New Martyr parish website

Read this first in every session. The person you're working with is the parish priest, Fr. Arkady (Migunov). He is not a programmer; he updates the site by asking you in plain words. Reply in plain language, make the change, and say briefly what changed.

## The parish
- St. Elizabeth the New Martyr Orthodox Church, 28010 East Broadway S, Walbridge, OH 43465. Phone (419) 662-3922 (call or text Fr. Arkady).
- Bulgarian Diocese of the Orthodox Church in America; bishop: His Eminence Archbishop Alexander (Golitzin). List Archbishop Alexander first on the About page.
- Almost entirely English-speaking. Founded as St. George Parish in East Toledo in 1936 by Bulgarian and Macedonian immigrants; St. George Cathedral in Rossford 2002–2023; first Liturgy in the 1883 Walbridge church on Palm Sunday 2024.
- Main audience: Protestant and some Catholic seekers, plus non-religious newcomers. Tone: warm, plain, never polemical. Every teaching page carries Fr. Arkady's blessing; don't change doctrine wording without asking him.

## How the site works
- Django + django-distill, published as plain HTML on Render (free static site, see render.yaml). Pushing to GitHub redeploys automatically.
- All content is in content/ (Markdown pages, JSON data, history.html); photos in static/img/; styles in static/css/site.css. See README.md for the full map.
- Templates must stay readable by both Django and Jinja2 (build_preview.py): use only extends, block, include, for, if, {{ value }} and |safe. No {% static %} or {% url %}; use {{ static }} and plain paths. Don't name JSON keys "items", "keys" or "values".
- Before pushing: run `python manage.py distill-local public --force --collectstatic` and check pages at phone width (390px) and desktop.

## Design rules
- Palette from the church: brick #8b3a2b, ink #1b2233, glass blue #1e4f8f, gilt #b8892b (decoration and focus only, never text), plaster #f5f6f3. Fonts: Marcellus (headings), Public Sans (body).
- Pointed-arch motif (like the church windows) is used only for the homepage photo and the logo. Keep it rare.
- Calendar and Give must stay easy to see on every page, including phones. Keep WCAG AA contrast, visible focus, 44px tap targets, alt text on every meaningful photo.

## Routine updates
- Monthly calendar: add the PDF to static/calendar/ and a line to content/calendar.json ("YYYY-MM": "/static/calendar/file.pdf"). The site names this month and next month automatically.
- Livestream goes public: set "livestream_public": true in content/site.json.
- Service times: content/schedule.json. Ministries: content/ministries.json.

## Open items (as of November 17, 2026)
- Calendar PDFs still link to the old Squarespace site; move November/December PDFs into static/calendar/ before Squarespace is cancelled.
- Confirm Saturday Great Vespers at 4:00 PM is the regular weekly time.
- Fr. Arkady's title: the old site says Igumen (2021), the history file says Archimandrite. The site currently says "Fr. Arkady (Migunov)".
- Ministries: Fr. Arkady will send the full list (12+); current descriptions of Theotokos Tea and Church School are placeholders.
- Photo permissions pending: children's photos, the baptism photo, the St. George Cathedral exterior (DSC_0005), and the full-length St. Elizabeth icon (13340-elizavetaJPG_2000.jpg, may be from an icon shop). These are kept out of static/img/ except the icon, which is in use pending confirmation.
- Homepage Pascha photo is only 960px wide; ask for the original if available.
- Point stelizabethmartyr.org to Render when the site is approved.
