#!/usr/bin/env python3

from __future__ import print_function
from pathlib import PurePath
from aws_xray_sdk.core import patch_all
import boto3
import os

from aws_lambda_powertools import Logger

from aws_xray_sdk.core import xray_recorder
xray_recorder.configure(context_missing='LOG_ERROR')


patch_all()

logger = Logger(service="custom-ssm-resource",
                level=os.getenv('LOGLEVEL', 'INFO'))


@logger.inject_lambda_context(log_event=True)
def on_event(event, context):

    request_type = event['RequestType']
    if request_type == 'Create':
        return on_create(event)
    if request_type == 'Update':
        return on_update(event)
    if request_type == 'Delete':
        return on_delete(event)
    raise Exception("Invalid request type: {}".format(request_type))


def on_create(event):
    props = event["ResourceProperties"]
    logger.info("create new resource with props {}".format(props))

    prefix = PurePath(os.getenv('SSM_PATH_PREFIX', '/'))

    keyspace = PurePath(event['ResourceProperties'].get('keyspace', '/'))

    try:
        # check our keyspace starts with our prefix
        relative_path = keyspace.relative_to(prefix)

        # merge paths
        keyspace = prefix.joinpath(relative_path)

    except ValueError:

        # otherwise prepend prefix
        logger.info("keyspace isnt in prefix - appending full prefix")

        if keyspace.root == '/':
            # absolute path
            keyspace = prefix.joinpath(keyspace.relative_to('/'))
        else:
            # relative path
            keyspace = prefix.joinpath(keyspace)

    logger.info("querying param keyspace: {}".format(keyspace))

    physical_id = "CustomSSMResource" + convert_name(keyspace)

    response = {'PhysicalResourceId': physical_id, 'Data': {}}

    params = get_params(
        path=keyspace.as_posix()
    )

    for param in params:
        name = param.get('Name')
        value = param.get('Value')

        response['Data'].update({name: value})

    return response


def convert_name(name):

    return ''.join(x.title() for x in name.parts[1:])


def on_update(event):
    physical_id = event["PhysicalResourceId"]
    props = event["ResourceProperties"]
    logger.info("update resource {} with props {}".format(physical_id, props))
    return


def on_delete(event):
    physical_id = event["PhysicalResourceId"]
    logger.info("delete resource {}".format(physical_id))
    return


def get_params(path):

    logger.info("retrieving params for path {}".format(path))

    client = boto3.client('ssm')

    parameter_list = []

    try:

        paginator = client.get_paginator('get_parameters_by_path')

        for page in paginator.paginate(Path=path, Recursive=True, WithDecryption=True):
            for parameter in page['Parameters']:
                parameter_list.append(parameter)

    except Exception as e:
        logger.exception("Error retrieving param")

    return parameter_list


if __name__ == "__main__":

    import mockcontext

    on_event(
        event={'RequestType': 'Create',
               'ServiceToken': 'arn:aws:lambda:eu-west-1:123456789012:function:CustomSsmResourceStack-CustomSSMProviderframeworko-GCN5M7EYX4XL', 'ResponseURL': 'https://cloudformation-custom-resource-response-euwest1.s3-eu-west-1.amazonaws.com/arn%3Aaws%3Acloudformation%3Aeu-west-1%3A074705540277%3Astack/CustomSsmResourceStack/c2750a90-5e5a-11eb-88ee-0a27cca8e7e9%7CResource1%7C21d9ad30-aed7-43fc-98dc-752f6afb68f7?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210124T154353Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7199&X-Amz-Credential=AKIAJ7MCS7PVEUOADEEA%2F20210124%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=cac15fae25bfb69876bd7d1cae022802227ee405a05a1af224e4e9c7f2bb9a00',
               'StackId': 'arn:aws:cloudformation:eu-west-1:123456789012:stack/CustomSsmResourceStack/c2750a90-5e5a-11eb-88ee-0a27cca8e7e9',
               'RequestId': '21d9ad30-aed7-43fc-98dc-752f6afb68f7',
               'LogicalResourceId': 'Resource1',
               'ResourceType': 'AWS::CloudFormation::CustomResource',
               'ResourceProperties': {
                   'ServiceToken': 'arn:aws:lambda:eu-west-1:123456789012:function:CustomSsmResourceStack-CustomSSMProviderframeworko-GCN5M7EYX4XL',
                   'keyspace': '/isp/dev'
               }
               },
        context=mockcontext.MockContext(
            name='CustomResource', version='$LATEST')
    )
