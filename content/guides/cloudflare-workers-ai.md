---
slug: cloudflare-workers-ai
title: Cloudflare Workers AI free allowance and compatible API
lede: Cloudflare Workers AI is an official, OpenAI-compatible API. Its published free cap is in Neurons per day, not tokens, and the base URL includes your account id.
description: Cloudflare Workers AI snapshot from this tracker: 10,000 Neurons/day free allowance, OpenAI-compatible base URL with ACCOUNT_ID, and how to call it without inventing a token equivalent.
date_published: 2026-11-12
date_modified: 2026-11-12
provider_id: cloudflare
related: how-to-use-free-openai-compatible-apis, gemini-api, rate-limits-explained, official-vs-gateway-providers
---

## What is Cloudflare Workers AI on this tracker?

{{name}} is listed as an **{{category}}**, with OpenAI compatibility **{{openai_compatible}}**. The recorded free allowance is “{{free_allowance}}”. Tokens per day are **{{tokens_per_day}}**, because the cap is not published as tokens. Limits are **{{limits}}**. Card required is **{{card_required}}**. Relay warning: **{{relay}}**. Our notes say: {{notes}}

The official URL we store is [{{url}}]({{url}}). The entry was first listed on {{first_reported}} and last updated on {{entry_updated}}. The list snapshot is {{list_updated}}.

{{FACTBOX}}

## Why does this page refuse to convert Neurons into tokens?

Because our notes say the token equivalent depends on the model, and the official unit is Neurons. A homemade conversion would be an invented quota, which this site does not publish. If you need to know how a specific model spends Neurons, use Cloudflare’s official pricing documentation. For the wider idea that not every cap is a token cap, see [Rate limits explained](/guides/rate-limits-explained).

When you compare this row with providers that publish tokens per day, do not sort them as if the units were the same. The [current snapshot](/guides/best-free-llm-apis) will show Cloudflare in the official table with its Neuron wording, and it will be absent from the tokens-per-day table — that is expected.

## How do I use the published base URL?

The base URL in our list is `{{base_url}}`. The `{ACCOUNT_ID}` portion is a placeholder, not the literal text you should send. Replace it with the Cloudflare account id from your official dashboard. If you leave the braces in place, the request will not reach the API.

Once the URL is complete, the OpenAI SDK pattern is the same as for other compatible official providers. Copy the model id from Cloudflare’s official Workers AI model list.

{{SNIPPETS}}

Some official Cloudflare examples use their own Workers or bindings instead of an external SDK. Those are valid ways to call the same product. This page shows the compatible HTTP interface we recorded, because it is the one you need to point an existing OpenAI client at the published URL.

## What else should I check in the official docs?

Look for the current Neuron allowance, whether it still applies to the models you want, any request-rate limits that are not in our limits field (ours is **{{limits}}**), and how authentication is expressed. Cloudflare APIs often use account-scoped credentials; follow their current quickstart for the compatible endpoint rather than assuming that a generic bearer token setup is complete.

We will not invent extra headers or token-exchange steps that are not in our notes. If the official quickstart requires a different auth header than `Authorization: Bearer`, use the official quickstart.

## Is this an official provider or a gateway?

It is an official provider in our category field, with **{{relay}}** relay warning. You still need to read Cloudflare’s terms for how inputs are handled. Official hosting is a reason to prefer it over an unofficial relay for private text, not a waiver of the provider’s own policy. See [Official providers vs gateways](/guides/official-vs-gateway-providers) and [How to keep API keys safe](/guides/keep-api-keys-safe).

Card required is recorded as **{{card_required}}**. Confirm on the official signup and billing pages, especially if you already have a Cloudflare account with a card on file for other products.

## How might I try it safely?

Create or use a Cloudflare account, copy the account id, create the official API credential the docs require, and put that credential in an environment variable. Substitute the account id into the base URL. Send a one-line prompt with a model id from the official list. Then check the official usage or Neuron display, if one is shown, before connecting an agent that might loop.

If you are choosing among official compatible APIs, compare this Neuron-based allowance with [Groq](/guides/groq-free-api)’s published daily token and request caps and [Gemini](/guides/gemini-api)’s selected-model free tier. They are different shapes of “free,” not three sizes of the same cap.

## How do I report a change?

If Cloudflare’s official pricing page no longer matches the fact box, [send the public URL](/contact). We review the list on weekdays and will not update a Neuron figure from a forum post or from a conversion formula.


## How is this different from other Cloudflare products on a free plan?

Cloudflare offers many products, and a free plan on one product is not automatically a free LLM allowance on Workers AI. Our row is only about the Workers AI allowance we recorded — “{{free_allowance}}” — and the compatible API URL. Do not treat this page as a guide to Workers, Pages, DNS or billing for the rest of the account.

If you already use Cloudflare for hosting, you may still need to enable Workers AI and create the credential the official AI docs describe. Follow those docs rather than reusing an unrelated API token that does not have the right permission. This site cannot see your account and cannot tell you which token permission checkbox to tick if official docs change.

## What should I do after a first successful call?

Check any official usage or Neuron display. If you plan to call the API from a Worker as well as from an external SDK, confirm in the official docs whether those paths share the same daily Neuron allowance. We do not invent a split or a combined cap. Keep the credential in the environment, and do not put `{ACCOUNT_ID}` or the token into a public repository.
