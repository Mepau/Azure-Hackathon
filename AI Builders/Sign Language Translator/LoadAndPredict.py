import torch 
import torch.nn as nn
from EncoderRNN import EncoderRNN
from AttnDecoderRNN import AttnDecoderRNN
from LanguageBuilder import readLangs
from EvaluateLibs import evaluate

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


MAX_LENGTH = 10
SOS_token = 0
EOS_token = 1
filepath="./data/"

def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH 
        #and \ p[1].startswith(eng_prefixes)


def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]


def prepareData(lang1, lang2, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print("Read %s sentence pairs" % len(pairs))
    pairs = filterPairs(pairs)
    print("Trimmed to %s sentence pairs" % len(pairs))
    print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs



input_lang, output_lang, pairs = prepareData(filepath,'spanish', 'sign')
hidden_size = 256
encoder1 = EncoderRNN(input_lang.n_words, hidden_size)
attn_decoder1 = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.1)
checkpoint = torch.load("./sign_language_model.pt")

encoder1.load_state_dict(checkpoint["Enconder_state_dict"])
attn_decoder1.load_state_dict(checkpoint["Decoder_state_dict"])


output_words , attentions = evaluate(encoder1, attn_decoder1,input_lang, output_lang, "algo")

print(output_words, attentions)
