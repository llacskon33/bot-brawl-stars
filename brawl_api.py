from urllib.parse import quote

import requests


class BrawlAPIError(Exception):
    """Error presentado por la API de Brawl Stars o por la red."""


class BrawlStarsAPI:
    BASE_URL = "https://api.brawlstars.com/v1"
    TIMEOUT = 15

    def __init__(self, api_key):
        self.api_key = (api_key or "").strip()

    @staticmethod
    def normalize_tag(tag):
        value = (tag or "").strip().upper()
        if value.startswith("#"):
            value = value[1:]
        if not value:
            raise ValueError("El tag del jugador no puede estar vacío.")
        return value

    def get_player(self, tag):
        if not self.api_key:
            raise BrawlAPIError("La API key no puede estar vacía.")
        normalized = self.normalize_tag(tag)
        url = f"{self.BASE_URL}/players/%23{quote(normalized, safe='')}"
        try:
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.TIMEOUT,
            )
        except requests.Timeout as exc:
            raise BrawlAPIError("La solicitud tardó demasiado. Comprueba tu conexión.") from exc
        except requests.RequestException as exc:
            raise BrawlAPIError("No se pudo conectar con la API de Brawl Stars.") from exc

        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as exc:
                raise BrawlAPIError("La API devolvió una respuesta inválida.") from exc
        if response.status_code == 400:
            raise BrawlAPIError("El tag del jugador no es válido.")
        if response.status_code == 403:
            raise BrawlAPIError("La API key no es válida o no tiene permiso.")
        if response.status_code == 404:
            raise BrawlAPIError("No se encontró ningún jugador con ese tag.")
        if response.status_code == 429:
            raise BrawlAPIError("Demasiadas solicitudes. Inténtalo más tarde.")
        raise BrawlAPIError(f"La API devolvió el código HTTP {response.status_code}.")
