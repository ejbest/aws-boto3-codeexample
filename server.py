# Create Instance Version 1
# DevOps Testing: EJ Best erich.ej.best@gmail.com
# November 8, 2020
#
# Currently designed to deploy "a Linux AWS EC2 instance with two volumes and two users"
# - see accompaning server.yaml

import boto3
import yaml
import time
import subprocess

with open(r'server.yaml') as file:
    # Reading file server.yaml setting up EC2
    try:
        # bash commands for user/group
        # adding ssh config
        print("Loading yaml file ...")
        myfile = yaml.safe_load(file)

        print("Creating userdata script ...")
        script = "#!/bin/bash"
        script += "\n" + "groupadd "+ myfile["server"]["GroupName"]
        for user in myfile["server"]["users"]:
            script += "\n" + "adduser " + user["login"]
            script += "\n" + "usermod -a -G  " + myfile["server"]["GroupName"] + " "+ user["login"]
            script += "\n" + "mkdir -p /home/"+user["login"]+"/.ssh"
            with open(user["ssh_key"], 'r') as key:
                k = key.read()
                print(k)
                # clean up bad elements in key
                script += "\n" + "echo " + '"{}"'.format(k) + " >> /home/" + user["login"] +"/.ssh/authorized_keys"
        
        print("Creating block store ...")
        blockStore = []
        # mount volumes and assign access
        for device in myfile["server"]["volumes"]:
            script += "\n" + "mkdir -p " + device["mount"]
            script += "\n" + "mkfs -t " + device["type"] + " " + device["device"]
            script += "\n" + "mount " + device["device"] + " " + device["mount"]
            script += "\n" + "chgrp "+ myfile["server"]["GroupName"] + " " + device["mount"]
            script += "\n" + "chmod "+ device["permission"] + " " + device["mount"]
            blockStore.append({
                    'DeviceName': device["device"],
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': device["size_gb"],
                        'VolumeType': 'gp2'
                    },
                })
        script += "\n" + "service sshd restart"
        print("Deploying EC2 instance ...")
        # create ec2 in Region in server.yaml
        client = boto3.client('ec2', region_name=myfile["server"]["Region"])

        # print(script)
        filters = [{'Name':'tag:Name', 'Values':[myfile["server"]["TagName"]]}]
        response = client.describe_instances(Filters=filters)

        print("terminating already running instances...")
        instanceids = []
        for i in range(0,len(response['Reservations'])):
            state = response['Reservations'][i]['Instances'][0]['State']['Name']
            if state == "running":
                print("Got running instance ... Terminating ...")
                instanceid = response['Reservations'][i]['Instances'][0]['InstanceId']
                instanceids.append(instanceid)

        print(instanceids)
        if len(instanceids) != 0 :
            response = client.terminate_instances(
                InstanceIds=instanceids,
                DryRun=False
            )
        time.sleep(20)
        print("Terminated running instances ...")

        # Run the Instance(s)
        response = client.run_instances(
            BlockDeviceMappings=blockStore,
            UserData=script,
            ImageId=myfile["server"]["ImageId"],
            InstanceType=myfile["server"]["instance_type"],
            MaxCount=myfile["server"]["max_count"],
            MinCount=myfile["server"]["min_count"],
            Monitoring={
                'Enabled': False
            },
            SecurityGroupIds=[
                myfile["server"]["SecurityGroup"]
            ],
            TagSpecifications = [
                {
                    'ResourceType': 'instance', 'Tags': [
                        {
                            'Key': 'Name',
                            'Value': myfile["server"]["TagName"]
                        },
                    ]
                }
            ]
        )
        # print(response)
        print("waiting for instance to start ...")
        time.sleep(60)

        filters = [{'Name':'tag:Name', 'Values':[myfile["server"]["TagName"]]}]
        response = client.describe_instances(Filters=filters)

        for i in range(0,len(response['Reservations'])):
            state = response['Reservations'][i]['Instances'][0]['State']['Name']
            if state == "running":
                print("Got running instance ...")
                dns = response['Reservations'][i]['Instances'][0]['PublicDnsName']
                print("Getting instance dns")
                print(dns)

                print(" ")
                print("user1 & user2 Writing to volumes ...")
                user1_write_response = subprocess.check_output('ssh -i "key-foo-bar-tmp/user1" -o StrictHostKeyChecking=no user1@{} "touch /awesome-ext4/testfile" '.format(dns),shell=True)
                user2_write_response = subprocess.check_output('ssh -i "key-foo-bar-tmp/user2" -o StrictHostKeyChecking=no user2@{} "touch /awesome-xfs-data/testfile" '.format(dns),shell=True)

                print("user1 & user2 Reading from volumes ...")
                user1_read_response = subprocess.check_output('ssh -i "key-foo-bar-tmp/user1" -o StrictHostKeyChecking=no user1@{} "ls /awesome-ext4/" '.format(dns),shell=True)
                user2_read_response = subprocess.check_output('ssh -i "key-foo-bar-tmp/user2" -o StrictHostKeyChecking=no user2@{} "ls /awesome-xfs-data/" '.format(dns),shell=True)
                print(" ")
                print("user1 found in /awesome-ext4/", user1_read_response.decode("utf-8"))
                print("user2 found in /awesome-xfs-data/", user2_read_response.decode("utf-8"))
                print(" ")
                print("Success: created host, volumes, users; those 3 points tested ")

            else:
                pass

    # along with any exception; print error
    except yaml.YAMLError as exc:
        print(exc)
