
import torch
from filestoarray import fileToArray
from arraytotensor import lineToTensor
import random
filepath = "../data/identifiers/"

class trainerHelper:
    def __init__(self, fta):
        self.all_categories = fta.all_categories 
        self.category_lines = fta.category_lines
    
    def categoryFromOutput(self, output):
        top_n, top_i = output.topk(1)
        category_i = top_i[0].item()
        return self.all_categories[category_i], category_i

    def randomChoice(self, l):
        return l[random.randint(0, len(l) - 1)]

    def randomTrainingExample(self):
        category = self.randomChoice(self.all_categories)
        line = self.randomChoice(self.category_lines[category])
        category_tensor = torch.tensor([self.all_categories.index(category)], dtype=torch.long)
        line_tensor = lineToTensor(line)
        return category, line, category_tensor, line_tensor

        for i in range(10):
            category, line, category_tensor, line_tensor = randomTrainingExample()
            print('category =', category, '/ line =', line)