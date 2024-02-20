# 5gla-camera-integration-script

# Setup

## Use local camera

Define settings for the local network as follows:

Ethernet: 192.168.1.40/24
Gateway:192.168.1.83
Camera: 192.168.1.83

## Virtual Environment (Conda)

Create your virtual environment to ensure that you have the same python version and packages installed as the other
developers.

```bash
conda create -n 5gla-camera-integration-script python=3.11
conda activate 5gla-camera-integration-script
pip install -r requirements.txt
```

For Windows you could use Anaconda or Miniconda. For Linux you could use Miniconda. There are several installation
guides on the internet.

## Environment variables

To run the test cases and the other parts of the script, you need to define the API key and the API url to access the
5GLa API. You can
set the following environment variables:

| Variable | Description                         |
|----------|-------------------------------------|
| API_KEY  | The API key to access the 5GLa API. |
| API_URL  | The URL to access the 5GLa API.     |

There are currently two stages to access the 5GLa API:

| Stage | URL                             |
|-------|---------------------------------|
| DEV   | https://api.dev.5gla.de/api/v1/ |
| QA    | https://api.qa.5gla.de/api/v1/  |

## Where to find the API key

If you need an API, please have a look at the configuration for the stages. You can find the API key in the private GIT
repository.

| Stage | Link                                                                                                                  |
|-------|-----------------------------------------------------------------------------------------------------------------------|
| DEV   | https://github.com/vitrum-connect/5gla-cluster-config/blob/stages/dev/config/k8s/configmaps/fivegla-api-configmap.yml |
| QA    | https://github.com/vitrum-connect/5gla-cluster-config/blob/stages/qa/config/k8s/configmaps/fivegla-api-configmap.yml  |