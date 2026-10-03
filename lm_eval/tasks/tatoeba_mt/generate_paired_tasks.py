from utils import load_raw_rows

template = """include: ../tatoeba_mt.yaml

task: tatoeba_mt_{}_{}

metadata:
  srclang: {}
  tgtlang: {}"""

eu_official_languages = [
    "bul",
    "hrv",
    "ces",
    "dan",
    "nld",
    "eng",
    "est",
    "fin",
    "fra",
    "deu",
    "ell",
    "hun",
    "gle",
    "ita",
    "lav",
    "lit",
    "mlt",
    "pol",
    "por",
    "ron",
    "slk",
    "slv",
    "spa",
    "swe"
]

missing_eu_official_languages = eu_official_languages[:]

pairs = set()

for row in load_raw_rows():
    pairs.add((row["srclang"], row["tgtlang"]))
    pairs.add((row["tgtlang"], row["srclang"]))

for code_a, code_b in pairs:
    if code_a != code_b:
        with open(f"pairs/tatoeba_mt_{code_a}_{code_b}.yaml", "w") as f:
            f.write(template.format(code_a, code_b, code_a, code_b))

with open("groups/tatoeba_mt_eurollm_langs.yaml", "w") as f:
    f.write("group: tatoeba_mt_eurollm_langs\n")
    f.write("task:\n")
    for code_a, code_b in pairs:
        if code_a != code_b:
            if code_a.split("_")[0] in eu_official_languages and code_b.split("_")[0] in eu_official_languages:
                try:
                    missing_eu_official_languages.remove(code_a.split("_")[0])
                except ValueError:
                    pass
                try:
                    missing_eu_official_languages.remove(code_b.split("_")[0])
                except ValueError:
                    pass
                f.write(f"  - tatoeba_mt_{code_a}_{code_b}\n")


if missing_eu_official_languages != []:
    print(f"WARNING no sentences for languages {missing_eu_official_languages}")
