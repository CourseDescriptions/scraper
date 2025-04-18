#!/usr/bin/env python3

"""Course Descriptions Scraper -- CLI entrypoint."""

__version__ = "0.1"

import json
import logging
import sys
from pathlib import Path
import os
from datetime import datetime

import typer
from rich import print
from rich.console import Console
from rich.logging import RichHandler

CACHE_DIR = Path(__file__).parent.parent.parent / "cache"
from config import SITES

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

    # setup logging
    # Create a root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Console handler: info by default, or user specified
    log_level = logging.INFO
    if verbose: log_level = logging.DEBUG 
    if quiet: log_level = logging.CRITICAL
    rich_handler = RichHandler(
        markup=False,
        console=Console(width=180),
        show_time=True,
        show_level=True,
        show_path=True
    )
    rich_handler.setLevel(log_level)

    # File handler: only errors and above
    file_handler = logging.FileHandler('errors.log')
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(rich_handler)
    logger.addHandler(file_handler)


# list all schools with configs
@cli.command()
def list_ids():
    for site_id in SITES:
        print(site_id)


# logic for saving a catalog
def get_logic(site_id: str, limit: int | None = None, noCache: bool = False, id_num: int | None = None):
    logger = logging.getLogger(__name__)
    # make a cache
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.fatal("Could not create cache directory.")
        raise typer.Abort() from None

    # error if we don't have a config for this site
    if site_id not in SITES:
        logger.fatal('Configuration for site "%s" not found.', site_id)
        raise typer.Abort()

    # TODO: check if SITES is loading every single scraper multiple times?
    site_config = SITES[site_id]

    # use specified scraper type on site's config dict
    scraper = site_config["type"](site_config)

    # scrape the data (use flip of noCache as useCache arg)
    data = scraper.get(not noCache, limit)
    if id_num != None:
        for course in data:
            course.update({"school_id": id_num})

    # dump the data to the console
    json.dump(data, indent=2, fp=sys.stdout)

    # make a dir to dump jsons to
    try:
        os.mkdir("data")
    except FileExistsError:
        pass
    # make a dir to dump specifically this school to
    try:
        os.mkdir(f"data/{site_id}")
    except FileExistsError:
        pass

    # dump the json, prepend current time of scraping
    now = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    with open(f"data/{site_id}/{now}.json", "w+") as f:
        json.dump(data, f)


# command to scrape data from a specific school
@cli.command()
def get(
    site_id: str = typer.Argument(
        help="The ID of the site to scrape (e.g. UC_Davis, UC_Berkeley)"
    ),
    limit: int | None = typer.Option(
        None,
        "--limit",
        "-l",
        help="""
        Limit the number of results (for testing -- exact meaning is dependent on scraper backend)
        """.strip(),
    ),
    noCache: bool = typer.Option(
        False,
        "--no-cache",
        "-nc",
        help="""
        Ignore cache to force refetching from the website
        """.strip(),
        is_flag=True,
    ),
    id_num: int = typer.Option(
        None,
        "--id",
        "-id",
        help="""
        Add an id field to each course's output JSON
        """.strip(),
    ),
):
    get_logic(site_id, limit, noCache, id_num)
    

@cli.command()
def get_all(noCache: bool = typer.Option(
        False,
        "--no-cache",
        "-nc",
        help="""
        Ignore cache to force refetching from the website
        """.strip(),
        is_flag=True,
    ),
):
    with open("school_ids.txt") as f:
        school_ids = f.readlines()
    school_ids = {line.split(",")[1].rstrip(): line.split(",")[0].rstrip() for line in school_ids}

    print(school_ids)

    for site_id in SITES:
        get_logic(site_id, noCache=noCache, id_num=school_ids[site_id])


if __name__ == "__main__":
    cli()
