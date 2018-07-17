#!/usr/bin/env python

import argparse
import os
import re
import sys

try:
    import textfsm
except Exception as e:
    # jtextfsm is a fork that works with Python 3
    import jtextfsm as textfsm


def parseArguments():
    """Parse command-line arguments using argparse"""

    parser = argparse.ArgumentParser(
        description="Guest network IP usage"
    )

    parser.add_argument(
        "-f",
        "--file",
        help="The path to the dhcpd.leases file",
        required=True,
    )

    return parser.parse_args()


def getTextFSMTemplate(config=None):
    if not config:
        raise Exception("The TextFSM config must be specified")

    # If we're passed a fully-qualified path, use it
    if config[0:1] == "/":
        intConfTmpl = config
    else:
        # Figure out the path to the TextFSM template
        pwd = os.path.realpath(os.path.dirname(__file__))
        intConfTmpl = os.path.join(pwd, config)

    # Retrieve the textfsm template
    textfsTmpl = open(intConfTmpl, "r")
    th = textfsm.TextFSM(textfsTmpl)
    textfsTmpl.close()

    return th


def tableToDict(col_names=[], data=[]):
    """Changes a list of lists to a list of dictionaries"""

    ret = []

    for rowidx, row in enumerate(data):
        d = {}
        # Raise an exception if the row is too short
        if len(row) < len(col_names):
            raise Exception("Row %d has more data than expected" % rowidx)
        for idx, c in enumerate(row):
            col = col_names[idx]
            d[col] = c
        ret.append(d)

    return ret


def getDhcpdLeases(filename=None):
    """Retrieves and parses the dhcpd.leases file"""

    if not filename:
        raise Exception("No filename provided")

    if not os.path.isfile(filename):
        raise Exception("Filename '%s' not found" % filename)

    # Retrieve the textfsm template
    tfsmh = getTextFSMTemplate("dhcpd.leases.textfsm")

    fh = open(filename, "r")
    output = fh.read()

    # Parse the data
    fsm_results = tfsmh.ParseText(output)
    data = tableToDict(tfsmh.header, fsm_results)

    return data


def main():
    ips = {}
    states = {
        "abandoned": 0,
        "active": 0,
        "backup": 0,
        "expired": 0,
        "free": 0,
        "released": 0,
    }
    bottomhalf = re.compile(r"^10\.10\.9[6-9]\..*")
    tophalf = re.compile(r"^10\.10\.10[0-3]\..*")

    args = parseArguments()
    data = getDhcpdLeases(filename=args.file)

    for d in data:
        if d["IPAddress"] not in ips:
            ips[d["IPAddress"]] = ""
        ips[d["IPAddress"]] = d["BindingState"]

    for i in ips:
        if bottomhalf.search(i) or tophalf.search(i):
            status = ips[i]
            states[status] += 1

    print(states)


if __name__ == "__main__":
    ret = main()

    sys.exit(ret)
