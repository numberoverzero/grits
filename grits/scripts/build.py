import click
import grits


@click.command("build")
@click.option("--src", required=True, help="source directory")
@click.option("--dst", required=True, help="output directory")
@click.option("--css", required=False, type=str, help="additional css files", multiple=True)
@click.option("--js", required=False, type=str, help="additional js files", multiple=True)
def main(src, dst, css, js):
    ctx = grits.default_context()
    user_ctx = ctx.include("default", "user")
    user_ctx["css_files"].extend(css)
    user_ctx["js_files"].extend(js)
    grits.build(src, dst, ctx)
