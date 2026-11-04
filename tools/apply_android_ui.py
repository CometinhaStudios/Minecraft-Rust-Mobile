from pathlib import Path

def replace(path, old, new, count=1):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    found = text.count(old)
    if found != count:
        raise SystemExit(f"{path}: expected {count} matches, got {found}: {old[:90]!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")

# Persisted language setting. Android locale is queried via system property in Auto mode.
replace(
    "crates/horizon-client/src/android/catalog.rs",
    "    pub mod_source: crate::shader_catalog::Origin,\n}",
    """    pub mod_source: crate::shader_catalog::Origin,
    pub language: UiLanguage,
}

#[derive(Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum UiLanguage {
    #[default]
    Auto,
    PortugueseBrazil,
}
impl UiLanguage {
    pub fn label(self) -> &'static str {
        match self {
            Self::Auto => "Automático",
            Self::PortugueseBrazil => "Português (Brasil)",
        }
    }
    pub fn portuguese(self) -> bool {
        match self {
            Self::PortugueseBrazil => true,
            Self::Auto => {
                let value = std::process::Command::new("/system/bin/getprop")
                    .arg("persist.sys.locale")
                    .output()
                    .ok()
                    .filter(|output| output.status.success())
                    .map(|output| String::from_utf8_lossy(&output.stdout).trim().to_ascii_lowercase())
                    .unwrap_or_default();
                value.starts_with("pt")
            }
        }
    }
}"""
)

# Add the language action to the real Android launcher UI.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "    GpuProfile,\n}",
    "    GpuProfile,\n    Language,\n}"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "        let tabs = Page::ALL.len() as f32;",
    "        let pt = self.catalog.config.language.portuguese();\n        let tabs = Page::ALL.len() as f32;"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "        let compact = w < 700.0;",
    "        let compact = w < 700.0;"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '                "Launch settings",',
    '                if pt { "Configurações" } else { "Launch settings" },'
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '                (\n                    "Server",',
    '                (\n                    if pt { "Idioma" } else { "Language" }, c.language.label().to_owned(), Action::Language,\n                ),\n                (\n                    if pt { "Servidor" } else { "Server" },'
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "            Some(Action::ConfirmExit) => {",
    """            Some(Action::Language) => {
                self.catalog.config.language = match self.catalog.config.language {
                    crate::catalog::UiLanguage::Auto => crate::catalog::UiLanguage::PortugueseBrazil,
                    crate::catalog::UiLanguage::PortugueseBrazil => crate::catalog::UiLanguage::Auto,
                };
                self.catalog.config.save(&self.home)?;
                self.catalog.status = if self.catalog.config.language.portuguese() {
                    "Idioma salvo: Português (Brasil).".into()
                } else {
                    "Language saved: Automatic (Android system language).".into()
                };
            }
            Some(Action::ConfirmExit) => {"""
)
# Translate the main navigation labels without changing page behavior.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                if w < 700.0 {
                    match page {
                        Page::Installed => "Files",
                        Page::Settings => "Setup",
                        _ => page.name(),
                    }
                } else {
                    page.name()
                },""",
    """                if pt {
                    match page {
                        Page::Play => "Jogar",
                        Page::Mods => "Mods",
                        Page::Packs => "Texturas",
                        Page::Shaders => "Shaders",
                        Page::Installed => "Arquivos",
                        Page::Settings => "Config.",
                        Page::Skins => "Aparência",
                    }
                } else if w < 700.0 {
                    match page {
                        Page::Installed => "Files",
                        Page::Settings => "Setup",
                        _ => page.name(),
                    }
                } else {
                    page.name()
                },"""
)
print("Android launcher language integration applied.")
