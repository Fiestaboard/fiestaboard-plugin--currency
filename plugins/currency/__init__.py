"""Display live currency exchange rates using the Frankfurter API."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://api.frankfurter.dev/v1/latest"
USER_AGENT = "FiestaBoard Currency Exchange Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--currency)"


class CurrencyPlugin(PluginBase):
    """Currency Exchange plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "currency"

    def fetch_data(self) -> PluginResult:
        try:
            base = (self.config.get("base") or "USD").upper()[:3]
            targets_raw = self.config.get("targets") or "EUR,GBP,JPY"
            targets = [t.strip().upper()[:3] for t in targets_raw.split(",") if t.strip()][:3]

            response = requests.get(
                API_URL,
                params={"base": base, "to": ",".join(targets)},
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            rates = data.get("rates", {})
            date = data.get("date", "")

            # Pad targets list to 3 entries
            while len(targets) < 3:
                targets.append("")

            def get_rate(code):
                if not code or code == base:
                    return 0.0
                return round(float(rates.get(code, 0.0)), 4)

            return PluginResult(
                available=True,
                data={
                    "base": base,
                    "rate_1_code": targets[0],
                    "rate_1_value": get_rate(targets[0]),
                    "rate_2_code": targets[1],
                    "rate_2_value": get_rate(targets[1]),
                    "rate_3_code": targets[2],
                    "rate_3_value": get_rate(targets[2]),
                    "date": date,
                },
            )
        except Exception as e:
            logger.exception("Error fetching currency rates")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        base = config.get("base", "")
        if not base or len(str(base)) != 3:
            errors.append("base must be a 3-letter ISO currency code")
        return errors

    def cleanup(self) -> None:
        pass
