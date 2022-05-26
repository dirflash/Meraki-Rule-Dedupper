#!/usr/bin/env python3
"""This is a very rough script that adds a static layer 3 firewall rule to a Meraki MX security appliance."""

__author__ = "Aaron Davis"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2022 Aaron Davis"
__license__ = "MIT License"

import configparser
import json
from rich import print, box  # pylint: disable=redefined-builtin, unused-import
from rich.console import Console
from rich.table import Table
import requests

if __name__ == "__main__":
    console = Console()
    config = configparser.ConfigParser()
    config.read("config.ini")
    meraki_api_key = config["DEFAULT"]["meraki_api_key"]
    net_id = config["DEFAULT"]["net_id"]

    get_url = f"https://api.meraki.com/api/v1/networks/{net_id}/appliance/firewall/l3FirewallRules"
    get_payload = {}
    get_headers = {"X-Cisco-Meraki-API-Key": meraki_api_key}
    response = requests.request("GET", get_url, headers=get_headers, data=get_payload)
    data = response.json()

    SYS_ENABLE = bool(False)

    new_rule = dict(
        {
            "comment": "NEW RULE COMMENT ADDED BY PYTHON",
            "policy": "deny",
            "protocol": "Any",
            "srcPort": "Any",
            "srcCidr": "Any",
            "dstPort": "Any",
            "destCidr": "2.2.2.2/32",
            "syslogEnabled": SYS_ENABLE,
        }
    )

    data["rules"].pop(-1)
    data["rules"].append(new_rule)

    put_url = f"https://api.meraki.com/api/v1/networks/{net_id}/appliance/firewall/l3FirewallRules"
    put_payload = json.dumps(data)
    put_headers = {
        "X-Cisco-Meraki-API-Key": meraki_api_key,
        "Content-Type": "application/json",
    }

    response = requests.request("PUT", put_url, headers=put_headers, data=put_payload)
    print(f"Response status code: {response.status_code}")

    response = requests.request("GET", get_url, headers=get_headers, data=get_payload)

    data = response.json()
    table = Table(title="L3 Firewall Rules")
    FIRST_LOOP = True

    for x in data["rules"]:
        entry = data["rules"].index(x)
        comment = x["comment"]
        policy = x["policy"]
        protocol = x["protocol"]
        srcPort = x["srcPort"]
        srcCidr = x["srcCidr"]
        destPort = x["destPort"]
        destCidr = x["destCidr"]
        syslogEnabled = x["syslogEnabled"]

        if FIRST_LOOP is True:
            table.add_column("Rule", style="red")
            table.add_column("Comment", style="red", no_wrap=True)
            table.add_column("Policy", style="red")
            table.add_column("Protocol", style="red")
            table.add_column("Src Port", style="red")
            table.add_column("Src CIDR", style="red")
            table.add_column("Dest Port", style="red")
            table.add_column("Dest CIDR", style="red")
            table.add_column("SYSLOG", style="red")
            table.add_column("Dup Rule", style="red")

        table.add_row(
            str(entry),
            comment,
            policy,
            protocol,
            srcPort,
            srcCidr,
            destPort,
            destCidr,
            str(syslogEnabled),
        )
        FIRST_LOOP = False

    console.print(table)
