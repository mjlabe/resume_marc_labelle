import os
import typing
import urllib
from contextlib import contextmanager
from datetime import datetime
from io import BytesIO
from pathlib import Path
from subprocess import Popen, run
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

import click
import pendulum
import requests
from PyPDF2 import PdfReader, PdfWriter, PageObject
from pyramid.paster import bootstrap

@contextmanager
def _serve_web(config_uri: str, content_file: str):
    proc = None
    try:
        proc = Popen(
            [
                "pserve",
                config_uri,
            ],
            env={
                **os.environ,
                "RESUME_DEFAULT_CONTENT": f"content/{content_file}.yaml",
            },
        )
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


def _render_html_to_pdf(
    url: str,
    destination: Path,
    run=run,
):
    run(
        [
            "chromium",
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={destination}",
            url,
        ],
        check=True,
    )


def _generate(
    file_name_suffix: str,
    url: str,
    output_dir: Path,
    config_uri: str,
    content_file: str,
):
    pdf = Path(output_dir, f"{file_name_suffix}.pdf")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    with _serve_web(config_uri, content_file):
        _render_html_to_pdf(url, pdf)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("config_uri", default="resume.ini")
@click.option(
    "--content-file",
    default="staff",
    help="Resume content filename without the .yaml suffix",
)
def resume_to_pdf(config_uri: str, content_file: str):
    """
    Run webpage in the background and download the PDF to the project root
    """
    config_uri = str(Path("configs", config_uri))
    runtime_configs = _generate_runtime_settings(config_uri)
    now = pendulum.now("US/Eastern")
    _generate(
        file_name_suffix=f"marc_labelle_resume_{content_file}_{now.format('YY-MM-DD')}",
        url="http://localhost:6543/resume",
        config_uri=config_uri,
        output_dir=Path(runtime_configs["root_dir"], "output"),
        content_file=content_file,
    )


if __name__ == "__main__":
    cli()
