from storages.backends.s3boto3 import S3Boto3Storage


class PublicFileStorage(S3Boto3Storage):
    location = ""
    file_overwrite = False


class LocationImageStorage(S3Boto3Storage):
    location = "location_images"
    file_overwrite = True


class BackgroundImageStorage(S3Boto3Storage):
    location = "background_images"
    file_overwrite = False