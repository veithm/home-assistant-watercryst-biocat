import requests
import logging

_LOGGER = logging.getLogger(__name__)
API_BASE = "https://appapi.watercryst.com"

def pause_protection(api_key: str, minutes: int = 60):
    url = f"{API_BASE}/leakageprotection/pause?minutes={minutes}"
    headers = {"X-API-Key": api_key}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        _LOGGER.info(f"[Watercryst] Leakage Protection für {minutes} Minuten pausiert.")
    except Exception as e:
        _LOGGER.error(f"[Watercryst] Fehler beim Pausieren: {e}")

def unpause_protection(api_key: str):
    url = f"{API_BASE}/leakageprotection/unpause"
    headers = {"X-API-Key": api_key}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        _LOGGER.info("[Watercryst] Leakage Protection wurde reaktiviert.")
    except Exception as e:
        _LOGGER.error(f"[Watercryst] Fehler beim Unpausieren: {e}")
