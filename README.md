# bot-brawl-stars

Aplicación Android para automatizar acciones en Brawl Stars mediante un bot con IA (Pyla AI).

## Estado actual (Fase 1)

Esta primera fase entrega una versión **mínima y funcional** de la app:

- Se instala y abre correctamente en Android 13 (API 33).
- Interfaz básica con un botón **Iniciar** y otro **Detener**.
- Sin lógica de bot ni de IA todavía; esas funciones se añadirán en fases posteriores.

## Requisitos

- Android Studio (Koala o superior) o Gradle 8.7 con JDK 17.
- Android SDK con la plataforma `android-34` y `android-33` (o superior) instaladas.

## Compilar e instalar

```bash
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

O simplemente abre el proyecto en Android Studio y pulsa "Run".