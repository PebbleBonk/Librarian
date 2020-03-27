import boto3
from librarian.actors.actor import Actor


class S3Actor(Actor):
    """ Actor to upload files to S3 cloud storage

        Args:
            bucket_name (str): Bucket to which upload the files
            prefix (str): prefix added to the filename
            suffix (str): suffix added to the filename
    """
    def __init__(self, acess_key, secret_key, bucket_name, prefix="", suffix=""):
        super().__init__()
        self.description = "Uploads the data to S3 storage as a file"
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.suffix = suffix
        # Let's use Amazon S3
        self.s3 = boto3.resource(
            's3', aws_access_key_id=acess_key,
            aws_secret_access_key=secret_key
        )
        self.bucket = self.s3.Bucket(bucket_name)

    def print_buckets(self):
        # Print out bucket names
        for bucket in self.s3.buckets.all():
            print(bucket.name)

    def upload_image(self, key, data):
        # Upload a new file
        #self.s3.Bucket('my-bucket').put_object(Key=key, Body=data)
        pass

    def act(self, data, uid):
        # Try to get the extension:
        ext = ''

        # So ugly:
        try:
            ext = '.'+data.filename.split('.')[-1]
        except AttributeError as e:
            print("Extension exception from 'filename':", str(e))
            try:
                ext = '.'+data.name.split('.')[-1]
            except AttributeError as e:
                print("Extension exception from 'name':", str(e))

        # TODO: check for file conversion need
        data.stream.seek(0)
        key = self.prefix+uid+ext+self.suffix
        self.bucket.put_object(Key=key, Body=data.stream)