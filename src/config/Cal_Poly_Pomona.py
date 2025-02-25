def get_config(): return {
  "name": "Cal Poly Humboldt",
  "type": "moderncampus",
  "startUrl": "https://catalog.cpp.edu/content.php?catoid=68&navoid=5731",
  "selectors": {
      "code": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
          0
      ],
      "title": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
          1
      ],
  }
}