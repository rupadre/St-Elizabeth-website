"""Builds one URL per page from parish/routes.py.

`python manage.py runserver` serves the pages while editing;
`python manage.py distill-local public --force --collectstatic`
writes every page to public/ as plain HTML for Render.
"""
from django_distill import distill_path

from .routes import ROUTES
from .views import make_view

urlpatterns = []
for i, (url, template, build_context) in enumerate(ROUTES):
    urlpatterns.append(
        distill_path(
            url,
            make_view(template, build_context),
            name=f"page-{i}",
            distill_file=f"{url}index.html",
        )
    )
