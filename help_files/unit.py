from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from equipment import Weapon, Armor
from classes import UnitClass
from random import randint


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self._is_skill_used: bool = False

    @property
    def health_points(self) -> float:
        # TODO возвращаем аттрибут hp в красивом виде
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        # TODO возвращаем аттрибут hp в красивом виде
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        # TODO одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        # TODO Эта функция должна содержать:
        # TODO логику расчета урона игрока
        damage = self.weapon.damage * self.unit_class.attack

        # TODO логику расчета брони цели
        # TODO здесь же происходит уменьшение выносливости атакующего при ударе
        self.stamina -= self.weapon.stamina_per_hit

        # TODO и уменьшение выносливости защищающегося при использовании брони
        # TODO если у защищающегося нехватает выносливости - его броня игнорируется
        if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, 1)
        #  TODO после всех расчетов цель получает урон - target.get_damage(damage)
        target.get_damage(damage)

        #  TODO и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        return damage

    def get_damage(self, damage: int) -> None:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        if damage > 0:
            if self.hp - damage > 0:
                self.hp -= damage
            else:
                self.hp = 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернет нам строку, которая характеризует выполнение умения
        """
        if not self._is_skill_used:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        return "Навык уже использован ранее."


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f'"{self.name}" попытался использовать "{self.weapon.name}", но у него не хватило выносливости.'

        damage = self._count_damage(target)

        if damage > 0:
            return (
                f'"{self.name}" используя "{self.weapon.name}" пробивает "{target.armor.name}" '
                f'соперника и наносит {damage} урона.'
            )
        return (
            f'"{self.name}" используя "{self.weapon.name}" наносит удар, но "{target.armor.name}" '
            f'cоперника его останавливает.'
        )


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f'"{self.name}" попытался использовать "{self.weapon.name}", но у него не хватило выносливости.'

        damage = self._count_damage(target)

        if damage > 0:
            return (
                f'"{self.name}" используя "{self.weapon.name}" пробивает "{target.armor.name}" '
                f'и наносит Вам {damage} урона.'
            )
        return (
            f'"{self.name}" используя "{self.weapon.name}" наносит удар, но Ваш(а) "{target.armor.name}" '
            f'его останавливает.'
        )
