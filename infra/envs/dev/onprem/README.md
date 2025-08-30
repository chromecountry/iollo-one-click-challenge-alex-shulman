# On-Premise Deployment

Local Kubernetes cluster setup for customer isolation and testing.

## Purpose

This directory contains tools for creating isolated local Kubernetes clusters using [kind](https://kind.sigs.k8s.io/) (Kubernetes in Docker). Each customer gets their own cluster to simulate the customer-isolated environments that would be provisioned in a real cloud deployment.

## Quick Start

```bash
# Bootstrap cluster for a customer
./bootstrap.sh acme-corp

# Or using environment variable
CUSTOMER=startup-co ./bootstrap.sh
```

## What It Does

The bootstrap script:

1. **Creates isolated cluster** - Each customer gets `customer-<name>` cluster
2. **Sets up namespace** - Customer-specific namespace with labels
3. **Applies RBAC** - Basic role-based access control for isolation
4. **Configures kubectl** - Updates kubeconfig for easy access

## Cluster Architecture

```
┌─────────────────────────────────────┐
│ kind Cluster: customer-<name>       │
├─────────────────────────────────────┤
│ • 1x Control Plane Node             │
│ • 2x Worker Nodes                   │
│ • Customer namespace                │
│ • Isolated networking              │
└─────────────────────────────────────┘
```

## Real vs Local

| Aspect | Local (kind) | Production Cloud |
|--------|-------------|------------------|
| **Isolation** | Docker containers | Separate VPCs/clusters |
| **Scaling** | Limited to host | Auto-scaling groups |
| **Networking** | Bridge networks | VPC, subnets, load balancers |
| **Storage** | Host filesystem | EBS, EFS, persistent volumes |
| **DNS** | Local only | Route53, real domains |

## Commands

```bash
# List all customer clusters
kind get clusters

# Switch to customer cluster
kubectl config use-context kind-customer-<name>

# View customer resources
kubectl get all -n <customer-name>

# Delete customer cluster
kind delete cluster --name customer-<name>
```

## Prerequisites

- Docker Desktop or Docker Engine
- kubectl
- kind (`brew install kind` or see [installation guide](https://kind.sigs.k8s.io/docs/user/quick-start/))

## Limitations

This is a **development/testing approximation** of real customer isolation. In production:

- Clusters would be provisioned in cloud (EKS, GKE, AKS)
- Full network isolation with VPCs and security groups
- Persistent storage and backup solutions
- Production monitoring and logging
- Certificate management and HTTPS termination
- Auto-scaling and high availability
