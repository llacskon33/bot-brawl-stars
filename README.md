# Brawl Stars Stats

Aplicación Android en Python + Kivy para consultar estadísticas de jugadores de Brawl Stars.

## Requisitos

- Python 3.10 o superior para probar en escritorio.
- Linux o WSL2 para compilar el APK con Buildozer.
- Una API key propia de Brawl Stars.

## Prueba en escritorio

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env            # opcional
python main.py
```

También puedes introducir la API key directamente en la aplicación.

## API key

Obtén una API key en el portal oficial de desarrolladores de Brawl Stars. No la publiques en GitHub ni la incrustes en un APK que vayas a distribuir. La app permite introducirla en la pantalla; para pruebas locales también puede leerse desde `.env`.

## Crear el APK

En Linux/WSL instala Buildozer y sus dependencias del sistema según tu distribución. Después:

```bash
pip install buildozer cython
buildozer android debug
```

El APK aparecerá en la carpeta `bin/`. El primer build puede tardar bastante porque descarga el SDK y el NDK de Android.

## Uso

1. Abre la aplicación.
2. Escribe tu API key.
3. Introduce el tag del jugador, con o sin `#`.
4. Pulsa **Consultar estadísticas**.

La aplicación muestra nombre, tag, trofeos, récord de trofeos, nivel de experiencia, victorias, brawlers y club.
