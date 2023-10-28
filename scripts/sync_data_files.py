import os
from pathlib import Path

import boto3

client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('personal-data-dashboard.david-pw.com')

def get_s3_filenames(bucket: str, prefix: str):
    paginator = client.get_paginator('list_objects_v2')
    paginator_iterator = paginator.paginate(Bucket=bucket.name, Prefix=prefix)

    keys = []
    for result in paginator_iterator:
        if result is None or result.get('Contents') is None or len(result.get('Contents')) == 0:
            return []
        for content in result.get('Contents'):
            new_key = Path(content.get('Key')).relative_to(prefix)
            keys.append(os.path.join(prefix, new_key))
    return keys

def get_local_filenames(location: str, prefix: str):
    
    filepath = Path(os.path.join(location, prefix))
    valid_filenames = []
    for path, subdirs, files in os.walk(filepath):
        for name in files:
            local_file = Path(os.path.join(path, name)).relative_to(filepath)
            if Path(name).suffix in ['.json', '.csv']:
                valid_filenames.append(os.path.join(prefix, local_file))
    return valid_filenames

local_location = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

local_filenames = get_local_filenames(local_location, 'data') + get_local_filenames(local_location, 'metadata')
remote_filenames = get_s3_filenames(bucket, 'data') + get_s3_filenames(bucket, 'metadata')
filename_local_only = list(set(local_filenames).difference(set(remote_filenames)))
filename_remote_only = list(set(remote_filenames).difference(set(local_filenames)))

print(f"Number of valid local files: {len(local_filenames)}")
print(f"Number of remote files: {len(remote_filenames)}")
print(f"Number of valid local-only filenames: {len(filename_local_only)}")
print(f"Number of remote only filenames: {len(filename_remote_only)}")

print("Uploading exclusively local files to S3...")

# for every filename that is only available locally, upload to s3
for filename in filename_local_only:
    s3_filepath = Path(filename).as_posix()
    local_filepath = str(Path(os.path.join(local_location, filename)))

    print(f"Writing to S3 bucket {bucket.name} at {s3_filepath}...")

    bucket.upload_file(local_filepath, s3_filepath)

print("Downloading exclusively remote files locally...")

# for every filename that is only available remote, write the file locally
for filename in filename_remote_only:
    s3_filepath = Path(filename).as_posix()
    local_filepath = str(Path(os.path.join(local_location, filename)))
    Path(os.path.dirname(local_filepath)).mkdir(parents=True, exist_ok=True)

    print(f"Writing to local location {local_filepath}...")

    bucket.download_file(s3_filepath, local_filepath)

print("Done.")