# Lexical-Complexity
Automatically measuring lexical sophistication, lexical density, and lexical diversity

* COCA word frequency.xlsx
* `.py` files for calculating lexical complexity measures

## Get ready
Type the following commands in Mac Terminal to install the required packages:

1. SpaCy (https://spacy.io/usage)
You can just download the model you need after installation.
```
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_trf
python -m spacy download es_core_news_sm
python -m spacy download es_dep_news_trf
```
2. pylats, taaled, pandas, numpy, openpxl
`pip install XXX`

## Calculate lexical complexity measures
* To calculate the measures all at once for each text file in the folder, run `Lexical_Complexity_directory.py` (Refer to `./test_files/` for the required input format.) Results will be written into a .txt file, where values in each row are separated by `\t`. 
* To calculate the measures all at once for each row in one text file, run `Lexical_Complexity.py`(Refer to `all_txt_transcript.txt` for the required input format.) Results will be written into a .txt file.
* To calculate a specific category of measures, run the corresponding file.
  * Lexical sophistication
    * `Lexical_FreqBand.py`: Proportion of word tokens in each Frequency band from the COCA word frequency list.
    * `Lexical_PropSophisTypes.py`: Proportion of sophisticated word types (of which frequency rank > [cutoff])
  * Lexical density (`Lexical_Density.py`): Proportion of content word tokens
  * Lexical diversity (`Lexical_Diversity.py`)
    * MTLD
    * MATTR
