# Network Engineering Assistant

A conversational CLI agent for Cisco enterprise network diagnostics and troubleshooting, built with the [Claude Agent SDK](https://docs.anthropic.com/claude-agent-sdk).

## Features

- Multi-turn conversation with persistent context (last 10 exchanges)
- Live tool execution via the `Bash` tool — runs real commands on the local machine
- Animated terminal UI with color output and typewriter effect
- Tailored system prompt for Cisco/enterprise networking workflows

## Requirements

- Python 3.10+
- `claude_agent_sdk` package
- Claude Code CLI authenticated (the SDK delegates to your local Claude Code session)

## Installation

```bash
pip install claude-agent-sdk
```

## Usage

```bash
python conversation_agent.py
```

Then type any network engineering question. The agent can run shell commands (e.g., `ping`, `traceroute`, `ssh`, `nmap`) and explain the results in context.

Type `exit` to quit.

## Example Prompts

- "Check connectivity to 10.0.0.1 and tell me if there's packet loss"
- "What does a high input error count on a Cisco interface indicate?"
- "Run a traceroute to 8.8.8.8 and explain each hop"

## Architecture

```
conversation_agent.py
  └── ClaudeAgentOptions   — configures allowed tools & system prompt
  └── query()              — async generator from claude_agent_sdk
        ├── TextBlock      — streamed assistant text
        ├── ToolUseBlock   — tool invocation (Bash)
        └── ToolResultBlock — command output
```

## License

MIT
