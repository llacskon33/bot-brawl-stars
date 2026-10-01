import os
import subprocess
import zipfile
import shutil

# Paths
SDK_DIR = "/usr/local/lib/android/sdk"
BUILD_TOOLS_VERSION = "34.0.0"
PLATFORM_VERSION = "android-34"

AAPT2 = f"{SDK_DIR}/build-tools/{BUILD_TOOLS_VERSION}/aapt2"
D8 = f"{SDK_DIR}/build-tools/{BUILD_TOOLS_VERSION}/d8"
ZIPALIGN = f"{SDK_DIR}/build-tools/{BUILD_TOOLS_VERSION}/zipalign"
APKSIGNER = f"{SDK_DIR}/build-tools/{BUILD_TOOLS_VERSION}/apksigner"
ANDROID_JAR = f"{SDK_DIR}/platforms/{PLATFORM_VERSION}/android.jar"

# Build directories
BUILD_DIR = "build"
GEN_DIR = f"{BUILD_DIR}/gen"
CLASSES_DIR = f"{BUILD_DIR}/classes"
DEX_DIR = f"{BUILD_DIR}/dex"
OUTPUT_DIR = "app/build/outputs/apk/debug"

def run_cmd(cmd, description):
    print(f"--> Running: {description}")
    print(f"Command: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR: {description} failed!")
        print(f"STDOUT:\n{res.stdout}")
        print(f"STDERR:\n{res.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    print("SUCCESS")
    return res.stdout

def main():
    # Clean previous build directories
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(GEN_DIR, exist_ok=True)
    os.makedirs(CLASSES_DIR, exist_ok=True)
    os.makedirs(DEX_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Compile resources
    run_cmd(
        f"{AAPT2} compile --dir app/src/main/res -o {BUILD_DIR}/compiled_res.zip",
        "Compile Resources"
    )

    # 2. Link resources and generate R.java
    run_cmd(
        f"{AAPT2} link -o {BUILD_DIR}/unaligned.apk -I {ANDROID_JAR} "
        f"--manifest app/src/main/AndroidManifest.xml --java {GEN_DIR} {BUILD_DIR}/compiled_res.zip",
        "Link Resources and Generate R.java"
    )

    # Find generated R.java
    r_java_path = f"{GEN_DIR}/com/pyla/botbrawlstars/R.java"
    if not os.path.exists(r_java_path):
        raise FileNotFoundError(f"Generated R.java not found at {r_java_path}")

    # 3. Compile Kotlin/Java sources
    kotlin_src = "app/src/main/java/com/pyla/botbrawlstars/MainActivity.kt"
    run_cmd(
        f"kotlinc -cp {ANDROID_JAR} -d {CLASSES_DIR} {kotlin_src} {r_java_path}",
        "Compile Kotlin & Java Sources"
    )

    # 4. Dex classes to classes.dex
    # Find all compiled class files
    class_files = []
    for root, _, files in os.walk(CLASSES_DIR):
        for f in files:
            if f.endswith(".class"):
                class_files.append(os.path.join(root, f))
    
    if not class_files:
        raise FileNotFoundError("No compiled class files found!")

    class_files_str = " ".join(f"'{cf}'" for cf in class_files)
    run_cmd(
        f"{D8} --lib {ANDROID_JAR} --output {DEX_DIR} {class_files_str}",
        "Dex Compiled Class Files"
    )

    # 5. Add classes.dex to the unaligned APK
    dex_file_path = f"{DEX_DIR}/classes.dex"
    if not os.path.exists(dex_file_path):
        raise FileNotFoundError(f"classes.dex not found at {dex_file_path}")

    print("--> Adding classes.dex to APK")
    unaligned_apk = f"{BUILD_DIR}/unaligned.apk"
    with zipfile.ZipFile(unaligned_apk, 'a') as apk:
        apk.write(dex_file_path, "classes.dex")
    print("SUCCESS")

    # 6. Align APK
    aligned_apk = f"{BUILD_DIR}/aligned.apk"
    run_cmd(
        f"{ZIPALIGN} -f 4 {unaligned_apk} {aligned_apk}",
        "Align APK"
    )

    # 7. Generate temporary debug keystore if not exists
    keystore_path = f"{BUILD_DIR}/debug.keystore"
    run_cmd(
        f"keytool -genkey -v -keystore {keystore_path} -storepass android "
        f"-alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 "
        f'-dname "CN=Android Debug,O=Android,C=US"',
        "Generate Debug Keystore"
    )

    # 8. Sign APK
    final_apk_path = f"{OUTPUT_DIR}/app-debug.apk"
    run_cmd(
        f"{APKSIGNER} sign --ks {keystore_path} --ks-pass pass:android "
        f"--key-pass pass:android --out {final_apk_path} {aligned_apk}",
        "Sign APK"
    )

    print(f"\n🎉 BUILD SUCCESSFUL! APK generated at: {final_apk_path}")
    print(f"APK size: {os.path.getsize(final_apk_path) / 1024:.2f} KB")

if __name__ == "__main__":
    main()
