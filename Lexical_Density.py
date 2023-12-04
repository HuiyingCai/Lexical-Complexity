'''
Lexical density
    = Number of content word tokens / Total number of tokens.
'''

from pylats import lats  # load the small dataset in spaCy and the corresponding trained parameters
import pandas as pd
from Switch_Tagging import switchtagging_Penn2COCA as switchtagging  # switch POS tagging mode (Penn => COCA_freql)


# Define a function to calculate lexical density (content tokens/tokens) for each file
def calculate_density(tokens_coca, content=["n", "v", "j", "r"]):
    '''
        Input:
            * tokens_coca: a list of pairs of lemma token and COCA POS tag for one speech file, e.g., ["about_IN", "the_DT", "topic_NN", ...]
            * content: a list of POS taggs that indicate content words, typically, nouns, verbs, adjectives, and adverbs
        Output:
            density: lexical density value for the speech file
    '''
    # Number of total tokens in the speech file
    nb_tokens = len(tokens_coca)
    # Count the number of content words
    count_content_tokens = 0
    for pair in tokens_coca:
        # check whether a content token
        pos = pair.split("_")[1]
        if pos in content:
            count_content_tokens += 1
    density = round(count_content_tokens/nb_tokens,4)
    return density



if __name__ == "__main__":

    ## Set up new parameters for lats, using the large dataset in SpaCy for preprocessing
    myparameters = lats.parameters()
    myparameters.model = "en_core_web_lg"
    myparameters.nlp = lats.load_model(myparameters.model)
    myparameters.pos = "pos"
    myparameters.lemma = True

    # Read in the text file (each line represents one recording and has two fields (i.e., filename and transcript) separated by "\t")
    txts = open("all_txt_transcript.txt", "r").readlines()

    # Write density in a txt file
    with open("density.txt", "w") as fout:
        fout.write("ID\tDensity\n")
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
            # Calculate density
            density = calculate_density(tokens_coca)
            fout.write("{}\t{}\n".format(id, density))
