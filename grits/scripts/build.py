import click
import grits
existing_directory = click.Path(exists=True, dir_okay=True, file_okay=False)
directory = click.Path(exists=False, dir_okay=True, file_okay=False)


@click.command("build")
@click.option("--src", required=True, type=existing_directory, help="source directory")
@click.option("--dst", required=True, type=directory, help="output directory")
@click.option("--tpl", required=False, type=directory, help="templates directory")
def main(src, dst, tpl):
    grits.build(src_dir=src, out_dir=dst, template_dir=tpl)
