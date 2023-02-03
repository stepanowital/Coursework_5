from flask import Flask, render_template, request, redirect, url_for
from base import Arena
from equipment import Equipment
from classes import unit_classes
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__, template_folder='templates')

heroes = {
    "player": ...,
    "enemy": ...
}

arena = Arena()  # ODO инициализируем класс арены


@app.route("/")
def menu_page():
    # ODO рендерим главное меню (шаблон index.html)
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # ODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    # ODO рендерим экран боя (шаблон fight.html)
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    # ODO кнопка нанесения удара
    # ODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # ODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # ODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    # ODO кнопка использования скилла
    # ODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # ODO кнопка пропуск хода
    # ODO логика практически идентична предыдущему эндпоинту
    # ODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # ODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # ODO кнопка выбор героя. 2 метода GET и POST
    # ODO на GET отрисовываем форму.
    if request.method == 'GET':
        header = "Выберите героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            "header": header,
            "weapons": weapons,
            "armors": armors,
            "classes": unit_classes,
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']

        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        player.equip_armor(Equipment().get_armor(armor_name))
        heroes['player'] = player

        return redirect(url_for('choose_enemy'))
    # ODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # ODO кнопка выбор соперников. 2 метода GET и POST
    # ODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        header = "Выберите противника"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            "header": header,
            "weapons": weapons,
            "armors": armors,
            "classes": unit_classes,
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        heroes['enemy'] = enemy

        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
