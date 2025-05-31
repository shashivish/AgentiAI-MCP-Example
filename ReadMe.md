# 🧠 MCP Project Setup

This guide walks you through setting up a Python virtual environment and installing the required dependencies for an MCP-based project.

---

## 🔧 Setup Instructions

### 1. Create a Virtual Environment

```bash
python -m venv mcp-env

source mcp-env/bin/activate

pip install mcp
pip install fastmcp
pip install agno
pip install openai
pip install requests

```
`
### 1. Start MCp Server

```
python mcp_server.py

```

### 2.  Start Agent 
```shell
python agon_agent.py

```