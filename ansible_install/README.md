# ChallengeAnsible01

"Who wants some?" Duke Nukem, 1996 
[![N|Solid](https://yt3.ggpht.com/-KI4pTwXOjLs/AAAAAAAAAAI/AAAAAAAAAAA/htvqMgipOWo/s48-c-k-no-mo-rj-c0xffffff/photo.jpg)](https://github.com/h3ct0r/)

## Introduction 
This challenge was implemented and executed from MacOS Yosemite, with the help of: Ansible Up & Running (Lorin Hochstein), Ansible for DevOps (Jeff Geerling), and a big list of several other websites.

## First steps/How to 

- Create a new AWS instance or use Vagrant to create a new VM.
- Install brew if not already installed
- `brew install ansible`
- Clone this repo!
- `cd ChallengeAnsible01/playbooks`
- And then run `ansible-playbook -s -v challenge_full_config.yaml`
- Good to go!

## Scripts

##### load_test.py

> Small application to test load on a WebServer

`python load_test.py --url http://localhost/ --threads 10 --requests 100`

##### parse_access_log.py

> Another small app to parse nginx access log files, and then send a report of the accessed resources

`python parse_access_log.py --log /var/log/nginx/access.log --email-from fromme@gmail.com --email-to tome@gmail.com --smtp-user fromme@gmail.com --smtp-pass 12345`

## Small changelog:

- Create a `playbook` folder to store the playbooks
- Add hosts domains/ip to the `hosts` file
- Create `ansible.cfg` to automate some basic configs to the hosts
- Test if we reach the new host
	`ansible challengeserver -m ping`
- Server reached but remote server shows error '"/bin/sh: 1: /usr/bin/python: not found\r\n"', so we need to install python2.7
- Ran `ansible-playbook -s -v python2.yml` to install python2.7
- Ran `ansible-playbook -s -v nodejs_latest.yml` to install the latest nodejs
- Created the node app in anoter Git project (https://github.com/h3ct0r/ChallengeNodeApp01)
- Modify the project to allow use of several cores with the `cluster` module
- Created a tag on the node project
- Added the tag to the git config on the play (node_app.yml)
- Configured play to use `pm2` as deploy tool of the node app, using `-i max` as a load balancer
- Test play with version=2.0.0 now
- To change revisions of the app only need to change version parameter now. (playing with 1.0.0 and 2.0.0)
- Generated TSL keys for HTTPS:
	`openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -subj /CN=localhost \
        -keyout files/nginx.key -out files/nginx.crt`
- Adding auto respawn to nginx (pm2 does it by default on app crash)
- Added script to test server payload.
	- run: `python load_test.py --threads 30 --requests 300 --url http://localhost/`
- Get server log and begin testing the parsing script `scp -i "../key.pem" user@domain:'/var/log/nginx/access.log' /tmp/`
- Added script to parse and send email to server
- Configured the crontab to run it
- Add new playbook to join all configurations!