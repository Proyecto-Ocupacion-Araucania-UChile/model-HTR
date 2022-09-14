# Model HTR

## Summary
Repository for the production of HTR ground truth data, allowing the verification of the ontology and the xml structure with HTRVX. All the data (180 xml) produced for the moment are present in the folder `data/`

**Warning !** If you want to reuse the data, we advise you to use the data present in the following repository: https://github.com/Proyecto-Ocupacion-Araucania-UChile/HTR_Araucania_XIX

The folder `test_kami/` is a CLI allowing to execute a benchmarking with the [KaMi-lib](https://github.com/KaMI-tools-project/KaMi-lib) application on different HTR models developed from the [Kraken](https://github.com/mittagessen/kraken) OCR engine.

The `Preprocess/` folder: allows the cleaning of some REGEX initially transcribed, and the conversion of xml files to text format (cleaned).

## Tree
```
Project
│   README.md
│   requirements.txt   
│   transcription.csv
|   LICENCE
|   .gitignore
|
└───Preprocess/
│   │   XML_cleaning.py
│   │   no_clean/
|   |   clean_regex/
│   │   requirements.txt 
|
└───test_kami
│   │   test_utils.py
│   │   requirements.txt
|   |   clean_regex/
│   │
│   └───ground_truth
│   |    │   img/
│   |    │   **.xml
│   |
│   |
|   └─── model/
|         |   **.mlmodel
|         |   **.csv
|
└───Data/
```
