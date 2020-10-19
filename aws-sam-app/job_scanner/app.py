import dataclasses
import json
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

import boto3

from pipeline import Pipeline

s3_client = boto3.client('s3')


@dataclass
class RecommendationModel:
    jobs: List[Dict]
    mySkills: List[str]


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    resume_file_id = event.get('resume_file_id')
    if not resume_file_id:
        # Maybe it's passed from API gateway
        query_param = event.get('queryStringParameters')
        if query_param:
            resume_file_id = query_param.get('resume_file_id')
    if not resume_file_id:
        resume_file_id = event.get('body', {}).get('resume_file_id')

    if not resume_file_id:
        raise ValueError("Required field not found")

    pipe = Pipeline().load()

    # Get resume file (pdf) from s3 by file_id
    bucket = 'jobscanner-test'
    key = 'resume_upload/' + resume_file_id
    tmpkey = key.replace('/', '')

    with tempfile.TemporaryDirectory() as tmp_folder:
        tmp_folder = Path(tmp_folder)
        download_path = tmp_folder / '{}_{}'.format(uuid.uuid4(), tmpkey)
        download_path = str(download_path)
        s3_client.download_file(bucket, key, download_path)

        # Get text from pdf
        cv_text = pipe.cv_from_pdf(download_path)

        jobs, skills = pipe.get_job_recommendations(cv_text)
        ret_data = RecommendationModel(jobs=jobs, mySkills=list(skills))

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(dataclasses.asdict(ret_data)),
    }
