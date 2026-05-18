variable "project_name" {
  description = "Name of the SRE project"
  type        = string
  default     = "Online Cosmetics Store"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "local-sre-simulation"
}