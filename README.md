# Flask App Deployment

Deploying Python Flask application on AWS EC2 instance. The source repository is [https://github.com/david021903/Lambda_Funct](https://github.com/david021903/Lambda_Funct)

## Description

The Flask app was deployed on AWS EC2 instance using Docker, Docker Compose, and Nginx image as the proxy server.

## Setup on local machine

Before the setup, you must have `git`, `python`, and `docker` installed on your computer.

Clone this repository to your local machine by running the following commands

```bash
git clone https://github.com/praisegee/basic-flask-app.git
```

or using SSH

```bash
git clone git@github.com:praisegee/basic-flask-app.git

```

After the cloning, then run

```bash
cd basic-flask-app
```

```bash
docker compose up --build
```

The above command will spin up a docker container that expose port 80 for incoming request.

## Production server

This application was deploy on AWS EC2 instance with the public IP Address of [<ins>**54.235.51.80**</ins>](http://54.235.51.80/upload)
You can test the endpoints using any client agent. The command below shows the example using cURL.

```bash
curl -X POST -F 'file=@sample_file.txt' http://54.235.51.80/upload
```

The endpoint only accept `POST` HTTP method and the path to the file to upload.
**P.S:** For the above command to work, you will to have a file `sample_file.txt` from the example. The file can be plain text, pdf format, or json file.
