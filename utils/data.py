import os

PATH = 'data/'

class Data():
    def __init__(self, people=[], debt_graph=[], events=[]):
        self.people = people
        self.debt_graph = debt_graph
        self.events = events

class Debt():
    def __init__(self, giver, receiver, money):
        self.giver = giver
        self.receiver =receiver
        self.money = money

def init_data_storage():
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

def load_data(name):
    data = Data()
    try:
        with open(PATH + name, 'r') as f:
            data.people = eval(f.readline())
            data.debt_graph = eval(f.readline())
            data.events = eval(f.readline())
    except:
        data.people = []
        data.debt_graph = []
        data.events = []
    return data

def save_data(name, data):
    with open(PATH + name, 'w+') as f:
        f.write(str(data.people) + '\n')
        f.write(str(data.debt_graph) + '\n')
        f.write(str(data.events) + '\n')

def get_debts(people, debt_graph):
    debts = []
    for i in range(len(people)):
        for j in range(len(people)):
            if debt_graph[i][j] > 0:
                debts.append(Debt(people[i], people[j], debt_graph[i][j]))
    return debts

def add_debt(people, debt_graph, giver, receiver, money):
    assert money > 0

    if giver == receiver:
        return

    giver_i = people.index(giver)
    receiver_i = people.index(receiver)

    debt_graph[giver_i][receiver_i] += money

    # from others to giver
    for i in range(len(people)):
        if debt_graph[i][giver_i] > 0 and debt_graph[giver_i][receiver_i] > 0:
            transfer = min(debt_graph[i][giver_i], debt_graph[giver_i][receiver_i])
            debt_graph[i][giver_i] -= transfer
            debt_graph[giver_i][receiver_i] -= transfer
            add_debt(people, debt_graph, people[i], receiver, transfer)

    # from receiver to others
    for i in range(len(people)):
        if debt_graph[giver_i][receiver_i] > 0 and debt_graph[receiver_i][i] > 0:
            transfer = min(debt_graph[giver_i][receiver_i], debt_graph[receiver_i][i])
            debt_graph[giver_i][receiver_i] -= transfer
            debt_graph[receiver_i][i] -= transfer
            add_debt(people, debt_graph, giver, people[i], transfer)

def add_person(people, debt_graph, person):
    people.append(person)
    for i in debt_graph:
        i.append(0)
    debt_graph.append([0 for _ in range(len(people))])

def delete_person(people, debt_graph, index):
    people.pop(index)
    debt_graph.pop(index)
    for i in debt_graph:
        i.pop(index)

def dispense_money(money, n):
    average = money // n
    output = [average for _ in range(n)]
    for i in range(money % n):
        output[i] += 1
    return output
