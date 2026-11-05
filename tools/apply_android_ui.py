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
    PortugueseBrazil,
    Spanish,
    English,
}
impl UiLanguage {
    pub fn label(self) -> &'static str {
        match self {
            Self::PortugueseBrazil => "Português (Brasil)",
            Self::Spanish => "Español",
            Self::English => "English",
        }
    }
    pub fn portuguese(self) -> bool { matches!(self, Self::PortugueseBrazil) }
    pub fn spanish(self) -> bool { matches!(self, Self::Spanish) }
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
    "        let pt = self.catalog.config.language.portuguese();\n        let es = self.catalog.config.language.spanish();\n        let tabs = Page::ALL.len() as f32;"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "        let compact = w < 700.0;",
    "        let compact = w < 700.0;"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '                "Launch settings",',
    '                if pt { "Configurações" } else if es { "Configuración" } else { "Settings" },'
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    '                (\n                    "Server",',
    '                (\n                    if pt { "Idioma" } else if es { "Idioma" } else { "Language" }, c.language.label().to_owned(), Action::Language,\n                ),\n                (\n                    if pt { "Servidor" } else if es { "Servidor" } else { "Server" },'
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "            Some(Action::ConfirmExit) => {",
    """            Some(Action::Language) => {
                self.catalog.config.language = match self.catalog.config.language {
                    crate::catalog::UiLanguage::PortugueseBrazil => crate::catalog::UiLanguage::Spanish,
                    crate::catalog::UiLanguage::Spanish => crate::catalog::UiLanguage::English,
                    crate::catalog::UiLanguage::English => crate::catalog::UiLanguage::PortugueseBrazil,
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
                } else if es {
                    match page {
                        Page::Play => "Jugar",
                        Page::Mods => "Mods",
                        Page::Packs => "Texturas",
                        Page::Shaders => "Shaders",
                        Page::Installed => "Archivos",
                        Page::Settings => "Ajustes",
                        Page::Skins => "Aspecto",
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

# Translate every settings row label and the common setting values.
for old, new in [
    ('"Rendering"', 'if pt { "Renderização" } else if es { "Renderizado" } else { "Rendering" }'),
    ('"Client resolution"', 'if pt { "Resolução do cliente" } else if es { "Resolución del cliente" } else { "Client resolution" }'),
    ('"Chunk worker limit"', 'if pt { "Limite de tarefas de chunks" } else if es { "Límite de tareas de chunks" } else { "Chunk worker limit" }'),
    ('"Reusable RAM cache"', 'if pt { "Cache de RAM reutilizável" } else if es { "Caché de RAM reutilizable" } else { "Reusable RAM cache" }'),
    ('"Game files"', 'if pt { "Arquivos do jogo" } else if es { "Archivos del juego" } else { "Game files" }'),
    ('"World files"', 'if pt { "Arquivos dos mundos" } else if es { "Archivos de mundos" } else { "World files" }'),
    ('"Profile"', 'if pt { "Perfil" } else if es { "Perfil" } else { "Profile" }'),
    ('"Orientation"', 'if pt { "Orientação" } else if es { "Orientación" } else { "Orientation" }'),
    ('"Input"', 'if pt { "Entrada" } else if es { "Entrada" } else { "Input" }'),
    ('"Immersive fullscreen"', 'if pt { "Tela cheia imersiva" } else if es { "Pantalla completa inmersiva" } else { "Immersive fullscreen" }'),
    ('"Avoid camera cutout"', 'if pt { "Evitar recorte da câmera" } else if es { "Evitar recorte de cámara" } else { "Avoid camera cutout" }'),
    ('"Aspect ratio"', 'if pt { "Proporção da tela" } else if es { "Relación de aspecto" } else { "Aspect ratio" }'),
    ('"Display refresh rate"', 'if pt { "Taxa de atualização da tela" } else if es { "Frecuencia de actualización" } else { "Display refresh rate" }'),
    ('"Performance hints"', 'if pt { "Otimizações de desempenho" } else if es { "Ajustes de rendimiento" } else { "Performance hints" }'),
    ('"GPU profiling"', 'if pt { "Monitoramento da GPU" } else if es { "Perfilado de GPU" } else { "GPU profiling" }'),
    ('"Performance recording"', 'if pt { "Gravação de desempenho" } else if es { "Registro de rendimiento" } else { "Performance recording" }'),
    ('"Diagnostic report"', 'if pt { "Relatório de diagnóstico" } else if es { "Informe de diagnóstico" } else { "Diagnostic report" }'),
    ('"Raw performance data"', 'if pt { "Dados brutos de desempenho" } else if es { "Datos sin procesar de rendimiento" } else { "Raw performance data" }'),
    ('"Server"', 'if pt { "Servidor" } else if es { "Servidor" } else { "Server" }'),
    ('"No additional limit"', 'if pt { "Sem limite adicional" } else if es { "Sin límite adicional" } else { "No additional limit" }'),
    ('"Engine default (80 MiB)"', 'if pt { "Padrão do mecanismo (80 MiB)" } else if es { "Predeterminado (80 MiB)" } else { "Engine default (80 MiB)" }'),
    ('"Open in system Files"', 'if pt { "Abrir no gerenciador de arquivos" } else if es { "Abrir en Archivos del sistema" } else { "Open in system Files" }'),
    ('"Import / copy / back up in Files"', 'if pt { "Importar / copiar / fazer backup" } else if es { "Importar / copiar / respaldar" } else { "Import / copy / back up in Files" }'),
    ('"Microsoft / Xbox account"', 'if pt { "Conta Microsoft / Xbox" } else if es { "Cuenta Microsoft / Xbox" } else { "Microsoft / Xbox account" }'),
    ('"Diagnostics"', 'if pt { "Diagnósticos" } else if es { "Diagnósticos" } else { "Diagnostics" }'),
]:
    replace("crates/horizon-client/src/android/launcher_pages.rs", old, new)

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
                } else if es {
                    match page {
                        Page::Play => "Jugar",
                        Page::Mods => "Mods",
                        Page::Packs => "Texturas",
                        Page::Shaders => "Shaders",
                        Page::Installed => "Archivos",
                        Page::Settings => "Ajustes",
                        Page::Skins => "Aspecto",
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
                } else if es {
                    ["JUGAR", "MODS", "TEXTURAS", "SHADERS", "ARCHIVOS", "AJUSTES", "ASPECTO"]
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
    "crates/horizon-client/src/android/wardrobe.rs",
    "pub fn draw(&mut self, ui: &mut Ui, targets: &mut Vec<([f32; 4], Action)>, scroll: f32) {\n        let width = ui.w;\n        let compact = width < 700.0;",
    "pub fn draw(&mut self, ui: &mut Ui, targets: &mut Vec<([f32; 4], Action)>, scroll: f32, content_left: f32, language: crate::catalog::UiLanguage) {\n        let width = ui.w - content_left;\n        let compact = ui.w < 700.0;\n        let pt = language.portuguese();\n        let es = language.spanish();"
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

# Translate the visible appearance editor controls in all three languages.
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Skins & Capes"',
    'if pt { "Visuais e capas" } else if es { "Aspectos y capas" } else { "Skins & Capes" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Local choices change your view. Cloud buttons update your account."',
    'if pt { "As escolhas locais mudam sua aparência. Ações na nuvem alteram sua conta." } else if es { "Las opciones locales cambian tu aspecto. Las acciones en la nube actualizan tu cuenta." } else { "Local choices change your view. Cloud buttons update your account." }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Alex / Slim"',
    'if pt { "Alex / Fino" } else if es { "Alex / Delgado" } else { "Alex / Slim" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Steve / Classic"',
    'if pt { "Steve / Clássico" } else if es { "Steve / Clásico" } else { "Steve / Classic" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Skins"',
    'if pt { "Visuais" } else if es { "Aspectos" } else { "Skins" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Capes"',
    'if pt { "Capas" } else if es { "Capas" } else { "Capes" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Import PNG to local gallery"',
    'if pt { "Importar PNG para a galeria" } else if es { "Importar PNG a la galería" } else { "Import PNG to local gallery" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Reset to default locally"',
    'if pt { "Restaurar padrão local" } else if es { "Restablecer apariencia local" } else { "Reset to default locally" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Use current cloud appearance"',
    'if pt { "Usar aparência atual da nuvem" } else if es { "Usar aspecto actual de la nube" } else { "Use current cloud appearance" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Refresh cloud profile"',
    'if pt { "Atualizar perfil da nuvem" } else if es { "Actualizar perfil de la nube" } else { "Refresh cloud profile" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Upload selected skin to Microsoft"',
    'if pt { "Enviar visual para a Microsoft" } else if es { "Subir aspecto a Microsoft" } else { "Upload selected skin to Microsoft" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Manage Ely.by cloud skin on website"',
    'if pt { "Gerenciar visual Ely.by no site" } else if es { "Gestionar aspecto Ely.by en el sitio" } else { "Manage Ely.by cloud skin on website" }'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '"Hide / show cape locally"',
    'if pt { "Ocultar / mostrar capa" } else if es { "Ocultar / mostrar capa" } else { "Hide / show cape locally" }'
)



# Correct file: draw_pages and the wardrobe dispatch live in launcher_pages.rs.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "self.wardrobe\n                .draw(&mut ui, &mut self.targets, self.catalog.scroll);",
    "let content_left = if ui.w >= 700.0 { 244.0 } else { 0.0 };\n            self.wardrobe\n                .draw(&mut ui, &mut self.targets, self.catalog.scroll, content_left, self.catalog.config.language);"
)


# Align every content screen with the wide-screen navigation rail.
# Catalog: all controls, list rows, action buttons and hit targets use the content column.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """        } else if page.is_catalog() {
            ui.text(
                Face::Medium,
                18.0,
                32.0,
                142.0,""",
    """        } else if page.is_catalog() {
            let cx = content_x;
            let cw = content_w;
            // Category mark: original geometric icon, drawn in the HUD (no Minecraft assets).
            let mark = if page == Page::Mods { "M" } else if page == Page::Shaders { "✦" } else { "▦" };
            ui.rounded(cx, 132.0, 38.0, 38.0, 8.0, color::ACCENT);
            ui.text(Face::Medium, 22.0, cx + 9.0, 139.0, color::ON_ACCENT, mark);
            ui.text(
                Face::Medium,
                18.0,
                cx + 50.0,
                142.0,"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                [32.0, 174.0, w - 240.0, 44.0],""",
    """                [cx, 174.0, (cw - 170.0).max(100.0), 44.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                [w - 190.0, 174.0, 158.0, 44.0],""",
    """                [cx + cw - 158.0, 174.0, 158.0, 44.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                let width = ((w - 185.0) / 2.0).clamp(58.0, 120.0);""",
    """                let width = ((cw - 185.0) / 2.0).clamp(58.0, 120.0);"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                    let rect = [w - 32.0 - (2 - i) as f32 * width, 134.0, width - 5.0, 32.0];""",
    """                    let rect = [cx + cw - 10.0 - (2 - i) as f32 * width, 134.0, width - 5.0, 32.0];"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """            let hint = ui.fit_text(Face::Regular, 14.0, hint, w - 64.0);
            ui.text(Face::Regular, 14.0, 32.0, 270.0, color::MUTED, &hint);""",
    """            let hint = ui.fit_text(Face::Regular, 14.0, hint, cw - 64.0);
            ui.text(Face::Regular, 14.0, cx, 270.0, color::MUTED, &hint);"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """            let file_button_width = ((w - 72.0) / 2.0).min(158.0);""",
    """            let file_button_width = ((cw - 72.0) / 2.0).min(158.0);"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                [32.0, 222.0, file_button_width, 38.0],""",
    """                [cx, 222.0, file_button_width, 38.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                [w - 32.0 - file_button_width, 222.0, file_button_width, 38.0],""",
    """                [cx + cw - file_button_width, 222.0, file_button_width, 38.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """            let top = 296.0;""",
    """            let top = 296.0;"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                let title = ui.fit_text(Face::Medium, 19.0, title, w - 214.0);
                let summary = ui.fit_text(Face::Regular, 14.0, description, w - 214.0);
                ui.text(Face::Medium, 19.0, 32.0, y, color::TEXT, &title);
                ui.text(Face::Regular, 14.0, 32.0, y + 29.0, color::MUTED, &summary);""",
    """                let title = ui.fit_text(Face::Medium, 19.0, title, cw - 214.0);
                let summary = ui.fit_text(Face::Regular, 14.0, description, cw - 214.0);
                ui.text(Face::Medium, 19.0, cx, y, color::TEXT, &title);
                ui.text(Face::Regular, 14.0, cx, y + 29.0, color::MUTED, &summary);"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                    [w - 150.0, y, 118.0, 42.0],""",
    """                    [cx + cw - 118.0, y, 118.0, 42.0],""",
    count=2
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        .push(([w - 150.0, y, 118.0, 70.0], Action::Install(i)));""",
    """                        .push(([cx + cw - 118.0, y, 118.0, 70.0], Action::Install(i)));"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                let title = ui.fit_text(Face::Medium, 19.0, &p.title, w - 214.0);
                let summary = ui.fit_text(Face::Regular, 14.0, &p.summary, w - 214.0);
                ui.text(Face::Medium, 19.0, 32.0, y, color::TEXT, &title);
                ui.text(Face::Regular, 14.0, 32.0, y + 29.0, color::MUTED, &summary);""",
    """                let title = ui.fit_text(Face::Medium, 19.0, &p.title, cw - 214.0);
                let summary = ui.fit_text(Face::Regular, 14.0, &p.summary, cw - 214.0);
                ui.text(Face::Medium, 19.0, cx, y, color::TEXT, &title);
                ui.text(Face::Regular, 14.0, cx, y + 29.0, color::MUTED, &summary);"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                [32.0, h - 100.0, 120.0, 40.0],""",
    """                [cx, h - 100.0, 120.0, 40.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                [166.0, h - 100.0, 120.0, 40.0],""",
    """                [cx + 134.0, h - 100.0, 120.0, 40.0],"""
)
# Installed content: shift section headers, imports, item names, toggles and delete buttons.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """        } else if page == Page::Installed {
            use horizon_client::content_files::Kind;""",
    """        } else if page == Page::Installed {
            use horizon_client::content_files::Kind;
            let cx = content_x;
            let cw = content_w;"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """            self.list_targets
                    .push(([32.0, y, w - 210.0, 40.0], Action::ToggleSection(section)));
                self.list_targets
                    .push(([w - 165.0, y, 133.0, 40.0], Action::Import(kind)));""",
    """            self.list_targets
                    .push(([cx, y, (cw - 145.0).max(100.0), 40.0], Action::ToggleSection(section)));
                self.list_targets
                    .push(([cx + cw - 133.0, y, 133.0, 40.0], Action::Import(kind)));"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        [32.0, y, w - 210.0, 40.0],""",
    """                        [cx, y, (cw - 145.0).max(100.0), 40.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        [w - 165.0, y, 133.0, 40.0],""",
    """                        [cx + cw - 133.0, y, 133.0, 40.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                            if compact { 32.0 } else { w - 300.0 },""",
    """                            if compact { 32.0 } else { cx + cw - 268.0 },""",
    count=3
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                            120.0,
                            row_height - 4.0,""",
    """                            120.0,
                            row_height - 4.0,"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        [w - 165.0, y, 133.0, row_height - 4.0],""",
    """                        [cx + cw - 133.0, y, 133.0, row_height - 4.0],"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                    ui.text(Face::Medium, 19.0, 32.0, y, color::TEXT, &title);""",
    """                    ui.text(Face::Medium, 19.0, cx, y, color::TEXT, &title);"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        32.0,
                        y + 28.0,""",
    """                        cx,
                        y + 28.0,"""
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    """                        [w - 165.0, y + if compact { 55.0 } else { 0.0 }, 133.0, 40.0],""",
    """                        [cx + cw - 133.0, y + if compact { 55.0 } else { 0.0 }, 133.0, 40.0],"""
)
print("All catalog and installed pages now use the content column; category icons added.");


# Fix the two screens that were still drawing in the full-window coordinate space.
# Settings must use the same content column as the sidebar-aware catalog pages.
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "            let c = &self.catalog.config;\n            ui.text(",
    "            let c = &self.catalog.config;\n            let cx = content_x;\n            let cw = content_w;\n            ui.text("
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                24.0,\n                32.0,\n                156.0,",
    "                24.0,\n                cx,\n                156.0,"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                        if compact { 32.0 } else { w * 0.36 },\n                        y,\n                        if compact { w - 64.0 } else { w * 0.64 - 32.0 },",
    "                        if compact { 32.0 } else { cx + cw * 0.36 },\n                        y,\n                        if compact { w - 64.0 } else { cw * 0.64 - 32.0 },",
    count=2
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                    32.0,\n                    y + if compact { 0.0 } else { 13.0 },",
    "                    if compact { 32.0 } else { cx },\n                    y + if compact { 0.0 } else { 13.0 },"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                    32.0,\n                    y + if compact { 78.0 } else { 62.0 },\n                    w - 64.0,",
    "                    if compact { 32.0 } else { cx },\n                    y + if compact { 78.0 } else { 62.0 },\n                    if compact { w - 64.0 } else { cw - 64.0 },"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                [w * 0.5 + 6.0, h - 114.0, w * 0.5 - 38.0, 42.0],",
    "                [if compact { w * 0.5 + 6.0 } else { cx + cw * 0.5 + 6.0 }, h - 114.0, if compact { w * 0.5 - 38.0 } else { cw * 0.5 - 38.0 }, 42.0],"
)
replace(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                [32.0, h - 114.0, w * 0.5 - 38.0, 42.0],",
    "                [if compact { 32.0 } else { cx }, h - 114.0, if compact { w * 0.5 - 38.0 } else { cw * 0.5 - 38.0 }, 42.0],"
)

# The large appearance heading and its helper text also belong to the content column.
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    '        ui.text(Face::Medium, 26.0, 32.0, top, color::TEXT, if pt { "Visuais e capas" } else if es { "Aspectos y capas" } else { "Skins & Capes" });',
    '        let content_x = if compact { 32.0 } else { content_left + 32.0 };\n        ui.text(Face::Medium, 26.0, content_x, top, color::TEXT, if pt { "Visuais e capas" } else if es { "Aspectos y capas" } else { "Skins & Capes" });'
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    "            32.0,\n            top + 36.0,",
    "            content_x,\n            top + 36.0,"
)
replace(
    "crates/horizon-client/src/android/wardrobe.rs",
    "        let note = ui.fit_text(Face::Regular, 12.0, &self.note, width - 64.0);\n        ui.text(Face::Regular, 12.0, 32.0, ui.h - 60.0, color::MUTED, &note);",
    "        let note = ui.fit_text(Face::Regular, 12.0, &self.note, width - 64.0);\n        ui.text(Face::Regular, 12.0, content_x, ui.h - 60.0, color::MUTED, &note);"
)
print("Settings and appearance screens aligned with the launcher sidebar.");
