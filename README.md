# README
XXX description


## Use case
You are running a GCP workshop, training course, sandbox, hackathon... and you need to create several individual projects for participants.

Those project need IAM roles for participants, APIs enabled by default, billing enabled, etc., and most importantly, maybe multiple resources already created following a template.


## Usage
1. Pulumi set up instructions: https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started
1. Setup Pulumi passphrase: `export PULUMI_CONFIG_PASSPHRASE=passphrase && echo $PULUMI_CONFIG_PASSPHRASE`
1. Setup GCP authn for Pulumi CLI: `gcloud auth application-default login`
    1. Or use another gcloud CLI installation to create credentials file with said command
    1. Store output in local `credentials.json`
    1. Use its path for envvar: `export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json`, e.g. `export GOOGLE_APPLICATION_CREDENTIALS=$(readlink -f credentials.json) && echo $GOOGLE_APPLICATION_CREDENTIALS`
1. Include config in `Pulumi.STACK_NAME.yaml`:
    1. List of emails for access control to projects, with first email for the instructor
    1. List of roles to be assigned to emails
    1. List of APIs to be enabled in projects
    1. IDs for organization & billing account, folder name & display name
    1. Project prefix and random suffix, e.g. Project IDs created `PROJECT_PREFIX-0-PROJECT_RANDOM_SUFFIX`
    1. Example file in `example-Pulumi.prod-yaml`
1. Include IaC for creating template GCP resources in `resources.py` inside `create_resources` function, along Pulumi exports


## Requirements
Check `requirements.txt`.

- [Pulumi](https://www.pulumi.com/docs/) for Python v3
- Provider: [Google Cloud (GCP) Classic](https://www.pulumi.com/registry/packages/gcp/) v7


## TODOs
1. LICENSE file
1. Substitute infra importing method for: [https://github.com/pulumi/examples/tree/74db62a03d013c2854d2cf933c074ea0a3bbf69d/testing-unit-py]
1. Have a different resources file for each stack and import it programmatically: [https://stackoverflow.com/questions/301134/how-can-i-import-a-module-dynamically-given-its-name-as-string]
1. Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
1. Update quotas
