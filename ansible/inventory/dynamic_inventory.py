#!/usr/bin/env python3

import json
import subprocess

try:
    ip = subprocess.check_output(
        ["terraform", "output", "-raw", "minikube_public_ip"],
        cwd="../../infra"
    ).decode("utf-8").strip()

    inventory = {
        "minikube": {
            "hosts": [ip]
        },
        "_meta": {
            "hostvars": {
                ip: {
                    "ansible_user": "ubuntu"
                }
            }
        }
    }

    print(json.dumps(inventory))

except Exception as e:
    print(json.dumps({}))
