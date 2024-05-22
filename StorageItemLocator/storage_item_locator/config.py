from typing import Dict
from mcdreforged.api.utils.serializer import Serializable


class Configuration(Serializable):
    origin_pos: Dict[str, int] = {
        'x': 0,
        'y': 0,
        'z': 0
    }
    special_case: Dict[str, list] = {
        "minecraft:air": [0, 0, 0]
    }
