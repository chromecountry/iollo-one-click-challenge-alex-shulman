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
  validation {
    condition     = contains(["small", "medium", "large"], var.size)
    error_message = "Size must be one of: small, medium, large."
  }
}

variable "vpc_id" {
  description = "ID of the VPC to deploy into"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for deployment"
  type        = list(string)
}

variable "security_group_id" {
  description = "Security group ID for instances"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}
