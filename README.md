# LangChain + Ollama Agent with API Tool

A simple AI agent built using **Python, LangChain, and Ollama (Llama 3.2)** that understands natural-language requests and invokes a REST API to trigger service deployment operations.

The agent uses a custom LangChain tool to send deployment parameters to a backend API.

## Features

- Integrates Ollama with LangChain.
- Uses the `llama3.2` local language model.
- Supports tool calling through a LangChain agent.
- Accepts natural-language user queries.
- Calls a REST API using Python `requests`.
- Supports deployment parameters such as countries, version tags, environments, and services.
- Handles API connection errors and request timeouts.
- Supports interactive terminal-based conversations.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application language |
| Ollama | Runs the local LLM |
| Llama 3.2 | Language model |
| LangChain | Agent and tool orchestration |
| Requests | REST API communication |
| Jenkins | Deployment system behind the API |

## Architecture

```text
User
  |
  v
Python Application
  |
  v
LangChain Agent
  |
  +----------> Ollama (Llama 3.2)
  |                 |
  |            Understands query
  |            Selects tool if needed
  |
  v
call_api Tool
  |
  v
Backend REST API
  |
  v
Jenkins Deployment
  |
  v
API Response
  |
  v
LangChain Agent
  |
  v
User
```

## Prerequisites

Install the following before running the application:

- Python 3.10 or later (use a version supported by your installed LangChain packages).
- Ollama.
- A locally available `llama3.2` model.
- A running backend API at `http://localhost:3000/api/deploy`.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

Replace the placeholders with your repository URL and project directory.

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip

pip install langchain langchain-core langchain-ollama requests
```

### 4. Install and start Ollama

Download Ollama from:

https://ollama.com/download

Pull the model:

```bash
ollama pull llama3.2
```

Verify that the model is available:

```bash
ollama list
```

Run a quick model test:

```bash
ollama run llama3.2
```

Ensure Ollama is running before starting the agent.

## Configuration

The application currently uses the following configuration:

| Parameter | Value |
|---|---|
| LLM provider | Ollama |
| Model | `llama3.2` |
| Temperature | `0.7` |
| API endpoint | `http://localhost:3000/api/deploy` |
| Request timeout | 30 seconds |

Ensure that the backend service is accessible at the configured API endpoint.

## Deployment Tool Parameters

The `call_api` tool accepts four parameters.

| Parameter | Description | Allowed values |
|---|---|---|
| `countries` | Target country codes | `AUS`, `ZAF`, `GBR` |
| `tags` | Deployment version | For example, `v1.2.9` |
| `env` | Target environment | `s1`, `d1`, `p1` |
| `service` | Service to deploy | `mobile-backend`, `catalog`, `sso` |

### Environment mapping

- `s1` — Staging
- `d1` — Development
- `p1` — Production

### Example API payload

```json
{
  "countries": ["AUS", "GBR"],
  "tags": "v1.2.9",
  "env": "s1",
  "service": "catalog"
}
```

The tool sends this payload to the backend API using an HTTP POST request.

## Running the Application

Start the backend API first.

Then activate your virtual environment and run:

```bash
python simple_agent_test.py
```

Enter a natural-language query when prompted.

### Example interactions

**Example 1: Deployment request**

```text
User: Deploy catalog version v1.2.9 to AUS in staging.
```

The agent should identify the deployment parameters and call the `call_api` tool when the request is sufficiently clear and authorized.

**Example 2: Multiple countries**

```text
User: Deploy mobile-backend to AUS and GBR using v2.0.0 in development.
```

The agent should extract the country codes, version tag, environment, and service.

**Example 3: General question**

```text
User: What is your name?
```

The agent should answer conversationally without invoking the deployment API.

**Exit the application:**

```text
exit
```

## Error Handling

The `call_api` tool handles several API errors.

| Error | Behavior |
|---|---|
| Connection error | Returns a message indicating that the API is unreachable |
| Timeout | Returns a request timeout message |
| Other exceptions | Returns an error message |

Check that the backend API and Ollama are running if requests fail.

## Important Notes

1. **Validate deployment inputs.** The tool's docstring describes valid values, but documentation alone does not enforce them. Validate countries, environments, services, and version tags in Python and on the backend.
2. **Protect production deployments.** Require explicit user confirmation and authorization before triggering production changes.
3. **Handle HTTP failures.** Consider using `response.raise_for_status()` so unsuccessful HTTP responses are detected.
4. **Keep configuration external.** Move API URLs and other environment-specific settings into environment variables.
5. **Use appropriate logging.** Avoid logging credentials, tokens, or sensitive deployment information.
6. **Check model compatibility.** Tool calling depends on the Ollama model and its support for tool use.

## Troubleshooting

### Ollama connection error

Check that Ollama is running:

```bash
ollama list
```

If needed, start the Ollama service using the method appropriate for your operating system.

### Model not found

```bash
ollama pull llama3.2
```

Confirm that the model name in your Python code matches the installed model.

### Backend API connection error

Test the endpoint independently:

```bash
curl -X POST http://localhost:3000/api/deploy \
  -H "Content-Type: application/json" \
  -d '{"countries":["AUS"],"tags":"v1.2.9","env":"s1","service":"catalog"}'
```

Run this only when the backend is available and the requested deployment is safe to execute.

### Python module not found

Activate the correct virtual environment and install the dependencies:

```bash
python -m pip install langchain langchain-core langchain-ollama requests
```

## Future Improvements

- Add environment-based configuration.
- Add input validation using Pydantic.
- Add human approval before production deployments.
- Add structured logging and API response validation.
- Expose the agent through a FastAPI endpoint.
- Integrate an MCP server to expose deployment capabilities to other compatible agents.
- Add unit tests using mocked HTTP requests.

## License

Add your preferred license before distributing this project.
