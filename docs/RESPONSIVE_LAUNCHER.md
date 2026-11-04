# Minecraft Rust — responsive launcher specification

## Orientation contract

The launcher must follow the current Android window dimensions and the user's orientation choice. It must not force landscape. Android's sensor/user rotation controls the activity; the UI adapts after resize/configuration changes.

- **Landscape breakpoint:** width >= height. Use a compact left navigation rail and a wide content panel, echoing the desktop Minecraft Launcher.
- **Portrait breakpoint:** height > width. Use a top brand/header area, vertically stacked category navigation and a full-width Play panel. Content scrolls vertically.
- **Rotation:** preserve the selected page, scroll position, selected profile and in-progress text fields when dimensions change. Recompute hit targets and layout from the new window size.
- **Accessibility:** touch targets >= 48dp, readable labels, system back behavior and safe-area/cutout insets.

## Main navigation

1. Play
2. Textures — custom layered-sheet symbol
3. Mods — custom connected-nodes symbol
4. Shaders — custom prism/rays symbol
5. Settings — gear symbol

Use original vector artwork in `assets/icons/`; do not use Minecraft block/item sprites or copied official launcher assets.

## Visual language

- Near-black charcoal surfaces, restrained borders and soft corner radii.
- Minecraft-like green accent for primary actions and selected navigation.
- White/grey typography, compact metadata and a prominent green Play button.
- The Settings screen uses the same panel, row, icon, switch and dropdown language as the main menu.

## Settings sections

- Performance: frame cap (including Unlimited), render distance, resolution scale.
- Graphics: renderer (Vulkan/GLES), quality and antialiasing where supported.
- Drivers: installed driver metadata, safe ZIP validation and system-driver fallback.
- Textures, Mods, Shaders: dedicated management pages.
- Controls: touch, keyboard/mouse and controller.
- System: orientation, display and diagnostics.

## Implementation notes

The upstream Android UI is native Rust/wgpu and uses winit. Responsive layout belongs in the Rust launcher renderer, not a WebView. Avoid hard-coded orientation assumptions. The current upstream Android manifest uses `sensorLandscape`; this must be changed to user/sensor rotation support as part of the actual Android source integration and tested on portrait and landscape devices.

An Unlimited frame-cap setting must flow into the actual engine frame pacing/limiter path. It only removes the software cap; it cannot override refresh rate, VSync, thermal throttling or GPU limits.

Turnip packages require more than ZIP extraction. Validate archive paths, ABI, native library names, Vulkan loader integration and device compatibility. Never replace the system driver without a verified rollback path.
