# KamaenInfo Mod Entry

Source: `src/main/java/com/anw/kamaen/KamaenInfo.java`

## Links

- Registers [[Deferred Blocks]]
- Registers [[Deferred Items]]
- Registers [[Kamaen Creative Tab]]
- Loads [[Item Registration Scan Mixin]]

## Notes

`KamaenInfo` owns the central NeoForge deferred registers:

- `BLOCKS`
- `ITEMS`
- `CREATIVE_MODE_TABS`

It registers those containers on the mod event bus during construction.

