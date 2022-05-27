# Cisco Meraki L3 Rule Deduplicator

![Deduplicator](https://github.com/dirflash/Meraki_L3_Rules/blob/master/images/Deduper.jpg)

## **This Python script:**

1. Connects to a Meraki network
2. Evaluates the current L3 firewall rules
3. Removes duplicate rules
4. Uploads a clean, non-duplicated set up rules.

## What problem is this script trying to solve?

No doubt - The Meraki dashboard is great. However, it is possible to create duplicate L3 firewall rules. Overtime, this can result in an unnecessary amount of unused rules. This script compares the current set of rules, minus the comments, and uploads a clean new set of L3 firewall rules without the duplicates.

**_Before_**
![Duplicate rules](https://github.com/dirflash/Meraki_L3_Rules/blob/master/images/dup_rules_b4.jpg)

**_After_**
![Clean rules](https://github.com/dirflash/Meraki_L3_Rules/blob/master/images/after.JPG)

## Requirements

This script requires a Python environment and the libraries included in the [requirements.txt](https://github.com/dirflash/Meraki_L3_Rules/blob/master/requirements.txt) file.

Import requirements file: `pip install -r requirements.txt`

### Configparser to store and access secrets

All the API keys are stored in a config.ini file using [configparser](https://docs.python.org/3/library/configparser.html). Your config.ini file should look like this:

![Sample config.ini file](https://github.com/dirflash/Meraki_L3_Rules/blob/master/images/config.jpg)

### Project file structure

![This is a sample file structure](https://github.com/dirflash/Meraki_L3_Rules/blob/master/images/file_structure.JPG)

## Usage

```
$  python.exe rule_cleanup.py
```

## How do I get my Meraki API key?

Super easy! You can find the instructions in this [Meraki doc](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API).

## How do I get my Meraki Org ID and Network ID?

Also super easy! You can find the instructions in the [Meraki API documentation](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API).

## Known Issues

None.

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Author(s)

This project was written and is maintained by the following individuals:

- Aaron Davis <aarodavi@cisco.com>
