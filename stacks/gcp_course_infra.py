#!/usr/bin/env python3
"""Declare GCP templated resources to be created in each project"""

import pulumi
import pulumi_gcp as gcp

from __main__ import gcp_project_ids, generated_project_ids

# TODO
print('LOGGING BEFORE gcp_project_ids:')
print(gcp_project_ids)
print(type(gcp_project_ids[0]))

# Using output.property.apply() to convert and process Pulumi Outputs as they are async
gcp_project_ids = [id.apply(lambda s: str(s.split("/")[-1])) for id in gcp_project_ids] # return the last part of the ID

# TODO
print('LOGGING AFTER gcp_project_ids:')
print(gcp_project_ids)
print(type(gcp_project_ids[0]))


# Create a GCS bucket
bucket_urls = []
for gcp_project_id, generated_project_id in zip(gcp_project_ids, generated_project_ids):
    # TODO
    print('LOGGING LOOP gcp_project_ids:')
    print(gcp_project_id)
    print(type(gcp_project_id))

    bucket = gcp.storage.Bucket(gcp_project_id, name=gcp_project_id + '-bucket-test', location='US', project=gcp_project_id)
    bucket_urls.append(bucket.url)

pulumi.export('bucket_urls', bucket_urls)
