import boto3
import yaml
import os
from sys import argv,exit,stdout

UPLOADED_DATA = 0;
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

args = getopts(argv);

with open('config.yaml') as f:
      data = yaml.safe_load(f);

if len(args) == 2:
    if( not data['awsKey'] or not data['awsSecret'] or not data['bucket']):
        print("Please enter your s3 bukcet details on config file");
        exit(404);

if('-awsKey' not in args and 'awsKey' not in data):
      print("aws access key required (-awsKey)");
      exit(1);

if('-awsSecret' not in args and 'awsSecret' not in data):
      print("aws access secret required (-awsSecret)");
      exit(1);

if('-bucket' not in args and 'bucket' not in data):
      print("bucket name required (-bucket)");
      exit(1);

if('-filePath' not in args):
      print("file path required (-filePath)");
      exit(1);

if('-fileName' not in args):
      print("file name required (-fileName)");
      exit(1);

awsKey = args['-awsKey'] if '-awskey' in args  else data['awsKey'];
awsSecret = args['-awsSecret'] if '-awsSecret' in args else data['awsSecret'];
awsBucket = args['-bucket'] if '-bucket' in args else data['bucket'];

AWS_ACCESS_KEY_ID = awsKey;
AWS_SECRET_ACCESS_KEY = awsSecret;
bucket_name = awsBucket;

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

response = s3.list_buckets()

#buckets = [bucket['Name'] for bucket in response['Buckets']]

#print("Bucket List: %s" % buckets)

UPLOAD_FILE_SIZE = os.path.getsize(args['-filePath']);

def callback(inp):
    global UPLOADED_DATA;
    UPLOADED_DATA = UPLOADED_DATA + inp;
    stdout.write("\rUploaded "+ str(UPLOADED_DATA/1024) + "kb" + "/" + str(UPLOAD_FILE_SIZE/1024) + "kb");
    stdout.flush();

with open(args['-filePath'], 'rb') as data:
    s3.upload_fileobj(data, bucket_name, args['-fileName'],None,callback)
