package com.anw.kamaen;

import net.neoforged.fml.event.config.ModConfigEvent;
import net.neoforged.neoforge.common.ModConfigSpec;

public class Config {
    private static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();

    public static final ModConfigSpec.BooleanValue ENABLE_WORLDGEN_PLACEHOLDERS = BUILDER
            .comment("Reserved toggle for future Kamaen crystal world generation hooks.")
            .define("enableWorldgenPlaceholders", false);

    public static final ModConfigSpec.IntValue FRACTIONATING_BASE_TICKS = BUILDER
            .comment("Baseline processing time for the planned fractionating tower prototype.")
            .defineInRange("fractionatingBaseTicks", 200, 20, 20_000);

    static final ModConfigSpec SPEC = BUILDER.build();

    public static boolean enableWorldgenPlaceholders;
    public static int fractionatingBaseTicks;

    static void onLoad(final ModConfigEvent event) {
        enableWorldgenPlaceholders = ENABLE_WORLDGEN_PLACEHOLDERS.getAsBoolean();
        fractionatingBaseTicks = FRACTIONATING_BASE_TICKS.getAsInt();
    }
}
