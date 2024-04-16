# README
XXX description

## Instructions
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

## TODOs
1. LICENSE file
1. Testing
1. Import APIs, IAM roles, resources in projects, etc., from another file
