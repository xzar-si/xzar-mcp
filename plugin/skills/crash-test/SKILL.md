---
name: crash-test
description: Run an Xzar crash test, where Claude works one real decided professional case and gets an exact score against what was actually decided. Use when the user asks to test, benchmark or evaluate AI on real professional decisions, to try Xzar, to run an Xzar task or episode, to see how AI does on real patent examination, or to check their Xzar scorecard, credit or usage.
---

# Xzar crash test

Xzar gives an AI a real professional case, cut at the moment of decision, and grades its one answer exactly against what the professional actually decided. Patent examination is the first field. The tools come from the Xzar connector (`https://api.xzar.si/mcp`). If they aren't available, ask the user to connect Xzar from the plugin's Connectors tab and sign in with their Xzar API key. A key with $5 of free credit is at https://xzar.si/signup.html.

## Before you start

1. Each started task costs US$2.00 of the user's Xzar credit. Read the tools freely, but don't call `start_task` until the user has said to run a task in this conversation. If they asked for several, confirm the number and total cost first.
2. Call `get_usage` and tell the user their balance in one line.
3. Choose the task set. If the user doesn't say, use `patents-first-action`.
   - `patents-first-action`: the first examination. Reject or allow each claim, on which grounds, and citing which prior art. Library and rulebook tools.
   - `patents-response`: the next decision after the applicant answers a rejection. Rulebook tools.
   - `patents-appeal`: the appeal board's ruling, affirming or reversing the rejection of each appealed claim. Rulebook tools.

## Work the case

1. Call `start_task` with the task set. Read the returned instructions completely: they give the case, the answer format and the tool budget. Note the `episode_id`.
2. Work it like the professional would, within the budget:
   - Search the rulebook (`search_rules`, `read_rule`) for the tests that apply.
   - When library tools are available, search the case's library (`search_library`) with specific technical terms from the claims, and read the most promising publications (`read_publication`). Only publications from the library count as prior art.
   - Decide claim by claim. Don't reject a claim without a ground you can support, and don't cite a reference you haven't read. Wrong extra grounds cost more than missed ones.
3. Submit exactly one answer with `submit_answer`, in the JSON format the instructions give. For first actions it looks like this:
   `{"claims": [{"claim": 1, "rejected": true, "grounds": [{"ground": "103", "references": ["US 2017/0323236"]}]}, {"claim": 2, "rejected": false, "grounds": []}]}`
   You get one submission per episode, so check the claim numbers and format before sending.

## Report the result

Tell the user, in plain language:
- the score from 0 to 1, and its three parts: claim status, grounds and prior art;
- what the receipt says you got right and wrong, claim by claim, in a few lines (don't paste the raw response);
- one sentence on the likely reason for the miss, for example too lenient, wrong ground, or a reference not found.

Report the score as it is. Don't argue with the grade or say the recorded decision was wrong; the point of the test is to measure the gap. If the user ran several tasks, call `get_scorecard` and summarize their mean score, where they fail most, and how they compare with the two rules of thumb on the same tasks.

## Rules

- Answer keys never leave Xzar's servers. Don't guess or reconstruct what the recorded decision was beyond what the receipt shows.
- Each case is served once per account, so a task can't be retried. Starting another task costs another $2.00.
- If a tool returns an error, tell the user what it said. A start that fails on Xzar's side is refunded automatically.
- For a test in another field, a pilot, a quote or training access, use the `xzar-request` skill.
