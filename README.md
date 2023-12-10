# EJ Best: Coding Exercise - DevOps Engineer #

This script when run; will create an EC2 with 2 volumes and 2 users in a single step execution.  If you are able to follow the steps; you can see the test function or my contact details are below.

**Base Requirements**
 <br>
-  Linux or Mac workstation or Linux server
-  AWS Command Line and Account <br>
    https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html<br>
-  Python3 & Pip3 3.5  or later <br>
-  pip3 install boto3<br>
-  pip3 install pyyaml<br>
-  git client installed 

**Steps suggested to make run** 
1. Go to a command line of your workstation<br>
- script was tested on Linux and Mac
<br>

2. Clone the files from git<br><br>
    git clone https://github.com/ejbest/codeexample.git<br>
<br>

3. Go to the folder that was just created<br><br>
    cd codeexample<br>
<br>

4. Execute script provide<br><br>
    ./run.sh
<br>

5. Review Console Output
-  Details showing success or fail
-  See the Deploy to virtual machine
-  Script server.py will SSH into the instance as user1 and user2
-  There will be actions to write and read on each of two volumes

6. Considering if you have access and knowledge of the AWS console
- Check on the EC2 console in the left column for "Instances"<br>
- You should see your instance with the name "myAwesomeServer"<br>
- By clicking on the InstanceID; then Storage, you will see two volumes under "Block Devices"<br>
<br>

7. In closing 
- For a time savings in research some boto3 points were done in bash<br>
- Extra attention was paid to key handling for dynamic execution<br>
<br>
Please let me know any feedback; if any quesitons arise or if anything was interpreted incorrectly.
<br>


| Contact  | EJ Best
| ------------ | -------------------------------------
| Skype | erich.ej.best
| Email | reach me on linked in for phone / email
| Phone | reach me on linked in for phone / email
| LinkedIn | https://www.linkedin.com/in/ejbest
