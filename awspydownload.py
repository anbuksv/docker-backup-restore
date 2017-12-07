import boto3,yaml
import botocore
from sys import argv,exit

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

args = getopts(argv)

with open('config.yaml') as f:
      data = yaml.safe_load(f);

if('-awsKey' not in args and 'awsKey' not in data):
      print("aws access key required (-awsKey)");
      exit(1);

if('-awsSecret' not in args and 'awsSecret' not in data):
      print("aws access secret required (-awsSecret)");
      exit(1);

if('-bucket' not in args and 'bucket' not in data):
      print("bucket name required (-bucket)");
      exit(1);

if('-fileKey' not in args):
      print("download file key required (-fileKey)");
      exit(1);

awsKey = args['-awsKey'] if '-awskey' in args  else data['awsKey'];
awsSecret = args['-awsSecret'] if '-awsSecret' in args else data['awsSecret'];
awsBucket = args['-bucket'] if '-bucket' in args else data['bucket'];

AWS_ACCESS_KEY_ID = awsKey;
AWS_SECRET_ACCESS_KEY = awsSecret;
bucket_name = awsBucket;

BUCKET_NAME = awsBucket; # replace with your bucket name
KEY = args['-fileKey']; # replace with your object key

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def callback(inp):
    print(str(inp/1024) + "Kb");

try:
    s3.download_file(BUCKET_NAME, args['-fileKey'],args['-fileKey'],None,callback);
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object dose not exist.");
        exit(404);
    else:
        print(e.response);
        exit(405); 
