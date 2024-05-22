from .config import Configuration
from .utils import *
import os
import difflib

help_msg = RTextList(
    RText("Commands:", styles=[RStyle.bold, RStyle.italic]),
    "\n",
    RTextList(RText("!!ilocate", RColor.gold), " show this message")
    .h("click me to apply")
    .c(RAction.suggest_command, "!!ilocate help"),
    "\n",
    RTextList(RText("!!ilocate help", RColor.gold), " show this message")
    .h("click me to apply")
    .c(RAction.suggest_command, "!!ilocate help"),
    "\n",
    RTextList(RText("!!ilocate find <item_id>", RColor.gold), " locate item <item_id> in storage")
    .h("click me to apply")
    .c(RAction.suggest_command, "!!ilocate find "),
    "\n",
    RTextList(RText("!!ilocate reload", RColor.gold), " reload all config files")
    .h("click me to apply")
    .c(RAction.suggest_command, "!!ilocate reload"),
    "\n",
    RTextList(RText("!!ilocate generate", RColor.gold), " generate item mapping from litematica file")
    .h("click me to apply")
    .c(RAction.suggest_command, "!!ilocate generate")
)

psi = ServerInterface.psi()
CFG_DIR: str = psi.get_data_folder()
CFG = os.path.join(CFG_DIR, 'config.json')
LITEMATICA_DIR = os.path.join(CFG_DIR, 'litematica')
MAPPING = os.path.join(CFG_DIR, 'map.json')
item_map: dict = {}


def loadConfig() -> None:
    global item_map
    try:
        item_map = getMapping()
    except FileNotFoundError:
        psi.broadcast(RTextList(
            RText("[WARN]", RColor.dark_red),
            " failed to load item mapping, please check the mapping file"
        ))
    return


def initialize() -> None:
    global item_map
    if not os.path.exists(CFG_DIR):
        os.makedirs(CFG_DIR)
    if not os.path.exists(LITEMATICA_DIR):
        os.makedirs(LITEMATICA_DIR)
    if not os.path.exists(CFG):
        psi.load_config_simple('config.json', target_class=Configuration, in_data_folder=True)
    if os.listdir(LITEMATICA_DIR):
        generateMapping()

    loadConfig()

    return


def showHelpMsg(source: CommandSource) -> None:
    source.reply(help_msg)
    return


def reloadConfig(source: CommandSource) -> None:
    global item_map
    try:
        item_map = getMapping()
    except FileNotFoundError:
        source.reply(RTextList(
            RText("[WARN]", RColor.dark_red),
            " failed to load item mapping, please check the mapping file"
        ))
    return


def generate_mapping(source: CommandSource) -> None:
    try:
        source.reply("Generating item coord mapping...")
        generateMapping()
    except FileNotFoundError as e:
        source.reply(RTextList(
            RText("[WARN]", RColor.dark_red),
            f" {e}"
        ))
        return

    source.reply("item coord map generated, reloading config...")
    reloadConfig(source)
    source.reply("finished!")


def getItemLocation(source: CommandSource, ctx: CommandContext) -> None:
    item = ctx.command.split(' ')[2]

    # minecraft:grass_block
    if not item.startswith("minecraft:"):
        item = f"minecraft:{item}"

    if item not in item_map:
        close_match = difflib.get_close_matches(item, list(item_map.keys()), 2)
        reply_msg = RTextList(
            RText("[WARN]", RColor.dark_red),
            f" The query item is not in the record"
            )
        if len(close_match) == 0:
            reply_msg.append(", please check your spelling!")
            reply_msg.append("\n")
            reply_msg.append(RText("i.e. minecraft:grass_block", RColor.gray, RStyle.italic))
        if len(close_match) >= 1:
            reply_msg.append(", perhaps you meant ")
            reply_msg.append(
                RText(close_match[0], RColor.gray, RStyle.italic)
                .h("click me to apply")
                .c(RAction.suggest_command, f"!!ilocate find {close_match[0]}")
            )
        if len(close_match) == 2:
            reply_msg.append(" or ")
            reply_msg.append(
                RText(close_match[1], RColor.gray, RStyle.italic)
                .h("click me to apply")
                .c(RAction.suggest_command, f"!!ilocate find {close_match[1]}")
            )

        source.reply(RTextList(reply_msg))
        return

    server = source.get_server()
    x = item_map[item][0]
    y = item_map[item][1]
    z = item_map[item][2]
    server.execute(
        f"summon falling_block {x} {y} {z} {{Time:200, DropItem:0b, BlockState:{{Name:'minecraft:white_stained_glass'}}, NoGravity:1b, Glowing:1b, Tags:['blockHighlight']}}")
    source.reply(f"{item} is at [{x}, {y}, {z}]")


# def getCommands() -> Literal:
#     # ngl, this is a very hacky way to accomplish it, and I have no idea why am I doing this at this point
#     find_node: Literal = (
#         Literal('find')
#         .then(
#             Text('item_id')
#             .suggests(lambda: item_map.keys())
#             .runs(getItemLocation)
#         )
#     )
#
#     for i in item_map.keys():
#         find_node.then(Literal(f'{i}').runs(getItemLocation))
#
#     base_node: Literal = (
#         Literal('!!ilocate')
#         .runs(showHelpMsg)
#         .then(
#             Literal('help')
#             .runs(showHelpMsg)
#         )
#         .then(
#             Literal('reload')
#             .runs(loadConfig)
#         )
#         .then(
#             Literal('generate')
#             .runs(generate_mapping)
#         )
#         .then(
#             find_node
#         )
#     )
#
#     base_node.print_tree(psi.logger.info)
#     return base_node

# forget it, its not gonna work


def on_load(server: PluginServerInterface, old) -> None:
    initialize()

    server.register_help_message('!!ilocate', 'locate item in storage')
    server.register_command(
        Literal('!!ilocate')
        .runs(showHelpMsg)
        .then(
            Literal('help')
            .runs(showHelpMsg)
        )
        .then(
            Literal('reload')
            .runs(loadConfig)
        )
        .then(
            Literal('generate')
            .runs(generate_mapping)
        )
        .then(
            Literal('find')
            .then(
                Text('item_id')
                .runs(getItemLocation)
            )
        )
    )

# TODO: rewrite loading logic with plugin reload
# todo: separate functional and responsive function

