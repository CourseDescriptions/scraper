def get_config(): return {
  "name": "CSU San Bernadino",
  "type": "courseleaf",
  "subjectCodesUrl": "https://catalog.csusb.edu/coursesaz/",
  "selectors": {
      "code": lambda el: el.select_one(".coursetitle").text.split(". ")[0],
      "title": lambda el: el.select_one(".coursetitle").text.split(". ")[1],
      "description": lambda el: el.select_one(".courseblockdesc").text,
      # "description": lambda el: "".join([line for line in el.select_one(".courseblockdesc").get_text(strip=True, separator="\n").splitlines()
      #                            if "Prerequisite:" not in line and "Corequisite:" not in line]),
  }
}