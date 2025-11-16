# TODOs

In no particular order...

- Instructions to set PULUMI_CONFIG_PASSPHRASE_FILE instead of envvar
- Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
- Update quotas
- How to share GCP resources templates
- Explore if creating Pulumi projects using a project template: [pulumi new](https://www.pulumi.com/docs/cli/commands/pulumi_new/#:~:text=To%20create%20a%20project%20from%20a%20specific%20source%20control%20location%2C%20pass%20the%20url%20as%20follows%20e.g.)
- Switch to autonaming convention for physical resources: <https://www.pulumi.com/blog/autonaming-configuration/>
- Consider using the random provider instead of Python rand num gen
- Consider using project templates for creating new stacks: <https://www.pulumi.com/docs/iac/concepts/projects/project-file/#template-options>
- Allow to create projects folder inside an already created GCP folder, or skip folder creation
- Disable gcp:project default config warning with: `pulumi config set gcp:disableGlobalProjectWarning true`
- Check as you can't assign owner role to someone outside your org: <https://docs.cloud.google.com/iam/docs/roles-overview#:~:text=Generally%2C%20you%20can,of%20any%20organization.>
- Refactor whole approach? At least offer different instructions: either 1 repo cloned for multiple events & labs, or a single installation in the event/lab independent source repo
- Rewrite and clarify instructions
