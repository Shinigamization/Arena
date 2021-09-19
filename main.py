from flask import Flask, render_template, request, url_for, redirect
from database_init import *
from database_working import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.form.get('session_init'):
        create_unit_classes()
        for each_unit in all_units_list:
            update_unit(each_unit)
            all_current_coordinates[f'{each_unit.coordinates}'] = [each_unit.unit_id, each_unit]
        create_move_sequence()
        return redirect(url_for('arena'))
    return render_template('start.html')


# Основная страница арены
@app.route('/arena', methods=['GET', 'POST'])
def arena():
    global turn_phase
    global pl_active_turn
    global current_active_unit
    global possible_attack_points
    global log_comment
    if request.method == 'POST':
        global all_current_coordinates
        all_current_coordinates = update_all_coordinates(request.form.get('fighter_name'),
                                                         request.form.get('coordinates'))
        if request.form.get('fighter_name'):
            current_active_unit = request.form.get('fighter_name')
        possible_attack_points = possible_attack_targets(current_active_unit)
        print(possible_attack_points)
        if request.form.get('attack_direction') in possible_attack_points:
            try:
                print(all_current_coordinates)
                log_comment = hit_calc(determine_unit(current_active_unit), all_current_coordinates['attack_direction'][1])
            except:
                log_comment = 'There was no target.'
        turn_forward()
        return redirect(url_for('arena', pl_active_turn=pl_active_turn,
                                all_units_list=all_units_list, all_current_coordinates=all_current_coordinates,
                                turn_phase=turn_phase, unique_players=unique_players, possible_attack_points=possible_attack_points, log_comment=log_comment))
    return render_template('arena.html', pl_active_turn=pl_active_turn,
                           all_units_list=all_units_list, all_current_coordinates=all_current_coordinates,
                           turn_phase=turn_phase, unique_players=unique_players, possible_attack_points=possible_attack_points, log_comment=log_comment)


# Базовая страница мастера для выбора инструментов подготовки к сессии
@app.route('/master', methods=['GET'])
def master_home():
    return render_template('master_base.html')


# Страница создания персонажа в БД
@app.route('/master_char', methods=['GET', 'POST'])
def master_char_creation():
    with open('session1/session_init/armour_db.json', 'r') as file:
        arm_bd = json.load(file)
    with open('session1/session_init/weapons_db.json', 'r') as file:
        w_bd = json.load(file)
    if request.method == 'POST':
        try:
            char_init = [request.form.get('unit_id'), request.form.get('coordinates'), request.form.get('player'),
                         request.form.get('armour'), request.form.get('weapon'),
                         request.form.get('unit_class'), request.form.get('strength'),
                         request.form.get('toughness'), request.form.get('reaction'),
                         request.form.get('spirit'), request.form.get('speed'),
                         request.form.get('vitality'), request.form.get('hp'),
                         request.form.get('mp'), request.form.get('mp_regen')]
            print(char_init)
            create_char(*char_init)
            return redirect(url_for('db_result', db_result_var=f'Создан персонаж {char_init}'))
        except:
            return redirect(url_for('db_result', db_result_var='Ошибка создания персонажа'))

    return render_template('master_char.html', arm_bd=arm_bd, w_bd=w_bd)


# Страница создания оружия и брони в БД
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


# Вывод результата создания записи в БД
@app.route('/result', methods=['GET'])
def db_result():
    db_result_var = request.args.get('db_result_var')
    return render_template('db_result.html', db_result_var=db_result_var)


@app.route('/stats/<unique_player>')
def unit_stats(unique_player):
    unit_page = unique_players[unique_players.index(unique_player)]
    unit_page_return = []
    for n in all_units_list:
        if n.player == unit_page:
            unit_page_return.append(n)
    return render_template('stats.html', unit_page_return=unit_page_return)


if __name__ == '__main__':
    app.run(debug=True)

