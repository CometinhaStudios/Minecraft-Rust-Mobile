# Minecraft Rust

Android launcher fork/customization based on [Vasysik/horizon-android](https://github.com/Vasysik/horizon-android).

**Android application label:** Minecraft Rust  
**Repository:** Minecraft Rust Mobile

## Project direction

Minecraft Rust keeps the Horizon Rust game engine and develops a launcher UI inspired by the visual language of the official Minecraft Launcher, redesigned for Android.

### Responsive launcher

- **Landscape:** desktop-launcher composition: left navigation rail, large Play feature area, compact profile/version selector and green Play action.
- **Portrait:** same visual hierarchy adapted to a vertical layout: compact top bar, vertically stacked navigation cards, prominent Play action and scrollable content. No forced rotation; follow the user's Android orientation choice.
- **Navigation:** Textures, Mods, Shaders, Settings. Each category receives a custom original monochrome/pixel-friendly symbol; Settings uses a gear.
- **Settings:** dark panels, green selection accents, consistent rows, toggles, dropdowns and sliders.

### Planned engineering work

1. Responsive launcher layout and original icon set.
2. Separate Textures, Mods and Shaders pages with import/install/enable/remove flows supported by the engine.
3. FPS option **Unlimited**, after tracing the engine frame limiter and ensuring the setting reaches the actual render loop.
4. Driver management research. Turnip ZIP import must validate package contents, ABI, Vulkan driver integration and device compatibility; merely extracting a ZIP is not driver support.
5. Build and test signed/unsigned APKs for arm64 Android, then publish artifacts through GitHub Actions.

## Important compatibility notes

The upstream Android client is a native Rust/wgpu application. Its launcher is not a separate web page or a standard Kotlin activity. UI changes must be made in the Rust Android launcher code and preserve the engine lifecycle.

Turnip integration is not enabled by selecting a ZIP file. Android Vulkan driver loading has platform, ABI, linker and vendor constraints. Unsupported packages must be rejected safely and the system driver must remain available as fallback.

An Unlimited FPS option removes the app's configured cap only. It cannot guarantee a particular frame rate; display refresh rate, GPU/CPU load, thermal limits, synchronization and game workload still apply.

## Upstream

- Source: https://github.com/Vasysik/horizon-android
- Upstream Android branch: `android`
- Upstream documentation: `docs/android.md`

This repository is the project home. Source synchronization and implementation commits will be added as the fork is brought in and changes are tested.
