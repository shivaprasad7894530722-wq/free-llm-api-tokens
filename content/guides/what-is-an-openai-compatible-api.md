---
slug: what-is-an-openai-compatible-api
title: What is an OpenAI-compatible API?
lede: It is an HTTP API that speaks the same request shape as OpenAI’s, so you can usually keep your SDK and only change the base URL, the key and the model id.
description: Plain-language explanation of OpenAI-compatible APIs, what Yes, Partial and Not published mean on this tracker, and how base URLs and model ids work.
date_published: 2026-11-12
date_modified: 2026-11-12
related: how-to-use-free-openai-compatible-apis, best-free-llm-apis, official-vs-gateway-providers, rate-limits-explained
---

## What is an OpenAI-compatible API?

An OpenAI-compatible API is a server that accepts the same general request format as OpenAI’s HTTP API, especially the chat completions style: a JSON body with a model id and a list of messages, plus a bearer token. You can often use the official OpenAI SDK, or another client written for that protocol, by pointing it at a different base URL and using that provider’s key. Compatibility is about the interface, not about who trained the model.

It does not mean the provider is OpenAI, or that every OpenAI product feature is available. It also does not mean the free allowance, if any, will match OpenAI’s own plans.

## Why do so many free LLM APIs advertise this?

Most example code, agents, IDE plugins and tutorials already know how to call OpenAI’s API. If a new host implements the same path and field names, that ecosystem can switch with a configuration change. Providers get more users; developers avoid rewriting clients. That is why our tracker treats compatibility as a first-class field, next to the published [base URL](/).

The snapshot at {{list_updated}} is the source for how many listed providers currently say they are compatible. We do not infer compatibility from a blog post that only shows a screenshot of a chat box.

## What do “Yes”, “Partial” and “Not published” mean on this site?

**Yes** means the provider’s public docs describe an OpenAI-compatible endpoint, and we have recorded the base URL when it was published. **Partial** means the docs or our notes say that only some models, regions or features work that way — for example a chat endpoint without the rest of the API, or a compatibility layer with gaps. **No** means they document a different API. **Not published** means we have not seen a clear public statement, so we leave the field empty rather than guessing.

These labels are not certifications. A provider can change a path or add required headers after we last checked. If a documented “Yes” fails in your project, trust the live response and the official docs, then [send us the public page](/contact) if our row is stale.

## What is a base URL?

The base URL is the root the SDK prefixes to paths such as `/chat/completions`. Providers publish different shapes: some use `https://api.example.com/v1`, some use a path that already includes `/openai/v1`, and some official clouds include an account id in the path. Copy the string as published. Do not “normalise” it by stripping or adding `/v1` unless the official docs tell you to.

When our list says the base URL is Not published, this site will not invent one. The [how-to guide](/guides/how-to-use-free-openai-compatible-apis) shows the SDK fields you fill once you have the official string.

A base URL is also not a promise about privacy. The host behind that URL may be an official cloud or an unofficial relay. Check the relay flag and the [risks guide](/guides/relay-gateway-risks).

## Do I have to use the official OpenAI SDK?

No. Any HTTP client can POST JSON to a compatible server. The official SDK is convenient because `base_url` / `baseURL` is a single option and because it already handles request encoding. Other official or community SDKs that speak the same protocol can work too. If you use a third-party wrapper, confirm it lets you override the base URL and that it will not send your key to a different host than the one you set.

Some providers also offer their own SDKs. Those may expose features that the compatible layer does not. For a first test, the official OpenAI client plus a published base URL is usually enough.

## Are the model ids the same as OpenAI’s?

Usually not. A compatible API still expects a model id that exists **on that server**. Reusing `gpt-…` names from OpenAI’s catalogue will often return an error, or occasionally map to a different model if a gateway has defined an alias — which you should not assume. Copy the id from the provider’s model list or dashboard.

This tracker does not maintain a full model catalogue, because those lists change faster than daily allowances. When a provider note in our data mentions specific models, a [provider guide](/guides/) may repeat that note, and still tell you to re-check.

## What about authentication and extra headers?

Most compatible endpoints use `Authorization: Bearer <key>`, the same pattern as OpenAI. Some clouds also require an account id in the URL, a version header, or a provider-specific header. We only document headers when they appear in our public notes; we do not invent required headers. If a request fails with 401 or 403, read the official quickstart for that provider before changing keys again.

Never put the key in the base URL query string or in client-side frontend code. See [How to keep API keys safe](/guides/keep-api-keys-safe).

## Which features often differ even when chat completions work?

Compatibility is usually tested against a basic chat request. These areas are where “compatible” APIs often diverge, and where you should read official docs instead of assuming parity:

- Streaming (`stream: true`) and the exact event format
- Tool or function calling, including parallel tools
- JSON mode or structured output
- Vision, audio, or file inputs
- Embeddings, images, or moderation endpoints
- Batch jobs and cached tokens
- Organisation, project, or usage-header semantics

If your app depends on one of those features, try it on the free tier with a throwaway prompt before you migrate a full workflow.

## Is a compatible gateway the same as an official API?

No. A gateway can be OpenAI compatible and still proxy your request to someone else’s model. Official providers can also be compatible. Compatibility tells you how to form the request; it does not tell you who can read the prompt. Our category and relay-risk fields exist for that reason. The comparison is expanded in [Official providers vs gateways](/guides/official-vs-gateway-providers).

## How should I read compatibility when I compare free tiers?

Treat it as a filter, not a score. A non-compatible official API can still be a good free tier if you are willing to use its native SDK. A compatible relay with a large published cap can still be a poor place for private code. Combine the compatibility field with the official/gateway category, the card requirement, the written allowance, and the official rate-limit page.

The [current snapshot](/guides/best-free-llm-apis) lists OpenAI-compatible offers alongside those other fields. For request and token caps, see [Rate limits explained](/guides/rate-limits-explained).
