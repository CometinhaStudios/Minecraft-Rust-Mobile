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


# Real visual redesign: branded header, layered launcher surfaces and responsive Play CTA.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '            &format!("Horizon Android {}", crate::backend::VERSION),',
    '            &format!("MINECRAFT RUST  •  {}", crate::backend::VERSION),'
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '        if page == Page::Play {\n            use horizon_client::official_install::InstallStage;',
    '''        if page == Page::Play {
            // A distinct feature surface gives the home screen a launcher-style hero panel.
            ui.rounded(20.0, 142.0, (w - 40.0).max(1.0), (h - 162.0).max(1.0), 16.0, color::RAISED);
            ui.rounded(20.0, 142.0, 5.0, (h - 162.0).max(1.0), 2.0, color::ACCENT);
            use horizon_client::official_install::InstallStage;'''
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '''                    [32.0, h - 100.0, 320.0, 60.0],''',
    '''                    [32.0, h - 100.0, (w - 64.0).clamp(220.0, 420.0), 60.0],'''
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '''            ui.text(
                Face::Medium,
                32.0,
                32.0,
                top,
                color::TEXT,''',
    '''            ui.text(
                Face::Medium,
                if compact { 28.0 } else { 36.0 },
                32.0,
                top,
                color::TEXT,''',
)
print("Minecraft Rust launcher visual surfaces applied.")


# Replace the old horizontal tab strip with a real launcher sidebar on wide screens.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """        for (i, page) in Page::ALL.iter().enumerate() {
            let x = tab_margin + i as f32 * tab_width;
            button(
                &mut ui,
                &mut self.targets,
                [x, 88.0, tab_width - 4.0, 42.0],
                if pt {
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
                },
                Action::Page(*page),
                *page == self.catalog.page,
            );
        }
        let compact = w < 700.0;""",
    """        if w >= 700.0 {
            // Wide launcher: persistent left navigation instead of the legacy tab strip.
            ui.rounded(16.0, 88.0, 196.0, h - 104.0, 14.0, color::RAISED);
            ui.text(Face::Medium, 13.0, 38.0, 108.0, color::MUTED, "MINECRAFT RUST");
            for (i, page) in Page::ALL.iter().enumerate() {
                let labels = if pt {
                    ["JOGAR", "MODS", "TEXTURAS", "SHADERS", "ARQUIVOS", "CONFIGURAÇÕES", "APARÊNCIA"]
                } else {
                    ["PLAY", "MODS", "TEXTURES", "SHADERS", "FILES", "SETTINGS", "APPEARANCE"]
                };
                let y = 140.0 + i as f32 * 54.0;
                button(
                    &mut ui,
                    &mut self.targets,
                    [30.0, y, 164.0, 44.0],
                    labels[i],
                    Action::Page(*page),
                    *page == self.catalog.page,
                );
            }
        } else {
            for (i, page) in Page::ALL.iter().enumerate() {
                let x = tab_margin + i as f32 * tab_width;
                button(
                    &mut ui,
                    &mut self.targets,
                    [x, 88.0, tab_width - 4.0, 42.0],
                    if pt {
                        match page {
                            Page::Play => "Jogar",
                            Page::Mods => "Mods",
                            Page::Packs => "Texturas",
                            Page::Shaders => "Shaders",
                            Page::Installed => "Arquivos",
                            Page::Settings => "Config.",
                            Page::Skins => "Aparência",
                        }
                    } else {
                        match page {
                            Page::Installed => "Files",
                            Page::Settings => "Setup",
                            _ => page.name(),
                        }
                    },
                    Action::Page(*page),
                    *page == self.catalog.page,
                );
            }
        }
        let compact = w < 700.0;
        let content_x = if w >= 700.0 { 244.0 } else { 32.0 };
        let content_w = (w - content_x - 32.0).max(220.0);"""
)
# Draw the play page as a new launcher home, not the old instructional text list.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """            let top = 160.0;
            ui.text(
                Face::Medium,
                if compact { 28.0 } else { 36.0 },
                32.0,
                top,
                color::TEXT,
                if installing {
                    "Getting your game ready"
                } else if installed {
                    "Ready to play"
                } else {
                    if compact {
                        "Your Java worlds"
                    } else {
                        "Your Java worlds, on Android"
                    }
                },
            );""",
    """            let top = 168.0;
            let left = content_x;
            ui.text(Face::Medium, 13.0, left, 158.0, color::MUTED,
                if pt { "CENTRAL DE JOGO  /  JAVA EDITION" } else { "GAME HUB  /  JAVA EDITION" });
            ui.text(
                Face::Medium,
                if compact { 28.0 } else { 38.0 },
                left,
                top,
                color::TEXT,
                if installing {
                    if pt { "Preparando seu Minecraft" } else { "Getting your game ready" }
                } else if installed {
                    if pt { "Tudo pronto para jogar" } else { "Ready to play" }
                } else if pt {
                    "Seu Minecraft. Do seu jeito."
                } else {
                    "Your Minecraft. Your way."
                },
            );"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                32.0,
                top + 47.0,
                color::MUTED,
                &format!("Minecraft 26.3  /  Profile {}", self.catalog.config.profile),""",
    """                left,
                top + 52.0,
                color::MUTED,
                &format!("Minecraft 26.3  /  {}", if pt { format!("Perfil {}", self.catalog.config.profile) } else { format!("Profile {}", self.catalog.config.profile) }),"""
)
# Position home copy and primary CTA in the content column.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        32.0,
                        top + 100.0 + index as f32 * 42.0,""",
    """                        left,
                        top + 112.0 + index as f32 * 42.0,"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                    [32.0, h - 100.0, (w - 64.0).clamp(220.0, 420.0), 60.0],""",
    """                    [left, h - 100.0, content_w.min(420.0), 60.0],"""
)
print("Replaced legacy wide-screen tabs with launcher sidebar and rebuilt the home page.");


# Keep the home card inside the content column; do not paint over the sidebar.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """            // A distinct feature surface gives the home screen a launcher-style hero panel.
            ui.rounded(20.0, 142.0, (w - 40.0).max(1.0), (h - 162.0).max(1.0), 16.0, color::RAISED);
            ui.rounded(20.0, 142.0, 5.0, (h - 162.0).max(1.0), 2.0, color::ACCENT);""",
    """            // Main home surface sits beside the sidebar.
            ui.rounded(content_x - 12.0, 142.0, content_w + 24.0, h - 162.0, 16.0, color::RAISED);
            ui.rounded(content_x - 12.0, 142.0, 5.0, h - 162.0, 2.0, color::ACCENT);"""
)


# The wardrobe page is a two-column layout. Offset BOTH columns into the content
# area so the preview and its controls never sit underneath the navigation rail.
replace(
    "crates/horizon-client/src/android/launcher.rs",
    "self.wardrobe\n                .draw(&mut ui, &mut self.targets, self.catalog.scroll);",
    "let content_left = if ui.w >= 700.0 { 244.0 } else { 0.0 };\n            self.wardrobe\n                .draw(&mut ui, &mut self.targets, self.catalog.scroll, content_left);"
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    "pub fn draw(&mut self, ui: &mut Ui, targets: &mut Vec<([f32; 4], Action)>, scroll: f32) {\n        let width = ui.w;\n        let compact = width < 700.0;",
    "pub fn draw(&mut self, ui: &mut Ui, targets: &mut Vec<([f32; 4], Action)>, scroll: f32, content_left: f32) {\n        let width = ui.w - content_left;\n        let compact = ui.w < 700.0;"
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    "        let px = if compact {\n            (width - preview_width) * 0.5\n        } else {\n            32.0\n        };",
    "        let px = if compact {\n            (width - preview_width) * 0.5\n        } else {\n            content_left + 32.0\n        };"
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    "        let lx = if compact { 32.0 } else { 370.0 };",
    "        let lx = if compact { 32.0 } else { content_left + 370.0 };"
)
# Give the new wide layout a real content-column title/header, and avoid legacy label overlap.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '            &format!("MINECRAFT RUST  •  {}", crate::backend::VERSION),',
    '            &format!("MINECRAFT RUST  •  {}", crate::backend::VERSION),'
)
print("Wardrobe columns aligned after the sidebar.");


# Correct file: draw_pages and the wardrobe dispatch live in launcher_pages.rs.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "self.wardrobe\n                .draw(&mut ui, &mut self.targets, self.catalog.scroll);",
    "let content_left = if ui.w >= 700.0 { 244.0 } else { 0.0 };\n            self.wardrobe\n                .draw(&mut ui, &mut self.targets, self.catalog.scroll, content_left);"
)
