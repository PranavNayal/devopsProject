variable "aws_region" {
  description = "The AWS Region where resources are deployed"
  type        = string
  default     = "ap-southeast-2"
}

variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
  default     = "taskboard-eks"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.20.0.0/16"
}
