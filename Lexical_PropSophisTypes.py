'''
Proportion of sophisticated lexical items
    = Number of sophisticated word types (of which frequency rank > [cutoff]) / Total number of word types.
'''

from pylats import lats  # load the small dataset in spaCy and the corresponding trained parameters
import pandas as pd
from Switch_Tagging import switchtagging_Penn2COCA as switchtagging  # switch POS tagging mode (Penn => COCA_freql)



# Define a function to calculate proportion of sophisticated types for each file: (> 2000 types)/total types
def calculate_sophis_type(tokens_coca, lemmas_pos_ranked, cutoff=2000):
    '''
        Input: 
            * tokens_coca: a list of pairs of lemma token and COCA POS tag for one speech file, e.g., ["about_i", "the_a", "topic_n", ...]
            * cutoff: the frequency rank cutoff for sophisticated word types
            * lemmas_pos_ranked: the ranked lemma_pos pairs, a list of "lemma_pos" pairs (e.g., 'be_v') sorted by their frequency in the reference corpus 
        Output: 
            proportion_sophis: Proportion of sophisticated types to total types: (types with frequency > [cutoff])/total types
    '''

    # Number of total types in the speech file
    nb_types = len(set(tokens_coca))
    # Number of sophisticated types, if the frequency rank in COCA list greater than the cutoff
    sophis_type_list = [pair for pair in tokens_coca if pair in lemmas_pos_ranked[cutoff:]]
    nb_sophis_types = len(set(sophis_type_list))

    # Proportion of sophisticated lemma types for the speech file
    proportion_sophis = round(nb_sophis_types/nb_types, 4)

    return proportion_sophis



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

    # Read in the text file (each line represents one recording and has two fields (i.e., filename and transcript) separated by "\t")
    txts = open("all_txt_transcript.txt", "r").readlines()

    # Write proporation of sophistication types in a txt file
    with open("sophis_type.txt", "w") as fout:
        fout.write("ID\tProp_Sophis_type)\n")
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
            # Calculate proportion of sophisticated types
            proportion_sophis = calculate_sophis_type(tokens_coca, lemmas_pos_ranked, cutoff=2000)
            fout.write("{}\t{}\n".format(id, proportion_sophis))
