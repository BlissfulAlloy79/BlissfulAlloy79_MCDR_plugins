from mcdreforged.api.all import *
from litemapy import Schematic, Region, BlockState
from math import floor
from .config import Configuration
import os
import json

psi = ServerInterface.psi()
CFG_DIR: str = psi.get_data_folder()
CFG = os.path.join(CFG_DIR, 'config.json')
LITEMATICA_DIR = os.path.join(CFG_DIR, 'litematica')
MAPPING = os.path.join(CFG_DIR, 'map.json')


def getMapping() -> dict:
    if not os.path.exists(MAPPING):
        raise FileNotFoundError("mapping file `map.json` has not been found")
    with open(MAPPING, 'r', encoding='utf-8') as f:
        return json.load(f)


@new_thread("generate_mapping")
def generateMapping() -> None:
    if not os.listdir(os.path.join(CFG_DIR, 'litematica')):
        raise FileNotFoundError("cannot find any file in the litematica directory")

    cfg = psi.load_config_simple('config.json', target_class=Configuration, in_data_folder=True)

    special_case: dict = cfg.special_case
    ori_x = cfg.origin_pos['x']
    ori_y = cfg.origin_pos['y']
    ori_z = cfg.origin_pos['z']
    litematica_dir = os.path.join(CFG_DIR, "litematica")
    coord_map: dict = {}

    f = os.listdir(litematica_dir)[0]
    schem = Schematic.load(os.path.join(litematica_dir, f))

    for k, reg in schem.regions.items():
        items: dict = {}

        # block processing
        for i in reg.allblockpos():
            block: BlockState = reg.getblock(i[0], i[1], i[2])
            if block.blockid in special_case:
                continue
            items[i] = block.blockid

        # entity processing
        for i in reg.entities:
            try:
                item_id = i.get_tag('Item')['id']
            except KeyError:
                item_id = i.id
            pos = (floor(i.position[0]), floor(i.position[1]), floor(i.position[2]))
            items[pos] = item_id

        # for i in items:
        #     x = ORIGIN_X + reg.x + i[0]
        #     y = ORIGIN_Y + reg.y
        #     z = ORIGIN_Z + reg.z
        #     coord_map[items[i].replace("potted_", "")] = (x, y, z)

        # nah, I don't give a shit about sanity
        x = ori_x + reg.x
        y = ori_y + reg.y
        z = ori_z + reg.z
        tmp: dict = {item.replace("potted_", ""): (x + key[0], y, z + key[2]) for key, item in items.items()}
        coord_map.update(tmp)

    coord_map.update(special_case)

    with open(os.path.join(CFG_DIR, 'map.json'), 'w', encoding='utf-8') as o:
        json.dump(coord_map, o, indent=4)

    return
