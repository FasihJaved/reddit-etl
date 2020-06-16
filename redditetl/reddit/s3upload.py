import boto3
import airflow.hooks.S3_hook 

s3 = boto3.client('s3')

def create_s3_bucket():
    s3.create_bucket(Bucket=get_bucketname())

def create_bucket_key(file_address):
    key_prefix = get_key_prefix
    key = key_prefix+file_address.split(".")[0]+'/'+file_address
    return key

def get_bucketname():
    bucketname = 'reddit-data-pipeline'
    return bucketname

def get_aws_hook():
    hook = airflow.hooks.S3_hook.S3Hook('my_s3_conn')
    return hook

def get_file_names():
    files = ['posts.csv', 'comments.csv', 'bigrams.csv', 'words.csv']
    return files

def get_key_prefix():
    key_prefix = str(datetime.date.today().year)\
        +'/'+str(datetime.date.today().month)\
        +'/'+str(datetime.date.today().day)\
        +'/'
    return key_prefix

def upload_to_s3():
    create_s3_bucket()
    files = get_file_names()
    for file_ad in files:
        get_aws_hook().load_file('/home/airflow/'+file_ad, create_bucket_key(file_ad), get_bucketname())

