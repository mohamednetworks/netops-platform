
from netops.validator import (
    validate_vlan_ids,
    validate_ip_address,
    validate_config,
    validate_subnet_overlaps,
)


def test_valid_vlan_ids():
    assert validate_vlan_ids([10, 20, 30]) == []


def test_vlan_id_out_of_range():
    errors = validate_vlan_ids([0, 4095])
    assert len(errors) == 2


def test_duplicate_vlan_ids():
    errors = validate_vlan_ids([10, 10])
    assert len(errors) == 1
    assert "Duplicate VLAN ID" in errors[0]


def test_vlan_id_as_text():
    errors = validate_vlan_ids(["abc"])
    assert len(errors) == 1
    assert "Invalid VLAN ID" in errors[0]


def test_vlan_id_boolean_rejected():
    errors = validate_vlan_ids([True])
    assert len(errors) == 1


def test_valid_ipv4_address():
    assert validate_ip_address("192.168.1.1") == []


def test_invalid_ip_address():
    errors = validate_ip_address("999.999.1.1")
    assert len(errors) == 1


def test_valid_ipv6_address():
    assert validate_ip_address("2001:db8::1") == []


def test_valid_network_config():
    config = {
        "vlans": [
            {"id": 10, "name": "MANAGEMENT"},
            {"id": 20, "name": "USERS"},
        ],
        "devices": [
            {"hostname": "R1", "management_ip": "192.168.1.1"},
        ],
    }
    assert validate_config(config) == []

def test_invalid_network_config():
    config = {
        "vlans": [
            {"id": 5000, "name": "INVALID"},
            {"id": 10, "name": "USERS"},
            {"id": 10, "name": "DUPLICATE"},
        ],
        "devices": [
            {"hostname": "R1", "management_ip": "999.999.1.1"},
        ],
    }
    errors = validate_config(config)
    assert any("out of range" in error for error in errors)
    assert any("Duplicate VLAN ID" in error for error in errors)
    assert any("Invalid IP address" in error for error in errors)


def test_overlapping_subnets():
    errors = validate_subnet_overlaps([
        "192.168.1.0/24",
        "192.168.1.128/25",
    ])
    assert len(errors) == 1


def test_non_overlapping_subnets():
    errors = validate_subnet_overlaps([
        "192.168.1.0/24",
        "192.168.2.0/24",
    ])
    assert errors == []


def test_invalid_subnet():
    errors = validate_subnet_overlaps(["not-a-subnet"])
    assert len(errors) == 1
    assert "Invalid subnet" in errors[0]
