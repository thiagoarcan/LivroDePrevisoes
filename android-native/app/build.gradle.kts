plugins {
    id("com.android.application")
    kotlin("android")
}
android {
    namespace = "br.com.livrodeprevisoes"
    compileSdk = 36
    // Include the same Kotlin redistribution notices as the manual APK pipeline.
    sourceSets.getByName("main").assets.srcDir("../tools/apk-assets")
    defaultConfig {
        applicationId = "br.com.livrodeprevisoes"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}
dependencies {
    implementation(project(":domain"))
    implementation(project(":data"))
    implementation(project(":alerts"))
    testImplementation("org.json:json:20240303")
    testImplementation("junit:junit:4.13.2")
}
