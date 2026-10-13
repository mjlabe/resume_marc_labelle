import os

from pyramid.config import Configurator


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    selected_content = os.getenv("RESUME_DEFAULT_CONTENT")
    if selected_content:
        settings["resume.default_content"] = selected_content

    with Configurator(settings=settings) as config:
        config.include("pyramid_jinja2")
        config.include(".routes")
        config.scan()
    return config.make_wsgi_app()
