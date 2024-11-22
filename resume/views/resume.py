from pathlib import Path

import pdfkit
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.response import Response, FileResponse
from pyramid.view import view_config

from resume import models as default_models


def _get_resume_content(content_path: Path, model):
    content = model.parse_file(
        content_path,
        content_type="application/yaml",
    )
    return content


def _get_model(request):
    try:
        models = getattr(request, "models")
        return models.Resume
    except AttributeError:
        return default_models.Resume


@view_config(route_name="resume")
def resume(request):
    model = _get_model(request)
    resume_content = _get_resume_content(request.content_path, model)
    return render_to_response(
        f"{request.theme}:templates/resume.jinja2",
        resume_content,
        request=request,
    )


@view_config(route_name="resume_pdf")
def resume_pdf(request):
    model = _get_model(request)
    resume_content = _get_resume_content(request.content_path, model)
    result = render(
        f"{request.theme}:templates/resume.jinja2", resume_content, request=request
    )
    pdf_output = pdfkit.from_string(result, False)
    return Response(
        body=pdf_output,
        content_type="application/pdf",
        content_disposition='attachment; filename="Resume.pdf"',
    )


@view_config(route_name="favicon")
def favicon_view(request):
    return FileResponse(request.favicon, request=request)
