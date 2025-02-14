def get_config(): return {
    "name": "CSU Chico",
    "type": "courseleaf",
    "subjectCodesUrl": "https://catalog.csuchico.edu/courses/",
    "selectors": {
        "code": ".detail-code",
        "title": ".detail-title",
        "description": ".detail-description",
    }
}