from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


class Boez:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates


boizi_proverka = {
    'Tima1': '2_2',
    'Dal1': '2_12',
    'Shini1': '12_12',
    'Dima1': '12_2'
}

boizi = {
    '2_2': 'Tima1',
    '2_12': 'Dal1',
    '12_12': 'Shini1',
    '12_2': 'Dima1'
}

player_fighters = {
    'Tima': ['Tima1', 'Tima2'],
    'Dalamar': ['Dal1'],
    'Shini': ['Shini1'],
    'Dima': ['Dima1']

}

pl_active_turn = ['Tima', 'Dalamar', 'Shini', 'Dima']


@app.route('/', methods=['GET', 'POST'])
def arena():
    global pl_active_turn
    global player_fighters
    if request.method == 'POST':
        b = Boez(request.form.get('fighter_name'), request.form.get('coordinates'))
        boizi_proverka[b.name] = b.coordinates

        pl_active_turn.append(pl_active_turn[0])
        pl_active_turn.pop(0)
        boizi.clear()
        for k, v in boizi_proverka.items():
            boizi[v] = k
        return redirect(url_for('arena', boizi=boizi, pl_active_turn=pl_active_turn, player_fighters=player_fighters))
    return render_template('arena.html', boizi=boizi, pl_active_turn=pl_active_turn, player_fighters=player_fighters)


if __name__ == '__main__':
    app.run(debug=True)
