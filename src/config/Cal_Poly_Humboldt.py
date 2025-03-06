from scraper.moderncampus import ModernCampusScraper

def get_config(): return {
  "name": "Cal Poly Humboldt",
  "type": ModernCampusScraper,
  "startUrl": "https://catalog.humboldt.edu/content.php?catoid=10&navoid=1555",
  "selectors": {
      "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
          0
      ],
      "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
          1
      ],
  }
}