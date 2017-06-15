import bs4
from collections import ChainMap
import jinja2
import shutil
from pathlib import Path
from typing import MutableMapping, Mapping, Union

DEFAULT_MAPP_OUTPUT_PATH = "/static/mapp.min.js"

binary_suffixes = {
    "." + suffix
    for suffix in "gif img ico jpeg jpg png".split()
    if suffix.strip()  # guard against extra spaces
}


def default_is_binary(filename):
    """Used to tell the renderer which files to skip"""
    return Path(filename).suffix in binary_suffixes


def safe_context(context: Mapping=None) -> ChainMap:
    return ChainMap({}, (context or {}))


def extract_head(soup: bs4.BeautifulSoup, context: MutableMapping) -> None:
    head = None
    head_sections = soup.find_all("head")
    if head_sections:
        if len(head_sections) > 1:
            raise ValueError("html must have at most 1 <head> section.")
        head = head_sections[0].renderContents().decode("utf-8")
    context.setdefault("head", head)


def extract_main(soup: bs4.BeautifulSoup, context: MutableMapping) -> None:
    main_sections = soup.find_all("main")
    if len(main_sections) != 1:
        raise ValueError("html must have exactly 1 <main> section.")
    main = main_sections[0]
    context.setdefault("main", main.renderContents().decode("utf-8"))


def prettify_html(rendered: str) -> str:
    return bs4.BeautifulSoup(rendered, "html.parser").prettify()


def extract_scripts(soup: bs4.BeautifulSoup, context: MutableMapping) -> None:
    # Find top-level only, don't grab scripts in main twice
    scripts = soup.find_all("script", recursive=False)
    scripts = "\n".join((element.prettify()) for element in scripts)
    context.setdefault("scripts", scripts)


class Renderer:
    def __init__(self, environment: jinja2.Environment, src_dir: Union[str, Path], out_dir: Union[str, Path]) -> None:
        self.environment = environment
        self.src_dir = Path(src_dir).expanduser()
        self.out_dir = Path(out_dir).expanduser()
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def render_scaffolding(self, context: Mapping=None) -> None:
        """Required files to ensure mapp functions properly"""
        context = safe_context(context)
        self.render_template(name="_dynamicRoutes.json", context=context)
        self.render_template(name="_prefetchManifest.json", context=context)
        self.render_template(name="static/vendor/mapp.min.js", out_path="static/js/mapp.min.js", context=context)

    def render_template(self, name: str, out_path: Union[str, Path]=None, context: Mapping=None) -> None:
        if out_path is None:
            out_path = name
        context = safe_context(context)

        template = self.environment.get_template(name)
        rendered = template.render(context)

        # fix templating ugliness
        if name.endswith(".html"):
            rendered = prettify_html(rendered)

        dst = self.out_dir / out_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rendered, encoding="utf-8")

    def render_html(self, src_path: Union[str, Path], context: Mapping=None) -> None:
        src_path = Path(src_path).expanduser()
        out_path = src_path.relative_to(self.src_dir)

        context = safe_context(context)
        original = Path(src_path).expanduser().read_text(encoding="utf-8")
        soup = bs4.BeautifulSoup(original, "html.parser")
        try:
            extract_head(soup, context)
            extract_main(soup, context)
            extract_scripts(soup, context)
        except ValueError as error:
            raise ValueError(f"While parsing '{str(src_path)}', encountered an error:") from error

        self.render_template(name="__partial.html", out_path=Path("_") / out_path, context=context)
        self.render_template(name="__full.html", out_path=out_path, context=context)

    def render_asset(self, src_path: Union[str, Path], out_path: Union[str, Path]=None):
        src_path = Path(src_path).expanduser()
        if out_path:
            out_path = Path(out_path).expanduser()
        else:
            out_path = src_path.relative_to(self.src_dir)
        dst = self.out_dir / out_path
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy(str(src_path), str(dst))

    def process(self, context: Mapping=None) -> None:
        self.render_scaffolding(context=context)
        for src_path in self.src_dir.glob("**/*"):
            if src_path.is_dir():
                continue
            if src_path.suffix == ".html":
                self.render_html(src_path=src_path, context=context)
            else:
                self.render_asset(src_path=src_path)
