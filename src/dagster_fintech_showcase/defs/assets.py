import csv
from datetime import datetime, timezone
from pathlib import Path

import dagster as dg
import requests

DATA_FILE = Path("data/rates.csv")


@dg.asset
def fx_rates() -> dg.MaterializeResult:
    fx = requests.get(
        "https://api.frankfurter.dev/v1/latest",
        params={"base": "USD", "symbols": "INR"},
        timeout=10,
    )
    fx.raise_for_status()
    usd_inr = fx.json()["rates"]["INR"]

    btc = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin", "vs_currencies": "usd"},
        timeout=10,
    )
    btc.raise_for_status()
    btc_usd = btc.json()["bitcoin"]["usd"]

    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    DATA_FILE.parent.mkdir(exist_ok=True)
    is_new = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["fetched_at", "usd_inr", "btc_usd"])
        writer.writerow([fetched_at, usd_inr, btc_usd])

    return dg.MaterializeResult(
        metadata={"usd_inr": usd_inr, "btc_usd": btc_usd, "fetched_at": fetched_at}
    )