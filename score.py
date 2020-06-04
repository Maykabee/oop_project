import os
from copy import copy


class Score:

    def __init__(self):
        
        self.score = 0
        self.previous = 0


    def restart(self, level=False):

        if level:
            self.score = copy(self.previous)

        else:
            self.score = 0
            self.previous = 0

    def load_records(self, n=5):

        scores = []
        id_names = []

        if os.path.exists(os.path.join(os.getcwd(), 'records.txt')):
            with open(os.path.join(os.getcwd(), 'records.txt'), 'r') as f:
                lines = self.sort_records(f.readlines())
        
            if n > len(lines):
                n = len(lines)

            for i in range(n):
                scores.append(int(lines[i].split()[1]))
                id_names.append(lines[i].split()[0])

        return id_names, scores
        
    def save_record(self, id_name):        

        try:
            with open(os.path.join(os.getcwd(), 'records.txt'), 'a') as f:
                f.write(f'{id_name} {self.score}\n')
        except Exception as value:
            print(f'Error {value}')

    def sort_records(self, lines):
        return sorted(lines, key=lambda x: int(x.split()[1]))[::-1]
    
    def update_score(self, n_eresed):        
        self.score += n_eresed

    def previous_score(self):
        self.previous = copy(self.score)
        return self.previous