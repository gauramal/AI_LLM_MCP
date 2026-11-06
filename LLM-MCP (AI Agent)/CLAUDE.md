# LLM-MCP (AI Agent) - Project Conventions for Claude Code & AI Agents

## Project Overview
LLM-MCP is an AI agent-driven test automation and QA experimentation project. It combines Large Language Model (LLM) agents with Model Context Protocol (MCP) servers and Python Playwright end-to-end (E2E) testing against Rahul Shetty Academy practice applications, REST APIs, MySQL databases, and Excel data sources.

## Tech Stack
- **Language**: Python 3.12+
- **Test Framework**: Pytest (`pytest>=8.0`), `pytest-playwright>=0.5.0`
- **Pattern**: Page Object Model (POM)
- **Target Applications**:
  - Web Login: `https://rahulshettyacademy.com/loginpagePractise/`
  - Shop Catalog: `https://rahulshettyacademy.com/angularpractice/shop`
  - REST API: `https://rahulshettyacademy.com`
  - Database: Local MySQL 8.0 (`rahulshettyacademy`)
- **MCP Servers**:
  - `playwright`: Headed/headless browser automation via `@playwright/mcp@latest`
  - `filesystem`: Scoped workspace file operations via `@modelcontextprotocol/server-filesystem`
  - `excel-mcp-server`: Spreadsheet reading, editing, and formatting via `@negokaz/excel-mcp-server`
  - `rest-api`: HTTP request execution via `dkmaker-mcp-rest-api`
  - `mysql`: Database query and schema inspection via `mysql-mcp-server` (uvx)

## Project Structure
```
LLM-MCP (AI Agent)/
├── .agents/
│   └── mcp_config.json              # MCP server definitions for agent runtimes
├── .vscode/
│   ├── mcp.json                     # VS Code / Copilot MCP server definitions
│   └── settings.json
├── Python Practice/
│   ├── pytest.ini                   # Pytest configuration (Chromium, headed)
│   ├── requirements-test.txt        # Test dependencies
│   └── tests/
│       ├── __init__.py
│       ├── test_login_shop.py       # E2E test scenarios
│       └── pages/
│           ├── __init__.py
│           ├── login_page.py        # LoginPage (POM)
│           └── shop_page.py         # ShopPage (POM)
├── EcomBasic.postman_collection.json # API endpoints and collection tests
├── newdata.xlsx                     # Excel data-driven test dataset
├── Untitled.sql                     # MySQL database schema & seed scripts
├── CLAUDE.md                        # Claude Code conventions & project guide
└── AGENTS.md                        # Antigravity / Gemini agent conventions
```

## Architecture Pattern
- **Page Object Model (POM)**:
  - Page classes encapsulate selectors and page action methods (`tests/pages/`).
  - Tests call POM action methods and contain all assertions (`tests/test_*.py`).
- **Tool-Augmented Testing**:
  - Agents interact through standardized MCP tools (REST requests, MySQL SQL execution, Excel manipulation, and Playwright browser control).

## Commands to Run
```bash
# Activate virtual environment
source ../.venv/bin/activate

# Install test dependencies
pip install -r "Python Practice/requirements-test.txt"
playwright install chromium

# Run all Playwright tests
pytest "Python Practice/tests"

# Run a specific test file
pytest "Python Practice/tests/test_login_shop.py"

# Run a specific test by name
pytest "Python Practice/tests/test_login_shop.py" -k "test_valid_login_displays_iphone_x"

# Run in headless mode (overriding pytest.ini)
pytest "Python Practice/tests" --headed=false
```

## Testing Conventions
- All test files must be placed in `Python Practice/tests/` and named `test_<feature>.py`.
- Page objects belong in `Python Practice/tests/pages/`.
- **Locator Strategy (Priority Order)**:
  1. Accessibility roles: `page.get_by_role("button", name=...)`, `page.get_by_role("textbox", name=...)`
  2. Labels / Placeholders: `page.get_by_label(...)`, `page.get_by_placeholder(...)`
  3. Text: `page.get_by_text(...)`
  4. Stable IDs: `page.locator("#element-id")`
  5. Avoid brittle CSS hierarchies and absolute XPaths.
- **Wait Strategies**:
  - Never use hardcoded sleeps like `time.sleep()`.
  - Use Playwright web assertions and explicit state waits (e.g., `page.wait_for_url()`, `expect(element).to_be_visible()`).
- Tests should be self-contained and idempotent.

## MCP Server Reference

| Server | Command / Type | Purpose | Key Parameters / Config |
|---|---|---|---|
| `playwright` | `npx -y @playwright/mcp@latest` | Browser automation & UI testing | Standard browser control |
| `filesystem` | `npx -y @modelcontextprotocol/server-filesystem` | File reading & manipulation | Scoped to project root |
| `excel-mcp-server` | `npx -y @negokaz/excel-mcp-server` | Excel data-driven test data | Reads & writes `.xlsx` |
| `rest-api` | `npx -y dkmaker-mcp-rest-api` | REST API interaction | `REST_BASE_URL: https://rahulshettyacademy.com` |
| `mysql` | `uvx --from mysql-mcp-server mysql_mcp_server` | SQL queries & DB verification | Host: `localhost:3306`, DB: `rahulshettyacademy` |

## Test Accounts & Data Reference

### Web UI Login
- **URL**: `https://rahulshettyacademy.com/loginpagePractise/`
- **Username**: `rahulshettyacademy`
- **Password**: `Learning@830$3mK2`

### E-Commerce API Login (Postman)
- **Base URL**: `https://rahulshettyacademy.com`
- **User Email**: `rahulshetty@gmail.com`
- **Password**: `Iamking@000`

### MySQL Database (`rahulshettyacademy`)
- `RegistrationDetails` (`id_number`, `first_name`, `last_name`, `phone_number`, `occupation`, `gender`, `password`, `is_18_or_older`)
- `UserNames` (`id_number`, `email`)
- `Customers` (`id`, `name`, `city`, `age`)
- `Orders` (`order_id`, `customer_id`, `subject`, `company`, `order_date`)

## Code Style
- **Python**: PEP 8 style, strict type hints (`Page -> None`), descriptive variable and method names.
- Keep page classes focused on element resolution and user interactions; keep assertions inside test functions.
