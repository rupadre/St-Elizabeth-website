# Notes for Claude: St. Elizabeth the New Martyr parish website

Read this first in every session. The person you're working with is the parish priest, Fr. Arkady (Migunov). He is not a programmer; he updates the site by asking you in plain words. Reply in plain language, make the change, and say briefly what changed.

## The parish
- St. Elizabeth the New Martyr Orthodox Church, 28010 East Broadway St, Walbridge, OH 43465. Phone (419) 662-3922 (call or text Fr. Arkady).
- Bulgarian Diocese of the Orthodox Church in America; bishop: His Eminence Archbishop Alexander (Golitzin). List Archbishop Alexander first on the About page.
- Almost entirely English-speaking. Founded as St. George Parish in East Toledo in 1936 by Bulgarian and Macedonian immigrants; St. George Cathedral in Rossford 2002–2023; first Liturgy in the 1883 Walbridge church on Palm Sunday 2024.
- Main audience: Protestant and some Catholic seekers, plus non-religious newcomers. Tone: warm, plain, never polemical. Every teaching page carries Fr. Arkady's blessing; don't change doctrine wording without asking him.

## How the site works
- Django + django-distill, published as plain HTML on Render (free static site, see render.yaml). Pushing to GitHub redeploys automatically.
- All content is in content/ (Markdown pages, JSON data, history.html); photos in static/img/; styles in static/css/site.css. See README.md for the full map.
- Templates must stay readable by both Django and Jinja2 (build_preview.py): use only extends, block, include, for, if, {{ value }} and |safe. No {% static %} or {% url %}; use {{ static }} and plain paths. Don't name JSON keys "items", "keys" or "values".
- Before pushing: run `python manage.py distill-local public --force --collectstatic` and check pages at phone width (390px) and desktop.

## Publishing
- In cloud sessions, work on a branch so Fr. Arkady can review the change first.
- Fr. Arkady wants to see a preview before anything goes live. After every change: build, serve public/ on port 8765 (python3 -m http.server 8765 from public/), call report_preview_port for it, and send screenshots (phone and desktop). Never push to main until he has seen the preview and says "publish".
- When he says "publish" (or "make it live", "looks good, publish"), merge the branch into main and push. Render then rebuilds the live site from main within a few minutes. Confirm in plain words when it's done.

## Design rules
- Palette from the church: brick #8b3a2b, ink #1b2233, glass blue #1e4f8f, gilt #b8892b (decoration and focus only, never text), plaster #f5f6f3. Fonts: Marcellus (headings), Public Sans (body).
- Pointed-arch motif (like the church windows) is used only for the homepage photo and the logo. Keep it rare.
- Calendar and Give must stay easy to see on every page, including phones. Keep WCAG AA contrast, visible focus, 44px tap targets, alt text on every meaningful photo.

## Routine updates
- Monthly calendar: add the PDF to static/calendar/ and a line to content/calendar.json ("YYYY-MM": "/static/calendar/file.pdf"). The site names this month and next month automatically.
- Livestream goes public: set "livestream_public": true in content/site.json.
- Service times: content/schedule.json. Ministries: content/ministries.json.
- Events come from the monthly calendar: when Fr. Arkady sends a new month's calendar PDF, read it and add each feast, special service and parish event (not the regular weekly services) to content/events.json (date YYYY-MM-DD, optional end_date, title, time, text, optional photo). Copy times exactly from the calendar; never invent them. Events move from "Coming up" to "Past events" by themselves after their date; the homepage shows the next four. If the calendar shows a little picture next to an event (clip art or an icon), cut it out of the PDF, save it in static/img/ as event-<name>.jpg on a white background, and set image, image_alt and "image_small": true on that event.
- Bulletin: put the PDF in static/bulletin/ and set url and label (e.g. "Sunday, November 22") in content/bulletin.json. Empty url shows "Coming soon".

## Open items (as of November 17, 2026)
- Calendar PDFs still link to the old Squarespace site; move November/December PDFs into static/calendar/ before Squarespace is cancelled.
- Fr. Arkady's title: the old site says Igumen (2021), the history file says Archimandrite. The site currently says "Fr. Arkady (Migunov)".
- Ministries: the 12 parish ministries (from the Sunday of Ministries slides) are in content/ministries.json under "parish", shown as a diagram linked to cards. Descriptions were written by Claude for Fr. Arkady to review. Leaders' personal phone numbers and emails are in the slides but NOT on the site; ask before adding them. Youth uses a photo Fr. Arkady chose himself (children mostly seen from behind); the charity picture in the Drive folder is a watermarked stock photo, do not use it. Regular gatherings (Church School meets the second Sunday of each month; its description still a placeholder; Tea for the Theotokos was a one-time event on Nov 21, 2026, not a ministry) are under "entries".
- Photo permissions pending: children's photos, the baptism photo, the St. George Cathedral exterior (DSC_0005), and the full-length St. Elizabeth icon (13340-elizavetaJPG_2000.jpg, may be from an icon shop). These are kept out of static/img/ except the icon, which is in use pending confirmation.
- Homepage Pascha photo is only 960px wide; ask for the original if available.
- Giving: online giving is Tithe.ly (site.json giving_link, same link as the old site). The old Squarespace "Pledge Card Form" is replaced on /give/ by a form that opens the visitor's email to office@stelizabethmartyr.org (static/js/pledge.js; nothing stored). Printable card: static/give/pledge-card.pdf. Pledges go to office@ (confirmed). Venmo: QR in static/img/venmo-qr.png, link in site.json venmo_link (decoded from the QR). Checks are made out to "St Elizabeth New Martyr Church". Make sure office@ email keeps working after Squarespace is cancelled.
- Point stelizabethmartyr.org to Render when the site is approved.
- Events for November and December 2026 were read from the parish calendar PDFs on November 17, 2026.
- No bulletin posted yet; ask Fr. Arkady for the current bulletin PDF.
