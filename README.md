# Stock Next-Day Movement Predictor

Built a predictive model to forecast next-day stock price movements by combining historical data, AI-automated event analysis, and quantitative modeling methods to assess performance.

## Overview

This simple CLI tool predicts whether a stock will go up or down tomorrow using:
- Historical price data (CSV URL)
- Up to 3 news article URLs
- An LLM for quick sentiment classification on the news and a lightweight momentum signal on the historical data

Decision rule:
- If both the historical signal and the aggregate news sentiment are positive, the tool recommends BUY
- Otherwise the tool recommends HOLD (you can adjust to SELL if desired)

## Features
- Fetches historical CSV data from a URL
- Fetches article content from URLs and extracts text
- Uses an LLM to classify news as good/bad for the stock
- Computes a simple momentum-based historical signal
- Produces a one-day ahead BUY/HOLD recommendation

## Requirements
- Python 3.9+
- An OpenAI-compatible API key exported as `OPENAI_API_KEY`

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
export OPENAI_API_KEY=your_key_here
python -m src.main \
  --historical_csv_url "https://example.com/stock_history.csv" \
  --news_urls "https://news.site/article1" "https://news.site/article2"
```

Arguments:
- `--historical_csv_url` (required): URL to CSV of daily OHLC data with at least `Date` and `Close`.
- `--news_urls` (optional, up to 3): URLs to articles about the stock.
- `--ticker` (optional): Ticker symbol for prompts/logging.
- `--window` (optional): Window for momentum calculation (default 5).

Output example:

```text
Historical signal: POSITIVE
News sentiment: POSITIVE (2/2 articles positive)
Recommendation: BUY (historical and news both positive)
```

## Historical Signal
We compute a simple momentum: compare the latest close to the moving average over the past `window` days. If the latest close is above the SMA, we label it POSITIVE; else NEGATIVE.

## News Sentiment
Each article’s extracted text is summarized and scored by an LLM as GOOD or BAD for near-term price (next day). Majority vote across provided articles yields overall sentiment.

## Notes
- This is a toy example for educational purposes, not financial advice.
- Network fetching and LLM usage may incur latency and costs.

## Development
Run formatting/linting as needed. The code is organized under `src/`:
- `src/main.py`: CLI entrypoint
- `src/historical_analysis.py`: Momentum signal
- `src/news_sentiment.py`: Article fetching and sentiment via LLM
- `src/llm.py`: LLM client wrapper
- `src/utils.py`: Helpers

