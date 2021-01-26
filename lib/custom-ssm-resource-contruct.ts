import * as cdk from '@aws-cdk/core';
import * as logs from '@aws-cdk/aws-logs';
import * as lambda from "@aws-cdk/aws-lambda";
import * as cr from '@aws-cdk/custom-resources';
import * as iam from '@aws-cdk/aws-iam';

export interface CustomSSMProviderProps {
    trustedAccounts?: string[];
    prefix?: string;
}

export class CustomSSMProvider extends cdk.Construct {

    constructor(scope: cdk.Construct, id: string, props: CustomSSMProviderProps) {
        super(scope, id);

        let prefix = props.prefix || '/'

        // ensure prefix ends aith a /
        if (prefix.substr(-1) != '/') {
            prefix += '/'
        }

        const accounts = props.trustedAccounts || []

        const onEvent = new lambda.Function(this, "CustomSSMHandler", {

            runtime: lambda.Runtime.PYTHON_3_8,
            code: lambda.Code.fromAsset("resources", {
                bundling: {
                    image: lambda.Runtime.PYTHON_3_6.bundlingDockerImage,
                    command: [
                        'bash', '-c', `pip install -r requirements.txt -t /asset-output && cp -au . /asset-output`,
                    ],
                },
            }),
            handler: "lambda_function.on_event",
            tracing: lambda.Tracing.ACTIVE,
            timeout: cdk.Duration.seconds(10),
            logRetention: logs.RetentionDays.ONE_WEEK,
            environment: {
                SSM_PATH_PREFIX: prefix
            }
        });

        onEvent.role?.addToPrincipalPolicy(new iam.PolicyStatement({
            effect: iam.Effect.ALLOW,
            resources: [`arn:aws:ssm:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:parameter${prefix}*`],
            actions: ['ssm:GetParametersByPath'],
        }));

        const myProvider = new cr.Provider(this, 'CustomSSMProvider', {
            onEventHandler: onEvent,
            logRetention: logs.RetentionDays.ONE_WEEK
        });

        // grab the entry point lambda from service token.
        // not publically exposed other than via servicetoken/arn 
        const entrypointFunction = lambda.Function.fromFunctionAttributes(this, 'entryPoint', {
            functionArn: myProvider.serviceToken,
            sameEnvironment: true
        });

        // add permissions for other accounts to invoke
        accounts.forEach(function (account) {
            entrypointFunction.grantInvoke(new iam.AccountPrincipal(account));
        });

        new cdk.CfnOutput(this, "CustomSSMServiceToken", {
            value: myProvider.serviceToken,
        });

    }
}

