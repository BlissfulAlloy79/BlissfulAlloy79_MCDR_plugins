# ScoreboardTodoList

A plugin that utilizes scoreboard to use it as a simple todo list

`!!todo` or shows the help message

`!!todo show` shows the todo scoreboard

`!!todo hide` hides the todo scoreboard

`!!todo list` lists the entire todo list

`!!todo add <item_id>` adds an item into the todo list

`!!todo remove <item_id>` removes an item from the todo list

> `<item_id>` supports greedyText, so you can use space in the id
> 
> i.e. in `!!todo add get cherry wood` it will auto parse the `<item_id>` into `get_cherry_wood`

todo items will be stored in the config files `/config/todolist.json`

