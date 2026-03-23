"""HTML and PDF report generators."""

import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from stripe_inspector import __version__


def get_template_dir():
    return os.path.join(os.path.dirname(__file__), "web", "templates")


def generate_html_report(result: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(get_template_dir()),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("report.html")

    return template.render(
        result=result,
        result_json=json.dumps(result, indent=2, default=str),
        generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        version=__version__,
    )


def generate_pdf_report(result: dict) -> bytes:
    try:
        from weasyprint import HTML
    except ImportError:
        raise ImportError(
            "PDF generation requires weasyprint. Install it with: "
            "pip install stripe-inspector[pdf]"
        )

    html_content = generate_html_report(result)
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes
