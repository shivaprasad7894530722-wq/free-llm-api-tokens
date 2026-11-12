---
slug: gemini-api
title: Gemini API free tier — compatibility, base URL and notes
lede: Google’s Gemini API is listed as an official, OpenAI-compatible service with a free tier on selected models. This page only repeats what our tracker and the official docs publish.
description: Gemini API (Google AI Studio) free-tier snapshot from this tracker, including the OpenAI-compatible base URL, card requirement, and the note that free-tier prompts may be used to improve Google products.
date_published: 2026-11-12
date_modified: 2026-11-12
provider_id: gemini
related: how-to-use-free-openai-compatible-apis, groq-free-api, keep-api-keys-safe, official-vs-gateway-providers
---

## What is the Gemini API on this tracker?

The row is named **{{name}}** and is listed as an **{{category}}**. OpenAI compatibility is **{{openai_compatible}}**. The recorded free allowance is “{{free_allowance}}”. Tokens per day are **{{tokens_per_day}}** — Google does not give us a single daily token number to store, so we do not invent one. Limits are recorded as “{{limits}}”. A card is recorded as **{{card_required}}**. Relay warning: **{{relay}}**.

Our notes say: {{notes}} That is a policy point, not a performance claim, and you should read the official terms for the current wording. The official URL we store is [{{url}}]({{url}}). Entry last updated {{entry_updated}}; list snapshot {{list_updated}}.

{{FACTBOX}}

## How do I call Gemini with an OpenAI-compatible client?

Our list records this base URL: `{{base_url}}`. Copy it exactly, including the path suffix. Create a key in Google AI Studio (or the official console the docs currently describe), store it in an environment variable, and pass it to the official OpenAI SDK. Copy the model id from Google’s official Gemini documentation. We will not invent a model name here.

{{SNIPPETS}}

If the official docs also describe a native Gemini SDK or a different endpoint, that does not contradict compatibility. It is another supported interface. This page focuses on the compatible base URL we recorded, because that is what most people need to switch an existing OpenAI client.

## Why are tokens per day “Not published”?

Because the public sources we used did not give a single tokens-per-day number for the free tier as a whole. The limits field points you to Google’s rate-limit page, where caps may be expressed per model as RPM or RPD. We leave the numeric tokens-per-day field empty rather than averaging or guessing. See [Rate limits explained](/guides/rate-limits-explained) for how to read those units, and always open the official rate-limit page on the day you use the API.

“Selected models” in the allowance means the free tier does not automatically include every Gemini model. Which models are selected can change. Official docs are the source for the current set.

## What does the free-tier prompt note mean in practice?

Our notes record that free-tier prompts may be used to improve Google products. If that does not fit your data — private source code, customer text, or anything you cannot send to a product-improvement pipeline — do not put that data in the free tier. Check whether a paid official tier has a different policy, or use a different official provider, or run a model locally. This site cannot change Google’s policy and will not hide the note.

The same caution applies to any official free tier with a similar disclosure. “Official” is about who operates the API, not about training or retention. See [Official providers vs gateways](/guides/official-vs-gateway-providers).

## Is a credit card required?

In our data, card required is **{{card_required}}**. Confirm during signup, because official flows change. If you are choosing a first API and want to avoid a card, use the tracker filter and then read the official page, as described in [A free LLM API for beginners](/guides/free-llm-api-for-beginners).

## How should I handle keys for Gemini?

Treat the key as a secret, like any other provider key. Keep it out of git, browser demos and chat logs. If you use the OpenAI-compatible URL in a coding assistant, issue a dedicated key so you can revoke it without affecting other projects. See [How to keep API keys safe](/guides/keep-api-keys-safe).

Do not send your Gemini key to a third-party “relay” so it can call Google on your behalf unless you fully trust that operator. A leaked official key is more serious than a key that only exists on a throwaway gateway account.

## How does this compare with other official rows?

Gemini is useful to compare with [Groq](/guides/groq-free-api) and [Cloudflare Workers AI](/guides/cloudflare-workers-ai) because all three are official and recorded as OpenAI compatible, and all three currently list no card in our file, but they publish different kinds of allowance: a daily token and request cap (Groq), a Neuron cap (Cloudflare), and a selected-model free tier with per-model official rate limits (Gemini). None of those units should be converted into each other on this site.

For a table of all official rows, use [Best free LLM APIs (current)](/guides/best-free-llm-apis). That page is regenerated from the same data file.

## How do I verify or correct this entry?

Compare the official pricing and rate-limit pages with the fact box above. If a figure has changed, trust Google’s page and [email a public link](/contact). This row was first listed on {{first_reported}} and last changed on {{entry_updated}}. We do not update a quota from an unofficial screenshot.
