import lxml.html
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from texas import Context

from . import render

__version__ = "0.4"
GRITS_TEMPLATES = Path(os.path.abspath(os.path.dirname(__file__))).resolve() / "templates"


def extract_tag(html, tag, invert=False):
    """Takes a string of html and strip some elements from it.

    If ``invert`` is ``False``, returns a string with **only** the tag.
    Otherwise if invert is True, returns a string with all tags **except** the given tag.

    .. code-block:: pycon

        # Return all non-script elements
        >>> extract_tag("html...", "script", invert=True)
    """
    def match(el):
        return (el.tag == tag) is not invert

    def as_str(el):
        return lxml.html.tostring(el).decode("utf-8")

    elements = lxml.html.fromstring(html).getchildren()
    elements = filter(match, elements)
    return "\n".join(map(as_str, elements))


def static_file(filename: str, suffix: str):
    """unlike *.html, other files have absolute positions relative the root."""
    if not filename.endswith(suffix):
        filename += "." + suffix
    if not filename.startswith("/"):
        filename = "/" + filename
    return filename


def new_environment(templates_dir: str, jinja_options: dict):
    searchpath = [str(GRITS_TEMPLATES)]
    if templates_dir:
        # first entry so users can override __full.html, __partial.html
        searchpath.insert(0, templates_dir)
    loader = FileSystemLoader(searchpath)
    environment = Environment(loader=loader, **jinja_options)
    environment.filters["extract_tag"] = extract_tag
    return environment


def default_context():
    context = Context()
    context.include("default").update({
        "css_files": [],
        "js_files": ["static/vendor/mapp.min.js"],
        "inline_css": [],
        "inline_js": ["static/vendor/rq.min.js"],
        "static_file": static_file,
    })
    return context


def build(src_dir: str, out_dir: str, context: Context, jinja_options: dict=None):
    src_dir = Path(src_dir).expanduser().resolve()
    out_dir = Path(out_dir).expanduser().resolve()

    env = new_environment(str(src_dir), jinja_options or {})
    renderer = render.Renderer(env, context, out_dir)

    # Render fixed paths first so they're overwritten by any custom versions below
    renderer.render("_dynamicRoutes.json")
    renderer.render("_prefetchManifest.json")
    for js_file in renderer.context["js_files"]:
        renderer.render(js_file)
    for css_file in renderer.context["css_files"]:
        renderer.render(css_file)

    for path in src_dir.glob("**/*"):
        if path.is_dir():
            continue
        name = str(path.relative_to(src_dir))
        renderer.render(name, src_dir=src_dir)
