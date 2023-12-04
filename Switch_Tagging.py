'''
Note: pylats use Penn POS tags, while COCA uses their own tags
    => Define a function to switch POS tagging mode (Here, Penn => COCA_freql)
'''

from pylats import lats



## Preprocess and save the tokens with POS tags in to a dictionary for future mapping with the COCA frequency list, {id:[token1_tag, token2_tag, ...]}
def switchtagging_Penn2COCA(token_penn):
    '''
        Input: 
            token_penn: a pair of token and Penn POS tag, e.g., ["about_IN", "the_DT", "topic_NN", ...]
        Output: 
            token_coca: a pair of token and COCA POS tag, e.g., ["about_i", "the_a", "topic_n", ...]
    '''
    # tags that have to match actual words directly
    a = ["the", "a", "his", "my", "your", "their", "her", "our", "no", "every", "its"]
    m = ["one", "two", "first", "last", "three", "next", "four", "five", "second", "six", "million", "third", "seven", "eight", "ten", "billion", "nine", "hundred", "thousand", "fourth", "twenty", "dozen", "fifth", "thirty", "zero", "fifty", "twelve", "fifteen", "sixth", "forty", "seventh", "eleven", "eighth"]
    x = ["not", "n't"]
    
    # 1. Look up for actual words 
    token = token_penn.split("_")[0]
    penn = token_penn.split("_")[1]
    if token in a:
        coca = "a"
    elif token in m:
        coca = "m"
    elif token in x:
        coca = "x"
    # 2. Look up the "MD", modals
    elif penn == "MD":
        coca = "v"
    # 3. Look up the "^W", wh-words
    elif penn.startswith("W"):
        if penn[1] in ["D", "P", "R"]:
            coca = penn[1].lower()
    # 4. Regular changes, check against the first letter
    else:
        coca = penn[0].lower()
    token_coca = token + "_" + coca

    return token_coca



# Test
if __name__ == "__main__":

    ## Set up new parameters for lats, using the large dataset in SpaCy for preprocessing
    myparameters = lats.parameters()
    #myparameters.model = "en_core_web_lg"
    myparameters.nlp = lats.load_model(myparameters.model)
    myparameters.pos = "pos"
    myparameters.lemma = True
    
    # Read in the text file (each line represents one recording and has two fields (i.e., filename and transcript) separated by "\t")
    txts = open("all_txt_transcript.txt", "r").readlines()
    # Test for one file
    txt0 = txts[0]

    txt0 = txts[0]
    id = txt0.split("\t")[0]
    speech = txt0.split("\t")[1]
    # preprocess the speech
    tokens = lats.Normalize(speech, myparameters).toks
    # Switch POS tagging for each token pairs
    tokens_coca = list()
    for token in tokens:
        token_coca = switchtagging_Penn2COCA(token)
        tokens_coca.append(token_coca)

    print(tokens_coca) 
