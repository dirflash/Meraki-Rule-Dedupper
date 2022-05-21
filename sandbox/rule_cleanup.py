import configparser
import logging
from rich import print, box  # pylint: disable=redefined-builtin, unused-import
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
import requests

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

log = logging.getLogger("rich")


config = configparser.ConfigParser()
config.read("config.ini")
meraki_api_key = config["DEFAULT"]["meraki_api_key"]
net_id = config["DEFAULT"]["net_id"]

get_url = f"https://api.meraki.com/api/v1/networks/{net_id}/appliance/firewall/l3FirewallRules"
get_payload = {}
get_headers = {"X-Cisco-Meraki-API-Key": meraki_api_key}
response = requests.request("GET", get_url, headers=get_headers, data=get_payload)
data = response.json()

response = requests.request("GET", get_url, headers=get_headers, data=get_payload)

data = response.json()
l3_rules = data["rules"]
table_before = Table(title="L3 Firewall Rules Before")
FIRST_LOOP = True
rules = []
b4_compare = []
DUP = ""

for x in l3_rules:
    entry = l3_rules.index(x)
    comment = x["comment"]
    policy = x["policy"]
    protocol = x["protocol"]
    srcPort = x["srcPort"]
    srcCidr = x["srcCidr"]
    destPort = x["destPort"]
    destCidr = x["destCidr"]
    syslogEnabled = x["syslogEnabled"]

    ENTRY = [
        policy,
        protocol,
        srcPort,
        srcCidr,
        destPort,
        destCidr,
        syslogEnabled,
    ]

    if FIRST_LOOP is True:
        rules.append(entry)
        b4_compare.append(ENTRY)
        table_before.add_column("Rule", style="red")
        table_before.add_column("Comment", style="red", no_wrap=True)
        table_before.add_column("Policy", style="red")
        table_before.add_column("Protocol", style="red")
        table_before.add_column("Src Port", style="red")
        table_before.add_column("Src CIDR", style="red")
        table_before.add_column("Dest Port", style="red")
        table_before.add_column("Dest CIDR", style="red")
        table_before.add_column("SYSLOG", style="red")
        table_before.add_column("Dup Rule", style="red")
    else:
        if entry in rules:
            DUP = True
        else:
            rules.append(entry)
            b4_compare.append(ENTRY)
            DUP = ""

    table_before.add_row(
        str(entry),
        comment,
        policy,
        protocol,
        srcPort,
        srcCidr,
        destPort,
        destCidr,
        str(syslogEnabled),
        str(DUP),
    )
    FIRST_LOOP = False

console.log("[yellow]Delete 'Default rule'.")
rules.pop(-1)
b4_compare.pop(-1)

if len(rules) != len(b4_compare):
    console.log(
        "[bold red blink]TEST FAILED: (rules) and (b4_compare) length mismatch.[/]"
    )
else:
    console.log("[bold green]TEST PASSED: (rules) and (b4_compare) length match.[/]")

console.log(
    "[yellow]Ready for compare rules without 'Comment' to remove remaining duplicates.[/]"
)

console.log("[yellow]Combine rules into dictionary for compare.[/]")

RULE_CNT = len(rules)
console.log(
    f"[purple]There are {RULE_CNT} unique rules in the "
    f"{len(l3_rules)} total rules using native detection.[/]"
)

console.log("[yellow]Checking rules again, minus the comments.[/]")

EVAL_SAMPLE = []
for i in range(RULE_CNT):
    EVAL_SAMPLE.append("rule_dict" + str(i))

EVAL_KEYS = [
    "policy",
    "protocol",
    "srcPort",
    "srcCidr",
    "destPort",
    "destCidr",
    "syslogEnabled",
]

for y in range(RULE_CNT):
    EVAL_SAMPLE[y] = {}
    for x in range(len(EVAL_KEYS)):
        EVAL_SAMPLE[y].update({EVAL_KEYS[x]: b4_compare[y][x]})

SAMPLE_LEN = len(EVAL_SAMPLE)

console.log(f"[purple]Before evaluation, there are {SAMPLE_LEN} rules.[/]")

EVAL_RESULT = []
for i in range(SAMPLE_LEN):
    if EVAL_SAMPLE[i] not in EVAL_SAMPLE[i + 1 :]:
        EVAL_RESULT.append(EVAL_SAMPLE[i])

RESULT_LEN = len(EVAL_RESULT)

console.log(f"[purple]After evaluation, that are {RESULT_LEN} rules.[/]")
console.log(f"[red bold]Deleted {SAMPLE_LEN - RESULT_LEN} additional rules.[/]")
console.log("[orange1]Clean-up complete. Updating L3 firewall rules.[/]\n")

table_after = Table(title="L3 Firewall Rules After")

table_after.add_column("Rule", style="red")
table_after.add_column("Policy", style="red")
table_after.add_column("Protocol", style="red")
table_after.add_column("Src Port", style="red")
table_after.add_column("Src CIDR", style="red")
table_after.add_column("Dest Port", style="red")
table_after.add_column("Dest CIDR", style="red")
table_after.add_column("SYSLOG", style="red")

for rule in EVAL_RESULT:

    exit_entry = EVAL_RESULT.index(rule)
    exit_policy = rule["policy"]
    exit_protocol = rule["protocol"]
    exit_srcPort = rule["srcPort"]
    exit_srcCidr = rule["srcCidr"]
    exit_destPort = rule["destPort"]
    exit_destCidr = rule["destCidr"]
    exit_syslogEnabled = rule["syslogEnabled"]

    EXIT = [
        exit_policy,
        exit_protocol,
        exit_srcPort,
        exit_srcCidr,
        exit_destPort,
        exit_destCidr,
        exit_syslogEnabled,
    ]

    EXIT_COMMENT = "---"

    table_after.add_row(
        str(exit_entry),
        str(EXIT_COMMENT),
        exit_policy,
        exit_protocol,
        exit_srcPort,
        exit_srcCidr,
        exit_destPort,
        exit_destCidr,
        str(exit_syslogEnabled),
    )

console.print(table_before)
print("\n")
console.print(table_after)

console.log(
    "[bright_cyan]Default rule will be automatically added by Meraki API at upload.[/]"
)

console.log("\n[bright_green]Ready to POST updated ruleset to the Meraki network.[/]")
