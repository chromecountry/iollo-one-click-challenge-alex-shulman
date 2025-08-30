variable "customer_id" {
  description = "Unique identifier for the customer"
  type        = string
}

variable "region" {
  description = "AWS region for deployment"
  type        = string
}

variable "domain_suffix" {
  description = "Domain suffix for customer subdomains"
  type        = string
  default     = "example.com"
}

variable "load_balancer_dns_name" {
  description = "DNS name of the load balancer"
  type        = string
}

variable "load_balancer_zone_id" {
  description = "Zone ID of the load balancer"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}
