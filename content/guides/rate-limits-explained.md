---
slug: rate-limits-explained
title: Rate limits on free LLM APIs, explained
lede: A rate limit is a published cap on how much you can send, often per minute or per day, measured in requests, tokens, or a vendor unit that is not a token.
description: What RPM, RPD and tokens-per-day mean on free LLM APIs, how this tracker records limits, and how to handle 429 errors without inventing unpublished quotas.
date_published: 2026-11-12
date_modified: 2026-11-12
related: best-free-llm-apis, how-to-use-free-openai-compatible-apis, keep-api-keys-safe, official-vs-gateway-providers
---

## What is a rate limit on a free LLM API?

A rate limit is a cap on how much you may use the API in a window of time. Providers commonly publish limits as requests per minute (RPM), requests per day (RPD), tokens per day, or a credit or vendor unit such as a monthly call allowance. The cap may also differ by model. When this tracker has a public figure, it appears in the “limits” field or in tokens per day. When we do not, we show **Not published** instead of guessing.

Limits exist to keep free tiers shareable and to protect the service. Hitting one is usually a signal to slow down, not a sign that your key is necessarily revoked.

## What do RPM, RPD and tokens per day mean?

**Requests per minute (RPM)** is how many HTTP calls you may start in a minute, often counted at the project or key level. A chat request counts as one request whether the reply is short or long, unless the provider says otherwise.

**Requests per day (RPD)** is the same idea over a day. Some free plans publish a low daily request cap even when they do not publish a token cap. In our list, OpenRouter’s recorded free-model limit is an example of a daily request cap until credits are bought — always re-check their official page for the live number.

**Tokens per day** is a cap on the text you send and, usually, the text the model returns. A token is a small piece of text, typically a few characters or a short word, not a whole document. Providers do not all use the same tokenizer, so a token on one official page is not guaranteed to match another. If we have a numeric daily token figure, we store it in `tokens_per_day` and show it on the card. If we only have a prose allowance (“free experiment tier,” “10,000 Neurons/day”), we keep that wording and leave the numeric field empty.

Some official clouds use a unit that is **not** a token. Cloudflare Workers AI, in our list, publishes a daily Neuron allowance, and our notes say the token equivalent depends on the model. Do not convert Neurons into tokens unless the official docs give you a method.

## Why is “Not published” so common in the limits column?

Because many providers describe a free tier without putting a single RPM or RPD number on a public page, or they hide the exact cap behind a login. We do not copy numbers from unofficial screenshots or from memory. A missing number is not “unlimited.” It may still be enforced.

The [current snapshot](/guides/best-free-llm-apis) therefore separates providers that publish a daily token number from those that do not. Sorting the whole internet by tokens per day would quietly drop useful official tiers that only publish a prose description.

## Are all limits daily, and do they reset at midnight?

Not always, and not always in your timezone. Some windows are rolling 24 hours; some reset at midnight UTC; some are monthly; some are one-time signup credits that never refill. Our `tokens_per_day` field is only used when the public source is a daily token figure. A 1,000-calls-per-month trial, a 90-day credit, or a “while experimental” offer is stored in the allowance or limits text instead.

If you need to know the exact reset, the official rate-limit or billing page is the source. We will not invent a reset time.

## What happens when I hit a limit?

Most compatible APIs return HTTP **429** (Too Many Requests) or an error body that mentions rate limits. Some SDKs raise an exception with the same status. The response may include a `Retry-After` header, or a JSON field with a wait time. If it does, wait at least that long. If it does not, back off — wait, retry once or twice, then stop. Tight retry loops can turn a daily cap into an outage for your own key.

A 401 or 403 is usually authentication or permission, not a rate limit. A 400 with a model error usually means the model id is wrong or not included in the free tier. Read the body before you retry.

## How should I design a small app around a free cap?

Make one test request before you add a batch job. Log the model id and the status code, never the key. If you run an agent or an IDE plugin, set a local maximum number of calls, because tools may retry on their own. Prefer official providers when the job is important, because a relay can add a second, unpublished cap on top of the upstream one.

When you compare options, read the allowance as a sentence. “200,000 tokens/day on listed models,” “1,000 calls/month,” and “$5 starter credit” are not interchangeable. The first is a daily text cap, the second is a monthly request cap, the third is a credit that may end when it is spent or when a trial expires. Our [best free LLM APIs](/guides/best-free-llm-apis) tables keep those distinctions instead of producing a single score.

## Do limits vary by model?

Often yes. A provider may publish one cap for a small model and a tighter cap for a larger one, or they may share one pool across models. Our notes say so when the public source said so — Groq’s entry, for example, notes that limits vary by model, and the numeric daily token field is the published figure we recorded for listed models. The official rate-limit page remains the live authority.

If you switch model ids, do not assume the old cap still applies.

## How does this relate to cards and trials?

A published free limit can still sit behind a credit card, a phone check, or a short trial window. Cerebras, in our data, is recorded as a 1,000,000 tokens/day allowance during a $5 30-day trial with a card required. SambaNova’s free plan is recorded as requiring a card and a purchase after a mid-October change. Those details belong in the allowance and notes, not in a hidden multiplier. Confirm them on the official plans page before you design around the cap.

## How can I stay inside a cap without a published number?

Use small prompts, cap `max_tokens` when the API supports it, and watch the provider dashboard if one exists. Avoid concurrent workers until you know a request succeeds. If you receive 429s immediately, stop and read the official docs. Do not try to “measure” an unpublished limit by hammering the API; that can look like abuse and can get a key disabled.

This site’s last snapshot of published limits was {{list_updated}}. For how to form the request itself, return to [How to use free OpenAI-compatible APIs](/guides/how-to-use-free-openai-compatible-apis).
