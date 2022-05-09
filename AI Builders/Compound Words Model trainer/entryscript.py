import os
from torch import nn
import torch
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from C_WordsDS import C_WORDS

class TextClassificationModel(nn.Module):

    def __init__(self, vocab_size, embed_dim, num_class):
        super(TextClassificationModel, self).__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)

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
    
data_root ="."
train_iter = C_WORDS(root=data_root, split="train")
tokenizer = get_tokenizer('basic_english')
num_class = len(set([label for (label, text) in train_iter]))
vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<unk>"])
vocab.set_default_index(vocab["<unk>"])
vocab_size = len(vocab)
emsize = 64

vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<unk>"])
vocab.set_default_index(vocab["<unk>"])

text_pipeline = lambda x: vocab(tokenizer(x))

def init():
    global model
    model = TextClassificationModel(vocab_size, emsize, num_class)
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), "compound_words_model.pt")
    model.load_state_dict(torch.load(model_path))

def run(data):
    return ag_news_label[predict(data, text_pipeline)]