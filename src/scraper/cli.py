#!/usr/bin/env python3

"""Course Descriptions Scraper -- CLI entrypoint."""

__version__ = "0.1"

import json
import logging
import sys
from pathlib import Path
from datetime import datetime

import typer
from rich import print
from rich.console import Console
from rich.logging import RichHandler

from config import SITES

SCRAPER_ROOT_DIR = Path(__file__).parent.parent.parent

LOG_DIR = SCRAPER_ROOT_DIR / "logs"
DATA_DIR = SCRAPER_ROOT_DIR / "data"
CACHE_DIR = SCRAPER_ROOT_DIR / "cache"

cli = typer.Typer(
    add_completion=False, no_args_is_help=True, pretty_exceptions_show_locals=False
)
    
@cli.callback()
def common_options(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
    logAll: bool = typer.Option(False, "--log-all", "-la"),
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
    # make logging directory if doesn't exist
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.fatal("Could not create log directory.")
        raise typer.Abort() from None
    now = datetime.now().strftime("%Y-%m-%d_%H:%M")
    file_handler = logging.FileHandler(f"logs/{now}{"_errors" if not logAll else ""}.log")
    file_log_level = logging.DEBUG if logAll else logging.WARNING
    file_handler.setLevel(file_log_level)
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
def get_logic(site_id: str, limit: int | None = None, noCache: bool = False, id_num: int | None = None, user: str | None = None):
    logger = logging.getLogger(__name__)
    # make a cache
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.fatal("Could not create cache directory.")
        raise typer.Abort()

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

    # construct json with data and metadata
    now = datetime.now().strftime("%Y-%m-%d_%H:%M")
    output = {
        "data": data,
        "metadata": {
            "run_datetime": now,
            "config_author": site_config["author"] if "author" in site_config else "unknown",
            "scraper_author": scraper.get_author(),
            "run_by": user if user else "unknown"
        }
    }

    # dump the output to the console
    json.dump(output, indent=2, fp=sys.stdout)

    # make a dir to dump jsons for this school to
    site_data_dir = DATA_DIR / site_id
    try:
        # parents true so will make data/ if need be, exist_ok true cause might already exist
        site_data_dir.mkdir(parents=True, exist_ok=True) 
    except FileExistsError:
        logger.fatal(f"Could not create {site_data_dir} directory.")

    # dump the json, prepend current time of scraping
    with open(f"data/{site_id}/{now}.json", "w+") as f:
        json.dump(output, f)


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
    user: str = typer.Option(
        None,
        "--user",
        "-u",
        help="""
        Specify user running the scraper to include metadata in output JSON
        """.strip(),
    ),
):
    get_logic(site_id, limit, noCache, id_num, user)
    

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
    user: str = typer.Option(
        None,
        "--user",
        "-u",
        help="""
        Specify user running the scraper to include metadata in output JSON
        """.strip(),
    ),
):
    logger = logging.getLogger(__name__)
    
    with open("school_ids.txt") as f:
        school_ids = f.readlines()
    school_ids = {line.split(",")[1].rstrip(): line.split(",")[0].rstrip() for line in school_ids}

    for site_id in SITES:
        try:
            get_logic(site_id, noCache=noCache, id_num=int(school_ids[site_id]), user=user)
        except Exception as e:
            logger.fatal(f"Encountered exception while trying to scrape {site_id}, continuing", exc_info=True)
            continue


if __name__ == "__main__":
    cli()
