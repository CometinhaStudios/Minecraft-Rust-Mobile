# Minecraft Rust

Android launcher fork/customization based on [Vasysik/horizon-android](https://github.com/Vasysik/horizon-android).

**Android application label:** Minecraft Rust  
**Repository:** Minecraft Rust Mobile

## Current build target

The next ARM64 package is built from the real Horizon Android Rust engine, not the visual-only WebView demo. The build applies the Minecraft Rust native launcher customization before compiling and packages the engine into the APK.

### Launcher direction

- Minecraft Rust name and branding.
- Redesigned launcher home screen with a persistent navigation rail on wide layouts and a compact layout on phones.
- Portuguese, Spanish and English interface labels.
- Separate Play, Mods, Textures, Shaders, Installed content, Settings and Appearance sections.
- The Play action remains connected to Horizon's actual resource installation and game launch flow.

### Responsive launcher

- **Landscape:** desktop-launcher composition with left navigation rail, large Play feature area and primary Play action.
- **Portrait:** compact layout adapted to the phone screen, following the Android orientation choice.
- **Navigation:** Textures, Mods, Shaders, Installed, Settings and Appearance.
- **Settings:** dark panels, green selection accents and persisted language selection.

## Engine and compatibility

Minecraft Rust keeps the Horizon Rust/wgpu engine and its Android lifecycle. The app downloads and verifies the required Minecraft Java 26.3 resources on-device through the engine's existing installer. The build does not bundle Minecraft game files or accounts.

The upstream Android client is native Rust/wgpu; its launcher is not a standard WebView page. The production APK therefore applies the redesigned interface in the native launcher source while preserving the real engine.

Turnip ZIP import and Unlimited FPS are not included in this build. Android Vulkan driver loading has platform, ABI, linker and vendor constraints. An uncapped frame limiter also cannot guarantee a particular FPS because display refresh rate, workload and thermal limits still apply.

## Upstream

- Source: https://github.com/Vasysik/horizon-android
- Upstream Android branch: `android`
- Upstream documentation: `docs/android.md`

This project preserves upstream attribution and third-party notices. Minecraft Rust is unofficial and is not affiliated with or endorsed by Mojang or Microsoft.
