---
slug: sambanova-cloud
title: SambaNova Cloud free plan — published caps and card notes
lede: SambaNova Cloud is an official, OpenAI-compatible API. Our row records a per-model daily token cap and notes that the free plan has required a card and a purchase since mid-October.
description: SambaNova Cloud API snapshot from this tracker: 200,000 tokens/day per model (as of 3 Oct), 20 requests/day, card required, and the OpenAI-compatible base URL.
date_published: 2026-11-12
date_modified: 2026-11-12
provider_id: sambanova
related: cerebras-api, groq-free-api, how-to-use-free-openai-compatible-apis, rate-limits-explained
---

## What is SambaNova Cloud on this tracker?

{{name}} is listed as an **{{category}}** with OpenAI compatibility **{{openai_compatible}}**. The recorded free allowance is “{{free_allowance}}”. Tokens per day are **{{tokens_per_day}}**. Limits are “{{limits}}”. Card required is **{{card_required}}**. Relay warning: **{{relay}}**. Our notes say: {{notes}}

Those notes matter as much as the daily token figure. The official URL we store is [{{url}}]({{url}}). The entry was first listed on {{first_reported}} and last updated on {{entry_updated}} — later than many neighbouring official rows, because of the card-and-purchase change recorded in the notes. List snapshot: {{list_updated}}.

{{FACTBOX}}

## How should I read “per model” together with a request cap?

The daily token figure we store is described as applying **per model**, as of the official wording we saw on 3 October. That is not necessarily a single shared pool, and it is not a licence to assume every current model is in the free plan. Official plans may add, remove or re-price models later.

Separately, we record a limit of {{limits}}. A 20-requests-per-day cap, if still accurate on the official page, can stop a [coding assistant](/guides/free-llm-apis-for-coding) long before the token cap does. Always compare both fields, and confirm both on the official plans page. Background: [Rate limits explained](/guides/rate-limits-explained).

## What changed in the card requirement?

Our notes record that since 15 October the Free plan requires a card and a purchase. The card field is therefore **{{card_required}}**. We do not invent the size of that purchase, or whether a past no-card account was grandfathered; those details, if they exist, belong on the official site. If you signed up earlier, do not assume our older memory of a no-card plan still applies — look at the live plans page.

This is an example of why the tracker stores an entry-level `last_updated` date and a changelog on the home page, instead of treating every official free tier as frozen.

## How do I call the published base URL?

The base URL we record is `{{base_url}}`. Use a SambaNova key in the environment, the official OpenAI SDK, and a model id from SambaNova’s official documentation.

{{SNIPPETS}}

If the official console requires you to attach a card or complete a purchase before the key can call a model, the SDK will not bypass that. Handle 401, 403 and payment errors by reading the official account page, not by retrying in a loop.

## Is SambaNova a relay?

No. It is official in our category, with **{{relay}}** relay warning. You still accept SambaNova’s terms when you create an account. For private prompts, official providers are the default we recommend over flagged relays, as explained in [Official providers vs gateways](/guides/official-vs-gateway-providers).

## How does this compare with Groq and Cerebras?

In our file, Groq also has a recorded daily token figure of 200,000 on listed models, with a much higher recorded daily request cap and a card field of No — see [Groq](/guides/groq-free-api) and confirm both official pages, because those numbers can change. Cerebras records a higher daily token figure but only during a 30-day card-required trial — see [Cerebras](/guides/cerebras-api). SambaNova’s distinctive recorded constraints are the **per-model** wording, the **20 requests/day** limit, and the **card and purchase** note on the free plan.

None of these comparisons is a quality ranking. They are a reading of published fields.

## How do I verify this row?

Open [{{url}}]({{url}}) and check the allowance, the per-model language, the request cap, the card rule and the base URL. If something has changed, [send the official link](/contact). We will not drop the card note to make the row look easier, and we will not convert “per model” into a shared pool unless an official page says that.


## What should I do on signup day?

Open the official plans page first, not only this guide. Confirm whether a card and a purchase are still required, which models are in the free plan, and whether the 20-requests-per-day figure still holds. Then create the account, store the key in the environment, and make one short request with an official model id.

If you are doing this to run an editor assistant, do the maths in requests, not only in tokens: twenty official requests is a small number for an agent that retries. You may want a provider with a higher published request cap for that workflow, or you may want to use SambaNova only for single, careful calls.

## How should teams record this provider internally?

Write down the official plan name, the date you confirmed the card-and-purchase rule, and the two caps (tokens per model per day, requests per day) as they appeared on the official page. Link to the official plans URL. You can also link to this tracker row, but treat our snapshot date as a hint to re-check, not as a contract. If SambaNova’s official wording changes, update your internal note even if this page has not yet caught up.
