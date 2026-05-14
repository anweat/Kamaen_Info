package com.anw.kamaen;

import org.slf4j.Logger;

import com.mojang.logging.LogUtils;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

// The value here should match an entry in the META-INF/neoforge.mods.toml file
@Mod(KamaenInfo.MODID)
public class KamaenInfo {
    // Define mod id in a common place for everything to reference
    public static final String MODID = "kamaeninfo";
    // Directly reference a slf4j logger
    public static final Logger LOGGER = LogUtils.getLogger();
    // Create a Deferred Register to hold Blocks which will all be registered under the "kamaeninfo" namespace
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MODID);
    // Create a Deferred Register to hold Items which will all be registered under the "kamaeninfo" namespace
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MODID);
    // Create a Deferred Register to hold CreativeModeTabs which will all be registered under the "kamaeninfo" namespace
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    public static final DeferredItem<Item> RAW_KAMAEN_CRYSTAL = ITEMS.registerSimpleItem("kamaen_crystal_raw", new Item.Properties());
    public static final DeferredItem<Item> TUNED_KAMAEN_CRYSTAL = ITEMS.registerSimpleItem("kamaen_crystal_tuned", new Item.Properties());
    public static final DeferredItem<Item> INFO_PROBE = ITEMS.registerSimpleItem("info_probe", new Item.Properties().stacksTo(1));

    public static final DeferredBlock<Block> FRACTIONATING_TOWER = BLOCKS.registerSimpleBlock("fractionating_tower",
            BlockBehaviour.Properties.of().mapColor(MapColor.METAL).strength(3.5f, 6.0f));
    public static final DeferredBlock<Block> EXPLOSION_CHAMBER_CONTROLLER = BLOCKS.registerSimpleBlock("explosion_chamber_controller",
            BlockBehaviour.Properties.of().mapColor(MapColor.METAL).strength(6.0f, 12.0f));
    public static final DeferredBlock<Block> BLACK_HOLE_PARSER_CORE = BLOCKS.registerSimpleBlock("black_hole_parser_core",
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_BLACK).strength(8.0f, 24.0f).requiresCorrectToolForDrops());

    public static final DeferredItem<BlockItem> FRACTIONATING_TOWER_ITEM = ITEMS.registerSimpleBlockItem("fractionating_tower", FRACTIONATING_TOWER);
    public static final DeferredItem<BlockItem> EXPLOSION_CHAMBER_CONTROLLER_ITEM = ITEMS.registerSimpleBlockItem("explosion_chamber_controller", EXPLOSION_CHAMBER_CONTROLLER);
    public static final DeferredItem<BlockItem> BLACK_HOLE_PARSER_CORE_ITEM = ITEMS.registerSimpleBlockItem("black_hole_parser_core", BLACK_HOLE_PARSER_CORE);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> KAMAEN_INFO_TAB = CREATIVE_MODE_TABS.register("kamaen_info", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.kamaeninfo")) //The language key for the title of your CreativeModeTab
            .withTabsBefore(CreativeModeTabs.COMBAT)
            .icon(() -> RAW_KAMAEN_CRYSTAL.get().getDefaultInstance())
            .displayItems((parameters, output) -> {
                output.accept(RAW_KAMAEN_CRYSTAL.get());
                output.accept(TUNED_KAMAEN_CRYSTAL.get());
                output.accept(INFO_PROBE.get());
                output.accept(FRACTIONATING_TOWER_ITEM.get());
                output.accept(EXPLOSION_CHAMBER_CONTROLLER_ITEM.get());
                output.accept(BLACK_HOLE_PARSER_CORE_ITEM.get());
            }).build());

    // The constructor for the mod class is the first code that is run when your mod is loaded.
    // FML will recognize some parameter types like IEventBus or ModContainer and pass them in automatically.
    public KamaenInfo(IEventBus modEventBus, ModContainer modContainer) {
        // Register the commonSetup method for modloading
        modEventBus.addListener(this::commonSetup);
        modEventBus.addListener(Config::onLoad);

        // Register the Deferred Register to the mod event bus so blocks get registered
        BLOCKS.register(modEventBus);
        // Register the Deferred Register to the mod event bus so items get registered
        ITEMS.register(modEventBus);
        // Register the Deferred Register to the mod event bus so tabs get registered
        CREATIVE_MODE_TABS.register(modEventBus);

        // Register ourselves for server and other game events we are interested in.
        // Note that this is necessary if and only if we want *this* class (KamaenInfo) to respond directly to events.
        // Do not add this line if there are no @SubscribeEvent-annotated functions in this class, like onServerStarting() below.
        NeoForge.EVENT_BUS.register(this);

        // Register the item to a creative tab
        modEventBus.addListener(this::addCreative);

        // Register our mod's ModConfigSpec so that FML can create and load the config file for us
        modContainer.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
    }

    private void commonSetup(FMLCommonSetupEvent event) {
        LOGGER.info("Kamaen Info common setup initialized.");
    }

    // Add the example block item to the building blocks tab
    private void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS) {
            event.accept(FRACTIONATING_TOWER_ITEM);
            event.accept(EXPLOSION_CHAMBER_CONTROLLER_ITEM);
            event.accept(BLACK_HOLE_PARSER_CORE_ITEM);
        }
    }

    // You can use SubscribeEvent and let the Event Bus discover methods to call
    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event) {
        LOGGER.info("Kamaen Info server hooks are ready.");
    }
}
