"""Tests for the currency plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.currency import CurrencyPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "currency",
    "name": "Currency Exchange",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "base": {
                "type": "string",
                "title": "Base Currency",
                "description": "ISO 4217 currency code to convert from (e.g. USD).",
                "default": "USD",
                "minLength": 3,
                "maxLength": 3
            },
            "targets": {
                "type": "string",
                "title": "Target Currencies",
                "description": "Comma-separated ISO 4217 codes to show (e.g. EUR,GBP,JPY).",
                "default": "EUR,GBP,JPY"
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch rates (ECB updates once per business day).",
                "default": 3600,
                "minimum": 1800
            }
        },
        "required": [
            "base"
        ]
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "base": "USD",
    "date": "2026-05-01",
    "rates": {
        "EUR": 0.9234,
        "GBP": 0.7912,
        "JPY": 149.82
    }
}
""")


@pytest.fixture
def plugin():
    return CurrencyPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = CurrencyPlugin(MANIFEST)
    p.config = json.loads("""
{
    "base": "USD",
    "targets": "EUR,GBP,JPY"
}
""")
    return p


class TestCurrencyPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "currency"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.currency.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "base" in result.data, "missing variable: base"
        assert "rate_1_code" in result.data, "missing variable: rate_1_code"
        assert "rate_1_value" in result.data, "missing variable: rate_1_value"
        assert "rate_2_code" in result.data, "missing variable: rate_2_code"
        assert "rate_2_value" in result.data, "missing variable: rate_2_value"
        assert "rate_3_code" in result.data, "missing variable: rate_3_code"
        assert "rate_3_value" in result.data, "missing variable: rate_3_value"
        assert "date" in result.data, "missing variable: date"

    @patch("plugins.currency.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.currency.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

