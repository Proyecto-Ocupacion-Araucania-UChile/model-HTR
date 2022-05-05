import re, os, click, encodings
from constants import *

#Dict superscript
superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

#Current path
current_dir = os.path.dirname(os.path.abspath(__file__))

#List regex pattern
superscript_pattern = re.compile(r"\^([A-Za-zÀ-ÖØ-öø-ÿ -])")
correction_read_pattern = re.compile(r"\[\[[A-Za-zÀ-ÖØ-öø-ÿ -]+\|([A-Za-zÀ-ÖØ-öø-ÿ -]+)]]")
correction_pattern = re.compile(r"\[\[([A-Za-zÀ-ÖØ-öø-ÿ -]*)]]")
unreadable_pattern = re.compile(r"-\[([A-z -]*)]-")
borred_pattern = re.compile(r"\*\[([A-Za-zÀ-ÖØ-öø-ÿ -]+])\*")

@click.command()
def clean_model_regex():
    clean = os.path.join(current_dir, ALTO_CLEAN)
    for file in os.listdir(os.path.join(current_dir, ALTO_BRUT)):
        with open(os.path.join(current_dir, ALTO_BRUT, file), 'r') as f:
            xml = f.read()
            with open(f"{clean}/{file}", 'w') as write_file:
                for n, lines in enumerate(xml.split('\n')):
                    unread = re.search(unreadable_pattern, lines)
                    correction = re.search(correction_pattern, lines)
                    correction_read = re.search(correction_read_pattern, lines)
                    borred = re.search(borred_pattern, lines)
                    if unread is not None:
                        write_file.write(re.sub(unreadable_pattern, "xxx", lines))
                    elif correction is not None:
                        write_file.write(re.sub(correction_pattern, "\\1", lines))
                    elif correction_read is not None:
                        write_file.write(re.sub(correction_read_pattern, "\\1", lines))
                    elif borred is not None:
                        write_file.write(re.sub(borred_pattern, "xxx", lines))
                    for superscript in re.finditer(superscript_pattern, lines):
                        for letter in superscript.group():
                            if letter != "^" or letter != " ":
                                print(re.sub(superscript_pattern, superscript_map[letter], lines))
                    else:
                        write_file.write(lines)
                    write_file.write("\n")


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
    else:
        with open(f"{path}/error.txt", "a") as f:
            f.write(f"error: {file}, l.{n} -> {type}")



if __name__ == '__main__':
    clean_model_regex()