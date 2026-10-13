from configparser import ConfigParser
from pathlib import Path
from subprocess import run
from unittest import TestCase, main


PROJECT_ROOT = Path(__file__).parent.parent


class ResumeBuildTests(TestCase):
    def test_resume_passes_the_selected_resume_file_to_the_pdf_command(self):
        result = run(
            ["make", "--dry-run", "resume", "RESUME=lead"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "docker-compose run resume-web resume-to-pdf resume.ini --content-file lead",
            result.stdout,
        )

    def test_pdf_filename_includes_the_selected_resume_type(self):
        command_source = (PROJECT_ROOT / "resume" / "services" / "command.py").read_text()

        self.assertIn(
            'f"marc_labelle_resume_{content_file}_{now.format(\'YY-MM-DD\')}"',
            command_source,
        )

    def test_resume_config_defaults_to_the_staff_content_file(self):
        config_path = PROJECT_ROOT / "configs" / "resume.ini"
        config = config_path.read_text()

        self.assertIn("resume.default_content = %(here)s/../content/staff.yaml", config)
        self.assertNotIn("resume_content", config)

        parser = ConfigParser(defaults={"here": str(config_path.parent)})
        parser.read(config_path)

        self.assertEqual(
            Path(parser.get("app:main", "resume.default_content")).resolve(),
            PROJECT_ROOT / "content" / "staff.yaml",
        )

    def test_pdf_output_directory_is_ignored(self):
        ignore_file = (PROJECT_ROOT / ".gitignore").read_text()

        self.assertIn("output/", ignore_file)


if __name__ == "__main__":
    main()
