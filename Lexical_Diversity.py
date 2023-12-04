'''
Lexical diversity: MTLD, MATTR
'''

from pylats import lats
from taaled import ld  # if you see "plotnine has not been installed. To enable advanced data visualization features, please install plotnine.", just ignore it because this is just for visualization.

## Set up new parameters for lats, using the large dataset in SpaCy for preprocessing
myparameters = lats.parameters()
myparameters.model = "en_core_web_lg"
myparameters.nlp = lats.load_model(myparameters.model)
myparameters.pos = "pos"
myparameters.lemma = True

# Read in the text file (each line represents one recording and has two fields (i.e., filename and transcript) separated by "\t")
txts = open("all_txt_transcript.txt", "r").readlines()

# Write diversity measures into a text file for each file
with open("diversity.txt", "w") as fout:
    fout.write("ID\tMTLD\tMATTR50\tMATTR11\n")
    for txt in txts:
        id = txt.split("\t")[0]
        speech = txt.split("\t")[1]
        # Preprocess the speech, tokenized and lemmatized tokens with Penn POS tags
        tokens = lats.Normalize(speech, myparameters).toks
        # Calculate lexical diversity using different measures
        Lexdiv = ld.lexdiv()
        mtld = round(Lexdiv.MTLD(tokens),4)
        mattr50 = round(Lexdiv.MATTR(tokens),4)
        mattr11 = round(Lexdiv.MATTR(tokens, window_length=11),4)  # you can customize window length
        # Write by file
        fout.write("{}\t{}\t{}\t{}\n".format(id, mtld, mattr50, mattr11))
