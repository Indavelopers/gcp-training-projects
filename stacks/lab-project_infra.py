"""Declare GCP templated resources to be created in each project"""

import pulumi
import pulumi_gcp as gcp

# Importing from main script:
# - gcp_projects: list[str] - GCP project IDs after project creation, sets up implicit dependency when using "project" arg for resource creation
# - generated_project_ids: list[str] - GCP project IDs generated by Python and used for project creation
# - emails: list[str] - emails of attendees
from __main__ import gcp_projects, generated_project_ids, emails

bucket_urls = []

# Loop on GCP projects and create resources
for project, generated_project_id in zip(gcp_projects, generated_project_ids):
    # Create a GCS bucket
    bucket = gcp.storage.Bucket(generated_project_id + '-bucket', name=generated_project_id + '-bucket', location='US', project=project)

    bucket_urls.append(bucket.url)

pulumi.export('bucket_urls', bucket_urls)
