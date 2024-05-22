# StorageItemLocator

[image]

In minecraft 1.20, there are more than 1k survival obtainable items

even you got a powerful enough storage to sort all the items, locating them is still a headache in the storage tech community

so here it is, a plugin that helps you locate the item in your storage system

It might seem a little annoying on the setup, but its more of a "set and forget"

> this plugin utilizes `.litematic` files, make sure you are familiar with the [litematica](https://github.com/maruohon/litematica) mod or other similar mods that can produce `.litematic` files

## Commands

`!!ilocate` or `!!ilocate help`: shows help message

`!!ilocate find <item_id>`: locate the item in your storage

`!!ilocate reload`: reload config files

`!!ilcoate generate`: generate item mapping

## Feature

fuzzy match: forgot the damn long item name? no worries

it can still manage to understand at some point

[image]

[image]

## Setup

put the plugin into the `/plguin` directory

start the server or execute `!!MCDR r all` if the server already started

in your server's `/config` directory, you should see a newly generated `/storage_item_locator` files

inside there should be a `/litematica` file and `config.json`

### Creating the litematic file

join your server and open litematica GUI main menu (default pressing M)

set `Area Selection Mode:` into `Normal`

open `Area Selection browser` in the same menu

select `New selection`, name it whatever you want

after creating the new selection, open its `Configure` menu

In the newly opened `Area Editor` menu, turn `Manual Origin` to `ON`

> you can set the Origin coordinates to whatever you like, or just leave it alone

### Selecting regions

it is highly recommended to create a sub-region for each row of items in your storage, as shown below

[image]

you can create a new sub-region in the `Area Editor` menu as mentioned in the previous step

for each row (sub-region), you must include every block and entity (i.e. item frame and armour stand)

below is an example of my row selection (vertical)

[image]

here is another example of my row selection (horizontal)

[image]

save your litematic file

### Configuration

open `/config/storage_item_locator/config.json`

- `origin_pos`:

    enter the coordinate of the origin of the schematic, it can be found in the `Area Editor` menu

- `special_case`:

    see in the examples, the `minecraft:smooth_stone` appears as a filler block for the item frames to attach

    this serves no purpose in locating the smooth_stone item in the storage, so we have to manually record the coord of this item

    go back to your storage and find the real coord for the smooth_stone item, and put them down in the config

i.e.:

```json
"special_case": {
    "minecraft:air": [
        0,
        0,
        0
    ],
    "minecraft:smooth_stone": [
        33,
        47,
        3
    ]
}
```

### Loading

put your `.litematic` files into `/config/storage_item_locator/litematica/`

execute `!!ilocate reload` and `!!ilocate generate`

done!

