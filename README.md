# README
Demo project and how-to guide to use Pulumi as an IaC (Infrastructure as Code) tool for creating GCP sandbox projects with starting resources for demos, workshops, trainings, etc.

Learn more about the OSS Pulumi project: https://www.pulumi.com


## Use case
You are running a GCP workshop, training course, sandbox, hackathon... and you need to create several individual projects for participants.

Those project need IAM roles for participants, APIs enabled by default, billing enabled, etc., and most importantly, maybe multiple resources already created following a template.


## Usage
1. Follow Pulumi set up instructions: https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started
    1. You can use the course name/ID for the Pulumi stack name
1. You can setup Pulumi passphrase so you don't have to input it every time: `export PULUMI_CONFIG_PASSPHRASE=passphrase && echo $PULUMI_CONFIG_PASSPHRASE`
1. Setup GCP authn for Pulumi CLI: `gcloud auth application-default login`
    1. You need Cloud SDK installed locally (or use Cloud Shell)
    1. Or use another gcloud CLI installation to create credentials file with said command
    1. In the command output, check the path to the JSON file where the credentials are stored and move it to a known path, e.g. `credentials.json`
    1. Use its path for envvar and check its content: `export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json`, e.g. `export GOOGLE_APPLICATION_CREDENTIALS=$(readlink -f credentials.json)`, `echo $GOOGLE_APPLICATION_CREDENTIALS`
1. Include config in `Pulumi.STACK_NAME.yaml`:
    1. List of emails for access control to projects, with first email for the instructor
    1. List of roles to be assigned to emails
    1. List of APIs to be enabled in projects
    1. IDs for organization & billing account, folder name & display name
    1. Project prefix and random suffix, e.g. Project IDs created `PROJECT_PREFIX-0-PROJECT_RANDOM_SUFFIX`
    1. Example file in `example-Pulumi.prod-yaml`
1. Include IaC for creating template GCP resources in `resources.py` inside `create_resources` function, along Pulumi exports
1. Create resources with Pulumi CLI: `pulumi up`


## Multiple courses
You can store multiple courses using multiple [Pulumi stacks](https://www.pulumi.com/docs/concepts/stack/).

Each stack will have its own config & secrets files, e.g. `Pulumi.STACK_COURSE_NAME.yaml`, where you can store its config and template GCP resources.

Each stack will also have its own state for managing GCP resources.

You can manage stacks with `pulumi stack` ([docs](https://www.pulumi.com/docs/cli/commands/pulumi_stack/)):
- Create: `pulumi stack init`
- List: `pulumi stack ls`
- Switch: `pulumi stack select`
- Remove: `pulumi stack rm`

## Requirements
Check `requirements.txt`.

- [Pulumi](https://www.pulumi.com/docs/) for Python v3
- Pulumi provider: [Google Cloud (GCP) Classic](https://www.pulumi.com/registry/packages/gcp/) v7


## TODOs
1. Include infra file in stack config yaml, for supporting multiple stacks
1. LICENSE file
1. Substitute infra importing method for: [https://github.com/pulumi/examples/tree/74db62a03d013c2854d2cf933c074ea0a3bbf69d/testing-unit-py]
1. Have a different resources file for each stack and import it programmatically: [https://stackoverflow.com/questions/301134/how-can-i-import-a-module-dynamically-given-its-name-as-string]
1. Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
1. Update quotas
1. How to share project templates
1. CONTRIBUTION file
1. maintainer info
1. Info for registering issues
