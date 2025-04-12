"""Automatically sets up multiple GCP projects as lab environments for each event attendee"""

import pulumi
import pulumi_gcp as gcp
import hashlib
import importlib.util
import random
import string
import sys


# Config
config = pulumi.Config()
organization_id = config.require('organization_id')
billing_account_id = config.require('billing_account_id')
folder_name  = config.require('folder_name')
project_prefix = config.require('project_prefix')
emails = config.require_object('emails')
roles = config.require_object('roles')
apis = config.require_object('apis')
infra_script = config.require('infra_script')

n_students = len(emails)
stack_name = pulumi.get_stack()

# Create a GCP folder for the training projects
folder = gcp.organizations.Folder(folder_name, display_name=folder_name, parent=f'organizations/{organization_id}')

# Random salt to allow to create more than one GCP project for each email
# Includes random seed for reproducibility, if not, creates a new project everytime 'pulumi up' is run
# Includes organization ID, billing account ID, folder name, project prefix and stack name because, if not, same attendees and instructor
# for a different event generates a colliding GCP project ID
random.seed(3.1415926)
random_salts = [''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) +
                organization_id +
                billing_account_id +
                folder_name +
                project_prefix +
                stack_name
                for _ in range(n_students)]

# Generated project IDs are used as GCP projects IDs and for naming GCP and Pulumi resources
generated_project_ids = [project_prefix + '-' + str(index_number) + '-' + hashlib.sha256((random_salt + email).encode()).hexdigest()[:6]
                        for random_salt, email, index_number in zip(random_salts, emails, range(n_students))]

gcp_projects = []
for generated_project_id, email in zip(generated_project_ids, emails):
    # Create GCP projects under said folder
    project = gcp.organizations.Project(generated_project_id, 
                                        name=generated_project_id, 
                                        project_id=generated_project_id, 
                                        folder_id=folder.id,
                                        billing_account=billing_account_id,
                                        deletion_policy='DELETE')

    gcp_projects.append(project.project_id)

    # Enable APIs on projects
    for api in apis:
        project_api = gcp.projects.Service(generated_project_id + '-' + api, service=api, project=project, disable_on_destroy=False)

    # Setup IAM for the attendees
    for role in roles:
        project_binding = gcp.projects.IAMMember(generated_project_id + '-' + role, role=role, member=f'user:{email}', project=project)

pulumi.export('gcp_projects', gcp_projects)

# Imports and executes infra script to create GCP templated resources
def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    return module

import_from_path('infra_script', infra_script)
