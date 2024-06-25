# Mnist model serving using FastAPI, GKE, and Terraform

## Directory structure

```
├── infra
│   ├── modules
│   │   └── gke_cluster
│   │       ├── main.tf
│   │       ├── output.tf
│   │       └── variables.tf
│   ├── gcp-cred.json
│   ├── production.tf
│   ├── provider.tf
│   ├── terraform.tfvars
│   └── variables.tf
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
├── README.md
└── src
    ├── config
    │   ├── config.yml
    │   └── __init__.py
    ├── core
    │   └── model.py
    ├── dockerfile
    ├── docker_requirements.txt
    ├── entrypoint.sh
    ├── main.py
    ├── models
    │   └── mnist.pt
    └── test_data
```

## Infrastructure Provisioning

1. **Export GCP credentials:**
    Refer https://developers.google.com/workspace/guides/create-credentials

2. **Initialize Terraform:**
    ```sh
    cd infra
    terraform init
    ```

3. **Apply Terraform Configuration:**
    ```sh
    terraform apply
    ```

## Build and push docker image to GCP

1. **Build image:**
    ```sh
    cd src
    docker build -t mnist:latest
    ```

2. **Push the local image to GCP Artifact Registry**
    Refer https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling

3. **Edit deployment.yaml**
    Replace the docker image address in `k8s/deployment.yaml` to the one pushed to GCP Artifact Registry


## Deploy kubernetes cluster

1. **Start services**
    ```sh
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

## Highlights of the implementation
- Uses both normal and spot instances in the GKE cluster. Can be caliberated according to project requirements
- Nvidia Tesla T4 is being used as accelerator
- Infrastructure provisioning using Terraform as IaC ensure versioning and maintainability of the infrastructure
