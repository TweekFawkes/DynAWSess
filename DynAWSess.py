# dynawsess.py

import os
import sys
import requests
from dotenv import dotenv_values
import boto3
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format

# Initialize colorama
init(strip=not sys.stdout.isatty())

def get_current_ip():
    """Get the current public IP address."""
    try:
        response = requests.get('https://ipcurl.net/n', verify=False)
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error getting IP address: {e}")
        sys.exit(1)

def load_aws_config():
    """Load AWS configuration from the .config file."""
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    config_file = f"{script_name}.config"
    return dotenv_values(config_file)

def ec2_create_client(config):
    """Create and return an EC2 client."""
    return boto3.client('ec2',
                        region_name=config['AWS_REGION'],
                        aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

def rds_create_client(config):
    """Create and return an EC2 client."""
    return boto3.client('rds',
                        region_name=config['AWS_REGION'],
                        aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

def ec2_update_security_groups(ec2_client, current_ip):
    """Update security groups for all EC2 instances."""
    instances = ec2_client.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance['SecurityGroups']:
                ec2_update_security_group(ec2_client, sg['GroupId'], current_ip)

def ec2_update_security_group(ec2_client, group_id, current_ip):
    """Update a specific security group with the current IP."""
    try:
        sg = ec2_client.describe_security_groups(GroupIds=[group_id])['SecurityGroups'][0]
        for permission in sg['IpPermissions']:
            if permission['IpProtocol'] == 'tcp' and permission['FromPort'] in [22, 81, 5000]:
                ec2_client.revoke_security_group_ingress(
                    GroupId=group_id,
                    IpPermissions=[permission]
                )
                ec2_client.authorize_security_group_ingress(
                    GroupId=group_id,
                    IpProtocol='tcp',
                    FromPort=permission['FromPort'],
                    ToPort=permission['ToPort'],
                    CidrIp=f"{current_ip}/32"
                )
        print(f"Updated security group: {group_id}")
    except Exception as e:
        print(f"Error updating security group {group_id}: {e}")

def rds_update_security_groups(rds_client, ec2_client, current_ip):
    """Update security groups for RDS instances."""
    try:
        instances = rds_client.describe_db_instances()
        for instance in instances['DBInstances']:
            for sg in instance['VpcSecurityGroups']:
                sg_id = sg['VpcSecurityGroupId']
                sg_info = ec2_client.describe_security_groups(GroupIds=[sg_id])
                
                for rule in sg_info['SecurityGroups'][0]['IpPermissions']:
                    if rule['IpProtocol'] == 'tcp' and 5432 in range(rule['FromPort'], rule['ToPort'] + 1):
                        for ip_range in rule['IpRanges']:
                            if ip_range['CidrIp'].endswith('/32'):
                                ec2_client.revoke_security_group_ingress(
                                    GroupId=sg_id,
                                    IpProtocol='tcp',
                                    FromPort=5432,
                                    ToPort=5432,
                                    CidrIp=ip_range['CidrIp']
                                )
                                
                                ec2_client.authorize_security_group_ingress(
                                    GroupId=sg_id,
                                    IpProtocol='tcp',
                                    FromPort=5432,
                                    ToPort=5432,
                                    CidrIp=f"{current_ip}/32"
                                )
                                print(f"Updated security group {sg_id} with new IP {current_ip}/32")
    except Exception as e:
        print(f"Error updating security groups: {e}")
        sys.exit(1)

def main():
    """Main function to run the script."""
    try:
        # Display ASCII art
        cprint(figlet_format('DynAWSess', font='slant'),
            'cyan', attrs=['bold'])

        current_ip = get_current_ip()
        print(f"Current IP: {current_ip}")

        config = load_aws_config()

        print("EC2 Security groups...")
        ec2_client = ec2_create_client(config)
        ec2_update_security_groups(ec2_client, current_ip)
        print("EC2 Security groups updated successfully!")
        #
        print("RDS Security groups...")
        rds_client = rds_create_client(config)
        rds_update_security_groups(rds_client, ec2_client, current_ip)
        print("RDS Security groups updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()