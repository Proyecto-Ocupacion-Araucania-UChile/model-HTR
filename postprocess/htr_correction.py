import os
import json

import spacy
import click
from lxml import etree
from spellchecker import SpellChecker

#contants
current_folder = current_dir = os.path.dirname(os.path.abspath(__file__))
XML_NOCLEAN ="data/xml_no_clean/"
XML_CLEAN ="data/xml_clean/"
punctuation = "!:;\",?’."

nlp = spacy.load("es_core_news_md")
spell = SpellChecker(language='es', case_sensitive=True, distance=2)


@click.command()
def word_parsing():

    """
    https://github.com/Anatole-DC/learning_english/blob/master/server/analyses.py
    https://github.com/ElkheirT/Data-Science-Final-Project/blob/main/main.py
    https://github.com/ElkheirT/Data-Science-Final-Project/blob/main/SpellCheck.py
    https://spacy.io/models/es
    https://github.com/andresdtobar/text_classification_GRUNet/blob/main/dictionary_construction.ipynb
    :return:
    """

    dict_files = {}
    list_files = []

    for file in os.listdir(os.path.join(current_folder, XML_NOCLEAN)):
        with open(os.path.join(current_folder, XML_NOCLEAN, file), 'r') as f:
            xml = etree.parse(f)
            nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
            text = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
            print("----" + file + "----")
            for n_line, line in enumerate(text):
                doc = nlp(str(line))
                words = [token.text for token in doc]
                print(words)





                """analyses = [
                    {
                        "word": str(token),
                        "type": str(token.pos_),
                        "corrected": spell.correction(str(token)) if spell.correction(str(token)) != str(
                            token) else None,
                        "suggestions": [sugg for sugg in spell.candidates(str(token))][:-1]
                    }
                    for token in doc
                ]

                dict_files[n_line] = analyses
                list_files.append(dict_files)
            with open(f"dict/{file}.json", mode="a") as f:
                json.dump(list_files, f, indent=3, ensure_ascii=False)"""







                """#clean lines
                line = line.replace("  ", " ")
                line = line.replace("   ", " ")
                line = line.replace("⁋", "")
                for punct in punctuation:
                    line = line.replace(punct, " ")
                #spliting to get words
                word = line.split(' ')
                ligne = [token.text for token in doc]"""

if __name__ == '__main__':
    word_parsing()