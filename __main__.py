"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp as gcp

# Config
N_STUDENTS = 3
ORGANIZATION_ID = "852525814022"
BILLING_ACCOUNT_ID = "00AF3E-CE59B2-0F49AE"
# E.g. Project IDs created: 'PROJECT_PREFIX-0-PROJECT_RANDOM_SUFFIX'
PROJECT_PREFIX = 'student'
PROJECT_RANDOM_SUFFIX = 'qwerty'
FOLDER_NAME = 'training-labs'
FOLDER_DISPLAY_NAME = 'Training Labs'

# It's recommended to create n_students + 1 projects, having "project-0" for the instructor
project_names = [PROJECT_PREFIX + '-' + str(i) for i in range(N_STUDENTS)]

# Create a GCP folder for the training projects
folder = gcp.organizations.Folder(FOLDER_NAME, display_name=FOLDER_DISPLAY_NAME, parent=f'organizations/{ORGANIZATION_ID}')

# Create GCP projects under said folder
project_ids = []
for p in project_names:
    project_id = p + '-' + PROJECT_RANDOM_SUFFIX

    project = gcp.organizations.Project(project_id, name=p, project_id=project_id, folder_id=folder.name, billing_account=BILLING_ACCOUNT_ID)
    project_ids.append(project.project_id)

# Exports
pulumi.export('organization_id', ORGANIZATION_ID)
pulumi.export('billing_account', BILLING_ACCOUNT_ID)
pulumi.export('folder_id', folder.name)
pulumi.export('project_ids', project_ids)
