---
slug: groq-free-api
title: Groq free API — allowance, base URL and limits
lede: Groq is an official, OpenAI-compatible provider. This page repeats the figures in our tracker and shows how to set the published base URL in the official SDK.
description: Groq free LLM API snapshot from this tracker: published daily token allowance, request limits, OpenAI-compatible base URL, and how to call it in Python or JavaScript.
date_published: 2026-11-12
date_modified: 2026-11-12
provider_id: groq
related: how-to-use-free-openai-compatible-apis, gemini-api, cerebras-api, rate-limits-explained
---

## What is Groq on this tracker?

Groq is listed as an **{{category}}** with OpenAI compatibility recorded as **{{openai_compatible}}**. In our file the published free allowance is “{{free_allowance}}”, tokens per day are **{{tokens_per_day}}**, and the recorded limits are “{{limits}}”. The notes say that limits vary by model. A card is recorded as **{{card_required}}**. There is **{{relay}}** relay warning on this row. These fields were last updated in the entry on {{entry_updated}}, and the overall list snapshot is {{list_updated}}.

This page does not add unpublished quotas, model names or hidden endpoints. Confirm every figure on Groq’s official documentation before you plan work around the cap. The official URL we store is [{{url}}]({{url}}).

{{FACTBOX}}

## How do I call Groq with the OpenAI SDK?

Use the official OpenAI client and set the base URL to the published value in our list: `{{base_url}}`. Put your Groq API key in an environment variable. Copy the model id from Groq’s official docs or console — this site will not invent one, because the notes say limits vary by model and catalogues change.

{{SNIPPETS}}

If a request fails with an unknown-model error, the id is usually wrong or not included in the free allowance. If it fails with 429, you have hit a cap on requests or tokens; see [Rate limits explained](/guides/rate-limits-explained).

## How should I read the published allowance?

The allowance we record is a **daily token** figure on listed models, plus a **daily request** figure on listed models. Both are limits, and either can stop a job first. Because limits vary by model, a number that holds for one official model id may not hold for another. We do not extrapolate a per-model table that Groq has not published in our source.

“Listed models” means the models Groq includes in that official rate-limit documentation on the day you check it, not a list we maintain here.

A card is recorded as **{{card_required}}** in our data. If the official signup flow later asks for a card, follow the official page and treat our field as stale until we update it.

## Is Groq a relay?

No. In this tracker Groq is an official provider with **{{relay}}** relay warning. You are still bound by Groq’s terms and privacy policy. Official is not the same as “my prompts are never stored.” Read their current policy if the text is sensitive. For the general distinction, see [Official providers vs gateways](/guides/official-vs-gateway-providers).

## How might I use this as a first official endpoint?

Groq is a reasonable first official OpenAI-compatible target when you want a published base URL and a published daily token figure without a relay in the middle. It is often used for short tests and for [coding assistants](/guides/free-llm-apis-for-coding), but assistants can consume a daily request cap quickly. Use a dedicated key, keep it in the environment, and start with a small prompt.

The setup steps are the same as in [A free LLM API for beginners](/guides/free-llm-api-for-beginners): official account, environment variable, exact base URL, official model id, one test request, then look at the dashboard.

## What will this page not tell you?

It will not name a “best” Groq model, quote a latency number, or convert tokens into words with a homemade formula. It will not claim the free allowance is permanent. It will not list regional endpoints that are not in our data. If you need those details, use Groq’s official docs.

If you compare Groq with other official rows that also publish a daily token figure, use the generated tables in [Best free LLM APIs (current)](/guides/best-free-llm-apis) rather than a memorised ranking. Several official providers publish no daily token number at all and still have a free tier; they will not sort to the top of a tokens-per-day list.

## How do I check that our row is still right?

Open the official rate-limit or docs link stored on the card, and compare the allowance, the request cap, the card requirement and the base URL. If they differ, trust the official page and [send us the public link](/contact). We update the list daily; this entry was first listed on {{first_reported}} and last changed on {{entry_updated}}.

Related official snapshots on this site include [Gemini](/guides/gemini-api) and [Cerebras](/guides/cerebras-api). Those pages follow the same rule: only data.json fields and official URLs, with placeholders that stay in sync when the list changes.


## What should I do after the first successful call?

Look at Groq’s official console for usage, if it shows remaining daily capacity. Then decide whether the published request cap or the published token cap is the tighter constraint for your kind of work. A few long completions can spend tokens quickly; a coding agent can spend the request cap quickly. If you stop for the day after a 429, wait for the official window to reset instead of creating extra keys to bypass a limit — that may break the provider’s terms.

Keep the test key dedicated to Groq. If you later add a second official provider, use a second environment variable rather than overwriting the first key. The [how-to guide](/guides/how-to-use-free-openai-compatible-apis) shows the same client with a different `base_url`.
