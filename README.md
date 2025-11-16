# README

Tool and how-to guide to use Pulumi OSS IaC (Infrastructure as Code) to create multiple Google Cloud sandbox projects with initialized resources for training courses, workshops, demos, etc.

Learn more about Pulumi IaC: [www.pulumi.com](https://www.pulumi.com)

Contact maintainer:

- Marcos Manuel Ortega: <info@indavelopers.com>
- Consultant, architect and trainer
- Google Cloud Authorized Trainer
- Google Developer Expert
- LinkedIn: [Marcos Manuel Ortega](https://www.linkedin.com/in/marcosmanuelortega)

## Use case

You are running a GCP workshop, training course, sandbox, hackathon... and you need to create several individual projects for each participant.

Each project need some IAM roles assigned to participants, APIs enabled, a billing account enabled, etc., and most importantly, maybe some resources already created following a template, as VM instances, DBs, GCS buckets, etc.

You don't want to have to setup all of that for each user and project manually, then redoing it all over again in the next event, forgetting to setup something, fixing errors live...

You would prefer to have a template for creating these projects automatically, and just reuse it every time new environments are needed or new attendees join, and even collaborate sharing project templates with other event organizers.

## Use of Pulumi projects and stacks for representing events and labs

Sometimes you just want one new environment for a single lab, sometimes you're running an event/workshop/course composed of multiple lab exercises.

You can organize multiple exercises by using [Pulumi projects](https://www.pulumi.com/docs/concepts/project/) and [Pulumi Stacks](https://www.pulumi.com/docs/concepts/stack/).

As a recommendation, this how-to guide uses this structure:

- `events` dir for all events, independent from `src` dir which contains Pulumi Python code and example config files for projects and stacks.
- `events/example-generic_events` for miscellaneous, single lab environments.
- `events/example-course` as a course or event composed of multiple labs, each one with its own `example-lab0` folder and `lab-project_infra.py` GCP resources file.

You could set up your dir structure as you prefer, or use them as example files expand the list of dirs inside `events`.

- Stacks config YAML files are created by default next to the project's `Pulumi.yaml` file, instead of the current dir.
- In each `Pulumi.yaml`, beware the relative paths to main Python entrypoint file, virtual env and requirements in `src`.
- Also beware the stack YAML file relative path to the stack's `STACK_NAME_infra.py` file.

## Usage

1. Clone repo and setup as working dir: `git clone https://github.com/Indavelopers/gcp-training-projects.git`, `cd gcp-training-projects`
2. Install Pulumi CLI: [Pulumi: Getting started](https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started), `curl -fsSL https://get.pulumi.com/ | sh`
    1. You can login to Pulumi Cloud or manage stack state locally:
        1. State file in `$HOME/.pulumi`: `pulumi login --local` (alias for `pulumi login file://~`)
        2. State file in another location: `pulumi login file://path/to/pulumi-config-dir`
    2. If you want to use the code in this repo, don't create a new Pulumi project in `src`, as will rewrite `__main__.py` file.
3. You can setup the Pulumi passphrase so you don't have to input it every time: `export PULUMI_CONFIG_PASSPHRASE=passphrase && echo $PULUMI_CONFIG_PASSPHRASE`
4. Setup GCP authn Application Default Credentials (ADC) for Cloud SDK and Pulumi CLI: `gcloud auth application-default login`
    1. You need a working local Cloud SDK installation or to use GCP Cloud Shell.
5. See previous instructions about the use of Pulumi projects and stacks to represent events and individual labs
   1. Then create a event/lab dir and work in that: `cd events`, `mkdir example-course1`, `cd example-course1`
6. Copy `src/Pulumi.yaml` and modify its content - `main` and `runtime` (example: `events/example-generic_events/Pulumi.yaml`)
7. Create a new Pulumi stack. You can use the lab name as the Pulumi stack name: `pulumi stack init STACK_NAME`
8. Include lab config in the auto-created `Pulumi.STACK_NAME.yaml` file next to the copied`Pulumi.yaml` (example: `src/example-Pulumi.stack_name-yaml`):
    1. List of attendees' emails. It's recommended to include also the instructor's email first.
    2. List of roles to be assigned to attendes in their projects.
    3. List of APIs/services to enable.
    4. Organization ID, billing account ID, and folder name.
    5. GCP project prefix, e.g. created GCP project IDs will be `PROJECT_PREFIX-00-EMAIL_HASH_SUFFIX`, with `00-99` as pseudo-random integers for each project.
        1. Project prefix can e.g. reflect the name of the lab or workshop, so can also be the same as Pulumi stack name.
        2. GCP project IDs must be 6 to 30 chars with lowercase letters, digits, hyphens, start with a letter, and trailing hyphens are prohibited, so this applies to project prefix as well.
            1. _Beware: No underscores in GCP project IDs._
    6. Relative path of the infrastructure resources script to be imported, relative to `src/__main__.py`:
        1. For clarity, you can use `STACK_NAME_infra`, but it's not enforced - e.g. this how-to guide examples use `lab-project_infra`.
    7. As we're creating a GCP folder and multiple projects, Pulumi config `gcp:project` is not used, so it can be skipped (Pulumi throwns a warning).
9. Include IaC for creating template GCP resources in `STACK_NAME_infra.py`.

### Python virtual environments in Pulumi

1. Pulumi automatically uses a Python virtual env when running Python programs, for example in `pulumi up`, without the user having to activate it.
2. `src/Pulumi.yaml` refers to a `src/venv` dir as virtual environment, it will be created when running e.g. `pulumi preview` or `pulumi up` for the first time.
3. It automatically installs Python packages `src/requirements.txt`, where you can include your Python packages.
4. You can point your IDE's Python interpreter or virtual environment to this `src/venv` dir.

#### Requirements

Check `stacks/requirements.txt`:

- [Pulumi](https://www.pulumi.com/docs/) for Python v3
- Pulumi provider: [Google Cloud (GCP) Classic](https://www.pulumi.com/registry/packages/gcp/) v7

### Pulumi's CLI usage

Manage Pulumi projects:

- Create a new Pulumi Python GCP project using `pulumi new` using the `GCP Python` template, or just copy a new `Pulumi.yaml`.
  - **Beware:** It rewrites the project's `__main__.py`, which you can copy again from `src/Pulumi.yaml`.
- Any `pulumi` command will run linked to the nearest Pulumi project `Pulumi.yaml` file, so you manage different stacks in each dir.

Manage Pulumi stacks:

- See dir stacks: `pulumi stack ls`
- See all stacks: `pulumi stack ls -aQ`
- Create a new stack and select it: `pulumi stack init STACK_NAME`
- Select a different stack: `pulumi stack select STACK_NAME`
- Remove a stack: `pulumi stack rm STACK_NAME`

Deploy GCP resources:

1. Check (updated) plan of resources to create, modify or delete: `pulumi preview`
2. Deploy resources: `pulumi up`
3. Check resources created: `pulumi stack`
4. Destroy folder, projects and resources: `pulumi down`

## License

GNU GPLv3

## Known issues

Tested at the time of last commit:

- GCP project IDs are created using a deterministic hashed salt, which includes args set in `Pulumi.STACK_NAME.yaml`, as everytime `pulumi up` is run it needs to match the same project IDs. As when a GCP project is deleted it enters a pending delete state for 30 d, if the same attendee **or instructor** is included in a different event using the same args, an error will be thrown when trying to create their project. In this case, just change some args like `stack name`, `project prefix` or `folder name` and a different hash will be produced. Check `main.py` for more.

If you find any issues, please open a GitHub issue before, (optionally) open a PR to fix it, or contact the maintainer directly any way.

## Contributions, help and discussions

Just open an issue, submit a pull request, or generally contact the author by any mean.

## TO-DOs

See to-dos in `to-dos.md`.
