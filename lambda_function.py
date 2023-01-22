import boto3, json
from botocore.exceptions import ClientError
import os, sys
import tempfile
import git
from oauth2client.service_account import ServiceAccountCredentials

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-1"
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    return get_secret_value_response['SecretString']

def get_sheets_creds():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    if "sheets_creds" in os.environ.keys():
        sheets_creds = os.environ["sheets_creds"]
    else:
        sheets_creds = get_secret("google_sheets_creds.json")
    return ServiceAccountCredentials.from_json_keyfile_dict(json.loads(sheets_creds))
    
def get_aws_creds():
    if "access_key" in os.environ.keys():
        # Get locally exported creds in test mode
        return { 
            "access_key": os.environ["access_key"],
            "secret_key": os.environ["private_key"],
        }
    else:
        secrets = get_secret("myq_credentials")
        return {
            'access_key': secrets['access_key'],
            'secret_key': secrets['secret_key'],
        }

def clone_repo():
    tmp_path = tempfile.mkdtemp()
    git_url = "https://github.com/michaelmu/lindabaird.git"
    git.Git(tmp_path).clone(git_url)
    return os.path.join(tmp_path, "lindabaird")

def lambda_handler(event, context):
    deploy = False if 'testmode' in event.keys() else True
    tmp_path = clone_repo()
    print("Temp path is: {}".format(tmp_path))
    sys.path.append(tmp_path)
    from build_site import SiteBuilder
    SiteBuilder(
        tmp_path, 
        aws_creds=get_aws_creds(),
        sheets_creds=get_sheets_creds(),
        ).update_site(deploy=deploy)
    