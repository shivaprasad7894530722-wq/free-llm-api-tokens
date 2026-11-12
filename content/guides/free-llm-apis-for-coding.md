---
slug: free-llm-apis-for-coding
title: Free LLM APIs for coding
lede: Coding assistants send many short requests, so a published daily cap can disappear quickly. Use an official compatible endpoint, a dedicated key, and a model id from the provider’s docs.
description: How to use free OpenAI-compatible LLM APIs with coding assistants and scripts, including rate-limit caution, key safety and official versus relay providers.
date_published: 2026-11-12
date_modified: 2026-11-12
related: how-to-use-free-openai-compatible-apis, rate-limits-explained, keep-api-keys-safe, relay-gateway-risks
---

## Can I use a free LLM API for coding work?

Yes, many people point an editor plugin, a CLI coding agent, or a small script at an OpenAI-compatible base URL and a free-tier key. The setup is the same pattern described in [How to use free OpenAI-compatible APIs](/guides/how-to-use-free-openai-compatible-apis): published base URL, provider key in the environment, model id copied from official docs. What changes is the volume. A chat playground sends one request when you press enter. A coding assistant may send many requests for a single edit, plus retries, plus context from your files.

That volume is why published [rate limits](/guides/rate-limits-explained) matter more for coding than for a one-line test, and why you should think carefully about [relays](/guides/relay-gateway-risks) before you index a private repository through a third-party host.

## What should I configure in a coding assistant?

Most OpenAI-compatible tools ask for three values:

- An API key, which should come from the environment or the tool’s secret store, not from a file inside the repo
- A base URL, copied from the provider’s docs or from the card on our [list](/)
- A model id, copied from the same provider, not from another catalogue

If the tool has a “provider” dropdown, only use a preset if it matches the official host you intend. A preset that points at an unknown relay is still a relay. If the tool lets you set a maximum number of requests or a monthly budget, set one before the first large run.

Do not commit the tool’s local config if it contains the key. Add those files to `.gitignore`.

## Why do free tiers run out faster during coding?

Coding prompts include source files, diffs and logs. Token counts grow with context, not just with the size of the visible answer. Agents may re-read a file, call tools, and retry on a failed patch. If the provider counts input and output tokens toward a daily cap, a long debugging session can exhaust it even when the published number looked large in a table.

If tokens per day are **Not published** in our list, you still have a cap; you just cannot plan from a number we recorded. Watch the official dashboard and stop on the first 429 response. Tight auto-retries will make the situation worse.

## Should I use an official provider or a gateway for code?

If the repository is private, prefer an official provider whose privacy terms you accept, or a model you run locally. Some official free tiers disclose that prompts may be used to improve the product. Our Gemini entry records that kind of note. Read the official policy for the specific tier, not only the marketing page.

Documented gateways can be convenient when you want to switch models through one base URL. They may also log prompts, and the model host behind a free route may log them too. Unofficial relays are a poor default for source code. Our **Hide relays** filter exists for this case.

The [current snapshot](/guides/best-free-llm-apis) will show large daily caps on some gateways. A large cap does not make a relay safer for a private codebase.

## How do I keep a coding key from leaking?

Issue a key that is only used by the assistant, so you can revoke it without rotating everything else. Keep it out of shell history if you can, out of screenshots of errors, and out of issue trackers when a command fails. Do not paste source that contains `.env` files into a prompt on a relay.

If the assistant can run terminal commands, it may accidentally `echo` the environment or print a debug HTTP dump. Treat that as a leak and revoke the key if a log might have been shared. The full checklist is in [How to keep API keys safe](/guides/keep-api-keys-safe).

## What code pattern works for small scripts?

For your own scripts, construct the client once and keep the model id in a variable or environment value such as `MODEL_ID`. That way you can switch providers without rewriting the rest of the program.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["API_BASE_URL"],
)

def complete(prompt: str) -> str:
    resp = client.chat.completions.create(
        model=os.environ["MODEL_ID"],
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content or ""
```

Set `API_BASE_URL` to the published base URL, including any `/v1` suffix the provider documents. Do not hard-code a host you saw in an unofficial list if our entry says Not published — look it up on the official site instead.

Add a clear failure path for 429 and 401. A script that ignores those errors can sit in a retry loop until the day cap is gone.

## Are there limits besides tokens?

Yes. Requests per minute, requests per day, concurrent connections, and maximum context size are all separate from a daily token figure. Some official pages publish per-model RPM and RPD; our list only repeats that when the public source said so, and otherwise leaves limits as Not published. A coding agent that fires parallel calls is often the first way people discover an unpublished RPM cap.

Phone checks, cards and trial end dates also matter. A trial with a high daily cap and a card on file is not the same as an ongoing no-card free tier. Those details are in each row’s allowance and notes, and in the provider guides.

## How should I evaluate whether a free API is “good for coding”?

This site does not invent quality scores, context-window sizes or latency figures. If you need those, measure them on a public sample, or read the official model card. What you can decide from our data is narrower and safer: whether a compatible base URL is published, whether the allowance is a trial or an ongoing tier, whether a card is required in the public terms, and whether we have flagged a relay.

Start with one official provider, one short file, and a request cap in the tool. If that loop is stable, then consider more context or a second model id. If the official terms do not fit a private repository, do not try to solve that with an unofficial free relay.

Provider-specific snapshots for widely used official APIs are linked from the [guides index](/guides/). The underlying figures follow the tracker snapshot at {{list_updated}}.
