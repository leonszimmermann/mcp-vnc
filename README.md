# mcp-vnc
Model Context Protocol (MCP) Server to **remotely control any desktop using LLMs** over VNC.

**Supports Windows, Linux and MacOS**; basically any VNC server (TightVNC / TigerVNC / RealVNC).\
Also, **VMware Workstation / Fusion has a built-in VNC server**. Under you Virtual Machine's Settings > Advanced > Remote display over VNC. Enable it, and make sure to set a password. The port should be kept at default, 5900.


As a client, I personally use the Anthropic **Claude Desktop** Application, with **Sonnet/Opus 4** (currently the best model for computer use).
Any MCP-compatible client should work.

**DO NOT TRUST ANY LLM TO RUN YOUR PC AUTONOMOUSLY WITHOUT SUPERVISION.**

## Installation

### Python required

This MCP server requires [Python](https://www.python.org/downloads/) (including PIP).

### Install the requirements
```
pip install --upgrade fastmcp pillow vncdotool
```

### Download the MCP server script (vnc-mcp.py)

### Example claude_desktop_config.json

Can be found in Claude (Desktop App) > Settings > Developer > Edit Config

The path to you python executable can be found using "where python" in the Windows terminal, or "which python" in the terminal on Linux / MacOS.

**Don't forget the double colon (::) instead of the normal single colon (:) in the host parameter.**

```json
{
    "mcpServers": {
        "computer": {
          "command": "/ABSOLUTE/PATH/TO/YOUR/PYTHON/EXECUTABLE/ENDING/IN/bin/python",
          "args": [
            "/PATH/TO/YOUR/mcp-vnc.py"
          ],
          "env": {
            "VNC_HOST": "localhost::5900",
            "VNC_PASS": "YOUR VNC PASSWORD"
          }
        }
      }
}
```

### Usage

Make sure to **set the screen resolution of your remote desktop to 1024 x 768**, this currently works best.
