# Azure Deployment Guide for Piston API

This guide covers deploying the Piston API to Azure Container Instances (ACI) or Azure App Service.

## Prerequisites

1. **Azure Account** - Sign up at https://azure.microsoft.com/
2. **Azure CLI** - Install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
3. **Docker** - For building images locally (optional)
4. **Azure Container Registry (ACR)** - For storing Docker images

## Option 1: Azure Container Instances (Recommended)

Azure Container Instances supports privileged containers and should work with isolate.

### Step 1: Install Azure CLI

```bash
# macOS
brew install azure-cli

# Or download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

### Step 2: Login to Azure

```bash
az login
```

### Step 3: Create Resource Group

```bash
az group create --name coding-engine-rg --location eastus
```

### Step 4: Create Azure Container Registry

```bash
# Create ACR (replace 'codingengine' with your unique name)
az acr create --resource-group coding-engine-rg \
    --name codingengine \
    --sku Basic \
    --admin-enabled true
```

### Step 5: Build and Push Docker Image

```bash
# Login to ACR
az acr login --name codingengine

# Build the image
docker build -f Dockerfile.azure -t codingengine.azurecr.io/piston-api:latest .

# Push to ACR
docker push codingengine.azurecr.io/piston-api:latest
```

**OR** use Azure Container Registry Build (no local Docker needed):

```bash
# Build directly in Azure
az acr build --registry codingengine \
    --image piston-api:latest \
    --file Dockerfile.azure .
```

### Step 6: Create Container Instance

```bash
# Get ACR login credentials
ACR_USERNAME=$(az acr credential show --name codingengine --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name codingengine --query passwords[0].value -o tsv)

# Create container instance with privileged mode
az container create \
    --resource-group coding-engine-rg \
    --name piston-api \
    --image codingengine.azurecr.io/piston-api:latest \
    --cpu 2 \
    --memory 4 \
    --registry-login-server codingengine.azurecr.io \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --ports 2000 \
    --ip-address Public \
    --environment-variables PORT=2000 \
    --dns-name-label codingengine-piston \
    --os-type Linux
```

### Step 7: Get Public IP

```bash
az container show --resource-group coding-engine-rg \
    --name piston-api \
    --query ipAddress.ip \
    --output tsv
```

Your API will be available at: `http://codingengine-piston.eastus.azurecontainer.io:2000`

## Option 2: Azure App Service (Alternative)

Azure App Service with containers is easier but may have limitations.

### Step 1-4: Same as above (Create RG, ACR, Build/Push)

### Step 5: Create App Service Plan

```bash
az appservice plan create \
    --name coding-engine-plan \
    --resource-group coding-engine-rg \
    --sku B1 \
    --is-linux
```

### Step 6: Create Web App

```bash
az webapp create \
    --resource-group coding-engine-rg \
    --plan coding-engine-plan \
    --name codingengine-piston \
    --deployment-container-image-name codingengine.azurecr.io/piston-api:latest
```

### Step 7: Configure App Settings

```bash
az webapp config appsettings set \
    --resource-group coding-engine-rg \
    --name codingengine-piston \
    --settings PORT=2000 \
    WEBSITES_PORT=2000 \
    DOCKER_REGISTRY_SERVER_URL=https://codingengine.azurecr.io \
    DOCKER_REGISTRY_SERVER_USERNAME=$ACR_USERNAME \
    DOCKER_REGISTRY_SERVER_PASSWORD=$ACR_PASSWORD
```

### Step 8: Enable Continuous Deployment

```bash
az webapp deployment container config \
    --name codingengine-piston \
    --resource-group coding-engine-rg \
    --enable-cd true
```

## Option 3: Azure Container Apps (Modern Approach)

Azure Container Apps is a newer service that might work well.

### Step 1-4: Same as above

### Step 5: Create Container Apps Environment

```bash
az containerapp env create \
    --name coding-engine-env \
    --resource-group coding-engine-rg \
    --location eastus
```

### Step 6: Create Container App

```bash
az containerapp create \
    --name piston-api \
    --resource-group coding-engine-rg \
    --environment coding-engine-env \
    --image codingengine.azurecr.io/piston-api:latest \
    --target-port 2000 \
    --ingress external \
    --cpu 2 \
    --memory 4Gi \
    --env-vars PORT=2000 \
    --registry-server codingengine.azurecr.io \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD
```

## Important Notes

1. **Privileged Mode**: Azure Container Instances supports privileged containers, which is required for isolate to work.

2. **Port Configuration**: Make sure to set `PORT=2000` and expose port 2000.

3. **Resource Limits**: 
   - Minimum: 2 CPU, 4GB RAM
   - Recommended: 4 CPU, 8GB RAM for better performance

4. **Cost**: 
   - ACI: Pay per second, ~$0.000012/second for 2 CPU, 4GB RAM
   - App Service: ~$13/month for B1 tier
   - Container Apps: Pay per use

5. **Networking**: 
   - ACI provides public IP automatically
   - App Service provides HTTPS endpoint
   - Container Apps provides HTTPS by default

## Testing

After deployment, test the API:

```bash
# Get the URL
API_URL="http://codingengine-piston.eastus.azurecontainer.io:2000"

# Test runtimes
curl $API_URL/api/v2/runtimes

# Test execution
curl -X POST $API_URL/api/v2/execute \
    -H "Content-Type: application/json" \
    -d '{"language":"python","version":"3.12.0","files":[{"content":"print(\"Hello\")"}],"stdin":""}'
```

## Updating the Deployment

To update after code changes:

```bash
# Rebuild and push
az acr build --registry codingengine \
    --image piston-api:latest \
    --file Dockerfile.azure .

# Restart container (ACI)
az container restart --resource-group coding-engine-rg --name piston-api

# Or for App Service, it auto-updates with continuous deployment
```

## Troubleshooting

1. **Check logs**:
   ```bash
   az container logs --resource-group coding-engine-rg --name piston-api
   ```

2. **Check if container is running**:
   ```bash
   az container show --resource-group coding-engine-rg --name piston-api
   ```

3. **If isolate fails**: Make sure you're using Azure Container Instances (not App Service) as it supports privileged mode.

