---
slug: best-free-llm-apis
title: Best free LLM APIs (current snapshot)
lede: A current snapshot of published free allowances from our provider list — not a paid ranking, and not a substitute for the official pages.
description: Current snapshot of the best-known free LLM API allowances, generated from this tracker’s data.json, including official providers and published tokens-per-day figures.
date_published: 2026-11-12
date_modified: 2026-11-12
related: how-to-use-free-openai-compatible-apis, official-vs-gateway-providers, relay-gateway-risks, free-llm-api-for-beginners
---

## What does “best” mean on this page?

“Best” here means “currently listed with a published free allowance you can verify,” grouped so you can compare official providers, published daily token figures, and OpenAI-compatible options that do not require a card in our data. It is not a paid placement, a benchmark, or a promise that one API is faster or more accurate than another. Every number is copied from our [provider list](/), last snapshotted at {{list_updated}}.

If a provider does not publish tokens per day, they will not appear in the daily-token table even if their free tier is useful. We would rather leave a gap than invent a rank.

{{STATS}}

## Which providers publish a daily token figure?

The table below includes only **active** offers in our data that have a numeric `tokens_per_day` value. A blank or “Not published” tokens-per-day field is not treated as zero. Higher published caps are not automatically safer: several of the largest figures belong to gateways with a **relay warning**. Read [Relay and gateway risks](/guides/relay-gateway-risks) before you put source code or private text into those services.

A tokens-per-day number also does not tell you which models are included, whether the cap is shared across models, or whether a trial later requires a card. Use the official link in each row.

{{TABLE_TPD}}

## Which official providers are in the current snapshot?

Official providers are model makers or clouds, not unofficial resellers. They can still have short trials, require a card, or leave limits unpublished. The table is alphabetical. Ended official offers are not shown here; they remain on the home page behind “Show ended offers.”

{{TABLE_OFFICIAL}}

Some official rows are a better first test than others because they document an OpenAI-compatible base URL and state that no card is required. That still is not a quality ranking. For example, a 30-day trial with a high daily cap is not the same as an ongoing free tier, and a cap measured in “Neurons” is not a token count. Individual notes live in the provider guides for [Groq](/guides/groq-free-api), [Gemini](/guides/gemini-api), [Cloudflare Workers AI](/guides/cloudflare-workers-ai), [Cerebras](/guides/cerebras-api), [SambaNova](/guides/sambanova-cloud) and [Mistral](/guides/mistral-api).

## Which OpenAI-compatible APIs list no card and no relay warning?

This cut is useful if you want to try the [OpenAI SDK](/guides/how-to-use-free-openai-compatible-apis) without a card and without an unofficial relay, according to our current fields. “No” in the card column can still change — some providers add a card later or after a credit is used up. Confirm on the official site.

{{TABLE_NO_CARD_OAI}}

Gateways can appear here if we have not flagged them as relays and they document compatibility. A missing relay flag is not a security audit. If you cannot tell who operates the GPU, treat prompts as public.

## What about offers that have already ended?

Ended offers stay in [data.json](/data.json) so that old links and screenshots remain explainable. They are hidden on the home page by default. Do not plan new work on them.

{{TABLE_ENDED}}

## How should I choose a starting point from these tables?

Use a short path instead of trying to optimise a single “winner”:

1. Decide whether you will send only throwaway prompts, or anything private. Private work should stay on official providers you trust, or on a model you run locally.
2. Filter for OpenAI compatibility if you want the SDK pattern in our how-to guide.
3. Prefer a published base URL. If the base URL is Not published, we will not invent one.
4. Read the allowance in words, not only the tokens-per-day column. A one-time credit, a 30-day trial, a monthly call cap and a daily token cap are different shapes of “free.”
5. Open the official pricing or rate-limit page and confirm the figure on the day you sign up.
6. Make one small request, then look at the dashboard before you write a loop.

Speed, quality and context-window size are not fields we invent. If you need those, measure them yourself or read the provider’s official model card.

## Why do some well-known names look modest in the tables?

A well-known official API may publish a free tier without a daily token number, so it will not lead a tokens-per-day sort. Another may publish a high cap that only applies during a card-backed trial. A gateway may advertise millions of tokens per day and still be a relay. Sorting by a single column would hide those differences, which is why this page keeps several tables and no single score.

OpenRouter, for example, is listed as a gateway with `:free` models and a published daily request cap until credits are bought; it does not have a tokens-per-day figure in our file, so it will not appear in the first table. That is a limitation of the data, not a judgement of the product.

## How is this page kept current?

Whenever [data.json](/data.json) is updated, this page’s tables, counts and “snapshot” timestamp are regenerated. The surrounding explanation stays the same unless we edit it. If a number on this page disagrees with a provider’s site, trust the provider’s site and [tell us](/contact) with a link to the official page.

For a comparison of official clouds versus gateways, continue with [Official providers vs gateways](/guides/official-vs-gateway-providers). For limits language such as RPM and RPD, see [Rate limits explained](/guides/rate-limits-explained).
