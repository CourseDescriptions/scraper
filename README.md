# Course Descriptions Scraper(s)


Project is managed with [uv](https://docs.astral.sh/uv/); use

```sh
% uv run src/scraper/cli.py --help

 Usage: cli.py [OPTIONS] COMMAND [ARGS]...

 Common options:

╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
│ --verbose                                                                                 │
│ --quiet                                                                                   │
│ --version                                                                                 │
│ --help               Show this message and exit.                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────╮
│ get                                                                                       │
│ list-ids                                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```


# How to write a config file !

To scrape a school, there must be a .py file for that school in the src/config folder. That's the folder that is checked when listing all the schools that can be scraped, and that's where it checks when asked to scrape a specific school.

The name of a config file should be Name_of_School.py - this matters because the name of the file is how the logic identifies which scraper is for which school - it's the name it'll show up as when cli.py list-ids is run, and its name is the parameter that needs to be passed when running `$uv run src/scraper/cli.py get`

The format of a config file can vary but the key part is creating a function called get_config. It should take no arguments and return a dictionary. An example config file might look like this:

```
"""
Filename - Cal_Poly_Humboldt.py
Written by Rohan Parekh, 5/12/2025
"""
from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
  "name": "Cal Poly Humboldt",
  "type": ModernCampusScraper,
  "startUrl": "https://catalog.humboldt.edu/content.php?catoid=10&navoid=1555",
  "selectors": {
      "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[0],
      "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[1],
  }
}
```

The dictionary should always have a name field, with the value being the name of the school.

The dictionary must have a type - this determines the class of scraper that will be used for the catalog. This is useful for schools that have similarly structured catalogs, often because they have the same provider. In this case, Cal Poly Humboldt's catalog follows the ModernCampus format, so we specify that scraper type. The type of the scraper informs what other key/value pairs must be in the dictionary (you can find the specifics in the __init__ for each scraper class in the src/scraper directory).

## Determining scraper type

To determine if a catalog fits in one of the existing types, there are a few things to check. First you need to click around and find the main listing page of the catalog. Keep an eye out for pages that look like they match other existing ModernCampus or Courseleaf pages

You can also look at the url of a page
- ModernCampus catalogs always contains a path that looks something like "/content.php?catoid=12&navoid=1976" 
- Courseleaf catalog home pages tend to have a simple path like "/courses" or "/all-courses" or "/course-descriptions" but it's inconsistent

You can look at the format of a page
- ModernCampus catalog home format is a list of all courses organized by department with multiple pages and clickable page numbers at the bottom
- Courseleaf format has a list of departments and a row of tiles to navigate alphabetically

But it's always the case that it could be neither and it needs a custom type of scraper. In this case you should define a new class in the config file and use that. (Look at UC_Santa_Barbara.py or UC_Santa_Cruz.py in src/config for examples of this)

## Creating selectors

For both ModernCampus and Courseleaf, the config needs to specify css selectors to extract the correct text from the page for each course. To figure out what selectors to use, open up a few of the target catalog's courses in a browser. Use inspect element to take a look at the structure of the html. If the code, title, and description are all split up into their own individual, identifiable elements, you can just specify a string that selects for that element. If it requires more processing (e.g. the code and the title are in the same element and need to be split up), you can use a lambda function that takes in the soup of the page and returns the string of the correct element. That would look something like `"code": lambda el: el.select_one("#course_preview_title").text.split(": ")[0]` in order to get the right element and split off the part before the colon. If you don't know how lambda functions work that's fine, basically the `lambda el` just means it takes one argument, `el` (the scraper should always pass the soup of the course as that argument). Then the function returns the value after the colon. So in this case we select the first element with id "course_preview_title", and we get the text before the first colon.

