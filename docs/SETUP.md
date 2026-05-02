# Currency Exchange Setup Guide

Display live currency exchange rates using the Frankfurter API.

## Overview

The Currency Exchange plugin fetches the latest exchange rates from the Frankfurter API (api.frankfurter.dev), which is backed by the European Central Bank. Display rates for up to three target currencies relative to a base currency. No API key required.

- API reference: https://www.frankfurter.app/docs/

### Prerequisites

No API key required. Uses ECB daily rates.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Currency Exchange**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `currency` plugin variables:
   ```
   {{{ currency.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `currency.base` | Base currency code | `USD` |
| `currency.rate_1_code` | First target currency code | `EUR` |
| `currency.rate_1_value` | Exchange rate for first target currency | `0.9234` |
| `currency.rate_2_code` | Second target currency code | `GBP` |
| `currency.rate_2_value` | Exchange rate for second target currency | `0.7912` |
| `currency.rate_3_code` | Third target currency code | `JPY` |
| `currency.rate_3_value` | Exchange rate for third target currency | `149.82` |
| `currency.date` | Date of the rates | `2026-05-01` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `base` | Base Currency | ISO 4217 currency code to convert from (e.g. USD). | `USD` |
| `targets` | Target Currencies | Comma-separated ISO 4217 codes to show (e.g. EUR,GBP,JPY). | `EUR,GBP,JPY` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch rates (ECB updates once per business day). | `3600` |

## Troubleshooting

- **Rate not found** — check the currency code is a valid ISO 4217 code.
- **Rates not updating** — ECB rates update once per business day; weekends show Friday's rate.

