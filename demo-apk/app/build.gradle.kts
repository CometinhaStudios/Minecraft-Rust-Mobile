plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "br.com.cometinha.minecraftrust.preview"
    compileSdk = 35
    defaultConfig {
        applicationId = "br.com.cometinha.minecraftrust.preview"
        minSdk = 23
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0-alpha-teste-1"
    }
}
