# Technical Report: NetOps Configuration Validator

## 1. Introduction

The NetOps Configuration Validator is a Python-based project designed to validate network configuration data before it is used in a network environment.

Network configuration errors, such as duplicate VLAN IDs, invalid IP addresses, and missing device information, can cause connectivity problems and increase troubleshooting time. This project aims to identify common configuration errors through automated validation.

The project uses Python, YAML, pytest, Git, and GitHub Actions.

## 2. Objectives

The main objectives of the project are to:

- Validate VLAN identifiers and detect duplicate values.
- Validate IPv4 and IPv6 addresses.
- Check network configuration data for missing or invalid fields.
- Detect duplicate device hostnames.
- Automate testing to improve reliability.
- Use version control and continuous integration to support maintainable development.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Implements the validation logic |
| YAML | Stores network configuration data |
| PyYAML | Loads YAML configuration files |
| pytest | Runs automated tests |
| Git | Tracks source code changes |
| GitHub | Hosts the project repository |
| GitHub Actions | Runs automated tests in a CI pipeline |

## 4. System Design and Implementation

The project separates configuration loading, validation logic, and automated tests into different files.

### 4.1 Configuration File

The file `configs/network.yml` contains example network configuration data, including VLAN identifiers, VLAN names, device hostnames, and management IP addresses.

The example configuration defines three VLANs:

- VLAN 10: MANAGEMENT
- VLAN 20: USERS
- VLAN 30: SERVERS

It also defines two example network devices, R1 and R2, with management IP addresses.

These values are sample data used for testing and do not represent a live production network.

### 4.2 Configuration Loader

The module `src/netops/config_loader.py` loads YAML configuration files using PyYAML.

It also checks that the loaded top-level YAML structure is a dictionary. This helps prevent unexpected configuration structures from being processed as valid input.

### 4.3 Validation Logic

The module `src/netops/validator.py` contains the main validation functions.

The implemented checks include:

- VLAN identifiers must be integers within the range 1–4094.
- Duplicate VLAN identifiers are reported.
- Boolean values and other non-integer VLAN identifiers are rejected.
- IPv4 and IPv6 addresses are checked for valid syntax.
- The configuration must contain correctly structured VLAN and device lists.
- VLAN entries must include an identifier and a non-empty name.
- Device entries must include a non-empty hostname and a management IP address.
- Duplicate device hostnames are reported.

The validator reports configuration errors rather than configuring or changing network devices.

## 5. Testing and Results

Automated tests are implemented in `tests/test_validator.py` using pytest.

The test cases cover valid and invalid VLAN identifiers, duplicate values, incorrect data types, IPv4 and IPv6 address validation, and network configuration validation.

The local test command is:

```bash
PYTHONPATH=src pytest -q
```

The recorded local test result was:

```text
10 passed
```

This result indicates that all ten tests passed in the tested local environment at that time.

## 6. Continuous Integration

The project uses GitHub Actions to automate testing when changes are pushed to the repository or when a pull request is opened or updated.

The workflow is defined in `.github/workflows/ci.yml`.

The pipeline checks out the repository, sets up Python 3.12, installs the project and its test dependencies, and runs pytest.

The first recorded GitHub Actions workflow run completed successfully. This confirms that the configured CI pipeline passed for that revision of the project.

## 7. Limitations

The current implementation focuses on validating structured configuration data.

It does not connect to routers or switches, apply configurations to network devices, or verify the live state of a network.

The current validation logic also does not implement subnet overlap detection or comprehensive network design checks.

The results depend on the configuration data provided to the validator and the validation rules implemented in the code.

## 8. Future Improvements

Potential future improvements include:

- Validating subnet masks and CIDR notation.
- Detecting overlapping IP networks.
- Adding more automated tests for malformed and incomplete configuration files.
- Improving error messages to identify the location of invalid configuration data.
- Adding static analysis and code quality checks to the CI pipeline.
- Exploring integration with network automation tools and device APIs.

These improvements would extend the project's validation capabilities and provide a foundation for further network automation work.

## 9. Conclusion

The NetOps Configuration Validator demonstrates how Python can be used to validate structured network configuration data and identify common errors before deployment.

The project combines configuration parsing, input validation, automated testing, version control, and continuous integration in a small, modular software project.

It provides a foundation for future development in network automation and infrastructure validation.

## 10. Repository

GitHub repository: https://github.com/mohamednetworks/netops-platform
