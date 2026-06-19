# TODOs

In no particular order...

- Choosing folder:
  - Select destination (org, folder), to create labs folder
  - Allow to create projects folder inside an already created GCP folder, or skip folder creation
  - Disable gcp:project default config warning with: `pulumi config set gcp:disableGlobalProjectWarning true`
- Code:
  - Change "lab-project_infra.py" to "lab_infra.py"
  - Update quotas
  - Switch to autonaming convention for physical resources: <https://www.pulumi.com/blog/autonaming-configuration/>
  - Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
- Templating:
  - How to share GCP resources templates
  - Explore if creating Pulumi projects using a project template: [pulumi new](https://www.pulumi.com/docs/cli/commands/pulumi_new/#:~:text=To%20create%20a%20project%20from%20a%20specific%20source%20control%20location%2C%20pass%20the%20url%20as%20follows%20e.g.)
  - Consider using project templates for creating new stacks: <https://www.pulumi.com/docs/iac/concepts/projects/project-file/#template-options>
- Refactor whole approach? At least offer different instructions: either 1 repo cloned for multiple events & labs, or a single installation in the event/lab independent source repo
  - Script to allow the student to individually run by themselves to create their project env, if needed
