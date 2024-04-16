"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp as gcp

# Config
# todo: get configs from config file
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
for project_name in project_names:
    project_id = project_name + '-' + PROJECT_RANDOM_SUFFIX
    project_ids.append(project_id)

    project = gcp.organizations.Project(project_id, name=project_name, project_id=project_id, folder_id=folder.name, billing_account=BILLING_ACCOUNT_ID)

# Exports
pulumi.export('organization_id', ORGANIZATION_ID)
pulumi.export('billing_account', BILLING_ACCOUNT_ID)
pulumi.export('folder_id', folder.name)
pulumi.export('project_ids', project_ids)


# Enable APIs on projects
apis = ['iam.googleapis.com', 'storage.googleapis.com']

pulumi.export('enabled_apis', apis)


# Setup IAM for the students

# todo: load students emails from file
emails = ['konigdermasai@gmail.com', 'konigdermasai@gmail.com', 'konigdermasai@gmail.com']
roles = ['roles/storage.admin']

# todo: check because role is not assigned
for project_id, email in zip(project_ids, emails):    
    for role in roles:
        project_binding = gcp.projects.IAMMember(project_id, project=project_id, role=role, member=f'user:{email}')

pulumi.export('emails', emails)
pulumi.export('roles', roles)


# Create template resources for the lab
bucket_urls = []
for project_id in project_ids:
    bucket = gcp.storage.Bucket(project_id, name=project_id + '-bucket', location='US', project=project_id)
    bucket_urls.append(bucket.url)


pulumi.export('bucket_urls', bucket_urls)
