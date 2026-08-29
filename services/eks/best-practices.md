---
service: EKS
category: best-practices
difficulty_levels: [L2, L3, L4]
aws_exam_relevance: [SAP-C02, DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - overview.md
---

# EKS Best Practices

## Cluster Security
- **Private API Endpoints:** Disable public endpoint access or restrict via CIDR blocks. Ensure `endpointPrivateAccess: true`.
- **KMS Envelope Encryption:** Enable KMS envelope encryption for Kubernetes secrets stored in etcd.
- **Audit Logging:** Enable control plane logging (API server, audit, authenticator, controller manager, scheduler) to CloudWatch Logs for compliance and forensics.

## Node Security
- **Use Bottlerocket or EKS Optimized AMIs:** Bottlerocket is a purpose-built OS for containers with a reduced attack surface.
- **IMDSv2:** Require IMDSv2 on all worker nodes to prevent SSRF attacks.
- **No SSH:** Disable SSH access to worker nodes. Use AWS Systems Manager (SSM) Session Manager if host-level access is required.

## Pod Security
- **Least Privilege IAM:** Use IRSA (IAM Roles for Service Accounts) or EKS Pod Identities. Never attach broad IAM roles directly to node EC2 instance profiles.
- **Pod Security Standards (PSS):** Apply Baseline or Restricted profiles via Pod Security Admission (PSA) to prevent privileged escalation, host path mounts, and root user execution.
- **Network Policies:** Implement Calico or VPC CNI Network Policies to enforce default-deny ingress/egress, explicitly allowing required traffic.

## Scaling and Compute
- **Use Karpenter over Cluster Autoscaler:** Karpenter responds faster and provisions exactly what is needed, removing the overhead of managing ASGs.
- **Spot Instances:** Leverage Spot instances for stateless, fault-tolerant workloads via Karpenter or Managed Node Groups. Ensure you handle `SpotInterruption` signals.
- **Fargate for Isolation:** Use AWS Fargate for workloads requiring strong isolation boundaries without node management overhead.

## Cost Optimization
- **Right-Sizing:** Use tools like Kubecost to gain visibility into per-namespace and per-deployment costs.
- **Requests vs. Limits:** Always set CPU and memory requests. Carefully consider limits (avoid CPU limits if latency is a concern, but always set memory limits to prevent OOM cascading failures).
- **Scale Down:** Implement scale-to-zero for non-production environments during off-hours using tools like KEDA or custom cron jobs.

## Upgrade Strategy
- **Infrastructure as Code:** Always use Terraform, CloudFormation, or CDK to manage cluster state and upgrades.
- **Blue/Green or In-Place:** Understand your risk appetite. In-place upgrades are fully supported, but Blue/Green cluster replacements offer a cleaner fallback mechanism for critical workloads.
- **Check Deprecations:** Always run `pluto` or `kubent` to check for deprecated APIs before initiating a control plane upgrade.

## Multi-Tenancy
- **Soft Multi-Tenancy:** Use namespaces, RBAC, Network Policies, and Resource Quotas to isolate teams within the same cluster.
- **Hard Multi-Tenancy:** Use separate clusters or AWS Fargate profiles to enforce stronger virtualization boundaries between untrusted workloads.
