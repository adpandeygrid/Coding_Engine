#!/bin/bash
# Quick deployment script for Azure Container Instances

set -e

# Configuration
RESOURCE_GROUP="coding-engine-rg"
ACR_NAME="codingengine"  # Change this to your unique ACR name
CONTAINER_NAME="piston-api"
LOCATION="eastus"
DNS_LABEL="codingengine-piston"  # Change this to your unique DNS label
CPU="2"
MEMORY="4"

echo "🚀 Starting Azure deployment..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure
echo "📝 Logging in to Azure..."
az login

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION || echo "Resource group already exists"

# Create Azure Container Registry
echo "🏗️  Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true || echo "ACR already exists"

# Build and push image
echo "🔨 Building and pushing Docker image..."
az acr build --registry $ACR_NAME \
    --image piston-api:latest \
    --file Dockerfile.azure .

# Get ACR credentials
echo "🔑 Getting ACR credentials..."
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# Create container instance
echo "🚢 Creating container instance..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image ${ACR_NAME}.azurecr.io/piston-api:latest \
    --cpu $CPU \
    --memory ${MEMORY}Gi \
    --registry-login-server ${ACR_NAME}.azurecr.io \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --ports 2000 \
    --ip-address Public \
    --environment-variables PORT=2000 \
    --dns-name-label $DNS_LABEL \
    --os-type Linux \
    --restart-policy Always || \
    az container create \
        --resource-group $RESOURCE_GROUP \
        --name $CONTAINER_NAME \
        --image ${ACR_NAME}.azurecr.io/piston-api:latest \
        --cpu $CPU \
        --memory ${MEMORY}Gi \
        --registry-login-server ${ACR_NAME}.azurecr.io \
        --registry-username $ACR_USERNAME \
        --registry-password $ACR_PASSWORD \
        --ports 2000 \
        --ip-address Public \
        --environment-variables PORT=2000 \
        --dns-name-label $DNS_LABEL \
        --os-type Linux \
        --restart-policy Always

# Get public IP
echo "🌐 Getting public IP..."
PUBLIC_IP=$(az container show --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --query ipAddress.ip \
    --output tsv)

FQDN=$(az container show --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --query ipAddress.fqdn \
    --output tsv)

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Public IP: $PUBLIC_IP"
echo "🌐 FQDN: $FQDN"
echo "🔗 API URL: http://${FQDN}:2000"
echo ""
echo "🧪 Test the API:"
echo "   curl http://${FQDN}:2000/api/v2/runtimes"
echo ""
echo "📊 View logs:"
echo "   az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME"
echo ""

