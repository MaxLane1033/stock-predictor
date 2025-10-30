from typing import List, Tuple
from .llm import LLMClient
from .utils import fetch_text_from_url, majority_label


def score_articles(ticker: str, urls: List[str]) -> Tuple[str, int, int]:
	if not urls:
		return ("NEUTRAL", 0, 0)
	client = LLMClient()
	labels = []
	for url in urls[:3]:
		try:
			text = fetch_text_from_url(url)
			label = client.classify_news_sentiment(ticker=ticker, article_text=text)
			labels.append(label)
		except Exception:
			labels.append("BAD")  # conservative fallback
	agg = majority_label(labels)
	return agg, labels.count("GOOD"), len(labels)
