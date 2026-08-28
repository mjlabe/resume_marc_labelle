"""Top-level package for Pyramid Resume Template Default."""

__version__ = "0.1.0"

from pathlib import Path

from pyramid_precis_creative_template import models


def includeme(config):
    config.include("pyramid_jinja2")
    config.add_jinja2_extension("jinja2.ext.with_")
    config.add_jinja2_search_path("pyramid_precis_creative_template:templates")
    config.add_static_view("pyramid_precis_creative_template_static", "pyramid_precis_creative_template:static/")
    config.add_request_method(lambda _: models, "models", reify=True)
    config.add_request_method(
        lambda _: Path(config.registry.settings["resume.default_content"]), "content_path", reify=True
    )
    config.add_request_method(lambda _: "pyramid_precis_creative_template", "theme", reify=True)
    config.add_request_method(lambda _: "favicon_io/favicon.ico", "favicon", reify=True)
