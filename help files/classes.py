from dataclasses import dataclass
from skills import FuryPunch, HardShot, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass("Воин", 60, 30, 0.8, 0.9, 1.2, FuryPunch())

ThiefClass = UnitClass("Вор", 50, 25, 1.5, 1.2, 1.0, HardShot())

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}

