---
slug: about
title: About this tracker
lede: A weekday-updated list of sites that give free LLM API tokens, with the figures each provider actually publishes.
description: How Free LLM API Tokens Tracker is compiled, how often it is updated, and why some figures are marked Not published.
date_published: 2026-11-12
date_modified: 2026-11-12
---

## What is this site?

Free LLM API Tokens Tracker is a public catalogue of websites and providers that advertise a free allowance for large language model APIs. For each entry we record whether the API is OpenAI compatible, the published base URL, the free allowance, a tokens-per-day figure when one is published, rate limits, whether a card is required, and a relay-risk flag. The machine-readable source is [data.json](/data.json).

The aim is practical: if you want to try a model through an API without paying first, you should be able to see what is on offer, what is not published, and where the official documentation lives. The site is independent and is not affiliated with any provider in the list.

## How are the figures collected?

Every quota, price, rate limit and endpoint on this site is copied from a provider’s own public pages on the date shown in that entry. If a provider does not publish a figure, we show **Not published** (or “Unspecified” in the raw data). We do not estimate, scrape private dashboards, or fill gaps from memory.

When an offer ends, we keep the row and mark the allowance so the history stays visible. Ended offers are hidden on the home page unless you choose to show them.

Some sites are official model makers or clouds. Others are gateways or resellers. We flag unofficial relays so you can avoid sending private prompts through them. Read [relay and gateway risks](/guides/relay-gateway-risks) before you use a flagged site.

## How often is the list updated?

The list is reviewed on weekdays. The “last checked” time on the home page is stored with an India Standard Time offset (Asia/Calcutta) and was {{list_updated}} at the last snapshot. An entry also has its own “updated” date, which changes only when that row changes.

A [weekday changelog](/) on the home page records additions and corrections. Guides that include live tables, such as [Best free LLM APIs (current)](/guides/best-free-llm-apis), are regenerated from the same data file whenever the list is updated.

## What does “OpenAI compatible” mean here?

“Yes” means you can point an OpenAI SDK, or another client that speaks the OpenAI HTTP API, at the provider’s base URL and use that provider’s key. “Partial” means only some models or features work that way. “Not published” means we have not seen a clear public statement, and we will not guess. See [What is an OpenAI-compatible API?](/guides/what-is-an-openai-compatible-api) and [How to use free OpenAI-compatible APIs](/guides/how-to-use-free-openai-compatible-apis).

## Who is behind the site?

The site is maintained as a public tracker. For questions, corrections or a takedown request, email [{{email}}](mailto:{{email}}). Please do not send API keys or other secrets to that address.

If you found a published allowance that does not match our list, include the provider name and a link to the official page you used. We will check the public source before changing a figure.

## Advertising and analytics

The site may show ads and may use Google Analytics once those services are configured. Details, cookie use and opt-out links are in the [privacy policy](/privacy). The [terms](/terms) explain that the list is provided as-is and that you must check each provider’s current terms before you rely on a free tier.
