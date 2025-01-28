# README

Demo project and how-to guide to use Pulumi as an IaC (Infrastructure as Code) tool for creating GCP sandbox projects with starting resources for demos, workshops, trainings, etc.

Learn more about the OSS Pulumi project: [www.pulumi.com](https://www.pulumi.com)

Contact maintainer:

- Marcos Manuel Ortega: <info@indavelopers.com>
- LinkedIn: [Marcos Manuel Ortega](https://www.linkedin.com/in/marcosmanuelortega)

## Use case

You are running a GCP workshop, training course, sandbox, hackathon... and you need to create several individual projects for participants.

Those project need IAM roles for participants, APIs enabled by default, billing enabled, etc., and most importantly, maybe multiple resources already created following a template.

You don't want to setup each all of that for each user and project manually, then doing it all over again for each event, forgetting to setup something, fixing errors during the event...

You would prefer to have a template for creating projects automatically, just reusing it every time new environments are needed, and even collaborate sharing project templates.

## Usage

1. Clone repo and setup as working dir: `git clone REPO_URL`, `cd gcp-training-projects`
1. Install Pulumi CLI: [Pulumi: Getting started](https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started), `curl -fsSL https://get.pulumi.com/ | sh`
    1. (Optional, works without it) Install Pulumi Python package:
        1. (Recommended) Create a Python virtual environment (eg. using venv): `python -m venv .venv`
        1. Activate virtual environment: `source .venv/bin/activate`
        1. Install Pulumi GCP Python package: `pip install -r requirements.txt`
    1. You can login to Pulumi or manage stack states locally:
        1. State file in `$HOME/.pulumi`: `pulumi login --local` (alias for `pulumi login file://~`)
        1. State file in another location: `pulumi login file://path/to/pulumi-state`
    1. If you want to use the code in this repo, don't create a new Pulumi project, as will rewrite `__main__.py` file.
1. You can setup Pulumi passphrase so you don't have to input it every time: `export PULUMI_CONFIG_PASSPHRASE=passphrase && echo $PULUMI_CONFIG_PASSPHRASE`
1. Setup GCP authn Application Default Credentials (ADC) for Cloud SDK and Pulumi CLI: `gcloud auth application-default login`
    1. You need a working Cloud SDK installation or use GCP Cloud Shell.
1. Work under `stacks` dir: `cd stacks`
1. Create a new Pulumi stack. You can use the lab name as the Pulumi stack name: `pulumi stack init STACK_NAME`
1. Include config in `Pulumi.STACK_NAME.yaml` (example file: `example-Pulumi.stack_name-yaml`). Requires:
    1. List of emails of attendees for access control to projects. Recommended to also include the first email for the instructor's project.
    1. List of roles to be assigned to all attendes in their projects.
    1. List of APIs/services to be enabled in all projects.
    1. IDs for organization & billing account, and folder name.
    1. Project prefix, e.g. Project IDs created `PROJECT_PREFIX-00-EMAIL_HASH_SUFFIX`, with `00-99` pseudo-random integers for each project
        1. Project prefix can e.g. reflect the name of the lab or workshop, so can also be the same as Pulumi stack name.
        1. GCP project IDs must be 6 to 30 with lowercase letters, digits, hyphens, start with a letter, and trailing hyphens are prohibited, so this also applies to project prefix.
            1. _No underscores in GCP project IDs._
    1. Name of the infrastructure resources script to be imported:
        1. For clarity, you can use `STACK_NAME_infra`, but it's not enforced - e.g. this how-to guide uses `lab-project_infra`.
        1. Don't add `.py` as it looks for the name of the Python module script, not the file itself.
    1. As we're creating a GCP folder and multiple projects, Pulumi config `gcp:project` is not used, so it can be skipped (Pulumi throwns a warning) or can be setup as any valid GCP project ID.
1. Include IaC for creating template GCP resources in `STACK_NAME_infra.py`, along Pulumi exports as needed.

### Pulumi's CLI usage

1. Check Pulumi's preview of resources to be created: `pulumi preview`
1. Create resources with Pulumi CLI: `pulumi up`
1. Check resources created: `pulumi stack`
1. Destroy folder, projects and resources: `pulumi down`

## Multiple projects, courses or exercises

Sometimes you just want one lab environment for a single exercise, sometimes you're running an event/workshop/course composed of multiple lab exercises.

You can organize multiple exercises by using [Pulumi projects](https://www.pulumi.com/docs/concepts/project/) and [Pulumi Stacks](https://www.pulumi.com/docs/concepts/stack/):

- Using a new stack for each environment is easier as you don't have to create new Pulumi projects, but doesn't allow to organize multiple exercises together.
- Creating a different Pulumi project and then multiple stacks for each exercise allows to organize them together and represent a single reproducible event.
- Each stack uses a different `Pulumi.STACK_NAME.yaml` args and `STACK_NAME_infra.py` GCP resources files, whether using different Pulumi projects or not.
  - `Pulumi.lab-project.yaml` and `lab-project_infra.py` files are provided as examples.
- You can have a main Pulumi project for multiple individual exercises/stacks, then also other Pulumi projects for specific multi-exercise/multi-stack events.

**Beware**: Creating a new Pulumi project rewrites `__main__.py`, losing all code, so you'll need to copy the file again.

You can create a new Pulumi project with `pulumi new` and use the `GCP Python` provied template.

You can manage stacks with `pulumi stack` ([docs](https://www.pulumi.com/docs/cli/commands/pulumi_stack/)):

- Create: `pulumi stack init`
- List: `pulumi stack ls`
- Check stack state and GCP resources crated: `pulumi stack`
- Choose current stack: `pulumi stack select`
- Remove: `pulumi stack rm`

## Requirements

Check `stacks/requirements.txt`:

- [Pulumi](https://www.pulumi.com/docs/) for Python v3
- Pulumi provider: [Google Cloud (GCP) Classic](https://www.pulumi.com/registry/packages/gcp/) v7

## License

GNU GPLv3

## Known issues and contribution

Tested at the time of last commit:

- GCP project IDs are created using a deterministic hashed salt, which includes args set in `Pulumi.STACK_NAME.yaml`, as everytime `pulumi up` is run it needs to match the same project IDs. As when a GCP project is deleted it enters a pending delete state for 30 d, if the same attendee **or instructor** is included in a different event using the same args, an error will be thrown when trying to create their project. In this case, just change some args like `stack name`, `project prefix` or `folder name` and a different hash will be produced. Check `main.py` for more.

If you find any issues, please open a GitHub issue before, (optionally) open a PR to fix it, or contact the maintainer directly any way.

## TO-DOs

See to-dos in `to-dos.md`.
