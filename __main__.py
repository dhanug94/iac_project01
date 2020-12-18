import pulumi
import pulumi_aws as aws

# Create a Security Group
sg = aws.ec2.SecurityGroup(
    "web-sg",
    description="Web security group for HTTP",
    ingress=[
        {
            'protocol': 'tcp',
            'from_port': 80,
            'to_port': 80,
            'cidr_blocks': ['0.0.0.0/0']
        }
    ]
)

# AMI image for EC2
ami = aws.get_ami(
    most_recent="true",
    owners=['amazon'],
    filters=[{"name": 'name', 'values': ['amzn-ami-hvm-*']}]
) 

# Create user data for web server
user_data = """
#!/bin/bash
uname -n > index.html
nohup python -m SimpleHTTPServer 80 &
"""

# Create an AWS resource (EC2 Instace)
instance = aws.ec2.Instance(
    "pulumi-webapp-demo",
    instance_type="t2.micro",
    vpc_security_group_ids=[ sg.id ],
    ami = ami.id,
    user_data=user_data,
)

# Export the IP of the webapp 
pulumi.export('web-app-ip', instance.public_ip)
