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
