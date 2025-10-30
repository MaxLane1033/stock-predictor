import argparse
from typing import List
from .historical_analysis import compute_momentum_signal
from .news_sentiment import score_articles


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Next-day stock movement predictor")
	parser.add_argument("--historical_csv_url", required=True, help="URL to historical CSV with Close column")
	parser.add_argument("--news_urls", nargs="*", help="Up to three news article URLs", default=[])
	parser.add_argument("--ticker", default="the stock", help="Ticker symbol, used in prompts")
	parser.add_argument("--window", type=int, default=5, help="SMA window for momentum")
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	history_label, history_rationale = compute_momentum_signal(args.historical_csv_url, window=args.window)
	news_urls: List[str] = args.news_urls[:3]
	news_label, num_good, total = score_articles(args.ticker, news_urls)
	buy = history_label == "GOOD" and news_label == "GOOD"
	print(f"Historical signal: {history_label} ({history_rationale})")
	if total > 0:
		print(f"News sentiment: {news_label} ({num_good}/{total} articles positive)")
	else:
		print("News sentiment: NEUTRAL (no articles provided)")
	print("Recommendation: " + ("BUY (historical and news both positive)" if buy else "HOLD"))


if __name__ == "__main__":
	main()
