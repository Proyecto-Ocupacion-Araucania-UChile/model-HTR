import re, os, click, encodings
from constants import *

#Current path
current_dir = os.path.dirname(os.path.abspath(__file__))

#List regex pattern
superscript_pattern = re.compile(r"\^([A-Za-zÀ-ÖØ-öø-ÿ -])")
correction_read_pattern = re.compile(r"\[\[[A-Za-zÀ-ÖØ-öø-ÿ -]+\|([A-Za-zÀ-ÖØ-öø-ÿ -]+)]]")
correction_pattern = re.compile(r"\[\[([A-Za-zÀ-ÖØ-öø-ÿ -]*)]]")
unreadable_pattern = re.compile(r"-\[([A-z -]*)]-")
borred_pattern = re.compile(r"\*\[([A-Za-zÀ-ÖØ-öø-ÿ -]+])\*")




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
def clean_model_regex():
"""
Function to clean xml files in folder ALTO BRUT with regex to write a cleaned outpout xml
return: xml files cleaned
"""
    clean = os.path.join(current_dir, ALTO_CLEAN)
    for file in os.listdir(os.path.join(current_dir, ALTO_BRUT)):
        with open(os.path.join(current_dir, ALTO_BRUT, file), 'r') as f:
            xml = f.read()
            with open(f"{clean}/{file}", 'w') as write_file:
                try:
                    for n, lines in enumerate(xml.split('\n')):
                        unread = re.search(unreadable_pattern, lines)
                        correction = re.search(correction_pattern, lines)
                        correction_read = re.search(correction_read_pattern, lines)
                        borred = re.search(borred_pattern, lines)
                        superscript = re.search(superscript_pattern, lines)
                        if unread is not None:
                            write_file.write(re.sub(unreadable_pattern, "xxx", lines))
                        elif correction is not None:
                            write_file.write(re.sub(correction_pattern, lambda m: m.group(0), lines))
                        elif correction_read is not None:
                            write_file.write(re.sub(correction_read_pattern, lambda m: m.group(0), lines))
                        elif borred is not None:
                            write_file.write(re.sub(borred_pattern, "xxx", lines))
                        elif superscript is not None:
                            write_file.write(re.sub(superscript_pattern, lambda m: to_superscript(m[1]), lines))
                        else:
                            write_file.write(lines)
                        write_file.write("\n")
                except Exception as erreurs:
                    basename = os.path.basename(os.path.join(current_dir, ALTO_BRUT, file))
                    journal_error(clean, basename, n, erreurs)

if __name__ == '__main__':
    clean_model_regex()
