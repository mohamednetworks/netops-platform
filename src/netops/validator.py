
import ipaddress


def validate_vlan_ids(vlan_ids: list[int]) -> list[str]:
    errors = []
    seen = set()

    for vlan_id in vlan_ids:
        if not isinstance(vlan_id, int) or isinstance(vlan_id, bool):
            errors.append(f"Invalid VLAN ID: {vlan_id}")
            continue

        if not 1 <= vlan_id <= 4094:
            errors.append(f"VLAN ID out of range: {vlan_id}")
            continue

        if vlan_id in seen:
            errors.append(f"Duplicate VLAN ID: {vlan_id}")
        else:
            seen.add(vlan_id)

    return errors


def validate_ip_address(address: str) -> list[str]:
    try:
        ipaddress.ip_address(address)
    except (ValueError, TypeError):
        return [f"Invalid IP address: {address}"]

    return []


def validate_config(config: dict) -> list[str]:
    errors = []

    if not isinstance(config, dict):
        return ["Configuration must be a mapping"]

    vlans = config.get("vlans", [])
    devices = config.get("devices", [])

    if not isinstance(vlans, list):
        errors.append("'vlans' must be a list")
        vlans = []

    if not isinstance(devices, list):
        errors.append("'devices' must be a list")
        devices = []

    vlan_ids = []

    for vlan in vlans:
        if not isinstance(vlan, dict):
            errors.append(f"Invalid VLAN entry: {vlan}")
            continue

        if "id" not in vlan:
            errors.append(f"VLAN is missing an ID: {vlan}")
            continue

        vlan_ids.append(vlan["id"])

        if not isinstance(vlan.get("name"), str) or not vlan["name"].strip():
            errors.append(f"VLAN {vlan['id']} has an invalid name")

    errors.extend(validate_vlan_ids(vlan_ids))

    hostnames = set()

    for device in devices:
        if not isinstance(device, dict):
            errors.append(f"Invalid device entry: {device}")
            continue

        hostname = device.get("hostname")

        if not isinstance(hostname, str) or not hostname.strip():
            errors.append(f"Device has an invalid hostname: {device}")
        elif hostname in hostnames:
            errors.append(f"Duplicate hostname: {hostname}")
        else:
            hostnames.add(hostname)

        if "management_ip" not in device:
            errors.append(f"Device {hostname} is missing a management IP")
        else:
            errors.extend(validate_ip_address(device["management_ip"]))

    subnets = config.get("subnets", [])

    if not isinstance(subnets, list):
        errors.append("'subnets' must be a list")
    else:
        errors.extend(validate_subnet_overlaps(subnets))

    return errors


def validate_subnet_overlaps(subnets: list[str]) -> list[str]:
    errors = []
    networks = []

    for subnet in subnets:
        try:
            network = ipaddress.ip_network(subnet, strict=False)
        except (ValueError, TypeError):
            errors.append(f"Invalid subnet: {subnet}")
            continue

        for existing in networks:
            if (
                network.version == existing.version
                and network.overlaps(existing)
            ):
                errors.append(
                    f"Overlapping subnets: {existing} and {network}"
                )

        networks.append(network)

    return errors

