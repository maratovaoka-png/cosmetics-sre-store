output "infrastructure_plan_file" {
  description = "Generated infrastructure plan file"
  value       = local_file.cosmetics_infrastructure_plan.filename
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}