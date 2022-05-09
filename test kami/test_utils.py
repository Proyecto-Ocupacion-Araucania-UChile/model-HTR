import csv
from datetime import datetime
import io
import pprint
import os
import click

import pandas as pd

from kami.Kami import Kami

# deux phrases d'exemples
ground_truth = " 1 : J'aime Python comme langage de programmation !!"
hypothesis = "2: J'adore python comme Langage    de dévelloppement web ?   "

# Appel de la classe
k = Kami([ground_truth, hypothesis], verbosity=False, truncate=True, percent=True, round_digits='0.01')

# Affichage des phrases d'exemples
current_folder = current_dir = os.path.dirname(os.path.abspath(__file__))
folder_data ="data_test/ground_truth/"
model_folder ="data_test/model/"

#Dictionary author
author = {
    "244_a.xml": "Dias",
    "173_1_b.xml": "Villalon",
    "156_a.xml": "Saavedra",
    "275_a.xml": "Garcia",
    "270_a.xml": "Contreras",
    "215_1_b.xml": "Escala"
}
@click.command()
def test_htr(model_name: str, transforms="XP", verbosity=False, truncate=True, percent=True, round_digits='0.01'):
    for file in os.listdir(os.path.join(current_folder, folder_data)):
        if file != "img":
            name_img = os.path.basename(file).replace(".xml", ".jpg")
            ground_truth = file
            image = os.path.join(current_folder, folder_data, f"img/{name_img}")
            model = os.path.join(current_folder, model_folder, model_name)

            kevaluator = Kami(ground_truth,
                              model=model,
                              image=image,
                              apply_transforms=transforms,
                              verbosity=verbosity,
                              truncate=truncate,
                              percent=percent,
                              round_digits=round_digits)

            metadatas = {}
            metrics = {}

            now = datetime.now()
            metadatas['DATETIME'] = now.strftime("%d_%m_%Y_%H:%M:%S")
            metadatas['IMAGE'] = image
            metadatas['GROUND_TRUTH'] = ground_truth
            metadatas['MODEL'] = model

            for key, value in kevaluator.scores.board.items():
                if type(value) != dict and key not in ['levensthein_distance_char',
                                                       'levensthein_distance_words',
                                                       'hamming_distance',
                                                       'wer',
                                                       'cer',
                                                       'wacc',
                                                       'mer',
                                                       'cil',
                                                       'cip',
                                                       'hits',
                                                       'substitutions',
                                                       'deletions',
                                                       'insertions']:
                    metadatas[key] = value
                else:
                    metrics[key] = value
            try:
                df_metrics = pd.DataFrame.from_dict(metrics)
            except:
                df_metrics = pd.DataFrame.from_dict(metrics, orient='index')

            name_csv = f"evaluation_report_kami_{metadatas['DATETIME']}_{metadatas['MODEL']}_{author[file]}.csv"

            with open(name_csv, 'w') as csv_file:
                writer = csv.writer(csv_file,
                                    delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
                for key, value in metadatas.items():
                    row = []
                    row.append(key)
                    row.append(value)
                    writer.writerow(row)

            df_metrics.to_csv(name_csv, mode='a', header=True)


if __name__ == '__main__':
    test_htr()