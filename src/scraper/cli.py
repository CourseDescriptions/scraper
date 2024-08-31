#!/usr/bin/env python3

"""Course Descriptions Scraper -- CLI entrypoint."""

__version__ = "0.1"

import json
import logging
import sys

import typer
from rich import print
from rich.console import Console
from rich.logging import RichHandler

from scraper.config import CACHE_DIR, SITES
from scraper.moderncampus import ModernCampusScraper
from scraper.courseleaf import CourseLeafScraper
from scraper.ucla import UclaScraper

cli = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_show_locals=False
)


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
def list_ids():
    for site_id in SITES:
        print(site_id)


@cli.command()
def get(
    site_id: str = typer.Argument(
        help="The ID of the site to scrape (e.g. UC_Davis, UC_Berkeley)"
    ),
):
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        logging.fatal("Could not create cache directory.")
        raise typer.Abort() from None

    if site_id not in SITES:
        logging.fatal('Configuration for site "%s" not found.', site_id)
        raise typer.Abort()

    site_config = SITES[site_id]

    if site_config["type"] == "courseleaf":
        scraper = CourseLeafScraper(site_config)
    elif site_config["type"] == "moderncampus":
        scraper = ModernCampusScraper(site_config)
    elif site_config["type"] == "ucla":
        scraper = UclaScraper(site_config)
    else:
        logging.fatal('Scraper type "%s" not supported.', site_config["type"])
        raise typer.Abort()

    data = scraper.get()

    json.dump(data, indent=2, fp=sys.stdout)


if __name__ == "__main__":
    cli()
