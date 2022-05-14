import torch 
import torch.nn as nn
from EncoderRNN import EncoderRNN
from AttnDecoderRNN import AttnDecoderRNN
from LanguageBuilder import readLangs
from EvaluateLibs import tensorFromSentence
from HelperLibs import normalizeString

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


MAX_LENGTH = 20
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


def evaluate(encoder, decoder, input_lang,output_lang,sentence, max_length=MAX_LENGTH, device="cpu"):
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1]
input_lang, output_lang, pairs = prepareData(filepath,'spanish', 'sign')
hidden_size = 256
encoder1 = EncoderRNN(input_lang.n_words, hidden_size)
attn_decoder1 = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.1)
checkpoint = torch.load("./sign_language_model.pt")

encoder1.load_state_dict(checkpoint["Enconder_state_dict"])
attn_decoder1.load_state_dict(checkpoint["Decoder_state_dict"])

text_to_translate = "Hola."

print(normalizeString(text_to_translate))

output_words , attentions = evaluate(encoder1, attn_decoder1,input_lang, output_lang, normalizeString(text_to_translate))

print(output_words)
