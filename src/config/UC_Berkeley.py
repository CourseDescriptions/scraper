def get_config(): return {
"name": "UC Berkeley",
        "type": "courseleaf",
        "subjectCodesUrl": "https://guide.berkeley.edu/courses/",
        "selectors": {
            "code": ".courseblocktitle .code",
            "title": ".courseblocktitle .title",
            # Text content from the .descshow element minus the part before the first
            #  <br/> element plus the text from the .deschide element if it exists
            "description": lambda el: (
                descshow := el.select_one(".descshow"),
                descshow.contents[0].extract(),
                descshow.text,
            )[-1]
            + getattr(el.select_one(".deschide"), "text", ""),
        }
}