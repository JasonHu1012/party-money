from flask import *
from utils.data import *

app = Flask(__name__)
init_data_storage()

@app.route('/<user>/people', methods=['POST'])
def people_func(user):
    data = load_data(user)

    if 'add' in request.form:
        name = request.form['name']
        add_person(data.people, data.debt_graph, name)

    elif 'delete' in request.form:
        index = int(request.form['delete'])
        delete_person(data.people, data.debt_graph, index)

    else:
        raise

    save_data(user, data)

    return redirect(url_for('main_page', user=user))

@app.route('/<user>/events', methods=['POST'])
def events_func(user):
    data = load_data(user)

    if 'add' in request.form:
        giver = request.form['giver']
        money = int(request.form['money'])
        name = request.form['name']

        # gather receivers
        receivers_i = []
        for i in range(len(data.people)):
            if data.people[i] in request.form:
                receivers_i.append(i)

        # debt
        n = len(receivers_i)
        debt_money = dispense_money(money, n)
        for i in range(n):
            # the giver and receiver are switched
            add_debt(data.people, data.debt_graph, data.people[receivers_i[i]], giver, debt_money[i])

        # event
        data.events.append({'name': name,
                            'giver': giver,
                            'receivers': ','.join([data.people[i] for i in receivers_i]),
                            'money': money})

    elif 'delete' in request.form:
        index = int(request.form['delete'])
        data.events.pop(index)

    else:
        raise

    save_data(user, data)

    return redirect(url_for('main_page', user=user))

@app.route('/<user>/debts', methods=['POST'])
def debts_func(user):
    data = load_data(user)

    if 'delete' in request.form:
        index = int(request.form['delete'])
        debts = get_debts(data.people, data.debt_graph)
        debt = debts[index]

        giver_i = data.people.index(debt.giver)
        receiver_i = data.people.index(debt.receiver)
        data.debt_graph[giver_i][receiver_i] = 0

    else:
        raise

    save_data(user, data)

    return redirect(url_for('main_page', user=user))

@app.route('/<user>', methods=['GET'])
def main_page(user):
    data = load_data(user)
    debts = get_debts(data.people, data.debt_graph)
    return render_template('index.html', user=user, people=data.people, debts=debts, events=data.events)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        user = request.form['user']
        return redirect(url_for('main_page', user=user))

    else:
        raise

if __name__ == '__main__':
    app.run()
