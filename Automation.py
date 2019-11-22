from copy import deepcopy

class Automation:
    def __init__(self, productions, v, t):
        self.productions = productions
        self.collections = []
        self.go = {}
        self.goto = None
        self.action = None
        self.first = {}
        self.follow = {}
        self.v = v
        self.t = t
    
    def calculate_table(self):
        # self.generate_collections()
        self.cal_first_follow()

        for item in self.first:
            print(item, self.first[item])
        
    def cal_first_follow(self):
        for token in self.v:
            if token not in self.first:
                self.cal_first(token)

    def cal_first(self, token):
        for production in self.productions:
            if production[0] == token:
                if production[1][0] in self.v and production[1][0] != token:
                    if production[1][0] not in self.first:
                        part = self.cal_first(production[1][0])
                    else:
                        part = self.first[production[1][0]]
                    if token in self.first:
                        self.first[token] += part
                        self.first[token] = list(set(self.first[token]))  # get rid of the repeat items
                    else:
                        self.first[token] = part
                elif production[1][0] in self.t:
                    if token in self.first and production[1][0] not in self.first[token]:
                        self.first[token].append(production[1][0])
                    else:
                        self.first[token] = [production[1][0]]
        return self.first[token]

    
    def generate_collections(self):
        program_0 = [self.productions[0][0], self.productions[0][1], 0]
        # ['E', 'E+T', 0-3]
        self.collections.append(self.calculate_closure([program_0]))
        counter = 0

        for i, collection in enumerate(self.collections):
            collections_from = self.partition(collection)        
            for token in collections_from:
                result = self.calculate_closure(collections_from[token])
                next_state = -1
                if result not in self.collections:
                    self.collections.append(result)
                    counter += 1    # corresponding to the status number
                    next_state = counter
                else:
                    next_state = self.collections.index(result)
                
                if i in self.go:
                    self.go[i].append([next_state, token])     # counter = go(0, function)
                else:
                    self.go[i] = [[next_state, token]]
            

    def calculate_closure(self, programs):
        collection = deepcopy(programs)
        # add itself to the collection

        for program in collection:
            if program[2] < len(program[1]):
                next_token = program[1][program[2]]

                if next_token in self.v:
                    for production in self.productions:
                        if production[0] == next_token:
                            new = [production[0], production[1], 0]
                            if new not in collection:
                                collection.append(new)
        return collection

    def partition(self, collection):
        # partition programs belongs to the same next start programs 
        # e.g. {E->·E+T, E->·E-T}
        programs = {}
        # {'E': [['E', 'E+T', 0], ['E', 'E-T', 0]]}
        for program in collection:
            if program[2] < len(program[1]):
                next_token = program[1][program[2]]
                if next_token in programs:
                    programs[next_token].append([program[0], program[1], program[2]+1])
                
                else:
                    programs[next_token] = [[program[0], program[1], program[2]+1]]
        
        return programs

if __name__ == '__main__':
    example_v = {'E': 0, 'T': 1, 'F': 2}
    example_t = {'n': 0, '+': 1, '-': 2, '*': 3, '/': 4, '(': 5, ')': 6, '$': 7}
    productions = [['S', 'E'], 
                   ['E', 'E+T'], 
                   ['E', 'E-T'], 
                   ['E', 'T'], 
                   ['T', 'T*F'],
                   ['T', 'T/F'],
                   ['T', 'F'],
                   ['F', '(E)'],
                   ['F', 'n']]
    auto = Automation(productions, example_v, example_t)
    auto.calculate_table()