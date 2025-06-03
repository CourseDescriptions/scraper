from scraper.moderncampus import ModernCampusScraper, extract
from scraper.common import normalize_text

def extract_desc_rough(el):
  start = el.select_one("hr + strong ~ br")

  text = []
  for sibling in start.next_siblings:
    if sibling.name == "br":
      break
    text.append(sibling.text.strip())

  return normalize_text("\n".join(text))

def get_config(): return {
  "name": "Cal Poly Pomona",
  "type": ModernCampusScraper,
  "startUrl": "https://catalog.cpp.edu/content.php?catoid=68&navoid=5731",
  "selectors": {
      "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
          0
      ],
      "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
          1
      ],
      "description": lambda el: extract_desc_rough(el) if el.select_one("hr + strong") else extract(el)
  },
  "author": "Rohan Parekh"
}