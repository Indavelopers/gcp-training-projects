# README
Demo project and how-to guide to use Pulumi as an IaC (Infrastructure as Code) tool for creating GCP sandbox projects with starting resources for demos, workshops, trainings, etc.

Learn more about the OSS Pulumi project: https://www.pulumi.com

Contact maintainer:
- Marcos Manuel Ortega: info@indavelopers.com
- LinkedIn: https://www.linkedin.com/in/marcosmanuelortega


## Use case
You are running a GCP workshop, training course, sandbox, hackathon... and you need to create several individual projects for participants.

Those project need IAM roles for participants, APIs enabled by default, billing enabled, etc., and most importantly, maybe multiple resources already created following a template.

You don't want to setup each project manually, then setting up every needed resources and config in each project...

You would like to have a template for creating projects automatically, repeating every time the environments are needed, and even collaborate sharing the project templates.


## Usage
1. Clone repo and setup as working dir: `git clone REPO_URL`, `cd gcp-training-projects`
1. Install Pulumi CLI (read below first): https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started, `curl -fsSL https://get.pulumi.com/ | sh`
    1. You can login to Pulumi or manage stack states locally:
        1. State file in `$HOME/.pulumi`: `pulumi login --local` (alias for `pulumi login file://~`)
        1. State file in another location: `pulumi login file://path/to/pulumi-state`
    1. If you want to use the code in this repo, don't create a new Pulumi project, as will rewrite `__main__.py` file
1. You can setup Pulumi passphrase so you don't have to input it every time: `export PULUMI_CONFIG_PASSPHRASE=passphrase && echo $PULUMI_CONFIG_PASSPHRASE`
1. Setup GCP authn for Pulumi CLI: `gcloud auth application-default login`
    1. You need Cloud SDK installed locally (or use Cloud Shell)
    1. Or use another gcloud CLI installation to create credentials file with said command
    1. In the command output, check the path to the JSON file where the credentials are stored and move it to a known path, e.g. `credentials.json`
    1. Use its path for envvar and check its content: `export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json && echo $GOOGLE_APPLICATION_CREDENTIALS`, e.g. `export GOOGLE_APPLICATION_CREDENTIALS=$(readlink -f credentials.json) && echo $GOOGLE_APPLICATION_CREDENTIALS`
1. Work under `stacks` dir: `cd stacks`
1. Create a new Pulumi stack. You can use the course name/ID for the Pulumi stack name: `pulumi stack init`
1. Include config in `Pulumi.STACK_NAME.yaml`. Requires:
    1. List of emails for access control to projects, with first email for the instructor
    1. List of roles to be assigned to emails
    1. List of APIs to be enabled in projects
    1. IDs for organization & billing account, folder name & display name
    1. Project prefix and random suffix, e.g. Project IDs created `PROJECT_PREFIX-0-PROJECT_RANDOM_SUFFIX`
    1. Name of the infrastructure resources script to be imported:
        1. For clarity, you can use `STACK_NAME_infra`, but it's not enforced - i.e. script for this how-to guide is `gcp_course_infra`
        1. Don't add `.py` as it's the name of the Python module script
        1. Example file in `example-Pulumi.stack_name-yaml`
    1. As we're creating a GCP folder and projects, Pulumi config `gcp:project` is not used, so can be setup as any valid GCP project ID
1. Include IaC for creating template GCP resources in `STACK_NAME_infra.py`, along Pulumi exports
1. Create resources with Pulumi CLI: `pulumi up`
    

## Multiple courses
You can store multiple courses using multiple [Pulumi stacks](https://www.pulumi.com/docs/concepts/stack/).

Each stack will also have its own state for managing GCP resources.

You can manage stacks with `pulumi stack` ([docs](https://www.pulumi.com/docs/cli/commands/pulumi_stack/)):
- Create: `pulumi stack init`
- List: `pulumi stack ls`
- Choose current stack: `pulumi stack select`
- Remove: `pulumi stack rm`

Each stack will have its own config & secrets files, e.g. `Pulumi.STACK_COURSE_NAME.yaml`, where you can store its config and reference the template GCP resources file, which you can modify to follow the `example-Pulumi.gcp_course-yaml` example config file.


## Requirements
Check `requirements.txt`.

- [Pulumi](https://www.pulumi.com/docs/) for Python v3
- Pulumi provider: [Google Cloud (GCP) Classic](https://www.pulumi.com/registry/packages/gcp/) v7


## License
GNU GPLv3


## Known issues and contribution
Tested at the time of last commit.

- When reducing the email student list and updating the stack (with `pulumi up`), last student projecs are deleted, instead of the leaving student's projects
    - Workaround: please maintain students email although they leave till deleting every project
    - No issue when adding new students, and therefore projects

If you find any issues, please open a GitHub issue before (optionally) opening a PR to fix it, or contact the maintainer directly any way.


## TODOs
- Enable APIs
- Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
- Update quotas
- How to share project templates
- When deleting emails from email list, just delete the project related to the student and not the last project -- so project ids need to be related to a specific email, and not be monotonically increasing
- How-to guide to destroy resources
- How-to guide to import resources like projects, or refresh state/stack -- you don't have to include the code to create the resource, as the repo code will define/create it
