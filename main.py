import datetime
import json
import sys
import requests


class Config:  # Configuration class to obtain argument and JSON data
    def __init__(self):
        self.revoke_data = {}
        with open("config.json", 'r') as datafile:
            self.settings = json.load(datafile)  # open config JSON file and serialize into dict

        self.read_arguments()

    def read_arguments(self):  # Function to read script arguments and build dictionary
        script_fields = ["CertificateID", "Reason", "Comment"]  # define arguments for dict
        cert_data_lst = sys.argv[1:]
        self.revoke_data = dict(zip(script_fields, cert_data_lst))  # build dictionary of fields and arguments


def evaluate(r):  # Function to evaluate status code of API response
    if r.status_code == 204:  # API response code 204 = success
        log_text = "API call succeeded with status code " + str(r.status_code) + " OK"
        write_to_log(log_text)
    else:
        log_text = "API call failed with status code " + str(r.status_code)
        write_to_log(log_text)
        sys.exit(r.status_code)  # API failure exits script with status code


def write_to_log(text):  # Function to write output text to log file
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    with open("log.txt", 'a') as log:
        log.write(str(timestamp + text) + '\n')


def revoke_cert():
    config = Config()
    headers = {'authorization': config.settings["Auth"]["APIAuthorization"], 'Content-Type': 'application/json',
               'Accept': 'application/json',
               'x-keyfactor-requested-with': 'APIClient'}
    body = {
        "CertificateIds": [
            config.revoke_data["CertificateID"]
        ],
        "Reason": config.revoke_data["Reason"],
        "Comment": config.revoke_data["Comment"],
        "EffectiveDate": datetime.datetime.utcnow().isoformat() + "Z"
    }
    r = requests.post(config.settings["URL"]["RevokeCertURL"], headers=headers, json=body)
    evaluate(r)
    print("Certificate with ID ", config.revoke_data["CertificateID"], " has been revoked")
    return


def main():
    revoke_cert()

    return 0


main()
