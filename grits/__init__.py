import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from . import render

__version__ = "0.5.0"
GRITS_TEMPLATES = Path(os.path.abspath(os.path.dirname(__file__))).resolve() / "templates"
DEFAULT_JINJA_OPTIONS = {"trim_blocks": True, "lstrip_blocks": True}


def new_environment(template_dir: str, jinja_options: dict):
    searchpath = [str(GRITS_TEMPLATES)]
    if template_dir:
        # insert so users can override __full.html, __partial.html
        searchpath.insert(0, str(template_dir))
    loader = FileSystemLoader(searchpath)
    return Environment(loader=loader, **jinja_options)


def build(src_dir: str, out_dir: str, template_dir: str=None, context: dict=None, jinja_options: dict=None):
    environment = new_environment(
        template_dir,
        jinja_options=(jinja_options or dict(DEFAULT_JINJA_OPTIONS)))
    renderer = render.Renderer(environment=environment, src_dir=src_dir, out_dir=out_dir)
    renderer.process(context=context)
    return renderer
