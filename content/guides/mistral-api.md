---
slug: mistral-api
title: Mistral API free experiment tier and compatible endpoint
lede: Mistral’s La Plateforme is an official, OpenAI-compatible API. Our list records a free experiment tier, but it does not publish a tokens-per-day number or a card requirement we can quote.
description: Mistral (La Plateforme) free-tier snapshot from this tracker, including the OpenAI-compatible base URL, what “Not published” means for limits and cards, and how to call the API in Python or JavaScript.
date_published: 2026-11-12
date_modified: 2026-11-12
provider_id: mistral
related: how-to-use-free-openai-compatible-apis, gemini-api, official-vs-gateway-providers, rate-limits-explained
---

## What is Mistral on this tracker?

The row is named **{{name}}** and is listed as an **{{category}}**. OpenAI compatibility is **{{openai_compatible}}**. The recorded free allowance is “{{free_allowance}}”. Tokens per day are **{{tokens_per_day}}**. Limits are **{{limits}}**. Card required is **{{card_required}}**. Relay warning: **{{relay}}**. There are no extra notes stored on this row: {{notes}}

“Free experiment tier” is a prose description, not a number we can turn into tokens per day. The official URL we store is [{{url}}]({{url}}). First listed {{first_reported}}, entry updated {{entry_updated}}, list snapshot {{list_updated}}.

{{FACTBOX}}

## Why are so many fields “Not published”?

Because the public sources we used for this row did not give us a single daily token cap, a numeric RPM/RPD table we could copy into the limits field, or a clear yes/no card rule. We display **Not published** rather than filling those gaps from a tutorial or from another tracker. That is the same rule as the rest of the site, described in the [about](/about) page.

Not published is not the same as unlimited, and it is not the same as “no card will ever be asked.” During signup, believe the official form. During use, believe official rate-limit responses and the official docs. See [Rate limits explained](/guides/rate-limits-explained).

## How do I call the published base URL?

The base URL we record is `{{base_url}}`. Create a key in Mistral’s official platform, store it in an environment variable, and use the official OpenAI SDK. Copy the model id from Mistral’s official documentation. Experiment-tier availability can differ by model, and we will not invent the list.

{{SNIPPETS}}

Mistral also documents native APIs and official SDKs. Those may include features that you should not assume exist on every compatible stub. If you only need a basic chat completion, the compatible client is usually enough to test the account.

## Is an “experiment tier” a standing free plan?

The wording in our allowance field is “Free experiment tier.” That suggests a tier intended for experimentation, but the exact duration, model list and future of the tier are official-product questions. We do not upgrade the wording to “free forever” or downgrade it to “trial ended” without a public source. If Mistral publishes a change, we will update the row; until then, re-read the official docs when you start a project that must last longer than an experiment.

If you need a row with a numeric daily token figure, use the tokens-per-day table in [Best free LLM APIs (current)](/guides/best-free-llm-apis) and still confirm the official page. Mistral will not appear in that particular table while `tokens_per_day` is empty, even though it remains an official compatible option with a recorded free experiment tier.

## Is Mistral a relay?

No. It is official, with **{{relay}}** relay warning. You still need to read Mistral’s terms for how prompts are handled on the experiment tier. Prefer official providers over flagged gateways for private text, as explained in [Official providers vs gateways](/guides/official-vs-gateway-providers) and [Relay and gateway risks](/guides/relay-gateway-risks).

Keep the key out of git and out of browser demos. [How to keep API keys safe](/guides/keep-api-keys-safe) applies the same way as for any other host.

## How might I try it as a first official API?

If you are comfortable with some fields being unpublished, Mistral is a straightforward official compatible target: published base URL, official docs, no relay flag in our data. Follow [A free LLM API for beginners](/guides/free-llm-api-for-beginners): official account, environment variable, exact base URL, official model id, one short request, then look for a dashboard or error body before you add a loop.

Compare it with [Gemini](/guides/gemini-api), which also lacks a numeric tokens-per-day field in our list but does record a no-card value and a note about free-tier prompt use, and with [Groq](/guides/groq-free-api), which publishes daily token and request figures. The right choice depends on official terms and on what you are sending, not on a score from this site.

## How do I correct this entry?

If official pages now publish a card rule, a numeric cap, or a change to the experiment tier, [send the public link](/contact). We would rather keep “Not published” than replace it with an unofficial number, and we will update the fact box when a citable official source is available.


## How do I work with an allowance that has no number attached?

Use operational caution instead of a homemade quota. Send one short request. Watch official dashboards or error bodies. Add a local maximum in your own code or assistant settings. If you receive a 429 or a message about exceeding an experiment cap, stop and read the official docs. Do not try to discover an unpublished number by running a tight loop; that can look like abuse.

When Mistral’s official pages do publish a number you need, prefer that number over anything cached in a chat or a blog. If it is a stable public figure, we can add it to the row later. Until then, the honest state of our list is the fact box above.

## What belongs in official docs that will never appear here?

Model cards, context-window sizes, pricing for paid plans, regional availability, and feature matrices for fine-tuning or batch jobs belong on docs.mistral.ai (or whatever official URL is current). This tracker only stores a free-allowance snapshot and a compatible base URL. Use official docs for product capability, and use this page only as a reminder of what was published about the experiment tier on the date of our entry.
