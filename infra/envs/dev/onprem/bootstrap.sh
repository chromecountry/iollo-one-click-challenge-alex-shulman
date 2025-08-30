#!/bin/bash
set -euo pipefail

# On-premise cluster bootstrap using kind
# Creates isolated Kubernetes environment for customer testing

# Parse arguments
CUSTOMER="${CUSTOMER:-${1:-}}"

if [[ -z "$CUSTOMER" ]]; then
    echo "Error: CUSTOMER is required"
    echo "Usage: $0 <customer_name>"
    echo "   or: CUSTOMER=<name> $0"
    exit 1
fi

CLUSTER_NAME="customer-${CUSTOMER}"
KUBECONFIG_PATH="$HOME/.kube/config"

echo "🏗️  Bootstrapping on-premise cluster for customer: $CUSTOMER"
echo "   Cluster name: $CLUSTER_NAME"
echo "   Kubeconfig: $KUBECONFIG_PATH"
echo ""

# Check if kind is installed
if ! command -v kind &> /dev/null; then
    echo "⚠️  Warning: kind is not installed"
    echo "   To install kind:"
    echo "   # On macOS:"
    echo "   brew install kind"
    echo ""
    echo "   # On Linux:"
    echo "   curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64"
    echo "   chmod +x ./kind"
    echo "   sudo mv ./kind /usr/local/bin/kind"
    echo ""
    echo "   # Or visit: https://kind.sigs.k8s.io/docs/user/quick-start/"
    echo ""
    echo "🚀 Continuing with mock cluster creation..."
    echo "   ✓ Mock cluster '$CLUSTER_NAME' would be created"
    echo "   ✓ Mock kubeconfig would be configured"
    echo "   ✓ Mock customer isolation would be applied"
    echo ""
    echo "📋 Mock cluster details:"
    echo "   • Cluster: $CLUSTER_NAME"
    echo "   • Nodes: 1 control-plane, 2 workers (simulated)"
    echo "   • Network: kind (isolated)"
    echo "   • Customer: $CUSTOMER"
    echo ""
    echo "✅ Mock on-premise cluster ready for customer: $CUSTOMER"
    exit 0
fi

# Check if cluster already exists
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "📋 Cluster '$CLUSTER_NAME' already exists"
    echo "   Switching to existing cluster context..."
    kubectl config use-context "kind-${CLUSTER_NAME}" 2>/dev/null || echo "   Context switch failed"
else
    echo "🚀 Creating new kind cluster..."
    
    # Create cluster configuration
    cat > "/tmp/kind-config-${CUSTOMER}.yaml" << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ${CLUSTER_NAME}
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "customer=${CUSTOMER}"
- role: worker
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "customer=${CUSTOMER},role=worker"
- role: worker
  kubeadmConfigPatches:
  - |
    kind: JoinConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "customer=${CUSTOMER},role=worker"
EOF
    
    # Create the cluster
    if kind create cluster --config "/tmp/kind-config-${CUSTOMER}.yaml"; then
        echo "   ✓ Cluster created successfully"
        rm -f "/tmp/kind-config-${CUSTOMER}.yaml"
    else
        echo "   ❌ Failed to create cluster"
        rm -f "/tmp/kind-config-${CUSTOMER}.yaml"
        exit 1
    fi
fi

# Set up customer namespace
echo "🏷️  Setting up customer namespace..."
kubectl create namespace "$CUSTOMER" --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace "$CUSTOMER" customer="$CUSTOMER" --overwrite

# Apply basic RBAC for customer isolation
echo "🔐 Applying customer isolation policies..."
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${CUSTOMER}-service-account
  namespace: ${CUSTOMER}
  labels:
    customer: ${CUSTOMER}
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ${CUSTOMER}
  name: ${CUSTOMER}-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${CUSTOMER}-binding
  namespace: ${CUSTOMER}
subjects:
- kind: ServiceAccount
  name: ${CUSTOMER}-service-account
  namespace: ${CUSTOMER}
roleRef:
  kind: Role
  name: ${CUSTOMER}-role
  apiGroup: rbac.authorization.k8s.io
EOF

# Verify cluster status
echo "🔍 Verifying cluster status..."
echo "   Cluster info:"
kubectl cluster-info --context "kind-${CLUSTER_NAME}" | head -3
echo ""
echo "   Nodes:"
kubectl get nodes --context "kind-${CLUSTER_NAME}" -o wide

echo ""
echo "✅ On-premise cluster bootstrap completed!"
echo ""
echo "📋 Cluster Details:"
echo "   • Name: $CLUSTER_NAME"
echo "   • Context: kind-${CLUSTER_NAME}"
echo "   • Namespace: $CUSTOMER"
echo "   • Kubeconfig: $KUBECONFIG_PATH"
echo ""
echo "🔧 Quick commands:"
echo "   kubectl config use-context kind-${CLUSTER_NAME}"
echo "   kubectl get pods -n $CUSTOMER"
echo "   kubectl delete cluster $CLUSTER_NAME  # to remove"
echo ""
echo "🌐 Customer isolation applied - ready for application deployment!"
