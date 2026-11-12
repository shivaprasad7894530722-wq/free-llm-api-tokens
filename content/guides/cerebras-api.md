---
slug: cerebras-api
title: Cerebras API trial allowance and compatible base URL
lede: Cerebras is an official, OpenAI-compatible API in our list. The recorded free allowance is a high daily token cap during a short, card-required trial — not an ongoing no-card tier.
description: Cerebras free-trial API snapshot from this tracker: 1,000,000 tokens/day during a $5 30-day trial, card required, OpenAI-compatible base URL, and how to call it in Python or JavaScript.
date_published: 2026-11-12
date_modified: 2026-11-12
provider_id: cerebras
related: how-to-use-free-openai-compatible-apis, sambanova-cloud, rate-limits-explained, best-free-llm-apis
---

## What is Cerebras on this tracker?

{{name}} is listed as an **{{category}}** with OpenAI compatibility **{{openai_compatible}}**. The recorded free allowance is “{{free_allowance}}”. Tokens per day are **{{tokens_per_day}}**. Limits are **{{limits}}**. Card required is **{{card_required}}**. Relay warning: **{{relay}}**. Our notes say: {{notes}}

Read that allowance as a **trial**, not as a standing free plan. The official URL we store is [{{url}}]({{url}}). Entry dates: first listed {{first_reported}}, last updated {{entry_updated}}. List snapshot: {{list_updated}}.

{{FACTBOX}}

## How should I read a trial cap that looks large?

A daily token number of {{tokens_per_day}} can look high next to ongoing free tiers in the [current snapshot](/guides/best-free-llm-apis). The same row also says the figure applies during a $5 30-day trial and that a card is required. If you sort only by tokens per day, you miss the time limit and the card. This is why our tables keep the written allowance and the card column, and why this guide exists beside the table.

When the trial window in the official terms ends, do not assume the same daily cap continues. We will mark the row when we see a public change; until then, the official plans page is the authority.

Limits in our file are **{{limits}}**. That means we did not record a separate public RPM or RPD figure, not that requests are unlimited. See [Rate limits explained](/guides/rate-limits-explained).

## How do I call the published endpoint?

The base URL we record is `{{base_url}}`. Use the official OpenAI SDK, a key from the Cerebras account you create, and a model id from Cerebras’s official docs. Do not invent a model name here.

{{SNIPPETS}}

If official docs require extra signup steps — a card, a trial opt-in, or a console flag — complete those first. A valid-looking key can still be rejected if the trial is not active.

## Why is a card required, and what should I watch for?

Our data records card required as **{{card_required}}**, and the notes repeat that the trial is 30 days with a card. A card on file can make it easier to continue onto a paid plan when a trial ends. Watch official emails and the billing dashboard so you are not surprised by a charge after the window described in the official terms. This site is not affiliated with Cerebras and cannot cancel a trial for you.

If you want an official compatible API whose card field is currently “No” in our list, compare rows in the snapshot tables rather than assuming every official provider has the same payment rule.

## Is Cerebras a relay?

No. It is classified as official, with **{{relay}}** relay warning. You still need to read Cerebras’s terms for data use. Prefer official providers over flagged relays for private prompts, as explained in [Relay and gateway risks](/guides/relay-gateway-risks). Keep the trial key in the environment and revoke it if it leaks; see [How to keep API keys safe](/guides/keep-api-keys-safe).

## How might I use the trial carefully?

Decide in advance whether a 30-day official trial fits the work. Put a reminder on the end date that the official terms describe. Use a dedicated key. Start with a small request, then — if you connect a [coding assistant](/guides/free-llm-apis-for-coding) — set a local request cap so the daily token figure is not spent in an unattended loop.

If you later move to another official compatible API, change the environment’s key, base URL and model id. Application code can stay the same if you only used features that both APIs support.

## How do I verify this row?

Compare the fact box with Cerebras’s official plans and docs. If the trial wording, the daily token figure, the card rule or the base URL has changed, [send the official link](/contact). We will not keep a high tokens-per-day figure in the “best of” table as if it were an unlimited ongoing plan.


## What should I log during the trial, and what should I never log?

Log the model id, the HTTP status and a timestamp so you can see how fast you are approaching the published daily token figure. Do not log the API key, the full request payload if it contains secrets, or card details. If you take screenshots for a teammate, crop the key.

If several people share the trial, they are also sharing the published cap. Agree who may run an agent overnight. A single unattended loop is enough to spend a daily token allowance that looked large in a table.

## What happens in my own planning when the 30 days end?

Read the official terms for what the account becomes after the trial: paid, disabled, or a smaller plan. This site will not invent that outcome. Set a reminder from the official start date, keep a second official provider ready if you still need a free compatible endpoint, and revoke keys you no longer use. Compare ongoing official options in the [current snapshot](/guides/best-free-llm-apis) instead of assuming a trial cap will be extended informally.
