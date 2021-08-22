from flask import Flask, render_template, request, url_for, redirect
from database_init import *

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


#@app.route('/new', methods=['GET', 'POST'])
#def new_session():


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


#Базовая страница мастера для выбора инструментов подготовки к сессии
@app.route('/master', methods=['GET'])
def master_home():
    return render_template('master_base.html')


#Страница создания персонажа в БД
@app.route('/master_char', methods=['GET', 'POST'])
def master_char_creation():
    with open('session1/armour_db.json', 'r') as file:
        arm_bd = json.load(file)
    with open('session1/weapons_db.json', 'r') as file:
        w_bd = json.load(file)
    if request.method == 'POST':
        try:
            char_init = [request.form.get('player'), request.form.get('unit_id'),
                request.form.get('armour'), request.form.get('weapon'),
                request.form.get('unit_class'), request.form.get('strength'),
                request.form.get('toughness'), request.form.get('reaction'),
                request.form.get('spirit'), request.form.get('speed'),
                request.form.get('vitality'), request.form.get('hp'),
                request.form.get('mp'), request.form.get('mp_regen')]
            create_char(*char_init)
            return redirect(url_for('db_result', db_result_var=f'Создан персонаж {char_init}'))
        except:
            return redirect(url_for('db_result', db_result_var='Ошибка создания персонажа'))

    return render_template('master_char.html', arm_bd=arm_bd, w_bd=w_bd)


#Страница создания оружия и брони в БД
@app.route('/master_items', methods=['GET', 'POST'])
def master_item_creation(*args):
    if request.method == 'POST':
        try:
            if request.form.get('weapon_name') is not '':
                weapon_init = [request.form.get('weapon_name'), request.form.get('damage_mod'),
                             request.form.get('w_hp'), request.form.get('w_accuracy'),
                             request.form.get('w_weight'), request.form.get('ignore_arm'),
                             request.form.get('w_range'), request.form.get('damage_type')]
                create_weapon(*weapon_init)
                return redirect(url_for('db_result', db_result_var=f'Создано оружие {weapon_init}'))
            elif request.form.get('armour_name') is not '':
                armour_init = [request.form.get('armour_name'), request.form.get('arm_mod'),
                               request.form.get('arm_hp'), request.form.get('arm_weight'),
                               request.form.get('element_type')]
                create_armour(*armour_init)
                return redirect(url_for('db_result', db_result_var=f'Создана броня {armour_init}'))
            else:
                return redirect(url_for('db_result', db_result_var='Ошибка создания предмета'))
        except:
            return redirect(url_for('db_result', db_result_var='Ошибка создания предмета'))
    return render_template('master_item.html')


#Вывод результата создания записи в БД
@app.route('/result', methods=['GET'])
def db_result():
    db_result_var = request.args.get('db_result_var')
    return render_template('db_result.html', db_result_var=db_result_var)


if __name__ == '__main__':
    app.run(debug=True)

