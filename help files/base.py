from typing import Optional

from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        # ODO НАЧАЛО ИГРЫ -> None
        # ODO присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        # ODO а также выставляем True для свойства "началась ли игра"
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        # ODO ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        # ODO проверка здоровья игрока и врага и возвращение результата строкой:
        # ODO может быть три результата:
        # ODO Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        # ODO если Здоровья игроков в порядке то ничего не происходит
        if self.enemy.hp > 0 and self.player.hp > 0:
            return None

        if self.enemy.hp <= 0 and self.player.hp <= 0:
            self.battle_result = "Ничья"
        elif self.player.hp <= 0:
            self.battle_result = "Игрок проиграл битву"
        elif self.enemy.hp <= 0:
            self.battle_result = "Игрок выиграл битву"
        return self._end_game()

    def _stamina_regeneration(self) -> None:
        # ODO регенерация здоровья и стамины для игрока и врага за ход
        # ODO в этом методе к количеству стамины игрока и врага прибавляется константное значение.
        # ODO главное чтобы оно не привысило максимальные значения (используйте if)
        units = (self.player, self.enemy)
        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> str:
        # ODO СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        # ODO срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        # ODO создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        # ODO если result -> возвращаем его
        # ODO если же результата пока нет и после завершения хода игра продолжается,
        # ODO тогда запускаем процесс регенерации стамины и здоровья для игроков (self._stamina_regeneration)
        # ODO и вызываем функцию self.enemy.hit(self.player) - ответный удар врага
        result = self._check_players_hp()
        if result is not None:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        # ODO КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        # ODO очищаем синглтон - self._instances = {}
        self._instances = {}
        # ODO останавливаем игру (game_is_running)
        self.game_is_running = False
        # ODO возвращаем результат
        return self.battle_result

    def player_hit(self) -> str:
        # ODO КНОПКА УДАР ИГРОКА -> return result: str
        # ODO получаем результат от функции self.player.hit
        # ODO запускаем следующий ход
        # ODO возвращаем результат удара строкой
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()

        result_enemy = self._check_players_hp()
        if result_enemy is not None:
            return f"{result}\n{turn_result}\n{result_enemy}"

        return f"{result}\n{turn_result}"

    def player_use_skill(self) -> str:
        # ODO КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # ODO получаем результат от функции self.use_skill
        # ODO включаем следующий ход
        # ODO возвращаем результат удара строкой
        result = self.player.use_skill(self.enemy)
        turn_result = self.next_turn()

        result_enemy = self._check_players_hp()
        if result_enemy is not None:
            return f"{result}\n{turn_result}\n{result_enemy}"

        return f"{result}\n{turn_result}"
