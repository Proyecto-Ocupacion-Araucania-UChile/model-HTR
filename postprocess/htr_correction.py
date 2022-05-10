import os

import click
from lxml import etree

#contants
current_folder = current_dir = os.path.dirname(os.path.abspath(__file__))
XML_NOCLEAN ="data/xml_no_clean/"
XML_CLEAN ="data/xml_clean/"
punctuation = "!:;\",?’."


@click.command()
def word_parsing():
    for file in os.listdir(os.path.join(current_folder, XML_NOCLEAN)):
        with open(os.path.join(current_folder, XML_NOCLEAN, file), 'r') as f:
            xml = etree.parse(f)
            nsmap = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
            text = xml.xpath("//alto:String/@CONTENT", namespaces=nsmap)
            print("----" + file + "----")
            for line in text:
                #clean lines
                line = line.replace("  ", " ")
                line = line.replace("   ", " ")
                line = line.replace("⁋", "")
                line = line.replace(punct, " ") for punct in punctuation
                #spliting to get words
                word = line.split(' ')
                for n, word in enumerate(word):
                    print(str(n) + " : " + word)

if __name__ == '__main__':
    word_parsing()