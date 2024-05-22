import time
import json
from mcdreforged.api.all import *


CFG: str = './config/todolist.json'

todo_list = []
help_msg = RTextList(
    RTextList(RText("!!todo", RColor.aqua), " show this message\n"),
    RTextList(RText("!!todo show", RColor.aqua), " show todo list\n")
    .h("show todo list, click to apply")
    .c(RAction.suggest_command, "!!todo show"),
    RTextList(RText("!!todo hide", RColor.aqua), " hide todo list\n")
    .h("hide todo list, click to apply")
    .c(RAction.suggest_command, "!!todo hide"),
    RTextList(RText("!!todo add <task name>", RColor.aqua), " add a task in todo list\n")
    .h("add task into todo list")
    .c(RAction.suggest_command, "!!todo add"),
    RTextList(RText("!!todo remove <task name>", RColor.aqua), " remove a task from todo list")
    .h("remove task from todo list")
    .c(RAction.suggest_command, "!!todo remove")
)


def initialize(server: ServerInterface) -> None:
    todo_list.clear()
    with open(CFG, 'r') as f:
        items = json.load(f)
    for i in items:
        todo_list.append(i)
    reload(server)


def show_help_msg(source: CommandSource) -> None:
    source.reply(help_msg)


def reload(server: ServerInterface) -> None:
    server.execute('gamerule sendCommandFeedback false')
    server.execute('scoreboard objectives remove todo')
    server.execute('scoreboard objectives add todo dummy {"text": "§6§l§o=====[TODO]=====§r"}')
    for i in todo_list:
        server.execute('scoreboard players add ' + str(i) + ' todo ' + str(todo_list.index(i)))
    server.execute('gamerule sendCommandFeedback true')
    with open(CFG, 'w') as w:
        json.dump(todo_list, w)


def showList(source: CommandSource) -> None:
    source.get_server().execute('scoreboard objectives setdisplay sidebar todo')


def hideList(source: CommandSource) -> None:
    source.get_server().execute('scoreboard objectives setdisplay sidebar')


def listList(source: CommandSource) -> None:
    for i in todo_list:
        source.reply(i)


def addList(source: CommandSource, ctx: CommandContext) -> None:
    item: str = ctx['item_id'].replace(' ', '_')
    if item in todo_list:
        source.reply(RTextList(RText("[WARN]", RColor.dark_red), " The item is already in the list!"))
    else:
        todo_list.append(item)
        source.get_server().logger.info(todo_list)
        reload(source.get_server())
        showList(source)


def removeList(source: CommandSource, ctx: CommandContext) -> None:
    item: str = ctx['item_id'].replace(' ', '_')
    if item not in todo_list:
        source.reply(RTextList(RText("[WARN]", RColor.dark_red), " The item is not in the list!"))
    else:
        todo_list.remove(item)
        source.get_server().logger.info(todo_list)
        reload(source.get_server())
        showList(source)


def on_load(server: PluginServerInterface, old) -> None:
    server.register_help_message('!!todo', '服务器任务列表')

    builder = SimpleCommandBuilder()
    builder.command('!!todo', show_help_msg)
    builder.command('!!todo show', showList)
    builder.command('!!todo hide', hideList)
    builder.command('!!todo list', listList)
    builder.command('!!todo add <item_id>', addList)
    builder.command('!!todo remove <item_id>', removeList)

    builder.arg('item_id', GreedyText)
    builder.register(server)

    if server.is_server_startup():
        initialize(server)


def on_server_startup(server: PluginServerInterface) -> None:
    initialize(server)
