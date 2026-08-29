---
service: EKS
category: troubleshooting
difficulty_levels: [L2, L3, L4]
aws_exam_relevance: [DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - overview.md
---

# EKS Common Issues & Troubleshooting

## 1. Node Not Joining Cluster
**Symptoms:** Newly provisioned EC2 instances do not appear when running `kubectl get nodes`.
**Root Causes & Fixes:**
- **IAM Role:** The Node Instance Role is not mapped in the `aws-auth` ConfigMap (legacy) or EKS Access Entries.
- **Network:** Nodes cannot reach the EKS control plane API. Ensure proper security group rules and route tables (NAT Gateway if nodes are in private subnets).
- **User Data:** The bootstrap script `bootstrap.sh` in the user data is missing or failing (common in self-managed nodes).

## 2. Pod Scheduling Failures (Pending State)
**Symptoms:** Pods remain in `Pending` state.
**Root Causes & Fixes:**
- **Resource Exhaustion:** Not enough CPU/Memory available on nodes. Check `kubectl describe pod <pod-name>` for `Insufficient cpu/memory`.
- **Taints/Tolerations:** Pods lack the necessary tolerations for node taints.
- **Node Selectors/Affinity:** Unmatchable node selectors.

## 3. VPC CNI IP Exhaustion
**Symptoms:** Pods fail to create with `FailedCreatePodSandBox` errors; VPC subnets have 0 available IPs.
**Root Causes & Fixes:**
- **Subnet Sizing:** Subnets are too small for the number of pods.
- **Fix:** Enable Custom Networking (CNI) to place pods in a secondary VPC CIDR (e.g., CGNAT range `100.64.0.0/10`), or use Prefix Delegation (`ENABLE_PREFIX_DELEGATION=true`) to pack more IPs onto ENIs.

## 4. IRSA Not Working (IAM Permissions Denied)
**Symptoms:** Pods get `AccessDenied` when interacting with AWS APIs (e.g., S3, DynamoDB) despite having an IAM role configured.
**Root Causes & Fixes:**
- **Trust Policy:** The OIDC trust relationship on the IAM role is misconfigured. Ensure `sts:AssumeRoleWithWebIdentity` is used, and the `aud` and `sub` fields precisely match the Service Account.
- **Service Account Annotation:** The pod's service account lacks the `eks.amazonaws.com/role-arn` annotation.
- **Token Mount:** Verify the projected service account token is successfully mounted in the pod (`/var/run/secrets/eks.amazonaws.com/role-arn`).

## 5. ALB Ingress Controller Issues
**Symptoms:** Ingress resources are created, but the AWS ALB is not provisioned.
**Root Causes & Fixes:**
- **Subnet Tagging:** Subnets lack the required tags (`kubernetes.io/role/elb=1` for public, `kubernetes.io/role/internal-elb=1` for private).
- **IAM Permissions:** The AWS Load Balancer Controller lacks permissions to create ALBs. Verify its IRSA setup.
- **Logs:** Check controller logs: `kubectl logs -n kube-system deployment.apps/aws-load-balancer-controller`.

## 6. DNS Resolution Failures
**Symptoms:** Pods cannot resolve external or internal services.
**Root Causes & Fixes:**
- **CoreDNS Scaling:** CoreDNS pods are under-resourced or insufficient in number. Scale the deployment or use cluster-proportional-autoscaler.
- **Security Groups:** Node security groups block UDP port 53 traffic between nodes.
- **NodeLocal DNSCache:** Implement NodeLocal DNSCache to reduce CoreDNS load and lower latency.

## 7. OOM Kills
**Symptoms:** Pods frequently crash with `OOMKilled` status.
**Root Causes & Fixes:**
- **Memory Limits:** The pod exceeded its defined `resources.limits.memory`. Use tools like Prometheus/Grafana to profile memory usage and adjust limits.
- **Node OOM:** The entire node ran out of memory. Ensure pods have appropriate requests/limits, and check for runaway unmanaged processes on the node.

## 8. Cluster Upgrade Failures
**Symptoms:** EKS control plane upgrade succeeds, but workloads break or add-ons fail.
**Root Causes & Fixes:**
- **Deprecated APIs:** Using removed API versions (e.g., `v1beta1` Ingress in 1.22+). Always run `pluto` before upgrading.
- **Add-on Compatibility:** Add-ons (VPC CNI, CoreDNS, kube-proxy) are severely outdated. Upgrade them explicitly to versions matching the new control plane version.
