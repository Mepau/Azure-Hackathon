import torch
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from C_WordsDS import C_WORDS
from TextClassifModel import TextClassificationModel

def yield_tokens(data_iter):
    for _, text in data_iter:
        yield tokenizer(text)

def predict(text, text_pipeline):
    with torch.no_grad():
        text = torch.tensor(text_pipeline(text))
        output = model(text, torch.tensor([0]))
        return output.argmax(1).item() + 1


ag_news_label = {1: "Compound",
                 2: "Not Compound"}
data_root ="./data"
train_iter, _ = C_WORDS(root=data_root)
tokenizer = get_tokenizer('basic_english')
num_class = len(set([label for (label, text) in train_iter]))
vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<unk>"])
vocab.set_default_index(vocab["<unk>"])
vocab_size = len(vocab)
emsize = 64
model = TextClassificationModel(vocab_size, emsize, num_class)

vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<unk>"])
vocab.set_default_index(vocab["<unk>"])

text_pipeline = lambda x: vocab(tokenizer(x))

model.load_state_dict(torch.load("./compound_words_model.pt"))
model = model.to("cpu")

ex_text_str = "Que tengas buenas tardes"


print("This is a %s sentence" %ag_news_label[predict(ex_text_str, text_pipeline)])