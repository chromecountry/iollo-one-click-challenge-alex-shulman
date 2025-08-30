# One-Click Deployment System

A complete one-click deployment system prototype built for **iollo**, demonstrating infrastructure automation, CI/CD pipelines, and AI-powered biomedical data analysis. This system provisions customer-isolated environments and performs comprehensive analysis on biomarker research data.

## Quickstart

Get the system running in under 5 minutes:

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd iollo-one-click-challenge/infra/envs/dev

# 2. Configure environment
cp .env.example .env
# Edit .env to add your GITHUB_TOKEN and ANTHROPIC_API_KEY

# 3. Validate infrastructure (requires Terraform)
cd infra/envs/dev && terraform init && terraform validate && cd ../../../

# 4. Run demo deployment
cd infra/envs/dev/automation && make demo

# 5. Test one-click customer deployment
./cli/deploy-customer.sh --customer acme --region us-east-1 --size small

# 6. Run biomedical data analysis  
cd infra/envs/dev/automation && make analyze

# 7. Test on-premise cluster (requires Docker + kind)
make onprem CUSTOMER=acme
```

## Repository Structure

```
iollo-one-click-challenge/
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT license
├── infra/
│   └── envs/dev/               # Development environment
│       ├── .env.example        # Environment template
│       ├── *.tf                # Terraform infrastructure
│       ├── .github/workflows/  # CI/CD pipeline
│       ├── scripts/            # Infrastructure automation
│       ├── cli/                # One-click deployment CLI
│       ├── onprem/             # Kubernetes cluster setup
│       ├── analysis/           # AI data analysis pipeline
│       └── automation/         # Makefile orchestration
```

## Key Features

### 🚀 **One-Click Customer Deployment**
- Automated infrastructure provisioning with Terraform
- Customer-isolated environments with proper RBAC
- GitHub Actions CI/CD pipeline integration
- DNS and SSL certificate automation (stubbed)

### 🧬 **Biomedical Data Analysis Pipeline**
Quinn-inspired AI analysis system that processes:
- **600+ biomarkers** per study (matching iollo's blood testing platform)
- **Drug discovery research** compressed from years to days
- **Healthspan analysis** with therapeutic potential scoring
- **Multimodal research** data with visualization dashboards

### 🏗️ **Infrastructure Automation**
- **Terraform modules**: networking, compute, DNS management
- **AWS-ready**: VPCs, subnets, load balancers, security groups
- **Scalable sizing**: small/medium/large instance configurations
- **Cost optimization**: automated resource sizing and cleanup

## Coding Agent Usage

Key Claude prompts that accelerated this 2-hour build:

1. **"Create Terraform module skeletons for networking, compute, and DNS with AWS best practices"**
   - Generated complete VPC setup with proper subnetting and security groups
   - Automated load balancer configuration with health checks

2. **"Build a GitHub Actions workflow for infrastructure deployment with proper validation and testing stages"**
   - Created comprehensive CI/CD pipeline with terraform plan/apply
   - Integrated smoke testing and deployment verification

3. **"Generate a Python data analysis pipeline with pandas, matplotlib for biomedical research data including correlation analysis and executive reporting"**
   - Built 5-component analysis system with statistical analysis
   - Created professional visualizations and automated report generation

4. **"Design a one-click CLI deployment script with GitHub API integration and proper error handling"**
   - Implemented workflow triggering with parameter validation
   - Added fallback mechanisms and comprehensive logging

5. **"Create Kubernetes kind cluster setup for customer isolation with proper RBAC and namespace management"**
   - Generated cluster bootstrap with customer-specific isolation
   - Implemented proper service accounts and role bindings

## Requirements

### Core Dependencies
- **Terraform** >= 1.0 (infrastructure automation)
- **Python 3.11+** with pip (data analysis pipeline)
- **Git** (version control and CLI deployment)
- **Bash** (automation scripts)

### Optional Dependencies
- **GitHub CLI** (`gh`) - for enhanced deployment features
- **Docker + kind** - for on-premise cluster simulation
- **AWS CLI** - for real infrastructure deployment (when enabled)

### Environment Setup
Create `.env` file with required API keys:

```bash
# GitHub token for workflow API access and CLI operations
# Create at: https://github.com/settings/tokens
# Required scopes: repo, workflow
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic API key for LLM agents in analysis pipeline  
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Analysis Results

The biomedical analysis pipeline processes iollo-relevant research data:

- **Study Types**: drug_discovery, healthspan_analysis, pharma_collab, blood_testing, multimodal_research
- **Key Metrics**: processing time (0.3-4.5 days), discovery rate (71-99%), therapeutic potential
- **Insights**: Strong correlation between data quality and discovery rate, blood testing fastest processing
- **Output**: Executive reports, correlation heatmaps, distribution plots, scatter analysis

## Assumptions & Limitations

### Mock/Development Mode
- **Infrastructure**: Terraform plans only, no real AWS resources created
- **DNS/SSL**: AWS CLI commands stubbed out for demonstration
- **CI/CD**: GitHub workflows present but use mock deployment scripts
- **Data**: Sample biomedical research data generated for analysis

### Production Considerations
For real deployment, this system would need:
- Actual AWS credentials and resource provisioning
- Real DNS domain management and certificate validation
- Production monitoring, logging, and alerting
- Secrets management (AWS Secrets Manager/HashiCorp Vault)
- Multi-environment promotion (dev → staging → prod)
- Backup and disaster recovery procedures

## Demo Scenarios

### Scenario 1: New Customer Onboarding
```bash
# Provision complete environment for new pharma customer
./cli/deploy-customer.sh --customer novartis --region eu-west-1 --size large
```

### Scenario 2: Biomedical Research Analysis
```bash
# Run Quinn-inspired analysis on research data
make analyze
# View results: analysis/outputs/[timestamp]/executive_report.md
```

### Scenario 3: On-Premise Deployment
```bash
# Setup isolated customer environment locally
make onprem CUSTOMER=stanford-research
kubectl get pods -n stanford-research
```

## Development

Built in **2 hours** as a coding challenge demonstration, showcasing:
- Rapid prototyping with AI-assisted development
- Infrastructure-as-Code best practices
- Modern CI/CD pipeline design
- Data analysis automation
- Production-ready project structure