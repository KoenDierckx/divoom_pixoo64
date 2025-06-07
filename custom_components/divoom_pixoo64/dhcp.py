"""DHCP discovery for Divoom Pixoo devices."""
from __future__ import annotations

from homeassistant.components.dhcp import DhcpServiceInfo
from homeassistant.const import CONF_HOST

# Espressif MAC prefix ranges
ESPRESSIF_MAC_PREFIXES = [
    "18:FE:34",  # Espressif Inc.
    "24:0A:C4",  # Espressif Inc.
    "24:6F:28",  # Espressif Inc.
    "2C:3A:E8",  # Espressif Inc.
    "2C:F4:32",  # Espressif Inc.
    "30:AE:A4",  # Espressif Inc.
    "3C:61:05",  # Espressif Inc.
    "3C:71:BF",  # Espressif Inc.
    "40:91:51",  # Espressif Inc.
    "40:F5:20",  # Espressif Inc.
    "48:27:E2",  # Espressif Inc.
    "48:31:B7",  # Espressif Inc.
    "4C:11:AE",  # Espressif Inc.
    "4C:75:25",  # Espressif Inc.
    "54:43:B2",  # Espressif Inc.
    "5C:CF:7F",  # Espressif Inc.
    "60:01:94",  # Espressif Inc.
    "68:67:25",  # Espressif Inc.
    "68:C6:3A",  # Espressif Inc.
    "70:04:1D",  # Espressif Inc.
    "7C:9E:BD",  # Espressif Inc.
    "7C:DF:A1",  # Espressif Inc.
    "84:0D:8E",  # Espressif Inc.
    "84:CC:A8",  # Espressif Inc.
    "84:F3:EB",  # Espressif Inc.
    "8C:4B:14",  # Espressif Inc.
    "8C:CE:4E",  # Espressif Inc.
    "94:B5:55",  # Espressif Inc.
    "94:B9:7E",  # Espressif Inc.
    "94:E6:86",  # Espressif Inc.
    "98:F4:AB",  # Espressif Inc.
    "A0:20:A6",  # Espressif Inc.
    "A4:7B:9D",  # Espressif Inc.
    "A4:CF:12",  # Espressif Inc.
    "AC:67:B2",  # Espressif Inc.
    "AC:D0:74",  # Espressif Inc.
    "B4:E6:2D",  # Espressif Inc.
    "BC:DD:C2",  # Espressif Inc.
    "BC:FF:4D",  # Espressif Inc.
    "C4:4F:33",  # Espressif Inc.
    "C4:DD:57",  # Espressif Inc.
    "C8:2B:96",  # Espressif Inc.
    "C8:C9:A3",  # Espressif Inc.
    "CC:50:E3",  # Espressif Inc.
    "D4:D4:DA",  # Espressif Inc.
    "D8:96:85",  # Espressif Inc.
    "D8:A0:1D",  # Espressif Inc.
    "DC:4F:22",  # Espressif Inc.
    "DC:54:75",  # Espressif Inc.
    "E0:5A:1B",  # Espressif Inc.
    "E0:E2:E6",  # Espressif Inc.
    "EC:62:60",  # Espressif Inc.
    "EC:FA:BC",  # Espressif Inc.
    "F0:08:D1",  # Espressif Inc.
    "F4:12:FA",  # Espressif Inc.
    "F4:CF:A2",  # Espressif Inc.
]

# Hostname contains pixoo
HOSTNAME_PATTERN = "pixoo"

def match_dhcp_discovery(service_info: DhcpServiceInfo) -> bool:
    """Check if a DHCP service is a Pixoo device."""
    mac_prefix = service_info.macaddress.upper()[:8]
    hostname = service_info.hostname.lower()
    
    # Check if the MAC address prefix matches Espressif and hostname contains pixoo
    if any(mac_prefix.startswith(prefix) for prefix in ESPRESSIF_MAC_PREFIXES) and HOSTNAME_PATTERN in hostname:
        return True
    
    return False
