# TODOs

In no particular order...

- Automatic testing: [unit, property and integration tests](https://www.pulumi.com/docs/using-pulumi/testing/)
- Update quotas
- How to share GCP resources templates
- How-to guide to import resources like projects, or refresh state/stack
  - If you're importing something this would create, you don't have to include the code, as it's already there
- Explore if creating Pulumi projects using a project template: [pulumi new](https://www.pulumi.com/docs/cli/commands/pulumi_new/#:~:text=To%20create%20a%20project%20from%20a%20specific%20source%20control%20location%2C%20pass%20the%20url%20as%20follows%20e.g.)
- Check if creating resources needs to depend on service enabling first
  - projects on folder
  - services, roles, etc., on projects
  - resources on services
- Add instructions on how to use a viewer for dependency graphs: `pulumi stack graph GRAPH_FILE`.
- Switch to autonaming convention for physical resources: <https://www.pulumi.com/blog/autonaming-configuration/>
- Update to provider GCP Classic v8
