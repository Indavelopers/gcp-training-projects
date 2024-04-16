# README
XXX description

## Instructions
1. Pulumi set up instructions: https://github.com/pulumi/pulumi?tab=readme-ov-file#getting-started
1. Setup GCP authn for Pulumi CLI: `gcloud auth application-default login`
    1. Or use another gcloud CLI installation to create credentials file with said command
    1. Store output in local `credentials.json`
    1. Use its path for envvar: `export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json`, e.g. `export GOOGLE_APPLICATION_CREDENTIALS=$(readlink -f credentials.json)`
1. 

## TODOs
1. Generate project IDs and save to file, load IDs from file if they exist
1. LICENSE file
1. Testing
