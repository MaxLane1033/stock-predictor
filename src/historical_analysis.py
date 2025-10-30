from typing import Tuple
import io
import requests
import pandas as pd

USER_AGENT = (
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def compute_momentum_signal(csv_url: str, window: int = 5) -> Tuple[str, str]:
	resp = requests.get(csv_url, headers={"User-Agent": USER_AGENT}, timeout=20)
	resp.raise_for_status()
	buf = io.StringIO(resp.text)
	df = pd.read_csv(buf)
	if "Close" not in df.columns:
		raise ValueError("CSV must contain a Close column")
	df = df.dropna(subset=["Close"])  # safety
	if len(df) < window + 1:
		raise ValueError("Not enough data to compute momentum")
	df["SMA"] = df["Close"].rolling(window=window).mean()
	last = df.iloc[-1]
	prev = df.iloc[-2]
	latest_close = float(last["Close"])
	latest_sma = float(last["SMA"]) if pd.notna(last["SMA"]) else float(prev["SMA"])  # fallback
	label = "GOOD" if latest_close >= latest_sma else "BAD"
	rationale = (
		f"latest_close={latest_close:.4f}, sma_{window}={latest_sma:.4f}, "
		f"signal={'above' if label=='GOOD' else 'below'} SMA"
	)
	return label, rationale
