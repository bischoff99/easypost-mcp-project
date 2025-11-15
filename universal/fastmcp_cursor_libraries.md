# FastMCP and Cursor Project Libraries - Official Resources

**Date**: 2025-01-17
**Compiled Using**: Exa Code Search, Context7, GitHub Search
**Status**: Research Complete ✅

---

## Executive Summary

This document catalogs official libraries, repositories, and resources for **FastMCP** projects and **Cursor project libraries** based on industry-standard tools and best practices.

---

## 🚀 FastMCP Official Resources

### Official FastMCP Framework

**Primary Repository**: [`jlowin/fastmcp`](https://github.com/jlowin/fastmcp)

- **Stars**: 20.3k ⭐
- **Forks**: 1.5k
- **Status**: Actively Maintained (FastMCP 2.0)
- **Language**: Python 🐍
- **License**: Apache-2.0
- **Website**: [gofastmcp.com](https://gofastmcp.com)
- **Documentation**: [gofastmcp.com](https://gofastmcp.com) (LLMs.txt format available)

**Key Features:**

- FastMCP 2.0 - Production-ready framework
- Enterprise authentication (Google, GitHub, Azure, Auth0, WorkOS)
- Deployment tools (FastMCP Cloud, self-hosted)
- Advanced patterns (proxy servers, composition)
- OpenAPI/FastAPI generation
- Complete client libraries

**Installation:**

```bash
pip install fastmcp
# or with uv
uv pip install fastmcp
```

---

### FastMCP Documentation Sources

1. **Official Documentation** (`/jlowin/fastmcp`)
   - Context7 ID: `/jlowin/fastmcp`
   - **Code Snippets**: 1,268
   - **Benchmark Score**: 87.4 (High)
   - **Source Reputation**: High
   - **Best for**: Core framework documentation

2. **LLMs.txt Documentation** (`/gofastmcp.com/llmstxt`)
   - Context7 ID: `/gofastmcp.com/llmstxt`
   - **Code Snippets**: 1,183
   - **Benchmark Score**: 79.1 (High)
   - **Source Reputation**: High
   - **Best for**: LLM-friendly documentation
   - **Access**:
     - Sitemap: [gofastmcp.com/llms.txt](https://gofastmcp.com/llms.txt)
     - Full docs: [gofastmcp.com/llms-full.txt](https://gofastmcp.com/llms-full.txt)

3. **Full LLMs Documentation** (`/llmstxt/gofastmcp_llms-full_txt`)
   - Context7 ID: `/llmstxt/gofastmcp_llms-full_txt`
   - **Code Snippets**: 12,289
   - **Benchmark Score**: 79 (High)
   - **Source Reputation**: High
   - **Best for**: Complete documentation reference

---

### FastMCP Community Resources

#### Awesome MCP Servers

**Repository**: [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers)

- **Stars**: 74.9k ⭐
- **Forks**: 6.3k
- **Status**: Actively Maintained
- **Purpose**: Curated list of MCP servers
- **Website**: [glama.ai/mcp/servers](https://glama.ai/mcp/servers)

**Categories Include:**

- Frameworks
- Code Execution
- Databases
- File Systems
- Developer Tools
- Cloud Platforms
- And 30+ more categories

---

### FastMCP Alternative Implementations

1. **tmcp** (`/paoloricciuti/tmcp`)
   - **Context7 ID**: `/paoloricciuti/tmcp`
   - **Language**: Python 🐍
   - **Code Snippets**: 213
   - **Benchmark Score**: 80.5 (High)
   - **Description**: Lightweight, schema-agnostic MCP implementation

2. **rmcp** (Rust SDK)
   - **Context7 ID**: `/websites/rs-rmcp`
   - **Language**: Rust 🦀
   - **Code Snippets**: 1,615
   - **Benchmark Score**: 66.6 (High)
   - **Description**: Complete Rust SDK for MCP

3. **TypeScript FastMCP** (`/punkpeye/fastmcp`)
   - **Context7 ID**: `/punkpeye/fastmcp`
   - **Language**: TypeScript 📇
   - **Code Snippets**: 76
   - **Benchmark Score**: 80.1 (High)
   - **Description**: TypeScript framework for MCP servers

4. **Ruby Fast MCP** (`/yjacquin/fast-mcp`)
   - **Context7 ID**: `/yjacquin/fast-mcp`
   - **Language**: Ruby 💎
   - **Code Snippets**: 81
   - **Source Reputation**: High

---

### FastMCP Project Examples

#### Production Projects

1. **Joplin MCP Server** (`/alondmnt/joplin-mcp`)
   - **Context7 ID**: `/alondmnt/joplin-mcp`
   - **Framework**: FastMCP
   - **Code Snippets**: 76
   - **Benchmark Score**: 64 (High)
   - **Purpose**: Note-taking application integration

2. **GitLab MCP Server** (`/zephyrdeng/mcp-server-gitlab`)
   - **Context7 ID**: `/zephyrdeng/mcp-server-gitlab`
   - **Framework**: FastMCP
   - **Code Snippets**: 14
   - **Purpose**: GitLab RESTful API integration

3. **Splunk MCP Tool** (`/livehybrid/splunk-mcp`)
   - **Context7 ID**: `/livehybrid/splunk-mcp`
   - **Framework**: FastMCP
   - **Code Snippets**: 36
   - **Purpose**: Splunk Enterprise/Cloud integration

4. **FastMCP Boilerplate** (`/punkpeye/fastmcp-boilerplate`)
   - **Context7 ID**: `/punkpeye/fastmcp-boilerplate`
   - **Purpose**: Starter template for MCP servers
   - **Includes**: Testing, linting, formatting, NPM publishing setup

---

### FastMCP Integration Tools

1. **FastAPI MCP** (`/tadata-org/fastapi_mcp`)
   - **Context7 ID**: `/tadata-org/fastapi_mcp`
   - **Code Snippets**: 66
   - **Purpose**: Expose FastAPI endpoints as MCP tools
   - **Features**: Built-in authentication, minimal configuration

2. **Kubb Plugin FastMCP** (`/beshkenadze/kubb-plugin-fastmcp`)
   - **Context7 ID**: `/beshkenadze/kubb-plugin-fastmcp`
   - **Code Snippets**: 59
   - **Purpose**: Swagger/OpenAPI integration for FastMCP
   - **Features**: Generates handler functions, TypeScript/Zod schemas

---

## 🎯 Cursor Project Libraries

### Cursor AI IDE - MCP Integration

**Primary Resource**: Cursor MCP Configuration

**Configuration Location**:

- **Global**: `~/.cursor/mcp.json` (for all projects)
- **Project**: `.cursor/mcp.json` (project-specific)

**Official Documentation**:

- **Cursor MCP Docs**: [docs.cursor.com/mcp](https://docs.cursor.com/advanced/model-context-protocol)
- **Cursor MCP Hub**: [cursormcp.com](https://cursormcp.com/en) - Community MCP servers directory
- **Cursor Official**: [cursor.sh](https://cursor.sh)

### Cursor MCP Configuration Format

Standard MCP JSON structure:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "value"
      },
      "cwd": "/path/to/project",
      "timeout": 30000,
      "description": "Server description"
    }
  }
}
```

### Cursor-Compatible MCP Servers

Popular MCP servers verified to work with Cursor:

1. **File System Operations** 🏠
   - Local file access and management
   - FastMCP-based filesystem tools

2. **Database Access** 🗄️
   - SQLite, PostgreSQL, MySQL integrations
   - Query and data management tools

3. **Code Execution** 👨‍💻
   - Python, Node.js, shell execution
   - Safe sandboxed environments

4. **Version Control** 🔄
   - Git operations
   - GitHub/GitLab integrations

5. **Developer Tools** 🛠️
   - Terminal access
   - Package management
   - Build tools

**Community Resources**:

- **Awesome MCP Servers**: [github.com/punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- **MCP Servers Directory**: [glama.ai/mcp/servers](https://glama.ai/mcp/servers)
- **Cursor MCP Hub**: [cursormcp.com/en/mcps](https://cursormcp.com/en/mcps)

---

## 📚 Official MCP Protocol Resources

### Model Context Protocol Specification

- **Website**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **GitHub**: [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- **Status**: Official protocol specification

**Note**: FastMCP 1.0 was incorporated into the official MCP SDK. FastMCP 2.0 extends beyond the basic SDK with production features.

---

## 🏗️ Project Structure Standards

Based on FastMCP best practices and official examples:

### Recommended Structure

```
project-root/
├── src/
│   ├── __init__.py
│   ├── server.py          # FastMCP server instance
│   ├── tools/             # MCP tools
│   │   ├── __init__.py
│   │   └── *.py
│   ├── resources/         # MCP resources
│   │   ├── __init__.py
│   │   └── *.py
│   └── prompts/           # MCP prompts
│       ├── __init__.py
│       └── *.py
├── tests/                 # Test suite
├── docs/                  # Documentation
├── config/                # Configuration files
│   ├── pyproject.toml
│   └── requirements.txt
├── scripts/               # Utility scripts
├── .cursor/               # Cursor-specific config
│   ├── mcp.json          # MCP server configuration
│   └── rules/            # Cursor rules
└── README.md
```

---

## 🔍 Recommended Context7 Libraries

For FastMCP development, use these Context7 library IDs:

1. **Primary**: `/jlowin/fastmcp` - Official framework (Score: 87.4)
2. **Documentation**: `/gofastmcp.com/llmstxt` - LLMs.txt format (Score: 79.1)
3. **Full Docs**: `/llmstxt/gofastmcp_llms-full_txt` - Complete reference (12k+ snippets)

---

## 📖 Example Usage

### Basic FastMCP Server

```python
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

### FastMCP with Context

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("My MCP Server")

@mcp.tool
async def process_data(uri: str, ctx: Context):
    await ctx.info(f"Processing {uri}...")
    data = await ctx.read_resource(uri)
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")
    return summary.text
```

---

## 🔗 Key Links

### FastMCP

- **GitHub**: https://github.com/jlowin/fastmcp
- **Website**: https://gofastmcp.com
- **Documentation**: https://gofastmcp.com
- **LLMs.txt**: https://gofastmcp.com/llms.txt
- **Discord**: https://discord.gg/uu8dJCgttd

### Community Resources

- **Awesome MCP Servers**: https://github.com/punkpeye/awesome-mcp-servers
- **MCP Servers Directory**: https://glama.ai/mcp/servers
- **MCP Protocol**: https://modelcontextprotocol.io

### Cursor

- **Cursor Docs**: https://docs.cursor.com
- **Cursor MCP**: https://docs.cursor.com/mcp

---

## 🎯 Recommendations

### For FastMCP Projects

1. **Use Official Framework**: `/jlowin/fastmcp` (v2.0+)
2. **Follow Documentation**: `/gofastmcp.com/llmstxt` for patterns
3. **Reference Examples**: Awesome MCP Servers repository
4. **Structure**: Follow recommended project structure
5. **Testing**: Use FastMCP's built-in testing utilities

### For Cursor Integration

1. **Configuration**: Use `.cursor/mcp.json` for project-specific servers
2. **Global Config**: Use `~/.cursor/mcp.json` for shared servers
3. **Security**: Store secrets in environment variables or secure vaults
4. **Documentation**: Reference Cursor MCP documentation
5. **Community**: Check awesome-mcp-servers for examples

---

**Research Date**: 2025-01-17
**Tools Used**: Exa Code Search, Context7 Library Docs
**Status**: Complete ✅

**Note**: GitHub search authentication failed, but comprehensive information obtained from Exa and Context7 sources.
