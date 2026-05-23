# Instructions:
#  1. create an EC2 instance
 # EC2 instance details : 
 # AMI : ubuntu 22.04 LTS
 # Instance type : t2.micro


#  2. Connect to the EC2 instance
 #ssh -i "key.pem" ubuntu@<ec2-ip-address>

#  3. Run the following commands
 #  a. sudo apt-get update
 #  b. sudo apt-get install -y docker.io
 #  c. sudo systemctl start docker
 #  d. sudo systemctl enable docker
 #  e. sudo usermod -aG docker $USER
 #  f. exit
 
#  4. Restart a new connection to EC2 instance
#  5. Run the following commands
 #  a. docker pull tweakster24/insurance-premium-api:latest
 #  b. docker run -p 8000:8000 tweakster24/insurance-premium-api

#  6. change security group settings
#  7. Check the API 
#  8. Change the frontend code