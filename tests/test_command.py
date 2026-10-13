from pathlib import Path
from unittest import TestCase

from resume.services.command import _render_html_to_pdf


class RenderHtmlToPdfTests(TestCase):
    def test_prints_the_html_resume_with_headless_chromium(self):
        destination = Path("/tmp/resume.pdf")
        commands = []

        def run(command, check):
            commands.append((command, check))

        _render_html_to_pdf(
            "http://localhost:6543/resume",
            destination,
            run=run,
        )

        self.assertEqual(
            commands,
            [
                (
                    [
                        "chromium",
                        "--headless",
                        "--no-sandbox",
                        "--disable-gpu",
                        "--no-pdf-header-footer",
                        f"--print-to-pdf={destination}",
                        "http://localhost:6543/resume",
                    ],
                    True,
                )
            ],
        )
