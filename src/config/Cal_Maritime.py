def get_config(): return {
  "name": "Cal Poly Humboldt",
  "type": "moderncampus",
  "startUrl": "http://catalog.csum.edu/content.php?catoid=13&navoid=912",
  "selectors": {
      "code": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
          0
      ],
      "title": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
          1
      ],
  }
}