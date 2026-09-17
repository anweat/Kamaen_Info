# Kamaen Info Resonance, Crystal, and Early Game Design

> Status: discussion baseline
> Scope: Kamaen crystal, early mechanical synthesis, resonance/separation platform, resource production, biological resource route, sensors, and data interfaces.

## 1. Design Position

The early and mid game should not be limited by raw energy. Power can appear early, but progress is limited by resonance control, phase stability, crystal quality, stress control, and analysis capability.

The central fantasy is:

```text
Matter has frequency.
Crystals carry and shape frequency.
Mechanical shock writes stress.
Power supplies phase.
Machines resonate, separate, analyze, and specialize.
```

The mod should keep vanilla material ecology mostly intact. New non-vanilla raw world resources should be minimized. Most new materials are processed products made from vanilla items and blocks.

Kamaen ore may exist as an optional world-generation resource, but it must not be mandatory for the main progression.

## 2. Kamaen Crystal Definition

Kamaen crystal is the core artificial frequency crystal of the mod.

Its main route is not mining:

```text
Cobblestone broad-spectrum matter
→ purification
→ seed-induced crystallization
→ crude Kamaen crystal
→ analyzed, stressed, annealed, specialized Kamaen crystal
```

Kamaen ore is optional:

```text
Kamaen ore
→ natural Kamaen crystal sample
→ natural seed / shortcut / high-quality reference material
```

It should help players skip some preparation or obtain better starting samples, but every required mainline step should remain possible without mining Kamaen ore.

## 3. Cobblestone as Broad-Spectrum Matter

Cobblestone is the unique broad-spectrum material.

It does not mean cobblestone is strong in every frequency. It means cobblestone weakly covers a very wide frequency range, making it suitable as:

- The base matter for Kamaen crystal production.
- A low-efficiency resonance fallback.
- A calibration and background reference material.
- A resource production substrate.

Design interpretation:

```text
Cobblestone contains weak, noisy, broad-spectrum mineral information.
Purification extracts stable frequency structures from this broad noise.
Crystal seeds lock selected structures into a Kamaen crystal lattice.
```

## 4. Kamaen Crystal Internal State

Kamaen crystals should support rich internal state, but the player-facing UI can reveal it gradually.

Recommended internal model:

```text
KamaenCrystalState
- spectrum
- stressTensor
- defectProfile
- orientation
- purity
- traits
```

### 4.1 Spectrum

The spectrum is the crystal's frequency response.

It may include:

- Main peaks.
- Peak width.
- Peak intensity.
- Harmonics.
- Side peaks.
- Noise floor.
- Axis response.
- Phase response.

This does not need to be fully visible at the beginning. Early tools can expose only rough main frequency and quality.

### 4.2 Stress Tensor

The internal stress state should use a tensor-like representation.

Recommended form:

```text
stressTensor =
[ σxx  τxy  τxz
  τxy  σyy  τyz
  τxz  τyz  σzz ]
```

This allows:

- Single-axis compression.
- Multi-axis compression.
- Stretching.
- Shear stress.
- Stress not aligned to the visible crystal axes.
- Smooth stress ellipsoid rendering.

The stress ellipsoid is a visualization of this tensor. Its axes are derived from eigenvalues and eigenvectors.

### 4.3 Defect Profile

Defects should be treated as real internal features, not just a single quality number.

Possible defect categories:

- Vacancy-like defects.
- Dislocation-like defects.
- Crack-like defects.
- Impurity clusters.
- Chaotic microstructure.

For gameplay, these can still be compressed into discrete display levels:

```text
Low / medium / high defect density
Known / unknown defect type
Localized / distributed defect pattern
```

### 4.4 Traits as Prior Properties

Kamaen crystals may have special traits. These traits are real crystal properties, not just derived labels.

They act as prior hidden or semi-hidden properties. Analysis turns them into posterior observations.

Example traits:

- Harmonic amplification.
- Phase delay.
- Axis locking.
- Broad-spectrum absorption.
- Stress focusing.
- Defect self-stabilization.
- Reverse phase response.
- Shock sensitivity.
- Thermal stability.
- Product bias.

Note: traits such as **axis locking**, **harmonic amplification**, **phase delay** and **broad-spectrum absorption** are the early-game precursors to the mid-game optical computing tier (Stage 6). The "waveguide" (导波) and "stable spectrum" (稳谱) crystal lines produced in Stages 2–3 are the raw material for Stage 6's silicon photonic waveguides and single-frequency laser sources respectively (see `docs/Kamaen_Info_Optical_Computing_Design.md` §3 for the process chain). Players who care about traits early can already plan toward optical hardware, but it is not required for main-line progression up to Stage 5.

Trait instance model:

```text
CrystalTraitInstance
- traitId
- strength
- directionBias
- frequencyBand
- stressAnchor
- revealLevel
```

Analysis does not need to immediately show trait names. It can first reveal effects:

```text
Unknown high-frequency side peak
Localized stress ellipsoid protrusion
Unusual noise suppression
Stable defect island
Phase lag around a specific axis
```

Later analysis can identify:

```text
Unknown anomaly
→ suspected harmonic amplification
→ confirmed second-order harmonic amplification
```

### 4.5 Stress Ellipsoid Trait Expression

Special traits can appear as local changes on the stress ellipsoid.

The base ellipsoid comes from the stress tensor. Traits add localized visual and analytical anomalies.

Examples:

```text
Stress focusing:
  Local spike or bright region on the ellipsoid.

Axis locking:
  Stable ring or band near the main axis.

Phase delay:
  Rotationally shifted ripple pattern.

Defect self-stabilization:
  Defect-heavy region appears smoother than expected.

Broad-spectrum absorption:
  Thicker, duller ellipsoid and broad absorption valley in spectrum.
```

The internal representation may use discrete data, but rendering should interpolate smoothly.

## 5. Frequency and Resonance Rules

Every registered object that participates in the system can have an intrinsic spectrum:

```text
Item / block / fluid / processed material
→ intrinsic spectrum
```

This spectrum is used for:

- Resonance-enhanced crafting.
- Byproduct amplification.
- Crystal specialization.
- Research comparison.
- Machine calibration.

Core concept:

```text
Recipe target frequency
+ input material spectrum
+ Kamaen crystal resonance
+ power phase stability
+ machine specialization
→ speed, yield, purity, byproduct weights, and output parameters
```

Multiple matching frequency components can stack strongly. High upper limits are acceptable, especially for late-game tuning, but should be gated by crystal purity, phase stability, machine tier, and analysis capability.

## 6. Power, Phase, and Machine Stability

Power appears early, but power quality matters.

Each machine can have a supply stability factor. This may affect:

- Crafting speed.
- Output purity.
- Defect generation.
- Byproduct selection.
- Crystal stress drift.
- Analysis precision.

Power properties:

- Voltage stability.
- Frequency stability.
- Phase stability.
- Waveform purity.
- Load fluctuation.

Three-phase power can interact with crystal axes:

```text
Crystal X/Y/Z axes
↔
Power phase A/B/C
```

Players can later rotate crystals, remap phases, or install phase-control modules.

Early game should not require deep phase control. It can start as rough matching and become explicit later.

## 7. Early Mechanical and Explosive Synthesis

The early game should include primitive mechanical technologies before stable resonance machines.

Important early tools:

- Portable explosion chamber.
- TNT explosion chamber.
- Basic resonant assembly platform.

Explosive synthesis is not only destruction. It is the earliest way to write stress into matter.

Explosion parameters can affect:

- Stress tensor.
- Defect density.
- Crack pattern.
- Temperature spike.
- Cooling rate.
- Spectrum shift.
- Trait expression chance.

### 7.1 Portable Explosion Chamber

Purpose:

- First manual shock synthesis.
- Low throughput.
- High variance.
- Safer and easier to place.
- Used before large multiblocks.

It can create:

- Crude powders.
- Shocked mineral mixtures.
- First crude Kamaen crystallization ingredients.
- Early stressed crystal samples.

### 7.2 TNT Explosion Chamber

Purpose:

- Larger early shock synthesis.
- Batch processing.
- Stronger stress writing.
- More dangerous or more structure-dependent.

It should remain relevant as a rough stress-writing tool, even after better machines exist.

## 8. Basic Synthesis Platform

The early game needs a basic crafting platform before multiblock machines.

Working name:

```text
Resonant Assembly Table
```

Purpose:

- Craft basic components.
- Perform low-precision frequency matching.
- Process crude crystals.
- Create initial multiblock blocks.
- Bridge explosion chambers and resonance/separation arrays.

Possible UI:

```text
Input slots
Crystal or seed slot
Manual tuning control
Output slot
Basic match display
```

It should support imperfect crafting. Bad matching may lower speed, consume extra material, or produce lower-quality output, but should not hard-block all early progress.

## 9. Basic Components

The component line should mostly use vanilla materials.

Example components:

- Copper wire.
- Copper plate.
- Gold contact.
- Quartz lens.
- Amethyst clamp.
- Phase coil.
- Resonance frame.
- Separation grid.
- Sensor port.
- Fluid interface.
- Item interface.
- Blast isolation plate.
- Broad-spectrum calibration block.

Example material logic:

```text
Copper:
  Conductive structure, wire, coils, heat exchange.

Iron:
  Mechanical frame, load-bearing structure.

Gold:
  Low-loss contacts and precision terminals.

Redstone:
  Signal, phase modulation, low-frequency control.

Quartz:
  High-frequency reference and lens-like precision component.

Amethyst:
  Crystal seed, anisotropic resonance, axis gameplay.

Glass:
  Vessel, lens, transparent analysis part.

Obsidian / deepslate:
  Blast isolation and high-stress containment.
```

## 10. Resonance and Separation Multiblock Platform

The main industrial and research machine should be a unified upgradeable multiblock platform.

Working name:

```text
Resonance Separation Array
```

It should act as:

- Resource production platform.
- Crystal analysis table.
- Resonance crafting platform.
- Separation machine.
- Research instrument.
- Sensor/data platform.

The machine's base structure handles resonance and separation. Extensions define specialized usage.

### 10.1 Base Structure

Possible blocks:

- Control core.
- Resonance chamber wall.
- Separation frame.
- Crystal holder.
- Item interface.
- Fluid interface.
- Power interface.
- Sensor port.

Minimum size can be small, then expanded.

Example tiers:

```text
Tier 1: Single-chamber array
  Small structure.
  One crystal slot.
  Rough scanning.
  Basic mineral separation and crude crystal work.

Tier 2: Dual-chamber array
  More output channels.
  Three crystal slots.
  Three-phase power support.
  Sensor support.

Tier 3: Array resonance system
  Multiple resonance zones.
  Stress ellipsoid visualization.
  Trait identification.
  Automation data interface.

Tier 4: Field-controlled array
  Frequency editing.
  Doping-like control.
  Advanced crystal engineering.
  Semiconductor-like components.
```

### 10.2 Extensions

Extensions specialize the unified platform:

- Mineral separation extension.
- Biological separation extension.
- Crystal growth extension.
- Stress processing extension.
- Phase control extension.
- Analysis/research extension.
- Data interface extension.

This avoids many unrelated machine families while still supporting many functions.

## 11. Resource Production and Byproduct Resonance

The mod should include machines for mass resource production.

Resource production is not simple duplication. It is resonance-biased extraction from broad or suitable substrates.

Core rule:

```text
Target byproduct has intrinsic frequency.
If input material, machine frequency, crystal resonance, and power phase match it,
the target byproduct weight increases.
```

General formula concept:

```text
targetWeight =
baseContent
× inputSpectrumCoverage
× targetFrequencyMatch
× crystalResonanceMultiplier
× powerStabilityFactor
× machineSpecialization
```

Specialized Kamaen crystals can enhance specific byproduct channels.

Examples:

- Silicate-biased crystal for quartz/silicate products.
- Copper-biased crystal for copper traces.
- Iron-magnetic crystal for iron traces.
- Redstone-phase crystal for redstone-like products.
- Glow-frequency crystal for glowstone/light-related products.
- Seed-biased crystal for Kamaen crystal nuclei.

These crystals can be produced by training, doping, resonance treatment, or exposure to vanilla samples.

## 12. Mineral Resource Route

Mineral production uses vanilla block substrates.

Inputs:

- Cobblestone.
- Deepslate.
- Gravel.
- Sand.
- Basalt.
- Netherrack.
- End stone.

Example route:

```text
Stone-like substrate
→ broad-spectrum crushing / slurry
→ resonance separation
→ main mineral powder
→ frequency-biased byproducts
```

Example outputs:

- Silicate powder.
- Iron trace powder.
- Copper trace powder.
- Redstone-phase dust.
- Quartz-like product.
- Kamaen crystal nuclei.

Dimensional materials can gate corresponding rare resources:

```text
Netherrack / basalt:
  Better for Nether-related byproducts.

End stone:
  Better for Ender-phase byproducts.
```

## 13. Biological Resource Route

Biological resources should use the same frequency/resonance logic.

It should not simply replace mob farms with free generation. It should require organic substrates and frequency samples.

Example route:

```text
Plant / bone / rotten flesh / fungus / slime / other organic input
→ organic slurry
→ life-spectrum separation
→ biological byproducts
```

Machine extensions:

- Biological separation extension.
- Cultivation sedimentation extension.
- Organic resonance reactor.
- Phase sterilization or stabilization module.

Biological frequency groups:

```text
Plant frequency:
  Seeds, fiber, paper-like pulp, dye precursors.

Animal structure frequency:
  Bone, calcium, leather/collagen, feather/keratin, wool fiber.

Viscoelastic frequency:
  Slime, honey, wax, resin-like products.

Decay/fungal frequency:
  Rotten flesh components, mushroom spores, fermented matter, Nether wart-like precursor.

Hostile creature frequency:
  Gunpowder precursor, spider silk protein, Ender-phase residue, Blaze heat residue.
```

Rare biological products should require samples:

```text
String or spider eye:
  Unlocks spider-silk frequency.

Gunpowder:
  Unlocks nitrated explosive frequency.

Blaze powder or blaze rod:
  Unlocks blaze heat frequency.

Ender pearl:
  Unlocks Ender-phase biological route.
```

The sample provides target frequency. Organic slurry provides matter. Crystal and machine resonance amplify the desired output.

## 14. Sensors and Data Interfaces

Sensors should be supported from the multiblock platform stage onward.

Early support can be redstone threshold output. Later support can provide structured data for automation, displays, and control systems.

Sensor types:

- Spectrum sensor.
- Stress sensor.
- Phase sensor.
- Product prediction sensor.
- Defect sensor.
- Trait anomaly sensor.

Basic redstone examples:

```text
Resonance match > threshold
Output buffer full
Phase unstable
Target byproduct detected
Defect level too high
```

Advanced data examples:

```text
frequency.main
frequency.noise
stress.tensor
stress.eigenvalues
stress.eigenvectors
phase.deltaAB
phase.deltaBC
product.predictedYield
trait.unknownAnomalyCount
```

The data interface should prepare for later computational systems without requiring them in the early game.

## 15. Early Progression Summary

Recommended early progression:

```text
Vanilla crafting
→ portable explosion chamber
→ crude powder and shock processing
→ resonant assembly table
→ basic components
→ crude Kamaen crystal from cobblestone purification and crystal seed
→ TNT explosion chamber
→ stronger stress writing and batch processing
→ first resonance separation array
→ mineral resource route
→ crystal analysis and refinement
→ biological resource route
→ phase control and sensors
→ larger specialized multiblock arrays
```

The early stage tone:

```text
Modern but rough.
Powered but not precise.
Experimental rather than primitive.
Built on explosions, cobblestone, seeds, manual tuning, and imperfect analysis.
```

## 16. Open Issues for Later

The following items are intentionally not solved in this document:

- Exact numeric formulas for resonance multiplier.
- Exact crystal generation algorithm.
- Full trait list and balancing.
- Whether machine recipes consume or only reference crystal parameters.
- How to prevent byproduct amplification from breaking vanilla resource balance.
- How much UI information should be shown at each research stage.
- How phase control should interact with existing Minecraft automation.
- Exact multiblock dimensions and validation rules.
- Conflict resolution with existing hardware tech tree documents.

