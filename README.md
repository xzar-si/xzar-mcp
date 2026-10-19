# Xzar MCP server

**Crash-test your AI agent on real professional decisions.** Xzar gives your agent real cases, cut at the moment of decision, and grades its answer against what the professional actually decided. Most cases were decided after current models were trained, so they can't have been memorized; fresh ones are added monthly.

Live today:
- **Tariff classification:** real U.S. classification decisions, graded exactly at 2, 4, 6, 8 and 10 digits, with a consistency check (the same case asked twice). Testing a tariff classifier? See https://xzar.si/scorecard
- **Patent examination:** first action, response and appeal.

More fields are on the way; ask for yours at https://xzar.si.

<!-- mcp-name: si.xzar/xzar -->

## Setup

1. Get an API key (with $5 of free credit) at https://xzar.si/signup.html
2. Add the server to your MCP client:

```json
{
  "mcpServers": {
    "xzar": {
      "command": "uvx",
      "args": ["xzar-mcp"],
      "env": { "XZAR_API_KEY": "your-key" }
    }
  }
}
```

## Hosted connector (no install)

In Claude or any MCP client that supports remote servers: add `https://api.xzar.si/mcp` and sign in with your Xzar API key.

## Claude plugin

The [`plugin/`](plugin) folder is the Xzar plugin for Claude. It bundles the hosted connector with two skills: `crash-test`, which runs a task end to end and explains the score, and `xzar-request`, for custom tests, pilots, quotes and training access. In Claude Code:

```
/plugin install xzar --marketplace xzar-si/xzar-mcp
```

## Tools

| Tool | What it does |
|---|---|
| `start_task` | Start a task: the case, the instructions and the tool budget |
| `search_library` | Search the case's reference library |
| `read_publication` | Read one library item |
| `search_rules` | Search the professional rulebook for the task |
| `read_rule` | Read one rulebook section |
| `submit_answer` | Submit the decision; returns the exact score and the grade receipt |
| `request_service` | Ask for a custom test for your field, a pilot, a quote, or training access; get a reference and next steps |
| `get_scorecard` | Your agent's scorecard across tasks |
| `get_usage` | Credit balance and usage |

Answer keys never leave Xzar's servers. This package holds no tasks; it calls the Xzar API with your key.

## Pricing

Prepaid credits, charged per task. See https://xzar.si/docs.html. Pilots and ongoing testing: https://xzar.si.
