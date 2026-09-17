package com.anw.kamaen.mixin;

import com.anw.kamaen.KamaenInfo;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Registry.class)
public interface RegistryMixin {
    @Inject(
            method = "register(Lnet/minecraft/core/Registry;Lnet/minecraft/resources/ResourceKey;Ljava/lang/Object;)Ljava/lang/Object;",
            at = @At("RETURN")
    )
    private static <V, T extends V> void kamaeninfo$scanItemRegistration(
            Registry<V> registry,
            ResourceKey<V> key,
            T value,
            CallbackInfoReturnable<T> callbackInfo
    ) {
        if (registry.key().equals(Registries.ITEM)
                && value instanceof Item
                && KamaenInfo.MODID.equals(key.location().getNamespace())) {
            KamaenInfo.LOGGER.info("Scanned item registration: {}", key.location());
        }
    }
}
