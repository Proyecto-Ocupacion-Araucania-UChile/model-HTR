import re, os, click
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
correction_read_pattern = re.compile(r"\[\[[A-Za-zÀ-ÖØ-öø-ÿ -]+\|[A-Za-zÀ-ÖØ-öø-ÿ -]+]]")
correction_pattern = re.compile(r"\[\[([A-Za-zÀ-ÖØ-öø-ÿ -])*]]")
unreadable_pattern = re.compile(r"-\[([A-z -]*)]-")
borred_pattern = re.compile(r"\*\[([A-Za-zÀ-ÖØ-öø-ÿ -]+])\*")

@click.command()
def clean_model():
    clean = os.path.join(current_dir, ALTO_CLEAN)
    for file in os.listdir(os.path.join(current_dir, ALTO_BRUT)):
        with open(os.path.join(current_dir, ALTO_BRUT, file), 'r') as f:
            xml = f.read()
            for lines in xml.split('\n'):
                print(re.sub(unreadable_pattern, "\\1", lines))


if __name__ == '__main__':
    clean_model()


#comte regex find by ligne

#-[mu]-jeres de los Soldados
# print(re.sub(unreadable_pattern, "\\1", lines))     fonctionne
"""@click.command()
def clean_model():
    clean = os.path.join(current_dir, ALTO_CLEAN)
    for file in os.listdir(os.path.join(current_dir, ALTO_BRUT)):
        with open(os.path.join(current_dir, ALTO_BRUT, file), 'r') as f:
            xml = f.read()
            with open(f"{clean}/{file}", 'w') as write_file:
                for lines in xml.split('\n'):
                    for match_super in re.search(superscript_pattern, lines):
                        match_cleaning = match_super.replace('^', '')
                        for letters in match_cleaning.split():
                            write_file.write(match_cleaning.replace(letters, superscript_map[letters]))
                    unread = re.search(unreadable_pattern, lines)
                    if unread is not None:
                        write_file.write(re.sub(unread, ''))
                    correction = re.search(correction_pattern, lines)
                    if correction is not None:
                        write_file.write(re.sub(correction, "\\1"))
                    correction_read = re.search(correction_read_pattern, lines)
                    if correction_read is not None:
                        write_file.write(re.sub(correction_read, "\\1"))
                    borred = re.search(borred_pattern, lines)
                    if borred is not None:
                        write_file.write(re.sub(borred, ""))

if __name__ == '__main__':
    clean_model()"""


#use .group for regex si il y a plusieurs resultats dans une meme ligne