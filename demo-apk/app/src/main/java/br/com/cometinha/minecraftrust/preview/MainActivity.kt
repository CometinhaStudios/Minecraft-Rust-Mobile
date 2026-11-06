package br.com.cometinha.minecraftrust.preview

import android.app.Activity
import android.os.Bundle
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.view.Gravity
import android.view.View
import android.widget.*

class MainActivity : Activity() {
    private val bg = Color.rgb(22, 23, 24)
    private val panel = Color.rgb(31, 33, 34)
    private val green = Color.rgb(45, 190, 65)
    private val white = Color.rgb(242, 242, 242)
    private val muted = Color.rgb(178, 181, 181)
    private lateinit var body: LinearLayout
    private lateinit var nav: LinearLayout
    private var selected = "Início"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = bg
        window.navigationBarColor = bg
        render()
    }

    private fun rounded(color: Int, radius: Float = 14f, stroke: Int = Color.TRANSPARENT): GradientDrawable =
        GradientDrawable().apply { setColor(color); cornerRadius = radius; if (stroke != Color.TRANSPARENT) setStroke(2, stroke) }

    private fun text(value: String, size: Float, color: Int = white, bold: Boolean = false): TextView =
        TextView(this).apply {
            text = value; textSize = size; setTextColor(color)
            if (bold) setTypeface(Typeface.DEFAULT, Typeface.BOLD)
            gravity = Gravity.CENTER_VERTICAL
        }

    private fun row(parent: LinearLayout, weight: Float = 0f): LinearLayout =
        LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL
            parent.addView(this, LinearLayout.LayoutParams(if (weight > 0) 0 else -1, -2, weight)) }

    private fun space(parent: LinearLayout, height: Int = 10) {
        parent.addView(View(this), LinearLayout.LayoutParams(1, height))
    }

    private fun button(label: String, action: () -> Unit): TextView =
        text(label, 17f, white, true).apply {
            gravity = Gravity.CENTER; background = rounded(green, 12f)
            setPadding(20, 14, 20, 14); setOnClickListener { action() }
        }

    private fun render() {
        val root = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; setBackgroundColor(bg) }
        nav = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(8, 12, 8, 12); setBackgroundColor(Color.rgb(17,18,19)) }
        root.addView(nav, LinearLayout.LayoutParams(dp(142), -1))
        val right = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(14, 8, 14, 12) }
        root.addView(right, LinearLayout.LayoutParams(0, -1, 1f))
        val header = row(right)
        header.addView(text("🟩   Minecraft ", 24f, white, true), LinearLayout.LayoutParams(-2, dp(48)))
        header.addView(text("Rust", 24f, Color.rgb(235,55,55), true))
        header.addView(text("   Launcher v0.1.0 (Alpha) • Teste 1", 13f, muted))
        space(right, 8)
        body = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(2, 2, 2, 2) }
        right.addView(body, LinearLayout.LayoutParams(-1, 0, 1f))
        listOf("Início", "Mods", "Shaders", "Texturas", "Skins", "Configurações").forEach { item ->
            val label = when(item) {
                "Início" -> "🌱   Início"
                "Mods" -> "🧩   Mods"
                "Shaders" -> "☀️   Shaders"
                "Texturas" -> "🟫   Texturas"
                "Skins" -> "👤   Skins"
                else -> "⚙️   Configurações"
            }
            val v = text(label, 16f, if (selected == item) white else muted, selected == item)
            v.setPadding(10, 13, 6, 13)
            v.background = rounded(if (selected == item) Color.rgb(34,76,45) else Color.TRANSPARENT, 10f)
            nav.addView(v, LinearLayout.LayoutParams(-1, dp(58)))
            v.setOnClickListener { selected = item; refresh() }
            space(nav, 5)
        }
        setContentView(root)
        refresh()
    }

    private fun refresh() {
        body.removeAllViews()
        when(selected) {
            "Início" -> home()
            "Mods" -> catalog("Mods", "Explore complementos para personalizar sua experiência.", listOf("Mini mapa", "Móveis e decoração", "Novos biomas"))
            "Shaders" -> catalog("Shaders", "Pré-visualização dos pacotes de iluminação.", listOf("Complementary Reimagined", "BSL Shaders", "Sildur's Vibrant"))
            "Texturas" -> catalog("Texturas", "Pacotes visuais para mudar o mundo.", listOf("Faithful", "Bare Bones", "Programmer Art"))
            "Skins" -> catalog("Skins", "Escolha uma aparência para seu personagem.", listOf("Steve clássico", "Alex clássica", "Minha skin"))
            "Configurações" -> settings()
        }
    }

    private fun home() {
        val top = row(body)
        val hero = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; gravity = Gravity.CENTER
            background = GradientDrawable(GradientDrawable.Orientation.TL_BR,
                intArrayOf(Color.rgb(239,133,64), Color.rgb(92,91,130), Color.rgb(30,76,49))).apply { cornerRadius = 16f }
            setPadding(18, 12, 18, 12)
        }
        top.addView(hero, LinearLayout.LayoutParams(0, dp(250), 1.7f))
        hero.addView(text("🌄  MINECRAFT RUST", 27f, Color.WHITE, true))
        hero.addView(text("Jogue, explore, sobreviva!", 17f, Color.WHITE, true))
        val news = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(16, 14, 16, 12); background = rounded(panel, 16f) }
        val p = LinearLayout.LayoutParams(0, dp(250), 1f); p.leftMargin = dp(12); top.addView(news, p)
        news.addView(text("ÚLTIMAS NOTÍCIAS", 20f, white, true))
        space(news, 10)
        news.addView(text("Bem-vindo ao Minecraft Rust!", 17f, white, true))
        space(news, 8)
        news.addView(text("Uma nova jornada começa agora. Explore um mundo infinito, construa, sobreviva e divirta-se!", 14f, muted))
        space(news, 12)
        news.addView(text("■  Suporte a mods e shaders\n■  Interface renovada\n■  Personalize suas texturas e skins", 14f, green))
        space(body, 14)
        body.addView(text("Novidades", 20f, white, true))
        space(body, 6)
        val card = text("🌸   Atualização de experiências\n       Descubra novas formas de jogar, com mais liberdade e criatividade!", 16f, white, true)
        card.setPadding(14, 12, 14, 12); card.background = rounded(panel)
        body.addView(card, LinearLayout.LayoutParams(-1, dp(74)))
        val bottom = row(body)
        bottom.gravity = Gravity.CENTER
        val play = button("▶   JOGAR") { Toast.makeText(this, "Demonstração visual: o jogo não está conectado.", Toast.LENGTH_SHORT).show() }
        val lp = LinearLayout.LayoutParams(dp(360), dp(58)); lp.topMargin = dp(14)
        bottom.addView(play, lp)
    }

    private fun catalog(title: String, subtitle: String, items: List<String>) {
        body.addView(text(title, 26f, white, true))
        space(body, 4)
        body.addView(text(subtitle, 14f, muted))
        space(body, 14)
        items.forEachIndexed { i, item ->
            val card = row(body)
            card.background = rounded(panel)
            card.setPadding(12, 8, 12, 8)
            val icon = listOf("🧩", "☀️", "🟫", "👤")[i % 4]
            card.addView(text("$icon   $item", 17f, white, true), LinearLayout.LayoutParams(0, dp(58), 1f))
            val action = text(if (title == "Skins") "Selecionar" else "Ver", 14f, green, true)
            action.setPadding(12, 8, 12, 8); card.addView(action)
            space(body, 9)
        }
        if (title == "Mods" || title == "Shaders" || title == "Texturas") {
            body.addView(text("Demonstração: os itens são exemplos visuais, sem instalação real.", 12f, muted))
        }
    }

    private fun settings() {
        body.addView(text("Configurações", 26f, white, true))
        space(body, 12)
        listOf("Idioma", "Aparência", "Notificações", "Sobre o Minecraft Rust").forEach { label ->
            val r = row(body); r.background = rounded(panel); r.setPadding(14, 4, 14, 4)
            r.addView(text(label, 17f, white, true), LinearLayout.LayoutParams(0, dp(54), 1f))
            r.addView(text(if (label == "Idioma") "Português (Brasil)  ▾" else "›", 14f, muted))
            space(body, 8)
        }
        body.addView(text("Protótipo de interface • Alpha 0.1 • Teste 1", 12f, muted))
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()
}
