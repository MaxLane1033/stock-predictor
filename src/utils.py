from typing import List
import requests
from bs4 import BeautifulSoup

USER_AGENT = (
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def fetch_text_from_url(url: str, timeout: int = 15) -> str:
	resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
	resp.raise_for_status()
	soup = BeautifulSoup(resp.text, "html.parser")
	for tag in soup(["script", "style", "noscript"]):
		tag.decompose()
	text = soup.get_text(separator=" ")
	return " ".join(text.split())


def majority_label(labels: List[str]) -> str:
	if not labels:
		return "NEUTRAL"
	good = sum(1 for l in labels if l == "GOOD")
	bad = sum(1 for l in labels if l == "BAD")
	if good > bad:
		return "GOOD"
	if bad > good:
		return "BAD"
	return "NEUTRAL"
