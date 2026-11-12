---
slug: official-vs-gateway-providers
title: Official LLM API providers vs gateways
lede: Official providers run or sell access under their own name. Gateways sit in front of one or more models. Compatibility and a free cap do not make those the same thing.
description: How this tracker distinguishes official LLM API providers from gateways and relays, and how to choose between them using only published fields.
date_published: 2026-11-12
date_modified: 2026-11-12
related: relay-gateway-risks, best-free-llm-apis, what-is-an-openai-compatible-api, how-to-use-free-openai-compatible-apis
---

## What is the difference between an official provider and a gateway?

An official provider, in this tracker, is a model maker or a cloud that offers the API under its own name and documentation. You create an account with that organisation and, typically, call a base URL on its domain. A gateway sits in front of one or more models — sometimes its own, often someone else’s — and gives you a single key and a single request format. Both can be OpenAI compatible. Both can have a free allowance. They are not the same kind of dependency.

Our data file stores this as `category`: `official` or `gateway`. A separate `relay_risk` flag marks unofficial resellers or unclear operators. Read that flag together with the category; do not treat every gateway as a relay, and do not treat every official row as a permanent free plan.

## Why does the distinction matter if the SDK call looks identical?

Because the request path is only the interface. The operator, the privacy policy, the logging, the uptime and the way a free tier ends all belong to the service behind the base URL. With an official API you can usually find a legal entity, a status page and a written data policy. With a gateway you must also ask where the model runs and who may store the prompt. With an unofficial relay you may not get a clear answer. The SDK will still return a string.

For private source code or personal data, that difference is the decision. The mechanics of setting `base_url` are covered in [How to use free OpenAI-compatible APIs](/guides/how-to-use-free-openai-compatible-apis). The risk details are in [Relay and gateway risks](/guides/relay-gateway-risks).

## How does this tracker classify a site?

We use the public site: who is named as the operator, whether the models are first-party, and whether the product is a router in front of other APIs. Official examples in the current list include Groq, Google’s Gemini API, Cloudflare Workers AI, Mistral, SambaNova and Cerebras. OpenRouter is recorded as a gateway: it is OpenAI compatible, it publishes a free-model request cap until credits are bought, and our notes say free-model providers may log prompts. That is a documented trade-off, not a hidden one.

If we cannot describe the operator as official, we use `gateway`. If the public information looks like an unofficial reseller or an unknown middleman, we also set the relay warning. Classifications can lag a rebrand; [contact](/contact) us with an official page if a row is wrong. The snapshot used on this page is {{list_updated}}.

## What trade-offs show up in the published fields?

Official providers often publish more durable documentation and, sometimes, tighter or more specific free caps. They may require a card for a trial, or they may state that free-tier prompts are used to improve the product. They may also end a free credit, as our list records for some official rows, including ended monthly credits on Hugging Face Inference Providers.

Gateways often advertise a long model list and a single compatible endpoint. That is convenient for comparison. The cost is an extra hop and, often, less clarity about training and retention — especially on “:free” routes. Some gateways in our tokens-per-day table also carry a relay warning and should not be used for private data, however large the published cap looks.

Card requirements, request caps and one-time credits appear in both categories. A card-backed official trial can be more constrained than a no-card official free tier with a smaller published number. Compare the sentence in the allowance field, not only the category badge. The [current snapshot tables](/guides/best-free-llm-apis) are generated from the same file so you can see those fields side by side.

## When is an official provider the better default?

Choose official first when:

- You are learning and want stable docs and a clear account to log into
- The prompt might include private code, internal text, or personal data
- You need to cite a vendor name in a school or work setting
- You want to avoid an extra unknown operator between you and the model

You still have to read that official provider’s free-tier policy. “Official” is not a synonym for “will not train on my prompts” or “will stay free.”

## When can a documented gateway be a reasonable choice?

A documented gateway can be reasonable when you are sending throwaway prompts, when you want to try several model names through one client, or when the official host you want is only reachable through that router and you accept both privacy policies. Keep a dedicated key. Do not use a bring-your-own official key unless you trust the gateway operator.

If the gateway is flagged as a relay, treat it as a public channel. A first “hello world” request is enough to test compatibility; it is not a reason to point your main repository at that base URL.

## How should I migrate from a gateway to an official API later?

If both are OpenAI compatible, keep the application code and change the environment: key, base URL, and model id. That is the practical benefit of compatibility, explained in [What is an OpenAI-compatible API?](/guides/what-is-an-openai-compatible-api). Test features you depend on — streaming, tools, JSON output — because they may differ even when a basic chat call works.

Do not assume the old model id exists on the new host. Do not assume the old daily cap applies. Update any allow-lists, logging and cost alerts to the new official account.

## How should I read our badges together?

Use them as a set:

- **Official provider** or the absence of that badge (gateway)
- **Relay warning** or its absence
- **OpenAI compatible** (yes, partial, no, or not published)
- The written free allowance, tokens per day if published, limits, and card required

No single badge is a recommendation. The site is not affiliated with the providers it lists, and it does not rank quality or speed. It records what was published, and it flags where an extra operator sits on the path. For a beginner path that starts on official compatible APIs, use [A free LLM API for beginners](/guides/free-llm-api-for-beginners).
