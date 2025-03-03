def get_config(): return {
  "name": "CSU San Bernadino",
  "type": "courseleaf",
  "subjectCodesUrl": "https://catalog.csusb.edu/coursesaz/",
  "selectors": {
      "code": lambda el: el.select_one(".coursetitle").text.split(". ")[0],
      "title": lambda el: el.select_one(".coursetitle").text.split(". ")[1],
      "description": ".courseblockdesc",
  }
}