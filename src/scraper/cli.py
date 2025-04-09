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

    log_level = logging.INFO
    if verbose: log_level = logging.DEBUG 
    if quiet: log_level = logging.CRITICAL
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(markup=False, console=Console(width=180))],
    )


# list all schools with configs
@cli.command()
def list_ids():
    for site_id in SITES:
        print(site_id)


# get logic for a site
def get_logic(site_id: str, limit: int | None = None, noCache: bool = False, id_num: int | None = None):
    # make a cache
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        logging.fatal("Could not create cache directory.")
        raise typer.Abort() from None

    # error if we don't have a config for this site
    if site_id not in SITES:
        logging.fatal('Configuration for site "%s" not found.', site_id)
        raise typer.Abort()

    site_config = SITES[site_id]

    # use specified scraper type on site's config dict
    scraper = site_config["type"](site_config)
    # logging.fatal('Scraper type "%s" not supported.', site_config["type"])
    # raise typer.Abort()

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
    # TODO: add an option to start from specific point in catalog
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
    school_ids = {
        "UC_Berkeley": 0,
        "UC_Davis": 1,
        "UC_Irvine": 2,
        "UCLA": 3,
        "UC_Merced": 4,
        "UC_Riverside": 5,
        "UC_San_Diego": 6,
        "UC_San_Francisco": 7,
        "UC_Santa_Barbara": 8,
        "UC_Santa_Cruz": 9,
        "CSU_Bakersfield": 10,
        "CSU_Channel_Islands": 11,
        "Chico_State": 12,
        "CSU_Dominguez_Hills": 13,
        "CSU_East_Bay": 14,
        "Fresno_State": 15,
        "CSU_Fullerton": 16,
        "Cal_Poly_Humboldt": 17,
        "CSU_Long_Beach": 18,
        "Cal_State_LA": 19,
        "Cal_Maritime": 20,
        "CSU_Monterey_Bay": 21,
        "CSUN": 22,
        "Cal_Poly_Pomona": 23,
        "Sacramento_State": 24,
        "CSU_San_Bernardino": 25,
        "San_Diego_State": 26,
        "San_Francisco_State": 27,
        "San_Jose_State": 28,
        "Cal_Poly_San_Luis_Obispo": 29,
        "CSU_San_Marcos": 30,
        "Sonoma_State": 31,
        "Stanislaus_State": 32,
    }
    for site_id in SITES:
        get_logic(site_id, noCache=noCache, id_num=school_ids[site_id])


if __name__ == "__main__":
    cli()
