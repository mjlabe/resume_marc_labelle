import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    "plaster_pastedeploy",
    "pyramid",
    "pyramid_jinja2",
    "pyramid_debugtoolbar",
    "waitress",
    "pydantic",
]

tests_require = ["WebTest", "pytest", "pytest-cov", "black"]

setup(
    name="resume",
    version="0.0",
    description="resume",
    long_description="resume",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web pyramid pylons",
    packages=find_packages(exclude=["tests"])
    + ["resume"]
    + find_packages(where="vendor/pyramid_precis_creative_template"),
    package_dir={
        "resume": "resume",
        "pyramid_precis_creative_template": "vendor/pyramid_precis_creative_template/pyramid_precis_creative_template",
    },
    package_data={
        "resume": ["data/*"],
        "pyramid_precis_creative_template": ["static/**/*", "templates/*.jinja2"],
    },
    include_package_data=True,
    zip_safe=True,
    extras_require={
        "testing": tests_require,
    },
    install_requires=requires,
    entry_points={
        "paste.app_factory": [
            "main = resume:main",
        ],
        "console_scripts": [
            "resume-to-pdf=resume.services.command:resume_to_pdf",
            "new-config=resume.services.command:new_config"
        ]
    },
)
