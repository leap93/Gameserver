import json
from app.models import LANGUAGES


def get_translations(language):
    #check if language is supported
    supported = False
    for supported_language in LANGUAGES:
        if supported_language[0] == language:
            supported = True
            break
    if not supported:
        language = "en"

    #open the file
    data = open('app/static/translations.json').read()
    json_data = json.loads(data)
    translations = {}
    #filter translations for the language
    for data in json_data:
        if data['language'] == language:
            translations[data["title"]] = data["content"]
    return translations