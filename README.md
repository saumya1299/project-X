# Exercise

This project is a Python-based endpoint monitoring tool designed for evaluating the availability percentage of HTTP endpoints, based on:

- HTTP **status codes** (`200-299`)
- HTTP **response time**(must be`less than 500ms`)

This script evaluates the health of endpoints using a YAML configuration file which runs every **15 seconds** and tracks cumulative availability by **domain name** (ignoring ports).

---

## Directory Structure

```
.
├── main.py           # Monitoring script
├── sample.yaml       # Sample configuration file (endpoints to monitor)
├── requirements.txt  # Required Python packages
└── README.md         # You're reading it!
```

---


## Setup Instructions

1. Clone this repository:
   ```bash
   git clone git@github.com:saumya1299/project-X.git
   cd project-X
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   - This creates an isolated Python Environment that avoid conflicts with your system packages.

3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

4. Run the script:
   ```bash
   python main.py sample.yaml
   ```
   - Press `Ctrl + C` anytime to stop monitoring.

5. Sample output:
 ```bash
   2025-04-16 19:55:29,050 - INFO - Checking https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body...
   2025-04-16 19:55:29,051 - INFO - https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body is DOWN (Response Time: 399.85ms)
   2025-04-16 19:55:29,132 - INFO - Checking https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/...
   2025-04-16 19:55:29,132 - INFO - https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/ is UP (Response Time: 81.09ms)
   2025-04-16 19:55:29,218 - INFO - Checking https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body...
   2025-04-16 19:55:29,219 - INFO - https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body is DOWN (Response Time: 86.31ms)
   2025-04-16 19:55:30,171 - INFO - Checking https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/error...
   2025-04-16 19:55:30,172 - INFO - https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/error is DOWN (Response Time: 951.91ms)
   2025-04-16 19:55:30,172 - INFO - 
   ============================================================
   2025-04-16 19:55:30,172 - INFO - Availability Summary @ 2025-04-16 19:55:30
   2025-04-16 19:55:30,172 - INFO - ------------------------------------------------------------
   2025-04-16 19:55:30,172 - INFO - Domain                                                       | Availability
   2025-04-16 19:55:30,172 - INFO - ------------------------------------------------------------
   2025-04-16 19:55:30,172 - INFO - dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com | 25%
   2025-04-16 19:55:30,172 - INFO - ============================================================
 ```

---

## YAML Configuration Format

Each entry in the config file should follow this structure:

```yaml
- name: sample name
  url: https://your-api.com/endpoint
  method: GET  # Optional, defaults to GET
  headers:
    Authorization: Bearer <token>  # Optional
  body: '{"key": "value"}'  # Optional
```
Supported fields:
- `name`: Human-readable label (required)
- `url`: Full endpoint URL (required)
- `method`: HTTP method (`GET`, `POST`, etc.) — defaults to `GET` if not given
- `headers`: Optional dictionary of headers
- `body`: Optional JSON string — only sent if provided
---

##  Requirements Met

- Accept YAML configuration via command-line
- Parse fields: `url`, `method`, `headers`, `body`
- Make HTTP requests with proper method and payload
- Consider endpoint "UP" only if:
  - Response code is 2xx
  - Response time is ≤ 500ms
- Aggregate availability **by domain** (ignoring ports)
- Log results every **15 seconds**
- Output clear **structured summary**
- Use Python logging instead of print

---

## 🔧 Improvements Made

| Area               | Change                                                                 |
|--------------------|------------------------------------------------------------------------|
| YAML Parsing       | Used `pyyaml` to load endpoint config                                  |
| HTTP Requests      | Added time tracking to calculate response time in milliseconds         |
| Domain Parsing     | Replaced string slicing with `urllib.parse.urlparse()`                 |
| Logging            | Used Python `logging` for structured logs with timestamps              |
| Summary Formatting | Added clean availability summary with timestamp per cycle              |
| Error Handling     | Gracefully handle connection errors and log warnings                   |

---

## 🚀 Future Improvements

- Add Slack integration using an incoming webhook for real-time critical alerts.
- Highlight endpoint latency with color-coded output (green for UP, red for DOWN).
- Send email notifications using SMTP when availability drops critically.
- Implement a dry-run mode to validate YAML structure without sending requests.
- Dockerize the project to run it anywhere as a portable container.

---

## ✨ Notes

> Final availability is logged as an integer (decimal dropped), and logs are output every 15 seconds regardless of request load.