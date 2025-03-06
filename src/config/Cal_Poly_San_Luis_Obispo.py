def get_config(): return {
    "name": "Cal Poly San Luis Obispo",
    "type": "courseleaf",
    "subjectCodesUrl": "https://catalog.calpoly.edu/coursesaz/",
    "selectors": {
      "code": ".detail-code",
      "title": ".detail-title",
      "description": ".courseblockextra:not(.noindent)",
  }
}