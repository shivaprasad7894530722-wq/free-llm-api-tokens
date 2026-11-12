---
slug: relay-gateway-risks
title: Relay and gateway risks for free LLM APIs
lede: A relay can look like an official API while forwarding your prompt to another service. Treat flagged sites as public, and prefer official providers for anything private.
description: How unofficial LLM API relays and gateways work, what this tracker’s relay warning means, and how to reduce the risk of leaked prompts and keys.
date_published: 2026-11-12
date_modified: 2026-11-12
related: keep-api-keys-safe, official-vs-gateway-providers, how-to-use-free-openai-compatible-apis, best-free-llm-apis
---

## What is a relay or unofficial gateway?

A relay is a site that gives you an API key and a base URL, then forwards your prompts to other model providers rather than running the models itself as the named official host. Some relays are clear about that. Others present a long model list and a generous free allowance without saying where the request actually goes. On this tracker, entries that we treat as unofficial resellers or unknown operators carry a **Relay warning**.

A “gateway” in our category field is broader. It includes documented routers and official multi-model gateways as well as unofficial relays. The warning flag, not the word “gateway” alone, is the signal to be careful with private data.

## Why can a relay be a problem?

The practical risks are about data and control, not about whether a sample “hello” request works.

Your prompt, system instructions and any files you attach may be visible to the relay operator, and may be logged or reused. The operator may also send that text to a third-party model host with its own logging policy. If you pasted customer data, private source code, or an API key inside the prompt, you have now shared it with at least one extra party.

You also have less control over the route. A model name can be mapped to a different model than the one you expected. A free cap can disappear. A site can start charging, change its domain, or shut down. Billing disputes and abuse reports are harder when the operator is unclear.

A relay can also collect **your** API keys if you are tricked into pasting a key from another provider into their dashboard. This tracker will never ask you for a key. If a site does, stop and read [How to keep API keys safe](/guides/keep-api-keys-safe).

## What does the relay warning on this site mean?

It means that, from public information, we treat the operator as an unofficial reseller, an unknown middleman, or a service whose routing we cannot describe as official. It is a caution, not a legal finding and not a claim that every flagged site is malicious. Absence of a warning is also not a certification. New sites appear often; the list was last snapshotted at {{list_updated}}.

Use the home-page filter **Hide relays** when you want the list without those rows. The [current snapshot](/guides/best-free-llm-apis) also shows a relay column on several tables so a large published token cap is not mistaken for a safe default.

## How do official providers, documented gateways and relays differ?

An **official provider** in our data is a model maker or cloud selling or giving access under its own name — for example a first-party API with docs on that company’s domain. You still need to read their privacy and training policy. Some official free tiers state that prompts may be used to improve the product.

A **documented gateway** routes to many models and says so. It may be useful as a single base URL. It may still log prompts, and the underlying model host may log them too. A well-known example in our list is OpenRouter, which we record as a gateway (not official), OpenAI compatible, with `:free` models and a published daily request cap until credits are bought, plus a note that free-model providers may log prompts. That note is a reason to keep private data out of `:free` routes, even without a relay flag.

An **unofficial relay** often has the weakest public documentation, the most aggressive advertised caps, and the least clarity about logging. Those are the rows we try to flag.

The comparison is spelled out further in [Official providers vs gateways](/guides/official-vs-gateway-providers).

## What should I never send through a flagged relay?

Do not send anything you would not be willing to post in a public forum. In particular:

- API keys, passwords, cookies, or private tokens (including keys for other providers)
- Customer records, health, financial or government identifiers
- Confidential source code, unreleased product plans, or internal documents
- Personal data about other people
- Content that the upstream provider would forbid, such as abuse of their models

If your workflow needs those inputs, use an official provider whose policy you accept, a contract that matches your requirements, or a model you run locally.

## How can I reduce risk if I still want to try a gateway?

Use a throwaway prompt and a key that exists only on that site. Do not reuse a production key. Do not point a production app at a new base URL until you have read the terms and privacy policy.

Check who is named as the operator, whether a company or legal entity is published, and whether the docs describe routing and logging. Prefer HTTPS base URLs from our list or from official docs — we do not invent endpoints. Watch for typo-squatting domains.

If the service asks you to paste an OpenAI, Google or other first-party key so they can “bring your own key,” understand that you are trusting them with a credential that can spend money or read projects on the first-party account. That is a different, higher risk than using a key they issued for their own endpoint.

Revoke the key when you are done experimenting.

## Can a generous tokens-per-day figure offset the risk?

No. A large published cap is a usage number, not a security control. Some of the highest daily figures in our snapshot belong to relay-flagged gateways. That is why the tokens-per-day table on the [best free LLM APIs](/guides/best-free-llm-apis) page includes a relay column, and why this guide exists beside it.

Cost can also appear later: a card on file, a quiet change from free to paid, or a key that is reused on a paid upstream. We only record card requirements that are published. If the field is Not published, we do not treat that as “no card.”

## How should teams use this warning?

Put the relay flag into your own checklist. If you maintain a shared allow-list of base URLs, do not add a flagged host for data that is not public. If you publish a tutorial, do not tell readers to paste secrets into a relay “just to try it.” If you correct our flag, send a [public official source](/contact) that shows who operates the service and how routing works.

## What this site will not do

We will not hide a relay warning to make a page look more inviting. We will not invent a logging policy for a site that does not publish one. We will not promise that official providers never train on free-tier prompts — some disclose that they may. The safe default is the same in every case: treat undocumented routes as public, keep keys in environment variables, and confirm terms on the official page before you rely on a free tier.
