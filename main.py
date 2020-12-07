"""
* FILE: main.py
* PROJECT: Revoke a certificate in KF
* PURPOSE: Use Python requests library and data as arguments to revoke a certificate in Keyfactor
* AUTHOR: Hayden Roszell
* HISTORY: Version 1.0 12/3/2020
*
* Copyright © 2020 Keyfactor. All rights reserved.
"""

import datetime
import json
import sys
import requests


class Config:
    def __init__(self):
        self.revoke_data = {}
        self.revoke_data_lst = []
        with open("config.json", 'r') as datafile:
            self.serial = json.load(datafile)  # open configuration file
        for i in range(len(sys.argv) - 1):
            self.revoke_data_lst.append(sys.argv[i + 1])  # read in script arguments
        self.script_args = ["CertificateID", "Reason", "Comment"]  # define arguments for dict
        self.zipped_cert_data = zip(self.script_args, self.revoke_data_lst)  # create iterator of tuples
        for field, data in self.zipped_cert_data:
            self.revoke_data[field] = data  # create dict of arguments


class Output:
    def __init__(self):
        self.output_text = str
        self.log_file = "log.txt"
        self.output_file = "output.txt"
        self.timestamp = str
        self.get_timestamp()

    def get_timestamp(self):
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    def write_to_file(self, option):
        timestamp = str(self.timestamp) + ": "
        if option == 1:
            write = timestamp + str(self.output_text)
            f = open(self.log_file, 'a')
        else:
            write = str(self.output_text)
            f = open(self.output_file, 'a')
        f.write(write + '\n')
        f.close()
        return

    def evaluate(self, r):
        if r.status_code == 204:
            self.output_text = "API call succeeded with status code " + str(r.status_code) + " OK"
            self.write_to_file(1)
            print(self.output_text)
        else:
            self.output_text = "API call failed with status code " + str(r.status_code)
            self.write_to_file(1)
            sys.exit(9)


def revoke_cert(output):
    config = Config()
    headers = {'authorization': config.serial["Auth"]["APIAuthorization"], 'Content-Type': 'application/json',
               'Accept': 'application/json',
               'x-keyfactor-requested-with': 'APIClient'}
    output.get_timestamp()
    body = {
        "CertificateIds": [
            config.revoke_data["CertificateID"]
        ],
        "Reason": config.revoke_data["Reason"],
        "Comment": config.revoke_data["Comment"],
        "EffectiveDate": output.timestamp
    }
    r = requests.post(config.serial["URL"]["RevokeCertURL"], headers=headers, json=body)
    output.evaluate(r)
    return


def main():
    output = Output()
    revoke_cert(output)

    return 0


main()
