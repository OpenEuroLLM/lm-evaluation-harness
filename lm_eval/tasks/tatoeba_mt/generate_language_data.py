# This file generates a mapping of the language codes present in tatoeba to natural language attributes
# It uses the langcodes and language_data libraries
# This is done ahead of time and committed to git to avoid adding a dep

from langcodes import Language
from utils import load_raw_rows
import json

overrides = {"toki_Latn": "Toki Pona (Latin)", "toki": "Toki Pona"}

# {{src_lang}} luonnollinen nimi kielelle
# {{tgt_lang}} luonnollinen nimi kielelle
# {{tgt_region}} luonnollinen nimi alueelle -> drop
# {{tgt_code}} koodi
# {{input_text}} lähdekielinen teksti


language_tags = {}
for row in load_raw_rows():
    language_tags[row["srclang"]] = None
    language_tags[row["tgtlang"]] = None

for key in language_tags:
    language_tags[key] = overrides.get(key, Language.get(key).display_name())

json.dump(language_tags, open("language_codes.json", "w"))