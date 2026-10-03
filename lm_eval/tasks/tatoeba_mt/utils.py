import code
from datasets import load_dataset, Dataset
from collections import defaultdict
from tqdm.auto import tqdm
import json
import pathlib

# args: (); kwargs: {'version': 1, 'dataset_dir': 'Helsinki-NLP/tatoeba_mt', 'split': 'test', 'config_source': '/Users/theo/git/lm-evaluation-harness-local/lm-evaluation-harness/lm_eval/tasks/tatoeba/tatoeba.yaml'}

# {{src_lang}} luonnollinen nimi kielelle
# {{tgt_lang}} luonnollinen nimi kielelle
# {{tgt_region}} luonnollinen nimi alueelle
# {{tgt_code}} koodi
# {{input_text}} lähdekielinen teksti

def load_raw_rows():
    """Load rows from tatoeba test set & make simple dictionaries semilosslessly"""
    ds = load_dataset("webdataset", data_files={"test": "https://object.pouta.csc.fi/Tatoeba-Challenge-devtest/test-v2023-09-26.tar"}, split="test")
    #print(ds)
    texts = []
    for row in tqdm(ds):
        if row["__key__"].endswith("README"): # We don't want to interpret the readme as actual data
            continue
        for text in row["txt"].strip("\n").split("\n"):
            srclang, tgtlang, srctext, tgttext = text.split("\t")
            texts.append({"srclang": srclang, "tgtlang": tgtlang, "srctext": srctext, "tgttext": tgttext})
    return texts

def load_tatoeba(*args, **kwargs):
    """Load the tatoeba data in a format compatible with the harness, incl. language codes"""
    texts = []
    code_mapping = json.load(open(
pathlib.Path(__file__).parent.resolve().joinpath("language_codes.json")))
    print(code_mapping)
    for text in load_raw_rows():
        if text["srclang"] == kwargs["srclang"] and text["tgtlang"] == kwargs["tgtlang"]:
            texts.append({"src_lang": code_mapping[text["srclang"]],
                            "tgt_lang": code_mapping[text["tgtlang"]],
                            "tgt_code": text["tgtlang"],
                            "input_text": text["srctext"],
                            "target_text": text["tgttext"]})
        elif text["srclang"] == kwargs["tgtlang"] and text["tgtlang"] == kwargs["srclang"]:
            texts.append({"src_lang": code_mapping[text["tgtlang"]],
                            "tgt_lang": code_mapping[text["srclang"]],
                            "tgt_code": text["srclang"],
                            "input_text": text["tgttext"],
                            "target_text": text["srctext"]})
    return {"test": Dataset.from_list(texts)}
