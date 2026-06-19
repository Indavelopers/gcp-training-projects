# README

Tool and how-to guide to use Pulumi OSS IaC (Infrastructure as Code) to create multiple Google Cloud sandbox projects with previously created resources for training courses, workshops, interactive demos, etc.

Learn more about Pulumi IaC: [www.pulumi.com](https://www.pulumi.com)

Contact maintainer:

- Marcos Manuel Ortega: <info@indavelopers.com>
- Consultant, architect and trainer
- Google Cloud Authorized Trainer
- Google Developer Expert in Google Cloud
- LinkedIn: [Marcos Manuel Ortega](https://www.linkedin.com/in/marcosmanuelortega)
- Made with ❤️ from Almería, Spain

## Use case

You want to run a GCP workshop, training course, sandbox, hackathon... and you need to create several individual projects for each participant.

Each participant needs a GCP project with some IAM roles assigned to them, APIs enabled, a billing account assigned, etc., and maybe some resources already created, as VM instances, GKE clusters, DBs, GCS buckets, etc.

Since last time, you don't want to have to setup again everything up for each participant manually, then again next time, maybe forgetting to setup something and trying to fix errors live...

You'd prefer to have a template and setting it all up automatically, and just reuse it every time new environments are needed or new attendees join, and even collaborate sharing project templates with other event organizers.

## Creating events and lab exercises

Sometimes you just want environments to for a single lab exercise, sometimes you're running an event/workshop/course composed of multiple labs.

Here, events are represented by [Pulumi projects](https://www.pulumi.com/docs/concepts/project/), and labs by [Pulumi Stacks](https://www.pulumi.com/docs/concepts/stack/).

Recommended dir structure:

- `events`: Holds all events and labs, independent from base `src`
  - `events/example-generic_events`: Miscellaneous, single labs.
  - `events/example-course`: Example course or event composed of multiple labs, each with own `example-lab0` stack, folder and `lab_infra.py` GCP resources file.
- `src`: Pulumi Python code and example/base config files:
  - `src/example-Pulumi.yaml`: Base Pulumi project config file.
  - `src/example-Pulumi.stack_name.yaml`: Base Pulumi stack config file.
  - `src/example-lab-project_infra.py`: Example Pulumi Python resource definition file.

You can use this structure, using them as example files and adding your new event dirs, or a custom one.

### Pulumi project and stack YAML config files

- Stacks config YAML files are created by default next to the project's `Pulumi.yaml` file, instead of the current dir.
- In each `Pulumi.yaml`, use relative paths to navigate up from the event directory to the repository root's `src` directory. For example, if your project is 2 levels deep (`events/example-course/`), use `../../src/__main__.py` and `../../src/venv`.
- Also, in each stack YAML file, use the correct relative path to the lab `lab_infra.py` file as evaluated from the main script (e.g., `../events/example-course/example-lab0/lab_infra.py` as seen from `src/__main__.py`).

### Writing GCP resources

As we're creating the GCP projects and enabling the GCP APIs or services in the same Pulumi script, you need to explicitly declare the GCP API/service each resource depends on. If not declared, APIs and resources would be created at the same time, and thus resource creation would fail as the API hasn't been enabled yet.

Something similar happens with GCP project creation: if the GCP project is not declared for each resource - even eg. for subnets, where the network is declared as an attribute, Pulumi would take your local Cloud SDK config GCP project, instead of the projects created by this script. Therefore, you need to explicitly include the GCP project using the `project` var from `gcp_projects` the loop is iterating over.

#### Assigning roles to attendees

Usually, you might want to assign the `roles/owner` role to attendees and go with it, but it has some limitations: <https://docs.cloud.google.com/iam/docs/roles-overview#:~:text=Generally%2C%20you%20can,of%20any%20organization.>.

A recommended alternative would be to use the new basic `roles/writer` or the legacy basic `roles/editor` instead, which would also be more secure.

#### Modifying GCP project quotas

You can modify project quotas directly in your `lab_infra.py` file using the `gcp.serviceusage.ConsumerQuotaOverride` resource ([docs](https://www.pulumi.com/registry/packages/gcp/api-docs/serviceusage/consumerquotaoverride/)). Ensure that the `serviceusage.googleapis.com` API is enabled for the project first (e.g., by adding it to the `apis` list in your stack configuration). Also, keep in mind that the requested quota overrides are still subject to the maximum bounds and limits allowed by your billing account or organization.

## Usage

1. Clone repo and open dir: `git clone https://github.com/Indavelopers/gcp-training-projects.git`, `cd gcp-training-projects`
2. Install Pulumi CLI: [Pulumi: Getting started](https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started), `curl -fsSL https://get.pulumi.com/ | sh`
    1. You can login to Pulumi Cloud or manage stack state locally with Pulumi IaC OSS:
        1. State file in `$HOME/.pulumi`: `pulumi login --local` (alias for `pulumi login file://~`)
        2. State file in another location: `pulumi login file://path/to/pulumi-config-dir`
    2. Don't create a new Pulumi project in `src`, as will rewrite `__main__.py` file. Check `Pulumi CLI usage` section for more.
3. You can setup the Pulumi passphrase so you don't have to input it every time: e.g. `export PULUMI_CONFIG_PASSPHRASE=passphrase && echo $PULUMI_CONFIG_PASSPHRASE`
   1. Alternatively, use PULUMI_CONFIG_PASSPHRASE_FILE envvar: e.g. `export PULUMI_CONFIG_PASSPHRASE_FILE=~/gcp-training-projects/src/pulumi_config_passphrase.txt && echo $PULUMI_CONFIG_PASSPHRASE_FILE`
   2. Add the passphrase in said file.
4. Setup GCP authn Application Default Credentials (ADC) for Pulumi CLI: `gcloud auth application-default login`
    1. You need a working local Cloud SDK installation or use GCP Cloud Shell.
5. Check first previous instructions about using Pulumi projects and stacks in section **Creating events and lab exercises**.
   1. Create a event/lab dir and work in it. As discussed in **Creating events and lab exercises**, you can either create an event dir with a single lab env, or an event dir with multiple labs envs or subdirs.
   2. E.g. for an event with a single lab: `cd events`, `mkdir example-event1 && mkdir example-event1`, `cd example-event1`.
   3. E.g. for an event with multiple lab envs: `cd events`, `mkdir example-course1 && mkdir example-course1/example-lab1`, `cd example-course1/example-lab1`.
6. For each new event dir, you need to create a new Pulumi project inside. For a new lab, you just need to create a new Pulumi stack.
   1. Creating a new project and stacks register them in your Pulumi state, and sets a new encryption salt for that stack.
7. Create a new Pulumi `Python GCP` project: `pulumi new`
8. Create a new Pulumi stack. You can use the lab name for the stack name: `pulumi stack init STACK_NAME`
9. Copy the `src/Pulumi.yaml` content into the `Pulumi.yaml` project config file, and modify paths to `src/__main__.py` and `src/venv` accordingly.
10. Copy the `src/example-Pulumi.stack_name-yaml` content into the `Pulumi.STACK_NAME.yaml` stack config file:
    1. `encryptionsalt`: Don't overwrite, unique to that stack.
    2. `infra_script`: Resources script to import, relative path from `src/__main__.py`.
       1. File can have any name, `lab_infra` is just a convention.
    3. `emails`: List of attendees' emails. You can add an environment for the trainer putting his email first.
    4. `apis`: List of GCP APIs/services to enable.
    5. `roles`: List of roles to be assigned to attendes in their projects.
    6. `parent_id`: GCP organization or folder ID to use as parent, in the format `organizations/org_id` or `folders/folder_id`.
    7. `billing_account_id`: GCP billing account ID.
    8. `folder_name`: GCP folder name.
    9. `project_prefix`: GCP project prefix, e.g. GCP project ID would be `PROJECT_PREFIX-00-HASH_SUFFIX`.
        1. `PROJECT_PREFIX`: Can reflect e.g. the lab or workshop name, so can be the same as Pulumi stack name.
           1. GCP project IDs must be 6-30 chars with lowercase letters, digits, hyphens. Should start with a letter, no underscores, and trailing hyphens are prohibited, therefore this applies to project prefix as well.
        2. `00-99`: Project/attendee index, following emails list.
        3. `HASH_SUFFIX`: Unique hash created using stack config fields and random data.
        4. For clarity, you can use `STACK_NAME_infra`, but it's not enforced - e.g. this how-to guide examples use `lab_infra`.
    10. `event_unique_id`: Unique event ID, modify if you want to repeat the event using the same stack name and at least one repeating user.
        1. As GCP project IDs should be globally unique, a unique `HASH_SUFFIX` for each user is computed.
        2. This hash is computed using the stack config and random data, as stated before.
        3. When you delete the GCP project (e.g. with `pulumi down`), it enters a [pending delete state for 30 days](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects), during which you can manually restore a project, but you can't use `pulumi up` to recreate them again.
        4. When running the same lab again, you should create a new stack with a different name and/or config, but sometimes you might just try to modify the email list and deploy again.
        5. If any email is used again (e.g. same trainer or any repeating attende), it would generate the same project ID for him, and would error out when creating the GCP project as is in a pending state or the project ID is not available.
        6. Therefore, if you need to repeat the same lab, you should modify any config or at least this unique event ID so that a different hash is created.
    11. As we're creating a GCP folder and multiple projects, Pulumi config `gcp:project` is not used, so it can be skipped (Pulumi throwns a warning).

Then *voilá*, check and deploy environments with `pulumi preview` and `pulumi up` (see **Pulumi CLI usage** section).

### User emails as secrets

If you want to store attendees emails as encrypted secrets instead of plain-text, you can leave them blank when writing the stack YAML file and add them manually: [Encrypted secrets in configuration data](https://docs.cloud.google.com/iam/docs/roles-overview#basic)

### Python virtual environments in Pulumi

1. Pulumi automatically creates and uses a Python virtual env when running e.g. `pulumi up` for the first time, without user creating or activating it.
   1. When writing your `lab_infra.py` files, you can select this virtual env for your IDE.
2. `src/Pulumi.yaml` refers to this `src/venv` virtual environment.
3. It automatically installs Python packages from `src/requirements.txt`.
4. You can point your IDE's Python interpreter or virtual environment to this `src/venv` dir.

#### Requirements

Check `src/requirements.txt`:

- [Pulumi](https://www.pulumi.com/docs/) CLI: 3.246.0
- Pulumi for Python : v3+
- Pulumi [Google Cloud (GCP) Classic](https://www.pulumi.com/registry/packages/gcp/) provider: v9+
- Tested on Python 3.14

You can add your Python modules here, or point to another `venv` dir in your stack config YAML file.

### Pulumi CLI usage

**BEWARE:**:

- When creating a new Pulumi project, it rewrites any `Pulumi.yaml` and `__main__.py` in that dir.
- Creating a new Stack rewrites any `Pulumi.STACK_NAME.yaml`.
- Therefore, it's recommended to first create projects and stacks, then overwriting the YAML with content from `src`.
- Also note that if you delete a Pulumi stack or project, said YAML files will also be deleted.

Manage Pulumi projects:

- Create a new Pulumi Python GCP project using the `GCP Python` template: `pulumi new`
- Any `pulumi` command will run linked to the nearest Pulumi project `Pulumi.yaml` file found in the same or parent dirs.

Manage Pulumi stacks:

- Create a new stack and select it: `pulumi stack init STACK_NAME`
- Get stack resources state: `pulumi stack`
- List stacks: `pulumi stack ls`
- List all stacks, including other projects: `pulumi stack ls -aQ`
- Select a different stack: `pulumi stack select STACK_NAME`
- Delete a stack: `pulumi stack rm STACK_NAME` (deletes stack YAML config file)

Deploy GCP resources:

1. Check plan of resources to create, modify or delete: `pulumi preview`
2. Deploy resources: `pulumi up`
3. Check created resources state: `pulumi stack`
4. Destroy resources: `pulumi down`

## License

GNU GPLv3

## Known issues

Tested at the time of last commit:

- None.

If you find any issues, please open a GitHub issue before, (optionally) open a PR to fix it, or contact the maintainer directly any way.

## Contributions, help and discussions

Just open an issue, submit a pull request, or generally contact the author by any mean.

## TO-DOs

See to-dos in `to-dos.md`.
