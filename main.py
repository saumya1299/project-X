import yaml
import requests
import time
import logging
from collections import defaultdict
from urllib.parse import urlparse
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks with response time logic
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body)
        duration_ms = (time.time() - start_time) * 1000  # Convert to ms

        if 200 <= response.status_code < 300 and duration_ms <= 500:
            return "UP", duration_ms
        else:
            return "DOWN", duration_ms
    except requests.RequestException as e:
        logging.warning(f"Request failed for {url}: {e}")
        return "DOWN", None

# Main function to monitor endpoints and print availability
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            parsed_url = urlparse(endpoint["url"])
            domain = parsed_url.hostname
            result, duration_ms = check_health(endpoint)

            logging.info(f"Checking {endpoint['url']}...")
            if result == "UP":
                logging.info(f"{endpoint['url']} is UP (Response Time: {duration_ms:.2f}ms)")
            elif duration_ms is not None:
                logging.info(f"{endpoint['url']} is DOWN (Response Time: {duration_ms:.2f}ms)")
            else:
                logging.info(f"{endpoint['url']} is DOWN (Request failed)")

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Enhanced Summary Output
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary_lines = [
            "\n" + "=" * 60,
            f"Availability Summary @ {timestamp}",
            "-" * 60,
            f"{'Domain'.ljust(60)} | Availability",
            "-" * 60
        ]

        for domain, stats in domain_stats.items():
            availability = int(100 * stats["up"] / stats["total"])
            summary_lines.append(f"{domain.ljust(60)} | {availability}%")

        summary_lines.append("=" * 60 + "\n")

        for line in summary_lines:
            logging.info(line)

        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logging.error("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
