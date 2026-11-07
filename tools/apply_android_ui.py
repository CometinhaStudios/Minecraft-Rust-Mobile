from pathlib import Path
import re
import shutil

ROOT = Path.cwd()
PROJECT = ROOT.parent
ANDROID = ROOT / "packaging/android"

def replace_once(path: Path, old: str, new: str) -> None:
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {count}: {old!r}")
    path.write_text(source.replace(old, new), encoding="utf-8")

# Keep the real Horizon Rust/Vulkan engine. Replace only its Android entry screen
# with the Minecraft Rust WebView launcher, following the Wudroid architecture.
assets = ANDROID / "assets/minecraft-rust"
assets.mkdir(parents=True, exist_ok=True)
shutil.copy2(PROJECT / "demo/app/src/main/assets/index.html", assets / "index.html")
shutil.copy2(PROJECT / "demo/app/src/main/assets/minecraft-logo.svg", assets / "minecraft-logo.svg")
if (PROJECT / "assets/icons").exists():
    shutil.copytree(PROJECT / "assets/icons", assets / "icons", dirs_exist_ok=True)

html = (assets / "index.html").read_text(encoding="utf-8")
html = html.replace("AndroidDemo.play()", "RustBridge.play()")
html = html.replace("Launcher Alpha 0.5 · Banner", "Minecraft Rust · Launcher")
html = html.replace("Preferências visuais desta demonstração.", "Preferências do Minecraft Rust.")
html = html.replace("Modo</span><span>Demonstração visual", "Motor</span><span>Horizon Rust + Vulkan")
(assets / "index.html").write_text(html, encoding="utf-8")

java_dir = ANDROID / "java/dev/horizon/android"
java_dir.mkdir(parents=True, exist_ok=True)
(java_dir / "MinecraftRustLauncherActivity.java").write_text("""package dev.horizon.android;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

public final class MinecraftRustLauncherActivity extends Activity {
    private WebView webView;

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().requestFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        webView = new WebView(this);
        webView.setBackgroundColor(android.graphics.Color.rgb(17, 20, 22));
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowContentAccess(true);
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        webView.addJavascriptInterface(new RustBridge(), "RustBridge");
        setContentView(webView);
        if (state == null) {
            webView.loadUrl("file:///android_asset/minecraft-rust/index.html");
        } else {
            webView.restoreState(state);
        }
    }

    public final class RustBridge {
        @JavascriptInterface public void play() {
            runOnUiThread(() -> startActivity(
                    new Intent(MinecraftRustLauncherActivity.this, HorizonActivity.class)));
        }
    }

    @Override protected void onSaveInstanceState(Bundle out) {
        if (webView != null) webView.saveState(out);
        super.onSaveInstanceState(out);
    }

    @Override public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override protected void onDestroy() {
        if (webView != null) { webView.destroy(); webView = null; }
        super.onDestroy();
    }
}
""", encoding="utf-8")

manifest = ANDROID / "AndroidManifest.xml"
source = manifest.read_text(encoding="utf-8")
source = source.replace('android:label="Horizon Android"', 'android:label="Minecraft Rust"')
source = source.replace('android:screenOrientation="sensorLandscape"', 'android:screenOrientation="user"')
alias = """        <activity-alias android:name="com.google.androidgamesdk.GameActivity" android:targetActivity="dev.horizon.android.HorizonActivity" android:exported="true">
            <meta-data android:name="android.app.lib_name" android:value="horizon_android" />
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
            </intent-filter>
        </activity-alias>"""
if source.count(alias) != 1:
    raise SystemExit("Expected exactly one upstream launcher alias to replace")
replacement = """        <activity android:name="dev.horizon.android.MinecraftRustLauncherActivity" android:exported="true" android:screenOrientation="user" android:configChanges="orientation|screenSize|keyboardHidden|keyboard|navigation|density|screenLayout" android:theme="@android:style/Theme.Material.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
            </intent-filter>
        </activity>
        <activity-alias android:name="com.google.androidgamesdk.GameActivity" android:targetActivity="dev.horizon.android.HorizonActivity" android:exported="true">
            <meta-data android:name="android.app.lib_name" android:value="horizon_android" />
        </activity-alias>"""
source = source.replace(alias, replacement)
manifest.write_text(source, encoding="utf-8")

# android_build.py creates a clean Gradle assets staging directory later in the
# workflow. Teach it to carry the custom WebView launcher assets into that APK.
build_script = ROOT / "tools/android_build.py"
build_source = build_script.read_text(encoding="utf-8")
needle = "    assets.mkdir(parents=True, exist_ok=True)\n"
insertion = needle + "    custom_assets = ROOT / 'packaging/android/assets'\n    if custom_assets.is_dir():\n        shutil.copytree(custom_assets, assets, dirs_exist_ok=True)\n"
if build_source.count(needle) != 1:
    raise SystemExit("Could not locate the Android Gradle assets staging point")
build_script.write_text(build_source.replace(needle, insertion), encoding="utf-8")

print("Minecraft Rust WebView launcher installed; Play opens the real Horizon NativeActivity.")
