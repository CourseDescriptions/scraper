def get_config(): return {
  "name": "Fresno State",
  "type": "moderncampus",
  "startUrl": "https://catalog.fresnostate.edu/content.php?catoid=5&navoid=193",
  "selectors": {
      "code": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
          0
      ],
      "title": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
          1
      ],
  }
}