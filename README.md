# 5gla-camera-integration-script

# Setup

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

## Where to find the API key

If you need an API, please have a look at the configuration for the stages. You can find the API key in the private GIT repository.

| Stage | Link |
| DEV | https://github.com/vitrum-connect/5gla-cluster-config/blob/stages/dev/config/k8s/configmaps/fivegla-api-configmap.yml |
| QA | https://github.com/vitrum-connect/5gla-cluster-config/blob/stages/qa/config/k8s/configmaps/fivegla-api-configmap.yml |