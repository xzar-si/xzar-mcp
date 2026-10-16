---
name: xzar-request
description: File a request with Xzar for something not yet self-serve, such as a custom AI test for the user's own field (insurance, trade, legal, finance and others), an evaluation pilot, a written quote, or training access (verifiable-reward RL environments or training episodes for a model). Use when the user wants to evaluate or train AI on real decisions in their industry, asks about Xzar pricing beyond self-serve, or wants to work with Xzar.
---

# Request an Xzar service

Xzar builds tests from real decided cases in any field where professional decisions are made and recorded. Requests go through the `request_service` tool on the Xzar connector, and no credit is used.

## Pick the type

| Type | When | Starting price |
|---|---|---|
| `custom_test` | A test for the user's own field and decision | Pilots from US$10,000 for 30 days |
| `pilot` | A 30-day evaluation on Xzar's cases, with a scorecard and written failure analysis | US$10,000, paid upfront |
| `quote` | Volume, pricing or anything else in writing | Self-serve tasks are US$2.00 each |
| `training_access` | A lab or model builder wants to train on Xzar cases (the model's own attempts plus Xzar's verdict as the reward) | US$2.00 / 1.50 / 1.00 per episode by monthly volume |

## File it

1. Collect a work email (required) and whatever the user already knows: name, company, the field, the decision their AI makes (for example "approve or deny a claim"), the volume and the deadline. For `custom_test`, the field or the decision is required. Don't pad the request with guesses.
2. Show the user what you will send and file it only after they agree. A person at Xzar reads every request.
3. Call `request_service`. Give the user the reference (it looks like `XZR-1A2B3C`), the next steps and the pricing it returns. Xzar replies within one business day.
4. Tell them they can check the status at `https://api.xzar.si/v1/requests/<reference>?email=<their email>`, or write to hello@xzar.si.

If the connector isn't connected, the user can file the same request at https://xzar.si/request.html, with no key needed.
