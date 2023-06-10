from sys import argv
from boto3 import client


ALLOWED_PREFIXES = [
    'dev',
]
DELETE = True


def clean_storage(repository, bucket_name):
    print(f'Cleaning Storage for {repository} on {bucket_name} bucket')
    current_tags = get_ecr_current_tags(repository)
    current_tags.extend(ALLOWED_PREFIXES)
    delete_bucket_folders_not_in_list(bucket_name, current_tags)


def get_ecr_current_tags(repository):
    ecr = client("ecr")
    response = ecr.list_images(repositoryName=repository)
    tags = []
    for tag in response["imageIds"]:
        tags.append(tag["imageTag"])
    tag_info = ', '.join(tags)
    print(f"Tags found on {repository} : {tag_info}")
    return tags


def delete_bucket_folders_not_in_list(bucket_name, list):
    list_info = ', '.join(list)
    print(f"Allowed prefixes on {bucket_name} : {list_info}")
    s3 = client("s3")
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Delimiter='/',
    )
    prefixes_found = []
    prefixes_to_delete = []
    for prefix in response["CommonPrefixes"]:
        prefix = prefix["Prefix"]
        prefix_name = prefix
        if prefix.endswith("/"):
            prefix_name = prefix_name[:-1]
        if prefix_name not in list:
            prefixes_to_delete.append(prefix_name)
        prefixes_found.append(prefix_name)

    prefixes_found_info = ', '.join(prefixes_found)
    prefixes_to_delete_info = ', '.join(prefixes_to_delete)
    print(f'Prefixes found on {bucket_name}: {prefixes_found_info}')
    if prefixes_to_delete:
        print(f'Prefixes to remove {prefixes_to_delete_info}')
    else:
        print('Nothing to remove')
    if DELETE:
        for prefix in prefixes_to_delete:
            print(f'Deleting {prefix}')
            objects_to_remove = []
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{prefix}/")
            for object in response["Contents"]:
                objects_to_remove.append({
                    "Key": object["Key"]
                })
            response = s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_remove})
            errors = response.get("Errors", [])
            if errors:
                for error in errors:
                    key = error["Key"]
                    code = error["Code"]
                    message = error["Message"]
                    print(f'Error deleting {key} : [{code}] {message}')
    print("Done")


if __name__ == "__main__":
    repository, bucket_name = argv[1:3]
    clean_storage(repository, bucket_name)
