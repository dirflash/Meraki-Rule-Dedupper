# Cisco Meraki L3 Rule Clean Up

## **This Python script:**

1. connects to a Meraki network
2. evaluates the current L3 firewall rules
3. removes duplicate rules
4. uploads a clean, non-duplicated set up rules.

## What problem is this script trying to solve?

No doubt - The Meraki dashboard is great. However, it is possible to create duplicate L3 firewall rules. Overtime, this can result in an unnecessary amount of unused rules. This script compares the current set of rules, minus the comments, and uploads a clean new set of L3 firewall rules without the duplicates.

## Requirements

This script requires a Python environment and the libraries included in the [requirements.txt](https://github.com/dirflash/Meraki_L3_Rules/blob/master/requirements.txt) file.

Import requirements file: `pip install -r requirements.txt`

### Configparser to store and access secrets

All the API keys are stored in a config.ini file using [configparser](https://docs.python.org/3/library/configparser.html). Your config.ini file should look like this:

![Sample config.ini file](https://github.com/dirflash/psirt/blob/master/images/config.jpg)

### Project file structure

![This is a sample file structure](https://github.com/dirflash/psirt/blob/master/images/file_structure.jpg)
