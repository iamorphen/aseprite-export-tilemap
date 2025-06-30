-- Export an Aseprite tilemap and supporting data to a binary file.
--
-- Output Schema
-- -------------
-- schema_major_ver: uint8_t
-- schema_minor_ver: uint8_t
-- schema_patch_ver: uint8_t
-- canvas_width_px : uint16_t
-- canvas_height_px: uint16_t
-- tilesets        : array<tileset>
-- layers          : array<layer>
--
-- array
-- -----
-- An array `array<T>` is a single `uint64_t` indicating the number of instances
-- of `T` immediately after. The instances of `T` are contiguous in memory.
-- For example, a 2-element array of type `array<uint8_t>` is laid out as
-- follows in memory:
--   uint64_t (num elements)
--   uint8_t  (first element)
--   uint8_t  (second element)
--
-- string
-- ------
-- A string is a single `uint64_t` indicating the number of characters
-- immediately following and then said number of characters. The characters are
-- 8-bit bytes. Each byte is a single ASCII character.
--
-- tileset
-- -------
-- image_pathname: string
-- tile_width_px : uint16_t
-- tile_height_px: uint16_t
--
-- layer
-- -----
-- name        : string
-- tileset_id  : uint16_t
-- width_tiles : uint16_t
-- height_tiles: uint16_t
-- tiles       : array<index_into_tileset>
--
-- index_into_tileset
-- ------------------
-- index: uint16_t
--
-- Notes:
-- - Strings do not support Unicode.
-- - All numbers are encoded as little-endian.
-- - The current schema only supports a single cel per layer.

local binary = { _version_major = 0, _version_minor = 0, _version_patch = 1 }

-- Write select keys out of table `t` to the open file `f` as binary. See
-- the output schema in the file documentation for what will be written out to
-- `f`.
function binary.encode(f, t)
  -- Schema version.
  f:write(string.pack("<I1", binary._version_major))
  f:write(string.pack("<I1", binary._version_minor))
  f:write(string.pack("<I1", binary._version_patch))

  -- Canvas width, height.
  f:write(string.pack("<I2", t.width))
  f:write(string.pack("<I2", t.height))

  -- Tilesets.
  f:write(string.pack("<I8", #t.tilesets))
  for i = 1, #t.tilesets do
    local ts = t.tilesets[i]
    f:write(string.pack("<I8", #ts.image))
    f:write(ts.image)
    f:write(string.pack("<I2", ts.grid.tileSize.width))
    f:write(string.pack("<I2", ts.grid.tileSize.height))
  end

  -- Layers.
  f:write(string.pack("<I8", #t.layers))
  for i = 1, #t.layers do
    local l = t.layers[i]
    f:write(string.pack("<I8", #l.name))
    f:write(l.name)
    f:write(string.pack("<I2", l.tileset))

    if #l.cels > 1 then
      error("Layer " .. i .. " has more than 1 cel")
    end

    local cel = l.cels[1]
    f:write(string.pack("<I2", cel.tilemap.width))
    f:write(string.pack("<I2", cel.tilemap.height))
    f:write(string.pack("<I8", #cel.tilemap.tiles))
    for j = 1, #cel.tilemap.tiles do
      f:write(string.pack("<I2", cel.tilemap.tiles[j]))
    end
  end
end

return binary
