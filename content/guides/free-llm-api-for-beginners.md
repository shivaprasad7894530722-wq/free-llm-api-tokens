---
slug: free-llm-api-for-beginners
title: A free LLM API for beginners, step by step
lede: You do not need to train a model. You create an account, copy a key, point a short script at the published base URL, and send one small request.
description: Beginner walkthrough for using a free LLM API: pick a provider, create a key, set the OpenAI SDK base URL, send a first request, and read common errors.
date_published: 2026-11-12
date_modified: 2026-11-12
related: how-to-use-free-openai-compatible-apis, keep-api-keys-safe, best-free-llm-apis, rate-limits-explained
howto_steps: Pick a provider from the list|Open the tracker, hide relays, and choose an official OpenAI-compatible provider with a published base URL.;;Create an account and key|Sign up on the official site and copy the API key into an environment variable.;;Install the SDK|Install the official OpenAI library for Python or JavaScript.;;Send one test request|Call chat completions with the published base URL and a model id copied from the provider’s docs.;;Read the result or error|If it works, inspect usage; if it fails, fix the key, URL or model id before writing a loop.
---

## What is a free LLM API, in one paragraph?

A free LLM API lets a program send text to a language model over the internet and get text back, using an allowance the provider currently advertises as free. You are not running the model on your laptop unless you choose a local tool. You are calling a remote service with a key. This tracker lists those allowances as they were published, with the snapshot at {{list_updated}}. Figures change, so the official site is the last word.

If you have never used an API before, this page is the slow path. The short path for people who already use the OpenAI SDK is [How to use free OpenAI-compatible APIs](/guides/how-to-use-free-openai-compatible-apis).

## What do I need on my computer?

You need a way to run a short Python or JavaScript program, a text editor, and a web browser to sign up with a provider. You do not need a GPU. You do not need to pay just to follow this page, but some providers in our list do require a card even for a trial. If you want to avoid that for a first test, use the home-page filter **No card needed**, then still confirm on the official signup screen.

You should also be willing to store a secret. An API key works like a password. Read [How to keep API keys safe](/guides/keep-api-keys-safe) before you paste anything into a file.

## How do I pick a first provider?

Open the [provider list](/) and keep these defaults for a first attempt:

1. Hide relays, so you are not sending a test through an unofficial middleman. See [Relay and gateway risks](/guides/relay-gateway-risks).
2. Filter to OpenAI compatible, so the code below applies.
3. Prefer a row marked Official provider, with a published base URL rather than “Not published.”
4. Read the allowance in words. A daily token cap, a monthly call cap and a one-time credit are different.
5. Click through to the official site and read the current free-tier or pricing page.

The [current snapshot](/guides/best-free-llm-apis) groups the same data into tables if you prefer to scan that way. Individual walkthroughs exist for [Groq](/guides/groq-free-api), [Gemini](/guides/gemini-api), [Cloudflare Workers AI](/guides/cloudflare-workers-ai), [Cerebras](/guides/cerebras-api), [SambaNova](/guides/sambanova-cloud) and [Mistral](/guides/mistral-api). Those pages use the same fields as the list and will not invent a quota that the list does not have.

## How do I create a key and keep it local?

On the official site, create an account, find the API key or console page, and create a key. Copy it once into your terminal as an environment variable:

```bash
export API_KEY="paste-your-key-here"
```

Do not put the key in the script you might later upload to GitHub. Do not send it to this site. If you use a `.env` file, add that file name to `.gitignore` first.

If the official site asks for a mobile number or a card, that matches (or may update) the “card required” field in our list. You can stop and pick a different official provider if you do not want to continue.

## How do I send the first request in Python?

Install the official library in a virtual environment if you use one:

```bash
pip install openai
```

Then run a script that sets `base_url` to the **exact** string from the provider card. The value `https://api.example.com/v1` below is a placeholder, not a real host.

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

Copy `MODEL_ID` from the provider’s official model list or dashboard. Do not invent it, and do not assume an OpenAI model name will work. If the base URL in our list contains `{ACCOUNT_ID}`, replace that part with the account id the provider shows you.

## How do I do the same in JavaScript?

```bash
npm install openai
```

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

Run this on your computer or a server. Do not put the secret key into a public web page.

## What should I do if the first request fails?

Read the error text slowly. These are the usual causes:

- **Authentication error:** the environment variable is missing, has a space or quote stuck to it, or the key was revoked.
- **Unknown model:** the model id is for a different provider, or it is not on the free tier.
- **Not found or connection error:** the base URL is mistyped, or an extra `/v1` was added.
- **429 or rate limit:** you have hit a cap, or a previous typo retried too often. Wait and see [Rate limits explained](/guides/rate-limits-explained).
- **Payment required:** the official free allowance does not include this request, or the offer has ended.

If the official docs disagree with our card, follow the official docs and [tell us](/contact) with a link.

## What should I do after a request succeeds?

Check the provider dashboard, if it shows usage. Then decide whether this provider’s published allowance is enough for a small project. Keep using short prompts until you understand how fast the cap moves. If you are writing code with an assistant, see [Free LLM APIs for coding](/guides/free-llm-apis-for-coding), because tools can send many hidden requests.

When you are finished experimenting, delete unused keys. If you pasted a key anywhere public by mistake, revoke it immediately.

## What this first project is not

It is not a way to get an unlimited commercial API. It is not permission to ignore the provider’s terms. It is not a reason to put private customer data into a free tier, especially one that may use prompts to improve a product — our Gemini notes, for example, record that free-tier prompts may be used to improve Google products. Always read the official privacy text for the tier you are on.

Once the first request works, you already know the whole pattern: official account, secret key, published base URL, official model id. Everything else is product detail, which belongs on the provider’s site and, for a snapshot of allowances, on this tracker.
