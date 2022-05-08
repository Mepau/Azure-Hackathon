import torch
from arraytotensor import lineToTensor
from rnn import RNN
from filestoarray import fileToArray
from traininghelper import trainerHelper
from arraytotensor import n_letters

filepath = "../data/identifiers/"
n_hidden = 128

fta = fileToArray(filepath)
tHelper = trainerHelper(fta)
model = RNN(n_letters, n_hidden, fta.n_categories)
model.load_state_dict(torch.load("./sign_language_id.pt"))
#model.eval()

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

        for i in range(n_predictions):
            value = topv[0][i].item()
            category_index = topi[0][i].item()
            print('(%.2f) %s' % (value, fta.all_categories[category_index]))
            predictions.append([value, fta.all_categories[category_index]])


predict('abeja')