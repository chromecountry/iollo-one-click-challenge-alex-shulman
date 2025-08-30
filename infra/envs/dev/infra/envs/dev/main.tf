# Dev environment - wires together networking, compute, and DNS modules
# MOCK/DRY-RUN ONLY - Safe for terraform validate/plan

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  # Mock/dry-run configuration - no real resources will be created
  default_tags {
    tags = {
      Project     = "one-click-deployment"
      Environment = "dev"
      Customer    = var.customer_id
      ManagedBy   = "terraform"
    }
  }
}

# Networking module
module "networking" {
  source = "../../modules/networking"

  customer_id = var.customer_id
  region      = var.region
  environment = "dev"
}

# Compute module (depends on networking)
module "compute" {
  source = "../../modules/compute"

  customer_id       = var.customer_id
  region            = var.region
  size              = var.size
  environment       = "dev"
  vpc_id            = module.networking.vpc_id
  subnet_ids        = module.networking.public_subnet_ids
  security_group_id = module.networking.security_group_web_id
}

# DNS module (depends on compute for load balancer)
module "dns" {
  source = "../../modules/dns"

  customer_id               = var.customer_id
  region                    = var.region
  environment               = "dev"
  load_balancer_dns_name    = module.compute.load_balancer_dns_name
  load_balancer_zone_id     = module.compute.load_balancer_zone_id
}

# Variables
variable "customer_id" {
  description = "Unique identifier for the customer"
  type        = string
}

variable "region" {
  description = "AWS region for deployment"
  type        = string
}

variable "size" {
  description = "Deployment size (small, medium, large)"
  type        = string
}

# Outputs
output "app_url" {
  description = "Application URL"
  value       = "https://${module.dns.app_domain_name}"
}

output "load_balancer_dns" {
  description = "Load balancer DNS name"
  value       = module.compute.load_balancer_dns_name
}

output "name_servers" {
  description = "Name servers for DNS delegation"
  value       = module.dns.hosted_zone_name_servers
}
