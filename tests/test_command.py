from contextlib import nullcontext
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, patch

from resume import main
from resume.services.command import _generate, _render_html_to_pdf, _serve_web, resume_to_pdf


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


class ServeWebTests(TestCase):
    @patch("resume.services.command.urlopen")
    @patch("resume.services.command.Popen")
    def test_passes_selected_content_to_the_web_process(self, popen, urlopen):
        process = MagicMock()
        popen.return_value = process

        with _serve_web("configs/resume.ini", "lead"):
            pass

        _, keyword_arguments = popen.call_args
        self.assertEqual(
            keyword_arguments.get("env", {}).get("RESUME_DEFAULT_CONTENT"),
            "content/lead.yaml",
        )
        process.kill.assert_called_once_with()


class ResumeApplicationTests(TestCase):
    @patch("resume.Configurator")
    @patch.dict(os.environ, {"RESUME_DEFAULT_CONTENT": "content/lead.yaml"})
    def test_uses_content_from_the_pdf_process(self, configurator):
        config = MagicMock()
        configurator.return_value.__enter__.return_value = config

        main({}, **{"resume.default_content": "content/staff.yaml"})

        settings = configurator.call_args.kwargs["settings"]
        self.assertEqual(settings["resume.default_content"], "content/lead.yaml")


class PdfExportTests(TestCase):
    @patch("resume.services.command._generate")
    @patch("resume.services.command._generate_runtime_settings")
    @patch("resume.services.command.pendulum.now")
    def test_exports_to_an_output_directory(self, now, runtime_settings, generate):
        now.return_value.format.return_value = "26-10-13"
        runtime_settings.return_value = {"root_dir": "/tmp/resume-project"}

        resume_to_pdf.callback("resume.ini", "lead")

        self.assertEqual(
            generate.call_args.kwargs["output_dir"],
            Path("/tmp/resume-project/output"),
        )

    @patch("resume.services.command._render_html_to_pdf")
    @patch("resume.services.command._serve_web")
    def test_creates_the_output_directory_before_rendering(self, serve_web, render_html):
        serve_web.return_value = nullcontext()

        with TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory, "output")
            _generate(
                file_name_suffix="resume",
                url="http://localhost:6543/resume",
                output_dir=output_directory,
                config_uri="configs/resume.ini",
                content_file="staff",
            )

            self.assertTrue(output_directory.is_dir())
