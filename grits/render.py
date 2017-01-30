import jinja2
import texas

from contextlib import contextmanager
from pathlib import Path
from typing import Union


@contextmanager
def temporary_value(d: dict, key: str, value):
    """Temporarily set a key in a dict, then revert to previous value if it had one"""
    missing = object()
    tmp = d.get(key, missing)
    d[key] = value
    yield d
    if tmp is missing:
        del d[key]
    else:
        d[key] = tmp


class Renderer:
    def __init__(self, environment: jinja2.Environment, context: texas.Context, out_dir: Union[str, Path]):
        self.environment = environment
        self._context = context
        self._context_views = ["default", "user"]
        self._out_dir = Path(out_dir).expanduser()

    @property
    def out_dir(self):
        self._out_dir.mkdir(parents=True, exist_ok=True)
        return self._out_dir.resolve()

    @property
    def context(self):
        """read-only.  Modifications not preserved."""
        return self._context.include(*self._context_views).snapshot

    def render(self, name: str, dst_name: str=None, context: dict=None):
        """
        render("style.css", "build/out.css") -> "build/out.css"
        render("hello.html", "output/here.html") -> "output/here.html", "output/_/here.html"
        """
        context = context or self.context
        if dst_name is None:
            dst_name = name

        if name.endswith(".html"):
            with temporary_value(context, "page_filename", str(name)):
                self._render_html(dst_name, context)
        else:
            self._render_asset(name, dst_name, context)

    def _render_html(self, dst_name: str, context: dict):
        # 1. Render to /some/path/dst.html
        tpl = self.environment.get_template("__full.html")
        rendered = tpl.render(context)
        dst = self.out_dir / dst_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rendered, encoding="utf-8")

        # 2. Render to /some/path/_/dst.html
        tpl = self.environment.get_template("__partial.html")
        rendered = tpl.render(context)
        dst = self.out_dir / "_" / dst_name  # type: Path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rendered, encoding="utf-8")

    def _render_asset(self, name: str, dst_name: str, context):
        tpl = self.environment.get_template(name)
        rendered = tpl.render(context)
        dst = self.out_dir / dst_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rendered, encoding="utf-8")
