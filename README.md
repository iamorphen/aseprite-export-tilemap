# aseprite-export-tilemap

This is based on a fork of
[export-aseprite-file](https://github.com/dacap/export-aseprite-file) by
David Capello. This project uses
[json.lua](https://github.com/rxi/json.lua) by
[rxi](https://github.com/rxi) to export Lua tables to JSON files.

## Example

This script will export data either as JSON or as binary.

```
# binary
aseprite -b map.aseprite --script-param export-type=bin --script export.lua

# JSON
aseprite -b map.aseprite --script-param export-type=json --script export.lua
```

The script will create a folder named `map` in the same parent directory as
`map.aseprite` and will add some files to the new `map` directory. The files
added depend on which export type the user selected.

Read the file documentation of [binary.lua](./binary.lua) to see the schema
of binary output.

<details>
<summary>Expand to see an example of exported JSON data.</summary>
If the JSON export type was selected, one of the emitted files will be
`map/sprite.json` and will have the following example content:

```json
{
  "filename": "map.aseprite",
  "width": 32,
  "height": 32,
  "frames": [
    { "duration": 0.1 },
    { "duration": 0.15 }
  ],
  "layers": [
    {
      "name": "Group Layer",
      "layers": [
        {
          "name": "Common Layer",
          "cels": [
            {
              "bounds": { "x": 10, "y": 13, "width": 12, "height": 13 },
              "frame": 0,
              "image": "map/image1.png"
            },
            {
              "bounds": { "x": 6, "y": 15, "width": 12, "height": 12 },
              "frame": 1,
              "image": "map/image2.png"
            }
          ]
        }
      ]
    },
    {
      "name": "Tilemap Layer",
      "tileset": 0,
      "cels": [
        {
          "bounds": { "x": 0, "y": 0, "width": 32, "height": 32 },
          "data": "text1",
          "frame": 0,
          "tilemap": {
            "width": 4,
            "height": 4,
            "tiles": [
              0, 1, 2, 3,
              4, 5, 5, 6,
              7, 5, 5, 8,
              9, 10, 11, 12
            ]
          }
        },
        {
          "bounds": { "x": 1, "y": 1, "width": 32, "height": 32 },
          "frame": 1,
          "color": "#f7a547",
          "data": "text2",
          "tilemap": {
            "width": 4,
            "height": 4,
            "tiles": [
              0, 1, 1, 3,
              4, 4, 4, 8,
              4, 4, 4, 8,
              9, 10, 10, 12
            ]
          }
        }
      ]
    }
  ],
  "tilesets": [
    {
      "grid": {
        "tileSize": { "width": 8, "height": 8 }
      },
      "image": "map/tileset1.png"
    }
  ],
  "tags": [
    {
      "name": "Tag A",
      "aniDir": "pingpong",
      "color": "#000000",
      "from": 0,
      "to": 2
    },
    {
      "name": "Tag B",
      "aniDir": "forward",
      "color": "#000000",
      "from": 0,
      "to": 1
    },
    {
      "name": "Tag C",
      "aniDir": "reverse",
      "color": "#000000",
      "from": 1,
      "to": 2
    }
  ],
  "slices": [
    {
      "name": "Slice 1",
      "color": "#0000ff",
      "bounds": { "x": 4, "y": 19, "width": 8, "height": 6 }
    },
    {
      "name": "Slice 2",
      "color": "#0000ff",
      "bounds": { "x": 14, "y": 9, "width": 9, "height": 11 },
      "center": { "x": 1, "y": 1, "width": 7, "height": 9 }
    },
    {
      "name": "Slice 3",
      "color": "#0000ff",
      "data": "text3",
      "bounds": { "x": 17, "y": 23, "width": 8, "height": 7 },
      "pivot": { "x": 4, "y": 2 }
    }
  ]
}
```
</details>
