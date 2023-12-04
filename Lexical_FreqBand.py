'''
Proportion of word tokens in each Frequency band
    = Number of word tokens in each frequency band / Total number of tokens.
'''

from pylats import lats  # load the small dataset in spaCy and the corresponding trained parameters
import pandas as pd
from Switch_Tagging import switchtagging_Penn2COCA as switchtagging  # switch POS tagging mode (Penn => COCA_freql)



# Define a function to calculate roportion of word tokens in each Frequency band for each file
def calculate_prop_freqband(tokens_coca, lemmas_pos_ranked, indices_band=[0, 500, 3000, 5000]):
    '''
        Input:
            * tokens_coca: a list of pairs of lemma token and COCA POS tag for one speech file, e.g., ["about_IN", "the_DT", "topic_NN", ...]
            * lemmas_pos_ranked: the ranked lemma_pos pairs, a list of "lemma_pos" pairs (e.g., 'be_v') sorted by their frequency in the reference corpus 
            * indices_band: indices for each frequency band of the COCA frequency list. By default, the frequency bands are 0-499, 500-2999, 3000-4999, 5000-
        Output:
            prop_freqband: proportion of word tokens in each frequency band, a dictionary of which structure is: {'band1':proportion, 'band2':proportion, ...}
    '''

    # Number of total tokens in the speech file
    nb_pairs = len(tokens_coca)

    ## Set up the frequency bands based on the frequency list
    # Number of bands, including the frequency band out of the frequency list
    nb_bands = len(indices_band)

    # A list containing lists of pairs of lemma and POS tag (each list is a frequency band within the frequency list)
    lemma_pos_bands = list()
    for i in range(nb_bands-1):
        lemma_pos_bands.append(lemmas_pos_ranked[indices_band[i]:indices_band[i+1]])
    
    # Set a list of band names, including the frequency band out of the frequency list
    band_nm = ["band{}".format(i+1) for i in range(nb_bands)]
    # Count tokens in the file for each band {'band1':0, 'band2':0, ...}
    count_band = {b: 0 for b in band_nm}
    for pair in tokens_coca:
        temp = 0  # for marking the one out of the list
        # for the ones within the frequency list
        for i in range(nb_bands-1):
            if pair in lemma_pos_bands[i]:
                count_band["band{}".format(i+1)] += 1
            else:
                temp += 1
        # for the ones out of the frequency list
        if temp == nb_bands-1:
            count_band["band{}".format(nb_bands)] += 1
            
    # Proportion of tokens for each frequency band
    prop_freqband = dict()
    for bd,ct in count_band.items():
        prop_freqband[bd] = round(ct/nb_pairs,4)

    return prop_freqband



if __name__ == "__main__":

    ## Set up new parameters for lats, using the large dataset in SpaCy for preprocessing
    myparameters = lats.parameters()
    myparameters.model = "en_core_web_lg"
    myparameters.nlp = lats.load_model(myparameters.model)
    myparameters.pos = "pos"
    myparameters.lemma = True

    # Load the COCA word frequency list (Sheet 1)
    lemma_freq_coca = pd.read_excel("COCA word frequency.xlsx", sheet_name=1)
    # Set up the ranked lemma_pos pairs (e.g., ['the_a', 'be_v', 'and_c', 'a_a', 'of_i'])
    lemmas_ranked = list(lemma_freq_coca["lemma"][:5000])
    pos_ranked = list(lemma_freq_coca["PoS"][:5000])
    lemmas_pos_ranked = [str(lemmas_ranked[i]).lower()+"_"+pos_ranked[i] for i in range(len(lemmas_ranked))]

    # Indices for each frequency band of the COCA frequency list
    indices_band = [0, 500, 3000, 5000]

    # Read in the text file (each line represents one recording and has two fields (i.e., filename and transcript) separated by "\t")
    txts = open("all_txt_transcript.txt", "r").readlines()

    # Write proportion of tokens for each frequency band in a txt file
    with open("frequency_band.txt", "w") as fout:
        # Write the headings
        fout.write("ID\t")
        for i in range(len(indices_band)):
            fout.write("Freq_Band{}\t".format(i+1))
        fout.write("\n")
        for txt in txts:
            id = txt.split("\t")[0]
            speech = txt.split("\t")[1]
            # Preprocess the speech, tokenized and lemmatized tokens with Penn POS tags
            tokens = lats.Normalize(speech, myparameters).toks
            # Switch POS tagging for each token pairs (from Penn to COCA POS tags)
            #tokens_coca = [switchtagging(token) for token in tokens]
            tokens_coca = []
            for token in tokens:
                # Remove the URL token that contains "https:"
                if "https:" in token:
                    continue
                else:
                    tokens_coca.append(switchtagging(token))
            # Calculate proportion of tokens in each frequency band
            prop_freqband = calculate_prop_freqband(tokens_coca, lemmas_pos_ranked, indices_band)
            props_string = ""
            for band,prop in prop_freqband.items():
                props_string += str(prop)+"\t"
            fout.write("{}\t{}\n".format(id, props_string))
