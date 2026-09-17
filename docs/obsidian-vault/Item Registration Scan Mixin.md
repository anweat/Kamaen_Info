# Item Registration Scan Mixin

Source: `src/main/java/com/anw/kamaen/mixin/RegistryMixin.java`

Mixin config: `src/main/resources/kamaeninfo.mixins.json`

## Purpose

This mixin injects into [[Registry.register]] and logs item registrations whose namespace is `kamaeninfo`.

## Observed Output

`runData` confirmed these registrations:

- [[Raw Kamaen Crystal]]
- [[Tuned Kamaen Crystal]]
- [[Info Probe]]
- [[Fractionating Tower Item]]
- [[Explosion Chamber Controller Item]]
- [[Black Hole Parser Core Item]]

## Related

- [[Minecraft Source CodeGraph]]
- [[Deferred Items]]

