"""MCP server (stdio) that lets any MCP-capable agent work tasks on the hosted environment.

Minimal JSON-RPC 2.0 over stdin/stdout implementing the MCP methods agents need: initialize,
tools/list, tools/call (plus ping and notifications). No SDK dependency. Every tool call goes to the
hosted API with the buyer's API key from the environment (XZAR_API_KEY, XZAR_API_URL); this process
holds no tasks and no answer keys.

Tools: start_task, search_library, read_publication, submit_answer, get_scorecard, get_usage.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Callable, TextIO

PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "xzar", "version": "0.1.1"}

TOOLS = [
    {"name": "start_task", "description": "Start a new task episode. Returns the episode id, the instructions and the tool budget.",
     "inputSchema": {"type": "object", "properties": {
         "task_id": {"type": "string", "description": "Optional specific task id"},
         "taskset": {"type": "string", "description": "Optional task set: patents-first-action (default), "
                                                      "patents-response or patents-appeal"}}}},
    {"name": "search_library", "description": "Search the episode's prior-art library (publications dated before the filing date).",
     "inputSchema": {"type": "object", "properties": {"episode_id": {"type": "string"}, "query": {"type": "string"}},
                     "required": ["episode_id", "query"]}},
    {"name": "read_publication", "description": "Read one publication from the episode's library.",
     "inputSchema": {"type": "object", "properties": {"episode_id": {"type": "string"}, "publication": {"type": "string"}},
                     "required": ["episode_id", "publication"]}},
    {"name": "search_rules", "description": "Search the examination manual for the rules and tests examiners apply.",
     "inputSchema": {"type": "object", "properties": {"episode_id": {"type": "string"}, "query": {"type": "string"}},
                     "required": ["episode_id", "query"]}},
    {"name": "read_rule", "description": "Read one examination manual section by number, e.g. 2143.01.",
     "inputSchema": {"type": "object", "properties": {"episode_id": {"type": "string"}, "section": {"type": "string"}},
                     "required": ["episode_id", "section"]}},
    {"name": "submit_answer", "description": "Submit the final answer (JSON object in the format the instructions give). One per episode.",
     "inputSchema": {"type": "object", "properties": {"episode_id": {"type": "string"}, "answer": {"type": "object"}},
                     "required": ["episode_id", "answer"]}},
    {"name": "get_scorecard", "description": "Your scorecard: scores by skill and where your agent fails.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "get_usage", "description": "Your credit balance and recent charges.", "inputSchema": {"type": "object", "properties": {}}},
]

# Directory requirement: every tool has a title and safety hints. Nothing here deletes or changes the user's data;
# start_task and submit_answer use credit, so they are not read-only.
ANNOTATIONS = {
    "start_task": {"title": "Start an evaluation task", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
    "search_library": {"title": "Search the case's reference library", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    "read_publication": {"title": "Read a library publication", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    "search_rules": {"title": "Search the rulebook", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    "read_rule": {"title": "Read a rulebook section", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    "submit_answer": {"title": "Submit the agent's answer for grading", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
    "get_scorecard": {"title": "Get your scorecard", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    "get_usage": {"title": "Get your credit balance and usage", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
}
for _tool in TOOLS:
    _tool["title"] = ANNOTATIONS[_tool["name"]]["title"]
    _tool["annotations"] = ANNOTATIONS[_tool["name"]]

Requester = Callable[[str, str, Any], tuple[int, Any]]


def http_requester(base_url: str, api_key: str) -> Requester:
    def request(method: str, path: str, body: Any) -> tuple[int, Any]:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(base_url.rstrip("/") + path, data=data, method=method,
                                     headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.status, json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read() or b"{}")
            except json.JSONDecodeError:
                return exc.code, {"error": f"HTTP {exc.code}"}
    return request


def call_tool(request: Requester, name: str, args: dict[str, Any]) -> tuple[bool, Any]:
    """Return (is_error, payload)."""
    eid = str(args.get("episode_id", ""))
    if name == "start_task":
        status, body = request("POST", "/v1/episodes", {k: args[k] for k in ("task_id", "taskset") if args.get(k)})
    elif name == "search_library":
        status, body = request("POST", f"/v1/episodes/{eid}/tools/search_library", {"query": args.get("query", "")})
    elif name == "read_publication":
        status, body = request("POST", f"/v1/episodes/{eid}/tools/read_publication", {"publication": args.get("publication", "")})
    elif name in ("search_rules", "read_rule"):
        payload = {"query": args.get("query", "")} if name == "search_rules" else {"section": args.get("section", "")}
        status, body = request("POST", f"/v1/episodes/{eid}/tools/{name}", payload)
    elif name == "submit_answer":
        status, body = request("POST", f"/v1/episodes/{eid}/submit", {"answer": args.get("answer")})
    elif name == "get_scorecard":
        status, body = request("GET", "/v1/scorecard", None)
    elif name == "get_usage":
        status, body = request("GET", "/v1/usage", None)
    else:
        return True, {"error": f"unknown tool {name}"}
    return status != 200, body


def handle_message(msg: dict[str, Any], request: Requester) -> dict[str, Any] | None:
    method, mid = msg.get("method"), msg.get("id")
    if mid is None:  # notification (e.g. notifications/initialized): no reply
        return None
    if method == "initialize":
        result: Any = {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}}, "serverInfo": SERVER_INFO}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = msg.get("params") or {}
        is_error, payload = call_tool(request, params.get("name", ""), params.get("arguments") or {})
        result = {"content": [{"type": "text", "text": json.dumps(payload)}], "isError": is_error}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def serve(stdin: TextIO, stdout: TextIO, request: Requester) -> None:
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            reply: dict[str, Any] | None = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            reply = handle_message(msg, request)
        if reply is not None:
            stdout.write(json.dumps(reply) + "\n")
            stdout.flush()


def main() -> None:
    key = os.environ.get("XZAR_API_KEY")
    if not key:
        sys.stderr.write("XZAR_API_KEY is required (get one at https://xzar.si/signup.html)\n")
        sys.exit(2)
    serve(sys.stdin, sys.stdout, http_requester(os.environ.get("XZAR_API_URL", "https://api.xzar.si"), key))


if __name__ == "__main__":
    main()
