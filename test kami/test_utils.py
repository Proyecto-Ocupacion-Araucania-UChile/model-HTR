from datetime import datetime
import shutil
import os
import click
import glob
import csv

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
@click.argument("model_name", type=str)
@click.option("-t", "--transforms", default="XP",
              help="""Allows you to apply transforms to the text. 
                        D : Deletes all digits and numbers;
                        U : Shift the text;
                        L : Minusculise the text;
                        P : Delete punctuation;
                        X : Deletes diacritical marks;""")
@click.option("-v", "--verbosity",  is_flag=True, default=False,
              help="Allows you to retrieve execution logs to follow the process. False by default")
@click.option("-tr", "--truncate",  is_flag=True, default=True,
              help="Option to use to truncate the final result. True by default")
@click.option("-p", "--percent",  is_flag=True, default=True,
              help="Option to display a result in percent. True by default")
@click.option("-r", "--round", "round_digits", default='0.01',
              help="Option to set the digits after the decimal point. 0.01 by default")
def test_htr(model_name, transforms, verbosity, truncate, percent, round_digits):
    """
    Function to product test model HTR on 6 hands to see differences between them.

    :param model_name: str, name of model in folder model
    :param transforms: str, option argument to configure transformation of text
    :param verbosity: Boolean option argument to retrieve execution logs
    :param truncate: Boolean, option argument to truncate the final result
    :param percent: Boolean, option to display a result in percent
    :param round_digits: str, option to set the digits after the decimal point
    :return: csv
    """
    for file in os.listdir(os.path.join(current_folder, folder_data)):
        if file != "img":
            name_img = os.path.basename(file).replace(".xml", ".jpg")
            ground_truth = os.path.join(current_folder, folder_data, file)
            image = os.path.join(current_folder, folder_data, f"img/{name_img}")
            model = os.path.join(current_folder, model_folder, model_name)
            path = os.path.join(current_folder, model_folder)

            kevaluator = Kami(ground_truth,
                              model=model,
                              image=image,
                              apply_transforms=transforms,
                              verbosity=verbosity,
                              truncate=truncate,
                              percent=percent,
                              round_digits=round_digits)

            #metada
            metadatas = {}
            metrics = {}

            now = datetime.now()
            metadatas['DATETIME'] = now.strftime("%d_%m_%Y_%H:%M:%S")
            metadatas['IMAGE'] = image
            metadatas['GROUND_TRUTH'] = ground_truth
            metadatas['MODEL'] = model

            #scoring
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
            # write csv zith data
            try:
                df_metrics = pd.DataFrame.from_dict(metrics)
            except:
                df_metrics = pd.DataFrame.from_dict(metrics, orient='index')

            name_csv = f"evaluation_report_kami_{metadatas['DATETIME']}_{model_name}_{author[file]}.csv"

            with open(os.path.join(path, name_csv), 'w') as csv_file:
                writer = csv.writer(csv_file,
                                    delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
                for key, value in metadatas.items():
                    row = []
                    row.append(key)
                    row.append(value)
                    writer.writerow(row)

            df_metrics.to_csv(os.path.join(path, name_csv), mode='a', header=True)
    
    move_model(model_name)
    print("work as well !")


def move_model(name):
    """
    Function to create folder with model and results of its tests
    :param name: str, name of model
    :return: None
    """
    try:
        name_folder = name.replace(".mlmodel", "")
        os.mkdir(os.path.join(current_folder, model_folder, name_folder))
        path = os.path.join(current_folder, model_folder, name_folder)
        shutil.move(os.path.join(current_folder, model_folder, name), path)
        for items in glob.glob(f"{model_folder}/*.csv"):
            shutil.move(items, path)
    except FileExistsError:
        return print(f"Files exists about {name_folder}")


if __name__ == '__main__':
    test_htr()
