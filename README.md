# NetOps Configuration Validator

A Python-based tool for validating network configuration data and identifying common errors before deployment.

This project demonstrates practical skills in network configuration validation, Python development, automated testing, and continuous integration.

## Features

- **VLAN validation** — validates VLAN IDs within the range 1–4094 and detects duplicates.
- **IP address validation** — validates IPv4 and IPv6 addresses.
- **Device validation** — checks hostnames and management IP addresses.
- **Configuration validation** — detects missing fields and invalid configuration structures.
- **Automated testing** — uses pytest to verify validation logic.
- **Continuous integration** — runs automated tests using GitHub Actions.

## Technologies

- Python
- YAML and PyYAML
- pytest
- Git and GitHub
- GitHub Actions

## Project Structure

```text
netops-platform/
├── configs/
│   └── network.yml
├── src/
│   └── netops/
│       ├── __init__.py
│       ├── config_loader.py
│       └── validator.py
├── tests/
│   └── test_validator.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── TECHNICAL_REPORT.md
├── pyproject.toml
└── README.md
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/mohamednetworks/netops-platform.git
cd netops-platform
```

Create a virtual environment and install the project with its test dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

Run the tests:

```bash
pytest -q
```

## Example Configuration

The project uses YAML to represent VLANs and network devices. For example:

```yaml
vlans:
  - id: 10
    name: MANAGEMENT
  - id: 20
    name: USERS
  - id: 30
    name: SERVERS

devices:
  - hostname: R1
    management_ip: 192.168.1.1
  - hostname: R2
    management_ip: 192.168.1.2
```

The example contains sample configuration data for validation. The tool does not configure live network devices.

## Testing and Continuous Integration

The project includes automated tests with pytest and a GitHub Actions workflow that runs tests when changes are pushed or pull requests are opened or updated.

The initial test suite contained 10 tests, all of which passed in the recorded local run. The published GitHub Actions runs have also completed successfully.

## Current Limitations

The current implementation validates configuration data but does not connect to routers or switches, deploy configurations, or detect overlapping IP subnets.

## Future Improvements

- CIDR and subnet validation
- Detection of overlapping IP networks
- Additional automated tests
- More detailed validation error messages
- Integration with network automation tools

## Technical Documentation

See [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) for more information about the design
