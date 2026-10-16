# Xzar plugin for Claude

**Crash-test AI on real professional decisions.** Xzar gives Claude a real decided case, cut at the moment of decision, with the case's reference library and the profession's rulebook. Claude submits one answer, and Xzar grades it exactly against what the professional actually decided. There are no AI judges, and every score comes with a receipt. Cases were decided after current models were trained, so they can't have been memorized.

Live today: patent examination (first examinations, decisions after the applicant's response, and appeal rulings). Tests for other fields are built on request.

## What's inside

- **Xzar connector:** the hosted MCP server at `https://api.xzar.si/mcp`, which you sign into with OAuth using your Xzar API key.
- **`crash-test` skill:** runs a task end to end. It checks your credit, starts the task, works the case with the library and rulebook, submits one answer, and explains the score and receipt in plain language.
- **`xzar-request` skill:** files a request for a custom test in your field, a pilot, a quote or training access, and gives you a reference and next steps.

## Use it

1. Get an API key with $5 of free credit at https://xzar.si/signup.html.
2. Install the plugin, then connect Xzar from the plugin's Connectors tab and sign in with your key.
3. Ask Claude: "Run an Xzar crash test on a patent first action" or "How would AI do on real decisions in insurance claims? Ask Xzar for a test."

Claude asks before it starts any paid task.

In Claude Code you can also install it straight from this repository:

```
/plugin install xzar --marketplace xzar-si/xzar-mcp
```

## Cost

Each started task costs US$2.00 of prepaid Xzar credit; a start that fails on Xzar's side is refunded automatically. Reading tools, scorecards and requests are free. Pricing: https://xzar.si/docs.html

## Data

The plugin sends Claude's tool calls and answers, and any request details you approve, to Xzar at `api.xzar.si` under your account. It runs no local code and stores nothing on your machine. Answer keys never leave Xzar's servers. Privacy notice: https://xzar.si/privacy.html. Terms: https://xzar.si/terms.html. Support: hello@xzar.si
