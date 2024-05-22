# StorageItemLocator

![ilocate_find](https://github.com/BlissfulAlloy79/BlissfulAlloy79_MCDR_plugins/assets/45236703/7a46c59c-81c7-4780-80f8-bf7308c89a2b)


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

![fuzzy_match](https://github.com/BlissfulAlloy79/BlissfulAlloy79_MCDR_plugins/assets/45236703/622c5702-4ba4-4c45-a4b4-816d8293c7dc)

![fuzzy_match_1](https://github.com/BlissfulAlloy79/BlissfulAlloy79_MCDR_plugins/assets/45236703/5c9196fe-a142-4a9b-b12d-9d7eb49c6210)

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

![selection_example](https://github.com/BlissfulAlloy79/BlissfulAlloy79_MCDR_plugins/assets/45236703/0ff011bd-3101-4fed-9112-fd89c08cac0c)

you can create a new sub-region in the `Area Editor` menu as mentioned in the previous step

for each row (sub-region), you must include every block and entity (i.e. item frame and armour stand)

below is an example of my row selection (vertical)

![sub-region_example](https://github.com/BlissfulAlloy79/BlissfulAlloy79_MCDR_plugins/assets/45236703/715df5b3-7984-4bcf-a4e5-6ac41f556152)

here is another example of my row selection (horizontal)

![sub-region_example_2](https://github.com/BlissfulAlloy79/BlissfulAlloy79_MCDR_plugins/assets/45236703/de6f9a5e-8112-4847-aafb-f21d39124f7f)

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

