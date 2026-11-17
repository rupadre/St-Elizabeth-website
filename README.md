# St. Elizabeth the New Martyr — parish website

A Django site published as plain web pages (with django-distill) and hosted free on Render as a static site.

## Where things live

| To change… | Edit this |
| --- | --- |
| Service times, parking note | `content/schedule.json` |
| Address, phone, giving link, livestream on/off | `content/site.json` |
| Ministries | `content/ministries.json` |
| Coming and past events | `content/events.json` (filled from each monthly calendar) |
| Weekly bulletin | Put the PDF in `static/bulletin/`, then set it in `content/bulletin.json` |
| Monthly calendars | Put the PDF in `static/calendar/` and add a line to `content/calendar.json`, e.g. `"2027-01": "/static/calendar/2027-01.pdf"` |
| "I'm new" pages | `content/new/*.md` |
| Orthodoxy 101 pages | `content/orthodoxy-101/*.md` |
| Worship, About, Calendar, Glossary, Contact, Give | `content/pages/*.md` |
| History page | `content/history.html` |
| Photos | `static/img/` |
| Colors and layout | `static/css/site.css` |
| Page layouts | `templates/` |

Each Markdown page starts with a short header:

```
---
title: Your first visit
summary: One sentence shown under the title.
order: 1
image: stained-glass
image_alt: A description of the photo for people who can't see it
---
```

The site always shows this month and next month by name, worked out from the visitor's date. A month without a PDF shows "Calendar coming soon".

**Turning on the livestream:** in `content/site.json`, change `"livestream_public": false` to `true`.

## Publishing on Render

1. Put this folder in a GitHub repository.
2. In Render, choose **New → Blueprint** and pick the repository. Render reads `render.yaml`.
3. Render runs `pip install -r requirements.txt && python manage.py distill-local public --force --collectstatic` and publishes the `public/` folder.
4. Under the site's **Settings → Custom Domains**, add `stelizabethmartyr.org` and `www.stelizabethmartyr.org`, then update the domain's DNS records as Render shows.

Every change pushed to GitHub republishes the site automatically, usually within a minute or two.

## Working on it locally

```
pip install -r requirements.txt
python manage.py runserver          # live site at http://127.0.0.1:8000
python build_preview.py preview     # same pages without Django, using Jinja2
```

Templates use only tags that Django and Jinja2 read the same way (`extends`, `block`, `for`, `if`, `{{ value }}` and `|safe`), so both builds match.
