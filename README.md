# Docker-Backup

Docker-Backup is a unofficial tool to backup your container to cloud.

# Features!
- backup the docker container into cloud
- restore the docker container from cloud
- aws s3 supported

# Installation
  - Python 2.7 or above with pip and pipenv required
  - Aws Simple Storage Service (S3)`*Config`

### Setup Ennvironment
- `$ sudo ./setup`

# Usage
- `$ ./docker-backup {continer Id or name} {backup image name}`
- `$ ./docker-restore {backup image name}`

# Notes
 - `*Config` update your aws s3 bucket details on config.yaml file
