#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CustomSsmResourceStack } from '../lib/custom-ssm-resource-stack';

const app = new cdk.App();
new CustomSsmResourceStack(app, 'CustomSsmResourceStack',
    {
        env: {
            account: process.env.CDK_DEFAULT_ACCOUNT,
            region: process.env.CDK_DEFAULT_REGION
        }
    }
);
