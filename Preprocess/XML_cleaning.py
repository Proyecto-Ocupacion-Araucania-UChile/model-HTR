import re, os, click
from lxml import etree

#Current path
current_dir = os.path.dirname(os.path.abspath(__file__))

#List regex pattern
superscript_pattern = re.compile(r"\^([A-Za-zÀ-ÖØ-öø-ÿ -])")
correction_read_pattern = re.compile(r"\[\[[A-Za-zÀ-ÖØ-öø-ÿ -]+\|([A-Za-zÀ-ÖØ-öø-ÿ -]+)]]")
correction_pattern = re.compile(r"\[\[([A-Za-zÀ-ÖØ-öø-ÿ -]*)]]")
unreadable_pattern = re.compile(r"-\[([A-z -]*)]-")
borred_pattern = re.compile(r"\*\[([A-Za-zÀ-ÖØ-öø-ÿ -]+])\*")

#Constantes
ALTO_BRUT = "no_clean"
ALTO_CLEAN = "clean_regex"




def to_superscript(num):
    """
    Function to convert character in superscript
    :num: str, data to transform
    :return:str, transform
    """
    transl = str.maketrans(dict(zip('abcdefghijklmnopqrstuvwxyz1234567890', 'ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹⁰')))
    return num.translate(transl)

def journal_error(path, file, n, type):
    """
    Transcribe a journal error with informations

    :param path: Str, better tu use os library
    :param file: Str, filename
    :param n: Int, line number of error
    :param type: Str, text to describe the error
    :return: None
    """
    if os.path.isfile(f"{path}/errors.txt"):
        with open(f"{path}/error.txt", "a") as f:
            f.write(f"error: {file}, l.{n} -> {type}")
            f.write("\n")
    else:
        with open(f"{path}/error.txt", "a") as f:
            f.write(f"error: {file}, l.{n} -> {type}")
            f.write("\n")

@click.command()
@click.option("-s", "--superscript", "superscript", is_flag=True, show_default=True, default=False, help="To transform superscript characters")
@click.option("-t", "--txt", "txt", is_flag=True, show_default=True, default=False, help="To scribe and clean text files")
def clean_model_regex(txt, superscript):
    """
    Function to clean xml or scribe and clean txt files in folder ALTO BRUT with regex to write a cleaned outpout xml/txt
    return: xml/txt files cleaned
    """
    clean = os.path.join(current_dir, ALTO_CLEAN)
    for file in os.listdir(os.path.join(current_dir, ALTO_BRUT)):
        if not file.endswith(".md"):
            with open(os.path.join(current_dir, ALTO_BRUT, file), 'r') as f:
                if txt:
                    file = file.replace(".xml", ".txt")
                    xml = etree.parse(f)
                    ns = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
                    text = xml.xpath("//alto:String/@CONTENT", namespaces=ns)
                    with open(f"{clean}/{file}", 'w') as write_file:
                        try:
                            for n, lines in enumerate(text):
                                lines = lines.replace("⁋", "")
                                unread = re.search(unreadable_pattern, lines)
                                correction = re.search(correction_pattern, lines)
                                correction_read = re.search(correction_read_pattern, lines)
                                borred = re.search(borred_pattern, lines)
                                if unread is not None:
                                    lines = re.sub(unreadable_pattern, "xxx", lines)
                                if correction is not None:
                                    lines = re.sub(correction_pattern, lambda m: m.group(1), lines)
                                if correction_read is not None:
                                    lines = re.sub(correction_read_pattern, (lambda m: m.group(1)), lines)
                                if borred is not None:
                                    lines = re.sub(borred_pattern, "xxx", lines)
                                if superscript:
                                    superscript_src = re.search(superscript_pattern, lines)
                                    if superscript_src is not None:
                                        lines = re.sub(superscript_pattern, lambda m: to_superscript(m[1]), lines)
                                write_file.write(lines)
                                write_file.write("\n")
                        except Exception as erreurs:
                            basename = os.path.basename(os.path.join(current_dir, ALTO_BRUT, file))
                            journal_error(clean, basename, n, erreurs)

                else:
                    xml = f.read()
                    with open(f"{clean}/{file}", 'w') as write_file:
                        try:
                            for n, lines in enumerate(xml.split('\n')):
                                unread = re.search(unreadable_pattern, lines)
                                correction = re.search(correction_pattern, lines)
                                correction_read = re.search(correction_read_pattern, lines)
                                borred = re.search(borred_pattern, lines)
                                if unread is not None:
                                    lines = re.sub(unreadable_pattern, "xxx", lines)
                                if correction is not None:
                                    lines = re.sub(correction_pattern, lambda m: m.group(1), lines)
                                if correction_read is not None:
                                    lines = re.sub(correction_read_pattern, (lambda m: m.group(1)), lines)
                                if borred is not None:
                                    lines = re.sub(borred_pattern, "xxx", lines)
                                if superscript:
                                    superscript_src = re.search(superscript_pattern, lines)
                                    if superscript_src is not None:
                                        lines = re.sub(superscript_pattern, lambda m: to_superscript(m[1]), lines)
                                write_file.write(lines)
                                write_file.write("\n")
                        except Exception as erreurs:
                            basename = os.path.basename(os.path.join(current_dir, ALTO_BRUT, file))
                            journal_error(clean, basename, n, erreurs)


if __name__ == '__main__':
    clean_model_regex()
