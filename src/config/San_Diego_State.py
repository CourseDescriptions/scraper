import logging

def get_desc(el):
    # Find the course title
    title = el.select_one("#course_preview_title")

    # # Find the next non-empty sibling (if it's an empty <strong> tag, skip it)
    # siblings = title.find_all_next("strong")

    # # Find the first sibling with text after an empty <strong> tag
    # for strong in siblings:
    #     if not strong.get_text(strip=True):
    #         print(strong.text)
    #         print(strong.find_next_sibling())

    # Find the next empty <strong> and get the text that follows
    texts = []
    for child in title.parent.contents:
        text = child.text.strip()
        # if len(text) == 0: continue
        # if "Print-Friendly Page" in text: continue
        # if "Units:" in text: continue
        # if "Minimum grade of C" in text: continue
        # if "Proof of completion of prerequisite(s) required: Copy of transcript." in text: continue
        # if "LCR:" in text: continue
        # if "Grading Method:" in text: continue
        # if "Prerequisite(s):" in text: continue
        # if "Formerly numbered" in text: continue
        # if "Note:" in text: continue
        # if "Maximum credits:" in text: continue
        texts.append(text)
    # get rid of everything before prereqs > grading method > units
    if "Prerequisite(s):" in texts:
        texts = texts[texts.index("Prerequisite(s):")+1 : ]
    elif "Grading Method:" in texts:
        texts = texts[texts.index("Grading Method:")+1 : ]
    elif "Units:" in texts:
        texts = texts[texts.index("Units:")+1 : ]
    # TODO: clip til after first instance of a double (triple?) break

    # get rid of everything after formerly numbered > maximum credits > note (maybe unecessary)
    if "May be repeated with new content." in texts:
        texts = texts[ : texts.index("May be repeated with new content.")]
    elif "Formerly numbered" in texts:
        texts = texts[ : texts.index("Formerly numbered")]
    elif "Maximum Credits:" in texts:
        texts = texts[ : texts.index("Maximum Credits:")]
    elif "Note:" in texts:
        texts = texts[ : texts.index("Note:")]

    # get first instance of sublist ['', '', ''] which seems consistent?
    target = ['', '', '']

    res = -1 # boolean variable 
    for idx in range(len(texts) - len(target) + 1):
        if texts[idx: idx + len(target)] == target:
            res = idx
            break
    # get first instance of actual text after target sublist
    if res == -1:
        logging.error("Could not find target sublist when looking for course description")
        return ""
    
    # slice off empty target
    texts = texts[idx + len(target): ]
    # join everything not empty (might get too much but better than too little!)
    return "\n".join([text for text in texts if text != ""])

def get_config(): return {
    "name": "San Diego State",
    "type": "moderncampus",
    "startUrl": "https://catalog.sdsu.edu/content.php?catoid=9&navoid=776",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ],
        "description": lambda el: get_desc(el)
        
    }
}