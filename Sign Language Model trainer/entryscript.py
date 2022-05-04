import torch.nn as nn
import torch
import string
import unicodedata
import glob
import os
import json
from azureml.core.model import Model
from ast import literal_eval

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)



all_categories = ['a0004', 'a0005', 'a0007', 'a0008', 'b0003', 'b0004', 'm0001', 'p0002', 't0001', 't0002', 'y0001']
all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)
n_hidden = 128
n_categories = len(all_categories)
category_lines = {}

# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


def evaluate(line_tensor):
    hidden = model.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = model(line_tensor[i], hidden)

    return output

def predict(input_line, n_predictions=3):
    print('\n> %s' % input_line)
    with torch.no_grad():
        output = evaluate(lineToTensor(input_line))

        # Get top N categories
        topv, topi = output.topk(n_predictions, 1, True)
        predictions = []
        return all_categories[topi[0][0].item()]

def init():
    global model
    model = RNN(n_letters, n_hidden, n_categories)
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), "sign_language_id.pt")
    model.load_state_dict(torch.load(model_path))

def run(data):
    eleToEval = literal_eval(data)
    predictions= []
    for ele in eleToEval:
        predictions.append(predict(ele))
    return predictions