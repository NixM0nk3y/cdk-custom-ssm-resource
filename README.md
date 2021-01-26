# AWS CDK SSM Param Cross Account Sharing Construct

An AWS CDK construct for creating a custom CF resource for sharing
SSM parameters over a number of (trusted!) accounts.

The custom resource is setup in the source of the SSM parameter and
is fed a list of accounts able to retrieve parameters.

Access to the SSM hierarchy can be restricted by passing a prefix.

# Source Account Setup

```js
import { CustomSSMProvider } from 'custom-ssm-resource-contruct';


const myProvider = new CustomSSMProvider(this, 'CustomSSMProvider', {
    trustedAccounts: ["123456789012", "123456789013", "123456789014"],
    prefix: "/dev/params"
});
```
The source provider will expose the custom CF resource service key as a
CF output.

# Reading account setup

```js
import { CustomResource } from '@aws-cdk/core';

const cr = new CustomResource(this, 'ResourceTest', {
    serviceToken: serviceToken,
    properties: {
        keyspace: '/dev/params/bar'
    }
});

new cdk.CfnOutput(this, "Output", {
    value: cr.getAttString("/dev/params/bar/wombat")
});

```
The custom resource will expose all the SSM params found under the `keyspace`
path as resource attributes.

# License

MIT

## Useful commands

 * `npm run build`   compile typescript to js
 * `npm run watch`   watch for changes and compile
 * `npm run test`    perform the jest unit tests
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
