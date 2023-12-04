'''
Calculate lexical complexity measures, including:
    * Lexical diversity:
        * MTLD
        * MATTR50
        * MATTR11
    * Proportion of tokens in each frequency band in the COCA word frequency list
        * Freq_Band1: ranked 1-500
        * Freq_Band2: ranked 501-3000
        * Freq_Band3: ranked 3001-5000
        * Freq_Band4: ranked 5001-
    * Proportion of sophisticated word types (ranked after 2000 in the COCA word frequency list)
    * Lexical density: Proportion of content word tokens
'''

import pandas as pd
import numpy as np
from pylats import lats
from taaled import ld
from Switch_Tagging import switchtagging_Penn2COCA as switchtagging
from Lexical_FreqBand import calculate_prop_freqband
from Lexical_PropSophisTypes import calculate_sophis_type
from Lexical_Density import calculate_density



## Set up new parameters for lats, using the large dataset in SpaCy for preprocessing
myparameters = lats.parameters()
myparameters.model = "en_core_web_lg"
myparameters.nlp = lats.load_model(myparameters.model)
myparameters.pos = "pos"
myparameters.lemma = True


# Load the COCA word frequency list (Sheet 1) for measures regarding frequency bands and sophistication types
lemma_freq_coca = pd.read_excel("COCA word frequency.xlsx", sheet_name=1)
# Set up the ranked lemma_pos pairs (e.g., ['the_a', 'be_v', 'and_c', 'a_a', 'of_i'])
lemmas_ranked = list(lemma_freq_coca["lemma"][:5000])
pos_ranked = list(lemma_freq_coca["PoS"][:5000])
lemmas_pos_ranked = [str(lemmas_ranked[i]).lower()+"_"+pos_ranked[i] for i in range(len(lemmas_ranked))]

# Indices for each frequency band of the COCA frequency list
indices_band=np.array([0, 500, 3000, 5000])


# Read in the text file (each line represents one recording and has two fields (i.e., filename and transcript) separated by "\t")
txts = open("all_txt_transcript.txt", "r").readlines()

# Write lexical complexity measures for each file into a text file
with open("Lexical_Complexity_results.txt", "w") as fout:

    # Write the headings
    fout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("ID", "MTLD", "MATTR50", "MATTR11", "Freq_Band1", "Freq_Band2", "Freq_Band3", "Freq_Band4", "Prop_Sophis_type", "Density"))

    ## Iterate by file
    for txt in txts:

        id = txt.split("\t")[0]
        speech = txt.split("\t")[1]

        # Preprocess the speech, tokenized and lemmatized tokens with Penn POS tags
        tokens = lats.Normalize(speech, myparameters).toks

        # Switch POS tagging for each token pairs (from Penn to COCA POS tags)
        #tokens_coca = [switchtagging(token) for token in tokens]
        tokens_clean = []
        tokens_coca = []
        for token in tokens:
            # Remove the URL token that contains "https:"
            if "https:" in token:
                continue
            else:
                tokens_clean.append(token)
                tokens_coca.append(switchtagging(token))

        ## Calculate lexical diversity using different measures
        Lexdiv = ld.lexdiv()
        mtld = round(Lexdiv.MTLD(tokens_clean),4)
        mattr50 = round(Lexdiv.MATTR(tokens_clean),4)
        mattr11 = round(Lexdiv.MATTR(tokens_clean, window_length=11),4)  # you can customize window length

        ## Calculate frequency-band measures
        prop_freqband = calculate_prop_freqband(tokens_coca, lemmas_pos_ranked, indices_band)
        props_fb_string = ""
        for band,prop in prop_freqband.items():
            props_fb_string += str(prop)+"\t"
        
        ## Calculate proportion of sophisticated word types
        proportion_sophis = calculate_sophis_type(tokens_coca, lemmas_pos_ranked, cutoff=2000)

        ## Calculate lexical density
        density = calculate_density(tokens_coca)

        fout.write("{}\t{}\t{}\t{}\t{}{}\t{}\n".format(id, mtld, mattr50, mattr11, props_fb_string, proportion_sophis, density))
