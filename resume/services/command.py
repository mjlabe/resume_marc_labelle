import typing
import urllib
from contextlib import contextmanager
from datetime import datetime
from io import BytesIO
from pathlib import Path
from subprocess import Popen
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

import click
import pendulum
import requests
from PyPDF2 import PdfReader, PdfWriter, PageObject
from pyramid.paster import bootstrap

from resume import DEFAULT_TEMPLATE, TEMPLATES


@contextmanager
def _serve_web(config_uri: str):
    proc = None
    try:
        proc = Popen(["pserve", config_uri])
        for _ in range(30):
            try:
                urlopen("http://localhost:6543/resume", timeout=1)
                break
            except URLError:
                print("Sleep for 1 second...")
                sleep(1)
        yield
    finally:
        if proc:
            proc.kill()


def _generate_runtime_settings(config_uri: str) -> typing.Dict[str, str]:
    env = bootstrap(config_uri)
    registry = env["request"].registry
    settings = registry.settings
    app_dir = settings["APP_DIR"]
    root_dir = settings["ROOT_DIR"]
    resume_static = settings["RESUME_STATIC"]
    content_dir = settings["CONTENT_DIR"]
    default_resume_content = settings["resume.default_content"]
    return {
        "app_dir": app_dir,
        "root_dir": root_dir,
        "resume_static": resume_static,
        "content_dir": content_dir,
        "default_resume_content": default_resume_content,
    }


def _generate(
    file_name_suffix: str,
    url: str,
    content_dir: Path,
    config_uri: str,
):
    pdf = Path(content_dir, f"{file_name_suffix}.pdf")
    with _serve_web(config_uri):
        with requests.get(url, stream=True) as r:
            pdf.write_bytes(r.content)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("config_uri", default="resume.ini")
def resume_to_pdf(config_uri: str):
    """
    Run webpage in the background and download the pdf directly to the content folder
    """
    config_uri = str(Path("configs", config_uri))
    runtime_configs = _generate_runtime_settings(config_uri)
    now = pendulum.now("US/Eastern").format("YYYYMMDD")
    _generate(
        file_name_suffix=f"Resume_{now}",
        url="http://localhost:6543/resume/pdf",
        config_uri=config_uri,
        content_dir=Path(runtime_configs["content_dir"]),
    )


@cli.command()
@click.argument("config_name")
@click.option(
    "--template",
    help="Choose a template",
    type=click.Choice(TEMPLATES),
    default=DEFAULT_TEMPLATE,
)
@click.option("--content-file", help="Name of content file", default="resume_content")
def new_config(config_name: str, template: str, content_file: str):
    """
    Create a new configuration file
    """
    config_uri = Path("configs", f"{config_name}.ini")
    template_ini = Path("configs", "template.ini")
    example_content = Path("content", "example_content")
    content_uri = Path("content", f"{content_file}.yaml")
    if not content_uri.exists():
        content_uri.write_text(example_content.read_text())
    template_str = template_ini.read_text()
    template_str = template_str.format(template=template, content=content_file)
    config_uri.write_text(template_str)


if __name__ == "__main__":
    cli()
