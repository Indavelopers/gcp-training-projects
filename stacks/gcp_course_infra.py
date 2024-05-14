#!/usr/bin/env python3
"""Declare GCP templated resources to be created in each project"""

import pulumi
import pulumi_gcp as gcp

from __main__ import gcp_project_ids, generated_project_ids

# Create a GCS bucket
bucket_urls = []
for gcp_project_id, generated_project_id in zip(gcp_project_ids, generated_project_ids):
    bucket = gcp.storage.Bucket(generated_project_id, name=generated_project_id + '-bucket', location='US', project=generated_project_id)
    bucket_urls.append(bucket.url)

pulumi.export('bucket_urls', bucket_urls)
