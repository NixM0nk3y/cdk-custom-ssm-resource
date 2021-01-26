import * as cdk from '@aws-cdk/core';
import { CustomSSMProvider } from '../lib/custom-ssm-resource-contruct';

export class CustomSsmResourceStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const myProvider = new CustomSSMProvider(this, 'CustomSSMProvider', {
            trustedAccounts: ["074705540277", "729638677489", "334012662223"],
            prefix: "/isp"
        });
    }
}
