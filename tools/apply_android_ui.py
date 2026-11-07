from pathlib import Path

def replace_once(path: str, old: str, new: str) -> None:
    file = Path(path)
    source = file.read_text(encoding="utf-8")
    matches = source.count(old)
    if matches != 1:
        raise SystemExit(
            f"{path}: expected exactly one current-source match, found {matches}: {old!r}"
        )
    file.write_text(source.replace(old, new), encoding="utf-8")


# The upstream Android launcher has evolved into a native, animated sidebar UI.
# Keep its real navigation, settings, account, downloads, and Play/install actions;
# only replace the upstream identity/copy with Minecraft Rust branding.
launcher = "crates/horizon-client/src/android/launcher_pages.rs"

replace_once(
    launcher,
    'ui.text(Face::SemiBold, 16.0, 54.0, 10.0, my3_text(), "Horizon");',
    'ui.text(Face::SemiBold, 16.0, 54.0, 10.0, my3_text(), "Minecraft Rust");',
)

replace_once(
    launcher,
    'let version_line = format!("Android {}", crate::backend::VERSION);',
    'let version_line = format!("Rust Engine  •  {}", crate::backend::VERSION);',
)

replace_once(
    launcher,
    '"Your Java worlds, on Android"',
    '"Minecraft Rust  •  Java Edition"',
)

replace_once(
    launcher,
    '"Your Java worlds"',
    '"Minecraft Rust"',
)

replace_once(
    launcher,
    '"Horizon Android is becoming Starling"',
    '"Your Minecraft. Your world."',
)

replace_once(
    launcher,
    '"Some Horizon Android features are still being transferred and merged. Export your worlds through Android Files (SAF) before moving."',
    '"Minecraft Rust combines a redesigned launcher with the Horizon Rust and Vulkan game engine. Install the game, manage your content, and launch it from one place."',
)

print("Minecraft Rust native launcher branding applied to the current Horizon Android source.")
