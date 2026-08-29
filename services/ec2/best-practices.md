---
service: EC2
category: Compute
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# EC2 Best Practices

## Security Best Practices
- **Use IMDSv2**: Enforce the use of IMDSv2 on all instances to prevent SSRF attacks.
- **Least Privilege IAM Roles**: Attach IAM roles to instances rather than storing long-term AWS credentials on them.
- **Security Groups**: Restrict inbound and outbound traffic. Use security group referencing instead of IP CIDRs where possible.
- **Patch Management**: Use AWS Systems Manager Patch Manager to automate OS patching.

## Reliability Best Practices
- **Auto Scaling**: Use Auto Scaling groups across multiple Availability Zones to ensure fault tolerance.
- **Health Checks**: Configure robust EC2 and ELB health checks.
- **Instance Recovery**: Enable CloudWatch alarm actions to automatically recover instances if system status checks fail.

## Performance Efficiency
- **Right-Sizing**: Continuously monitor CloudWatch metrics (CPU, Memory via agent) and use AWS Compute Optimizer to right-size instances.
- **Enhanced Networking**: Enable ENA for workloads requiring high packet-per-second performance and low latency.
- **Placement Groups**: Use Cluster Placement Groups for tightly coupled HPC workloads.

## Cost Optimization
- **Spot Instances**: Use Spot Instances for stateless, fault-tolerant, or flexible workloads (e.g., CI/CD agents, batch processing).
- **Savings Plans/RIs**: Commit to usage for predictable workloads.
- **Hibernate / Stop**: Automatically stop or hibernate non-production instances during off-hours.
- **Graviton Processors**: Migrate compatible workloads to AWS Graviton (ARM-based) instances for better price-performance.
