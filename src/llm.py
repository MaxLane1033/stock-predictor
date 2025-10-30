import os
from typing import Literal
from openai import OpenAI

Sentiment = Literal["GOOD", "BAD"]

class LLMClient:
	def __init__(self) -> None:
		api_key = os.getenv("OPENAI_API_KEY")
		if not api_key:
			raise RuntimeError("OPENAI_API_KEY is not set")
		self.client = OpenAI(api_key=api_key)

	def classify_news_sentiment(self, ticker: str, article_text: str) -> Sentiment:
		prompt = (
			f"You are a finance analyst. Given the following article text about {ticker}, "
			"classify its near-term (next trading day) impact on the stock price as GOOD or BAD. "
			"Only answer with a single word: GOOD or BAD.\n\n"
			f"ARTICLE:\n{article_text[:6000]}\n\n"
		)
		resp = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[
				{"role": "system", "content": "Return exactly one token: GOOD or BAD."},
				{"role": "user", "content": prompt},
			],
			temperature=0.0,
			max_tokens=2,
		)
		text = resp.choices[0].message.content.strip().upper()
		return "GOOD" if "GOOD" in text else "BAD"

	def classify_history_sentiment(self, ticker: str, rationale: str) -> Sentiment:
		prompt = (
			f"Historical assessment for {ticker}: {rationale}. "
			"Return GOOD if likely up tomorrow, otherwise BAD. Only return GOOD or BAD."
		)
		resp = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[
				{"role": "system", "content": "Return exactly one token: GOOD or BAD."},
				{"role": "user", "content": prompt},
			],
			temperature=0.0,
			max_tokens=2,
		)
		text = resp.choices[0].message.content.strip().upper()
		return "GOOD" if "GOOD" in text else "BAD"
