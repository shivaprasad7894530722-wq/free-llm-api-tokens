---
slug: how-to-use-free-openai-compatible-apis
title: How to use free OpenAI-compatible APIs
lede: Point the official OpenAI SDK at a provider’s published base URL, use that provider’s key, and copy the model id from their docs — not from a guess.
description: Step-by-step guide to using free OpenAI-compatible LLM APIs in Python and JavaScript, including base URL setup, keys, and what this tracker will not invent.
date_published: 2026-11-12
date_modified: 2026-11-12
schema: Article
related: what-is-an-openai-compatible-api, free-llm-api-for-beginners, keep-api-keys-safe, best-free-llm-apis
howto_steps: Create a provider account|Open an official provider from the tracker and create a free account on their site.;;Get an API key|Copy the key from the provider’s dashboard and store it in an environment variable, never in a public repo.;;Set the base URL|Create an OpenAI client with the provider’s published base URL and your key.;;Copy a model id|Take the model id from that provider’s official docs or dashboard. Do not invent one.;;Make a test request|Send a small chat completion, then confirm the response and your remaining quota on the provider’s site.
---

## What is the shortest way to use a free OpenAI-compatible API?

Create an account on a provider that this tracker marks as OpenAI compatible, copy an API key into an environment variable, and construct the official OpenAI client with that provider’s published base URL. Then copy a model id from the same provider’s documentation and send a small chat request. Confirm the live quota on their site, because published allowances change.

This page walks through that path in Python and JavaScript. It does not invent endpoints, model names or daily limits. When a figure is missing from our [provider list](/), we say so.

## What does “OpenAI compatible” mean in practice?

An OpenAI-compatible API accepts the same style of HTTP requests as OpenAI’s API — typically a `chat.completions` call with a model id and a list of messages. The official Python and JavaScript SDKs can talk to those servers if you change two things: the **base URL** and the **API key**.

“Compatible” is not a promise that every OpenAI feature exists. Streaming, tool use, vision, batch jobs or embeddings may be missing or named differently. In our list, **Yes** means the provider documents a compatible endpoint, **Partial** means only some of that surface works that way, and **Not published** means we have not seen a clear public statement. Read the longer explainer in [What is an OpenAI-compatible API?](/guides/what-is-an-openai-compatible-api).

## Which provider should I start with?

Prefer an entry marked **Official provider** if you are still learning, or if your prompts might include anything you would not post in public. Official providers run their own models or clouds. Many other rows are gateways: some are well documented, some are unofficial relays. A **Relay warning** on a card means you should not send private data through that site. See [Relay and gateway risks](/guides/relay-gateway-risks).

Use the home-page filters for “OpenAI compatible” and “No card needed”, then open the provider’s own pricing or rate-limit page from the card. If tokens per day are marked **Not published**, do not assume a number. The [current snapshot of published allowances](/guides/best-free-llm-apis) is generated from the same data file as the list.

## How do I keep the API key out of my code?

Store the key in an environment variable and read it at runtime. Do not paste it into a chat, a screenshot, a ticket, or a Git repository. If a key leaks, revoke it on the provider’s dashboard and create a new one. The full checklist is in [How to keep API keys safe](/guides/keep-api-keys-safe).

```bash
# In your shell, for the current session only
export API_KEY="paste-the-provider-key-here"
```

On Windows PowerShell the equivalent is `$env:API_KEY = "paste-the-provider-key-here"`. Use a `.env` file only if that file is listed in `.gitignore`.

## How do I call a compatible API from Python?

Install the official `openai` package, then pass `base_url` and `api_key`. Replace the base URL with the exact string from the provider card (or from their docs if our list says Not published). Replace `MODEL_ID` with a model id copied from that provider — not from this sentence.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url="https://api.example.com/v1",
)

resp = client.chat.completions.create(
    model="MODEL_ID",
    messages=[{"role": "user", "content": "Reply with the word ok."}],
)
print(resp.choices[0].message.content)
```

Some base URLs already end in `/v1` or `/openai/v1`. Copy them as published. Do not add a second `/v1` unless the official docs say to. A few official endpoints include a placeholder such as `{ACCOUNT_ID}`; those are not literal hostnames, and you must substitute the id the provider gives you.

## How do I call a compatible API from JavaScript?

The pattern is the same with the official `openai` Node SDK. In browsers you should not embed a secret key at all; call the provider from a server or a function you control.

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.API_KEY,
  baseURL: "https://api.example.com/v1",
});

const resp = await client.chat.completions.create({
  model: "MODEL_ID",
  messages: [{ role: "user", content: "Reply with the word ok." }],
});
console.log(resp.choices[0].message.content);
```

If you already have code written for OpenAI, this is often the only change you need, besides picking a model id that exists on the new provider.

## What does a raw HTTP request look like?

SDKs are optional. A compatible server usually accepts a JSON POST to `{base URL}/chat/completions` with a bearer token. If the published base URL already includes a version suffix, you still append `/chat/completions` unless the official docs say otherwise.

```bash
curl https://api.example.com/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Reply with the word ok."}]}'
```

If this returns an authentication error, the key or the header name may be wrong. If it returns a model error, the model id is usually wrong or not available on the free tier. If it returns a rate-limit error, you have hit a published or unpublished cap — see [Rate limits explained](/guides/rate-limits-explained).

## Why will this site not fill in a model id for you?

Model catalogues change. A name that worked last month may be paid-only, renamed, or removed from a free tier. Our [data.json](/data.json) file records allowances, compatibility and base URLs; it does not try to be a live model directory. Official docs and the provider dashboard are the right source for the string you put in the `model` field.

When an individual [provider guide](/guides/) mentions models, it only repeats what is already in that provider’s tracker notes or official documentation, and it still tells you to re-check.

## How should I test without burning the whole allowance?

Start with a one-line prompt and a low `max_tokens` value if the API supports it. Read the response headers or dashboard, if any, before you run a loop. Free tiers often count both input and output tokens, and a retry loop can exhaust a daily cap in minutes.

If you are comparing providers, use the same short prompt and log which base URL, model id and error you received. Do not use a relay for that experiment if the prompt includes source code or data you would not share.

## What are the usual ways this setup fails?

The common failures are practical, not mysterious:

- The base URL is mistyped, or a second `/v1` was added on top of a URL that already ends in `/v1`.
- The environment variable is unset, so the SDK sends an empty key.
- The model id was copied from a different provider.
- The free allowance does not include that model, or the offer has ended since our last snapshot.
- A card, phone check or extra header is required, and our card field still says you should confirm on the official site.
- You are calling a browser bundle with a secret key, or a proxy is stripping the `Authorization` header.

When an offer has ended we keep the row and hide it behind “Show ended offers” on the home page. Hugging Face’s free monthly inference credits, for example, are recorded as ended in the list rather than silently removed.

## How do I go from a test request to a small app?

Keep the client construction in one module so the base URL is not copied through your codebase. Load the key from the environment. Log the provider name and model id, not the key. Add basic backoff when you see HTTP 429. If you outgrow a free tier, switch the base URL and key rather than rewriting the rest of the app — that is the point of compatibility.

For IDE and coding-agent workflows, see [Free LLM APIs for coding](/guides/free-llm-apis-for-coding). For a slower walkthrough that starts from zero, see [A free LLM API for beginners](/guides/free-llm-api-for-beginners).

## How current is this advice?

The steps on this page — key in the environment, official SDK, published base URL, model id from official docs — do not depend on a particular quota. The list of who offers what was last snapshotted at {{list_updated}}. Always open the provider’s own page before you plan work around a daily cap.
