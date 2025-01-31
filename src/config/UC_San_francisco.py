def get_config(): return {
  "name": "UC San Francisco",
  "type": "courseleaf",
  "subjectCodesUrl": "https://catalog.ucsf.edu/course-catalog/",
  "selectors": {
      "code": ".detail-code",
      "title": ".detail-title",
      "description": ".courseblockextra:not(.noindent)",
  }
}