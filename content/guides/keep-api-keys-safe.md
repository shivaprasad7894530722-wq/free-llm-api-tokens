---
slug: keep-api-keys-safe
title: How to keep API keys safe
lede: Treat an API key like a password. Store it in the environment, never in a public repo or chat, and revoke it if it has been exposed.
description: Practical steps to store, use and revoke free LLM API keys, including environment variables, git mistakes, browser leaks and what to do after a key is exposed.
date_published: 2026-11-12
date_modified: 2026-11-12
related: how-to-use-free-openai-compatible-apis, relay-gateway-risks, free-llm-api-for-beginners, rate-limits-explained
howto_steps: Create a dedicated key|Issue a key from the provider dashboard for this project only, not a shared production key.;;Store it in the environment|Export the key in your shell or a gitignored .env file and read it in code from the environment.;;Keep it off the client|Call the provider from a server or function you control, not from browser JavaScript shipped to users.;;Watch for exposure|Search your git history and chat logs before you publish, and enable any provider usage alerts.;;Revoke and replace|If the key may have leaked, revoke it on the provider dashboard and create a new one.
---

## What is the basic rule for LLM API keys?

An API key is a secret that can spend a quota, generate content in your name, or unlock a paid account if a card is later attached. Store it outside your source code, in an environment variable or a secret manager, and give it only to the process that needs to call the API. Never paste it into a public repository, a ticket, a screenshot, a group chat, or an email to this site.

The rest of this page is a practical expansion of that rule for free LLM APIs. It does not replace a provider’s own security docs.

## Where should I store the key on my own computer?

The simplest safe pattern is an environment variable. In a bash or zsh session:

```bash
export API_KEY="the-key-from-the-dashboard"
```

Your Python or Node client then reads `os.environ["API_KEY"]` or `process.env.API_KEY`. See the snippets in [How to use free OpenAI-compatible APIs](/guides/how-to-use-free-openai-compatible-apis).

A `.env` file is fine for local work if it is ignored by git and is not copied into Docker images, CI logs or chat archives. Do not commit `.env.example` files that still contain a real key. On a shared laptop, prefer a per-user environment or a password manager over a file on the desktop.

For team or production use, prefer the secret store your host already offers rather than a plaintext file on a virtual machine.

## Where should a key never go?

Keep keys out of:

- Git commits, including “just this once” commits you plan to rewrite later
- Client-side JavaScript, mobile apps, or shipped desktop binaries
- CI logs, build output, or verbose HTTP debug traces
- Screenshots of a dashboard, especially when you post an error for help
- Prompts themselves (models and relays may log the input)
- This site’s [contact](/contact) email, issue trackers, or public chats
- URL query strings and pasted `curl` commands in documentation you will publish

If you are writing a tutorial, use a placeholder such as `$API_KEY` and state that the reader must create their own key.

## What if I already committed a key to Git?

Revoke the key first on the provider’s dashboard, then remove it from the repository. Rewriting a file in a later commit is not enough if the old commit is still on the remote or in forks. Rotate first, clean second. After rotation, check the provider’s usage screen for unexpected traffic.

The same rule applies to gist, pastebin, and messaging apps. If the key was in a public channel, treat it as compromised even if you deleted the message later.

## Can I use a free-tier key in a browser demo?

You should not embed a secret key in a page that other people can open. Anyone can copy it from the network tab or from the shipped source and exhaust the allowance — or, if a card is later attached, spend money. For a demo, put the key on a small backend, a serverless function, or a local proxy that you run, and rate-limit that backend.

Public demo spaces that ask you to paste a key into the browser are effectively asking you to share it with everyone who can view the page or the network traffic.

## How do keys interact with relays and “bring your own key” gateways?

A key issued **by** a relay only grants access to that relay. The main risk is the prompt and the relay’s own account, as described in [Relay and gateway risks](/guides/relay-gateway-risks).

A **bring-your-own-key** setup is different: you paste an official provider key into another site so it can call the official API as you. That site can then use the key until you revoke it. Only do that when you trust the operator and understand their policy. Prefer official OAuth or scoped keys if the official provider offers them. Never paste a production key into an unofficial dashboard to “unlock free models.”

## What extra habits help on free tiers?

Create a separate key for experiments so a leak does not touch production. Give the key a name in the dashboard that says where it is used. Delete keys you no longer need. If the provider shows usage, glance at it after you try a new tool or agent — coding agents can send many requests in a short time, which is also how people hit [rate limits](/guides/rate-limits-explained) unexpectedly.

Do not reuse the same key across untrusted plugins. A compromised editor extension with your environment variables is enough to empty a quota.

## What should I do if I think a key leaked?

1. Revoke or delete the key in the provider dashboard.
2. Create a new key and update only the places that should have it.
3. Check usage and any billing email for activity you do not recognise.
4. If the key was in git, treat history as tainted and clean it after rotation.
5. If the key was a bring-your-own-key stored at a third party, remove it there too.

Speed matters more than a perfect write-up. A free allowance can still be abused for spam or for work you do not want associated with your account.

## Will this website ever ask for my key?

No. We do not need a key to list public allowances, and [contact](/contact) is email only, without a form. If a page or message that looks like this site asks you to paste a key, it is not part of the published tracker. The canonical host is [freellmapi.link](https://freellmapi.link/).

Keep the same scepticism for lookalike provider dashboards and for search ads that sit above official docs.
