"""Every page on the site, in one list.

Django builds its URLs from ROUTES (see parish/urls.py), and the preview
builder renders the same list, so both always produce the same pages.
To add a page: add a Markdown file under content/ and, if it is in a new
section, a line below.
"""
import datetime
import json

from . import content

STATIC = "/static/"

NAV = [
    {"key": "new", "label": "I'm new", "url": "/new/"},
    {"key": "worship", "label": "Worship", "url": "/worship/"},
    {"key": "orthodoxy-101", "label": "Orthodoxy 101", "url": "/orthodoxy-101/"},
    {"key": "ministries", "label": "Ministries", "url": "/ministries/"},
    {"key": "events", "label": "Events & calendar", "url": "/events/"},
    {"key": "about", "label": "About", "url": "/about/"},
]


MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def calendar_months(today=None):
    """This month and next month, named, with the PDF link if one is posted.

    Computed when the site is built; static/js/calendar.js updates the same
    links in the visitor's browser so they stay right between builds."""
    today = today or datetime.date.today()
    months = content.data("calendar")["months"]
    result = []
    for offset in (0, 1):
        y, m = today.year + (today.month - 1 + offset) // 12, (today.month - 1 + offset) % 12 + 1
        key = f"{y}-{m:02d}"
        result.append({"key": key, "label": f"{MONTHS[m - 1]} {y}", "month": MONTHS[m - 1], "url": months.get(key, "")})
    return result


def base_context(section=""):
    return {
        "calendar_months": calendar_months(),
        "bulletin": content.data("bulletin"),
        "calendar_json": json.dumps(content.data("calendar")["months"]),
        "site": content.data("site"),
        "schedule": content.data("schedule"),
        "nav": NAV,
        "section": section,
        "static": STATIC,
    }


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def events(today=None):
    """All events, split into coming up (soonest first) and past (newest first).

    The split is made when the site is built; static/js/events.js moves
    events in the visitor's browser once their date has passed."""
    today = today or datetime.date.today()
    upcoming, past = [], []
    for e in content.data("events")["events"]:
        e = dict(e)
        start = datetime.date.fromisoformat(e["date"])
        end = datetime.date.fromisoformat(e.get("end_date", e["date"]))
        e["end_date"] = end.isoformat()
        e["day"] = start.day
        e["month_short"] = MONTHS[start.month - 1][:3]
        e["year"] = start.year
        e["long_date"] = _date_words(start)
        if end != start:
            e["long_date"] += f" to {_date_words(end)}"
        (past if end < today else upcoming).append(e)
    upcoming.sort(key=lambda e: e["date"])
    past.sort(key=lambda e: e["date"], reverse=True)
    return upcoming, past


RECENT_PAST_DAYS = 90   # past events newer than this stay open on the Events page
FEATURE_DAYS = 42       # a featured story stays on the homepage this many days (and always shows under Highlights on the Events page)


def _date_words(d):
    return f"{WEEKDAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}, {d.year}"


def stories():
    """Stories and photos from past events (content/parish-life/), newest first."""
    result = []
    for s in content.section_pages("parish-life"):
        d = datetime.date.fromisoformat(s["date"])
        s["year"] = d.year
        s["long_date"] = _date_words(d)
        s["is_featured"] = s.get("featured", "").lower() in ("yes", "true")
        s["feature_until"] = (d + datetime.timedelta(days=FEATURE_DAYS)).isoformat()
        result.append(s)
    result.sort(key=lambda s: s["date"], reverse=True)
    return result


def by_year(entries):
    years = []
    for e in entries:
        if not years or years[-1]["year"] != e["year"]:
            years.append({"year": e["year"], "entries": []})
        years[-1]["entries"].append(e)
    return years


def homepage_story(today=None):
    """The newest featured story, while it is still recent (FEATURE_DAYS)."""
    today = today or datetime.date.today()
    for s in stories():
        d = datetime.date.fromisoformat(s["date"])
        if s["is_featured"] and d <= today <= d + datetime.timedelta(days=FEATURE_DAYS):
            return s
    return None


def ctx_events():
    ctx = base_context("events")
    upcoming, past = events()
    cutoff = (datetime.date.today() - datetime.timedelta(days=RECENT_PAST_DAYS)).isoformat()
    ctx["upcoming"] = upcoming
    ctx["past"] = [e for e in past if e["end_date"] >= cutoff]
    ctx["older_years"] = by_year([e for e in past if e["end_date"] < cutoff])
    ctx["featured_stories"] = [s for s in stories() if s["is_featured"]][:3]
    return ctx


def ctx_parish_life():
    ctx = base_context("events")
    ctx["years"] = by_year(stories())
    return ctx


def ctx_story(slug):
    def build():
        ctx = base_context("events")
        all_stories = stories()
        i = next(n for n, s in enumerate(all_stories) if s["slug"] == slug)
        ctx["story"] = all_stories[i]
        ctx["newer"] = all_stories[i - 1] if i > 0 else None
        ctx["older"] = all_stories[i + 1] if i + 1 < len(all_stories) else None
        return ctx
    return build


def ctx_home():
    ctx = base_context("home")
    upcoming, _ = events()
    ctx["upcoming"] = upcoming[:4]
    ctx["story"] = homepage_story()
    ctx["paths"] = [content.page("new", s) for s in ("protestant", "catholic", "non-religious")]
    o101 = {p["slug"]: p for p in content.section_pages("orthodoxy-101")}
    ctx["questions"] = [o101[s] for s in ("icons", "mary-and-the-saints", "ethnic", "what-is-the-orthodox-church")]
    return ctx


def ctx_section_page(section, slug, template_section=None):
    def build():
        ctx = base_context(template_section or section)
        ctx["page"] = content.page(section, slug)
        ctx["siblings"] = content.section_pages(section)
        ctx["section_index"] = content.page(section, "index") if (content.CONTENT / section / "index.md").exists() else None
        ctx["section_url"] = f"/{section}/"
        return ctx
    return build


def ctx_section_index(section):
    def build():
        ctx = base_context(section)
        ctx["page"] = content.page(section, "index")
        ctx["children"] = content.section_pages(section)
        ctx["section_url"] = f"/{section}/"
        return ctx
    return build


def ctx_worship():
    ctx = base_context("worship")
    ctx["page"] = content.page("pages", "worship")
    return ctx


def ctx_service_texts():
    ctx = base_context("worship")
    ctx["groups"] = content.data("service_texts")["groups"]
    return ctx


def ctx_simple(slug, section):
    def build():
        ctx = base_context(section)
        ctx["page"] = content.page("pages", slug)
        return ctx
    return build


def ctx_ministries():
    ctx = base_context("ministries")
    ctx["page"] = content.page("pages", "ministries")
    ctx["ministries"] = content.data("ministries")
    return ctx


def ctx_history():
    ctx = base_context("about")
    ctx["history_html"] = content.raw_html("history")
    return ctx


def ctx_about():
    ctx = base_context("about")
    ctx["page"] = content.page("pages", "about")
    ctx["about_page"] = "about"
    return ctx


def ctx_saint():
    ctx = base_context("about")
    ctx["page"] = content.page("pages", "st-elizabeth")
    ctx["about_page"] = "saint"
    return ctx


def _build_routes():
    routes = [
        ("", "home.html", ctx_home),
        ("new/", "section_index.html", ctx_section_index("new")),
        ("orthodoxy-101/", "section_index.html", ctx_section_index("orthodoxy-101")),
        ("worship/", "worship.html", ctx_worship),
        ("worship/service-texts/", "service_texts.html", ctx_service_texts),
        ("ministries/", "ministries.html", ctx_ministries),
        ("about/", "about.html", ctx_about),
        ("about/st-elizabeth/", "saint.html", ctx_saint),
        ("about/history/", "history.html", ctx_history),
        ("calendar/", "calendar.html", ctx_simple("calendar", "events")),
        ("events/", "events.html", ctx_events),
        ("parish-life/", "parish_life.html", ctx_parish_life),
        ("glossary/", "page.html", ctx_simple("glossary", "new")),
        ("contact/", "contact.html", ctx_simple("contact", "contact")),
        ("give/", "give.html", ctx_simple("give", "give")),
    ]
    for story in stories():
        routes.append((f"parish-life/{story['slug']}/", "story.html", ctx_story(story["slug"])))
    for section in ("new", "orthodoxy-101"):
        for p in content.section_pages(section):
            routes.append((f"{section}/{p['slug']}/", "page.html", ctx_section_page(section, p["slug"])))
    return routes


ROUTES = _build_routes()
