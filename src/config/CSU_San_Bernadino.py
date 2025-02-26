def get_config(): return {
  "name": "CSU San Bernadino",
  "type": "courseleaf",
  "subjectCodesUrl": "https://catalog.csusb.edu/coursesaz/",
  "selectors": {
      "code": ".detail-code",
      "title": ".detail-title",
      "description": ".courseblockextra:not(.noindent)",
  }
}