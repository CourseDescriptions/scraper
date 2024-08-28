#!/usr/bin/env python3

"""Course Descriptions Scraper -- CLI entrypoint."""

__version__ = "0.1"

import logging

import typer
from rich import print
from rich.console import Console
from rich.logging import RichHandler

from scraper.config import SITES
from scraper.squares import SquaresScraper

cli = typer.Typer(add_completion=False, no_args_is_help=True)


@cli.callback()
def common_options(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
    version: bool = typer.Option(False, "--version"),
):
    """Common options:"""

    if version:
        print(__version__)
        raise SystemExit

    log_level = logging.DEBUG if verbose else logging.INFO
    log_level = logging.CRITICAL if quiet else log_level
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(markup=False, console=Console(width=180))],
    )


@cli.command()
def get(
    site_id: str = typer.Argument(
        help="The ID of the site to scrape (e.g. UC_Davis, UC_Berkeley)"
    ),
):
    if site_id not in SITES:
        logging.fatal('Configuration for site "%s" not found.', site_id)
        raise typer.Abort()

    site_config = SITES[site_id]

    scraper = SquaresScraper(site_config)
    scraper.get()


if __name__ == "__main__":
    cli()
