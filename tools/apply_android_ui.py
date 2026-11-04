from pathlib import Path

def edit(path, old, new, count=1):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != count:
        raise SystemExit(f"{path}: expected {count} occurrence(s), found {n}: {old[:100]!r}")
    p.write_text(s.replace(old, new), encoding="utf-8")

# Persistent language preference. Auto follows Android's locale; pt-BR is a manual override.
edit(
    "crates/horizon-client/src/android/catalog.rs",
    "    pub mod_source: crate::shader_catalog::Origin,\n}",
    "    pub mod_source: crate::shader_catalog::Origin,\n    pub language: UiLanguage,\n}\n\n#[derive(Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]\n#[serde(rename_all = \"kebab-case\")]\npub enum UiLanguage {\n    #[default]\n    Auto,\n    PortugueseBrazil,\n}\nimpl UiLanguage {\n    pub fn label(self) -> &'static str {\n        match self {\n            Self::Auto => \"Automático\",\n            Self::PortugueseBrazil => \"Português (Brasil)\",\n        }\n    }\n    pub fn portuguese(self) -> bool {\n        match self {\n            Self::PortugueseBrazil => true,\n            Self::Auto => {\n                let mut locale = std::env::var(\"LANG\").unwrap_or_default();\n                if locale.is_empty() {\n                    for key in [\"LC_ALL\", \"LC_MESSAGES\"] {\n                        if let Ok(value) = std::env::var(key) {\n                            if !value.is_empty() { locale = value; break; }\n                        }\n                    }\n                }\n                if locale.is_empty() {\n                    locale = std::process::Command::new(\"/system/bin/getprop\")\n                        .arg(\"persist.sys.locale\")\n                        .output().ok()\n                        .filter(|o| o.status.success())\n                        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_owned())\n                        .unwrap_or_default();\n                }\n                let locale = locale.to_ascii_lowercase();\n                locale.starts_with(\"pt\")\n            }\n        }\n    }\n}"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "    GpuProfile,\n}",
    "    GpuProfile,\n    Language,\n}"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "        let compact = w < 700.0;\n        let page = self.catalog.page;",
    "        let compact = w < 700.0;\n        let pt = self.catalog.config.language.portuguese();\n        let page = self.catalog.page;"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "            &format!(\"Horizon Android {}\", crate::backend::VERSION),",
    "            &format!(\"{} {}\", if pt { \"Minecraft Rust\" } else { \"Horizon Android\" }, crate::backend::VERSION),"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                if w < 700.0 {\n                    match page {\n                        Page::Installed => \"Files\",\n                        Page::Settings => \"Setup\",\n                        _ => page.name(),\n                    }\n                } else {\n                    page.name()\n                },",
    "                if pt {\n                    match page { Page::Play => \"Jogar\", Page::Mods => \"Mods\", Page::Packs => \"Texturas\", Page::Shaders => \"Shaders\", Page::Installed => \"Arquivos\", Page::Settings => \"Config.\", Page::Skins => \"Aparência\" }\n                } else if w < 700.0 {\n                    match page { Page::Installed => \"Files\", Page::Settings => \"Setup\", _ => page.name() }\n                } else { page.name() },"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                \"Launch settings\",",
    "                if pt { \"Configurações\" } else { \"Launch settings\" },"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "            self.catalog.scroll = self\n                .catalog\n                .scroll\n                .clamp(0.0, (18.0 * row_height - (h - 130.0 - 195.0)).max(0.0));",
    "            self.catalog.scroll = self.catalog.scroll.clamp(0.0, (19.0 * row_height - (h - 130.0 - 195.0)).max(0.0));"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                (18.0 * row_height - (h - 130.0 - 195.0)).max(0.0),",
    "                (19.0 * row_height - (h - 130.0 - 195.0)).max(0.0),"
);
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                (\\\"Server\\\",\\n                    if c.server.is_empty() {",
    "                (\\\"Server\\\",\\n                    if c.server.is_empty() {"
);
# Insert language row before Server.
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "                (\\\"Server\\\",\\n                    if c.server.is_empty() {",
    "                (\\\"Language / Idioma\\\", c.language.label().to_owned(), Action::Language),\\n                (\\\"Server\\\",\\n                    if c.server.is_empty() {"
);
# Translate visible settings rows.
for old,new in [
    ('("Rendering", c.renderer.label().to_owned(), Action::Renderer)', '((if pt { "Renderização" } else { "Rendering" }), c.renderer.label().to_owned(), Action::Renderer)'),
    ('("Client resolution",', '((if pt { "Resolução do cliente" } else { "Client resolution" }),'),
    ('("Chunk worker limit",', '((if pt { "Limite de tarefas dos chunks" } else { "Chunk worker limit" }),'),
    ('("Reusable RAM cache",', '((if pt { "Cache de RAM reutilizável" } else { "Reusable RAM cache" }),'),
    ('("Game files",', '((if pt { "Arquivos do jogo" } else { "Game files" }),'),
    ('("World files",', '((if pt { "Mundos" } else { "World files" }),'),
    ('("Profile", format!', '((if pt { "Perfil" } else { "Profile" }), format!'),
    ('("Orientation",', '((if pt { "Orientação" } else { "Orientation" }),'),
    ('("Input", c.input_host.label().to_owned(), Action::InputHost)', '((if pt { "Controles" } else { "Input" }), c.input_host.label().to_owned(), Action::InputHost)'),
    ('("Immersive fullscreen",', '((if pt { "Tela cheia imersiva" } else { "Immersive fullscreen" }),'),
    ('("Avoid camera cutout",', '((if pt { "Evitar recorte da câmera" } else { "Avoid camera cutout" }),'),
    ('("Aspect ratio",', '((if pt { "Proporção da tela" } else { "Aspect ratio" }),'),
    ('("Display refresh rate",', '((if pt { "Taxa de atualização" } else { "Display refresh rate" }),'),
    ('("Performance hints",', '((if pt { "Ajustes de desempenho" } else { "Performance hints" }),'),
    ('("GPU profiling",', '((if pt { "Perfil da GPU" } else { "GPU profiling" }),'),
    ('("Performance recording",', '((if pt { "Gravação de desempenho" } else { "Performance recording" }),'),
    ('("Diagnostic report",', '((if pt { "Relatório de diagnóstico" } else { "Diagnostic report" }),'),
    ('("Raw performance data",', '((if pt { "Dados brutos de desempenho" } else { "Raw performance data" }),'),
    ('("Server",', '((if pt { "Servidor" } else { "Server" }),'),
]:
    edit("crates/horizon-client/src/android/launcher_pages.rs",old,new)

# Keep the language row visible as a chooser-like one-tap toggle; selection is persisted.
edit(
    "crates/horizon-client/src/android/launcher_pages.rs",
    "            Some(Action::ConfirmExit) => {",
    "            Some(Action::Language) => {\n                self.catalog.config.language = match self.catalog.config.language {\n                    crate::catalog::UiLanguage::Auto => crate::catalog::UiLanguage::PortugueseBrazil,\\n                    crate::catalog::UiLanguage::PortugueseBrazil => crate::catalog::UiLanguage::Auto,\\n                };\n                self.catalog.config.save(&self.home)?;\\n                self.catalog.status = if self.catalog.config.language.portuguese() {\\n                    \\"Idioma salvo. Automático segue o idioma do Android; toque novamente para alternar.\\".into()\n                } else {\\n                    \\"Language saved. Automatic follows Android; tap again to switch.\\".into()\\n                };\n            }\n            Some(Action::ConfirmExit) => {"
);
