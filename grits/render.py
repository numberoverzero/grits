import jinja2
import texas
import shutil

from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union

binary_suffixes = {
    "." + suffix
    for suffix in "gif img ico jpeg jpg png".split()
    if suffix.strip()  # guard against extra spaces
}


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


def default_is_binary(filename):
    """Used to tell the renderer which files to skip"""
    return Path(filename).suffix in binary_suffixes


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

    def render(self, name: str, dst_name: str=None, src_dir: Optional[Path]=None, context: dict=None):
        """
        render("style.css", "build/out.css") -> "build/out.css"
        render("hello.html", "output/here.html") -> "output/here.html", "output/_/here.html"
        """
        print(f"rendering {name} {src_dir}")
        context = context or self.context
        if dst_name is None:
            dst_name = name

        is_binary = context.get("is_binary", default_is_binary)
        if is_binary(name):
            name = str(src_dir / name)
            self._render_binary(name, dst_name, context)
        elif name.endswith(".html"):
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

    def _render_binary(self, name: str, dst_name: str, context):
        dst = self.out_dir / dst_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(name, str(dst))
