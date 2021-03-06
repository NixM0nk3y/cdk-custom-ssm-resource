import random


class MockContext(object):
    def __init__(self, name, version):
        self.function_name = name
        self.function_version = version
        self.invoked_function_arn = (
            "arn:aws:lambda:us-east-1:123456789012:function:{name}:{version}".format(name=name, version=version))
        self.memory_limit_in_mb = float('inf')
        self.log_group_name = 'test-group'
        self.log_stream_name = 'test-stream'
        self.client_context = None

        self.aws_request_id = '-'.join([''.join([random.choice('0123456789abcdef')
                                                 for _ in range(0, n)]) for n in [8, 4, 4, 4, 12]])

    def get_remaining_time_in_millis(self):
        return float('inf')

    def get_remaining_time_in_millis(self):
        return float('inf')
