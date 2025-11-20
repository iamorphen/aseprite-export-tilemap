"""Parse a binary-encoded tilemap export file and print contents to stdout."""

import argparse
import sys
from struct import unpack_from

"""
Parse a u8 stored offset into bytes. Returns the parsed value and the next index
into bytes.
"""
def unpack_u8(b: bytes, offset: int) -> (int, int):
    return (unpack_from("<B", b, offset)[0], offset + 1)

"""
Parse a u16 stored offset into bytes. Returns the parsed value and the next
index into bytes.
"""
def unpack_u16(b: bytes, offset: int) -> (int, int):
    return (unpack_from("<H", b, offset)[0], offset + 2)

"""
Parse a u64 stored offset into bytes. Returns the parsed value and the next
index into bytes.
"""
def unpack_u64(b: bytes, offset: int) -> (int, int):
    return (unpack_from("<Q", b, offset)[0], offset + 8)

"""
Parse a string the_len bytes long stored offset into bytes. Returns the parsed
string and the next index into bytes.
"""
def unpack_str(b: bytes, offset: int, the_len: int) -> (str, int):
    return (
        unpack_from(f"{the_len}s", b, offset)[0].decode("utf-8"),
        offset + the_len
    )

"""
Parse an array of u16 stored offset into bytes. Returns the parsed array and the
next index into bytes.
"""
def unpack_array_u16(b: bytes, offset: int) -> (list[int], int):
    (the_len, i) = unpack_u64(b, offset)
    array_as_tuple = unpack_from(f"<{the_len}H", b, i)
    assert the_len == len(array_as_tuple)
    i += the_len * 2

    return (list(array_as_tuple), i)

"""Pretty print a list of tiles, adding a newline every width tiles."""
def pretty_print_tiles(tiles: list[int], width: int) -> None:
    elem_width = len(str(max(tiles)))
    for i in range(0, len(tiles)):
        print(f"{tiles[i]:0{elem_width}d},", end="")
        if (i + 1) % width == 0:
            print()
        else:
            print(" ", end="")

"""
Parse and print the schema version stored offset into bytes. Return the next
index into bytes.
"""
def parse_schema_version(b: bytes, offset: int) -> int:
    (major, i) = unpack_u8(b, offset)
    (minor, i) = unpack_u8(b, i)
    (patch, i) = unpack_u8(b, i)
    print(f"schema version: {major}.{minor}.{patch}")

    return i

"""
Parse and print the canvas dimensions stored offset into bytes. Return the
next index into bytes.
"""
def parse_canvas_dimensions(b: bytes, offset: int) -> int:
    (width, i) = unpack_u16(b, offset)
    (height, i) = unpack_u16(b, i)
    print(f"canvas width, height (px): ({width}, {height})")

    return i

"""
Parse and print a string stored offset into bytes. Return the next index into
bytes.
"""
def parse_string(b: bytes, offset: int) -> (str, int):
    (the_len, i) = unpack_u64(b, offset)
    (the_str, i) = unpack_str(b, i, the_len)

    return (the_str, i)

"""
Parse and print tilesets stored offset into bytes. Return the next index into
bytes.
"""
def parse_tilesets(b: bytes, offset: int) -> int:
    (num_tilesets, i) = unpack_u64(b, offset)
    print(f"num_tilesets: {num_tilesets}")

    for tileset in range(0, num_tilesets):
        print()
        print(f"tileset {tileset}:")
        (image_pathname, i) = parse_string(b, i)
        print(f"image pathname: \"{image_pathname}\"")
        (tile_width_px, i) = unpack_u16(b, i)
        (tile_height_px, i) = unpack_u16(b, i)
        print(f"tile width, height (px): ({tile_width_px}, {tile_height_px})")

    return i

"""
Parse and print layers stored offset into bytes. Return the next index into
bytes.
"""
def parse_layers(b: bytes, offset: int, hide_tiles: bool) -> int:
    (num_layers, i) = unpack_u64(b, offset)
    print(f"num layers: {num_layers}")

    for layer in range(0, num_layers):
        print()
        print(f"layer {layer}:")
        (name, i) = parse_string(b, i)
        print(f"name: \"{name}\"")
        (tileset_id, i) = unpack_u16(b, i)
        print(f"tileset id: {tileset_id}")
        (width_tiles, i) = unpack_u16(b, i)
        (height_tiles, i) = unpack_u16(b, i)
        print(f"width, height (tiles): ({width_tiles}, {height_tiles})")
        (tiles, i) = unpack_array_u16(b, i)
        if not hide_tiles:
            pretty_print_tiles(tiles, width_tiles)
            print()

    return i

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("binary_file", help="pathname to exported binary file")
    parser.add_argument(
        "--hide-tiles",
        help="don't print layer tile contents",
        action="store_true"
    )
    args = parser.parse_args()

    try:
        with open(args.binary_file, "rb") as f:
            file_bytes = f.read()
    except Exception as e:
        print(f"Error when opening file: {e}")

    i = parse_schema_version(file_bytes, 0)
    i = parse_canvas_dimensions(file_bytes, i)
    i = parse_tilesets(file_bytes, i)
    i = parse_layers(file_bytes, i, args.hide_tiles)

    if len(file_bytes) != i:
        print()
        print(f"warning: {len(file_bytes) - i} unparsed bytes remaining")

if __name__ == "__main__":
    main()
