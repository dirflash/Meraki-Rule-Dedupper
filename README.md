# Cisco Meraki L3 Rule Clean Up

**This Python script:**

1. connects to a Meraki network
2. evaluates the current L3 firewall rules
3. removes duplicate rules
4. uploads a clean, non-duplicated set up rules.

## What problem is this script trying to solve?

No doubt - The Meraki dashboard is great. However, it is possible to create duplicate L3 firewall rules. Overtime, this can result in an unnecessary amount of unused rules. This script compares the current set of rules, minus the comments, and uploads a clean new set of L3 firewall rules without the duplicates.

## Requirements

This script requires a Python environment and the libraries included in the [requirements.txt]() file.
