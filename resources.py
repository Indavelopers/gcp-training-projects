#!/usr/bin/env python3
"""Declare GCP resources to be created in each project"""

import pulumi
import pulumi_gcp as gcp

def create_resources(project_ids):
    # Create a GCS bucket
    bucket_urls = []
    for project_id in project_ids:
        bucket = gcp.storage.Bucket(project_id, name=project_id + '-bucket', location='US', project=project_id)
        bucket_urls.append(bucket.url)

    pulumi.export('bucket_urls', bucket_urls)
