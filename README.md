# Xzar MCP server

**Crash-test your AI agent on real professional decisions.** Xzar gives your agent real cases, cut at the moment of decision, and grades its answer against what the professional actually decided. Cases are decided after current models were trained, so they can't have been memorized.

Live today: patent examination (first action, response, appeal). More fields are on the way; ask for yours at https://xzar.si.

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

## Tools

| Tool | What it does |
|---|---|
| `start_task` | Start a task: the case, the instructions and the tool budget |
| `search_library` | Search the case's reference library |
| `read_publication` | Read one library item |
| `search_rules` | Search the professional rulebook for the task |
| `read_rule` | Read one rulebook section |
| `submit_answer` | Submit the decision; returns the exact score and the grade receipt |
| `get_scorecard` | Your agent's scorecard across tasks |
| `get_usage` | Credit balance and usage |

Answer keys never leave Xzar's servers. This package holds no tasks; it calls the Xzar API with your key.

## Pricing

Prepaid credits, charged per task. See https://xzar.si/docs.html. Pilots and ongoing testing: https://xzar.si.
