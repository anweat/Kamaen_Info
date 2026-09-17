# Kamaen Info Graph

This vault is a small Obsidian-facing knowledge graph for the mod.

## Entry Points

- [[KamaenInfo Mod Entry]]
- [[Item Registration Scan Mixin]]
- [[Minecraft Source CodeGraph]]
- [[Visualization Options]]

## Current Flow

```mermaid
flowchart LR
    Gradle["Gradle createMinecraftArtifacts"] --> Sources["NeoForge/Minecraft sources jar"]
    Sources --> CodeGraph["Minecraft Source CodeGraph"]
    CodeGraph --> Registry["Registry.register"]
    Registry --> Mixin["Item Registration Scan Mixin"]
    Mixin --> Log["kamaeninfo item registration logs"]
```

