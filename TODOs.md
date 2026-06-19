# TODOs

In no particular order...

- Disable gcp:project default config warning with: `pulumi config set gcp:disableGlobalProjectWarning true`
- Code:
  - Switch to autonaming convention for physical resources: <https://www.pulumi.com/blog/autonaming-configuration/>
  - Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
- Templating:
  - How to share GCP resources templates
  - Explore if creating Pulumi projects using a project template: [pulumi new](https://www.pulumi.com/docs/cli/commands/pulumi_new/#:~:text=To%20create%20a%20project%20from%20a%20specific%20source%20control%20location%2C%20pass%20the%20url%20as%20follows%20e.g.)
  - Consider using project templates for creating new stacks: <https://www.pulumi.com/docs/iac/concepts/projects/project-file/#template-options>
- Script to allow the student to individually run by themselves to create their project env, if needed
