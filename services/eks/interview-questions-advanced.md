---
service: EKS
category: advanced
difficulty_levels: [L3, L4]
aws_exam_relevance: [SAP-C02, DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - overview.md
---

# EKS Advanced Interview Questions

### Q1: Explain in detail how IRSA (IAM Roles for Service Accounts) works under the hood.
**Level:** L3 | **Category:** security
**Target Services:** EKS, IAM, STS

> **Quick Answer:** IRSA links a Kubernetes Service Account to an AWS IAM Role via an OIDC provider. It injects a secure token into the Pod, which the AWS SDK uses to assume the IAM Role.

<details>
<summary>Detailed Answer</summary>
1. EKS hosts a public OIDC discovery endpoint.
2. An IAM Identity Provider is created in AWS pointing to this endpoint.
3. An IAM Role is created with a Trust Policy allowing `sts:AssumeRoleWithWebIdentity` only if the `sub` matches `system:serviceaccount:<namespace>:<sa-name>`.
4. The Kubernetes Service Account is annotated with `eks.amazonaws.com/role-arn`.
5. When a Pod using this SA starts, the EKS Pod Identity Webhook intercepts the request and injects AWS-specific environment variables (e.g., `AWS_WEB_IDENTITY_TOKEN_FILE`) and mounts the OIDC token via a projected volume.
6. The AWS SDK in the application automatically reads this token and calls STS to get temporary AWS credentials.
</details>

### Q2: How do EKS Pod Identities differ from IRSA?
**Level:** L3 | **Category:** security
**Target Services:** EKS, IAM

> **Quick Answer:** Pod Identities remove the need to manage OIDC identity providers per cluster. Instead, an EKS agent runs on the nodes to broker credentials directly from AWS based on cluster-level identity mappings.

<details>
<summary>Detailed Answer</summary>
EKS Pod Identities simplify IAM mapping across many clusters. You use the EKS API to map an IAM Role directly to a Service Account in a specific namespace. The EKS Pod Identity Agent (a DaemonSet) runs on the worker nodes and proxies credential requests to AWS, abstracting away the OIDC federation complexity.
</details>

### Q3: What is the difference between Cluster Autoscaler and Karpenter?
**Level:** L3 | **Category:** scaling
**Target Services:** EKS, Karpenter

> **Quick Answer:** Cluster Autoscaler relies on AWS Auto Scaling Groups (ASGs) and scales based on node groups, while Karpenter bypasses ASGs, communicating directly with EC2 Fleet APIs to provision right-sized nodes in seconds based on pending pod requirements.

<details>
<summary>Detailed Answer</summary>
- **Cluster Autoscaler (CA):** Evaluates pending pods against existing ASGs. If an ASG can satisfy the pod, CA increments the desired count. It is slow and inflexible (requires many ASGs to support different instance types).
- **Karpenter:** A custom controller that looks at pod resource requests (CPU, memory, GPU) and node selectors. It calculates the optimal EC2 instance type and provisions it directly. Karpenter is faster, reduces costs by right-sizing instances dynamically, and actively consolidates underutilized nodes.
</details>

### Q4: How do you troubleshoot a VPC CNI IP exhaustion issue?
**Level:** L3 | **Category:** troubleshooting/networking
**Target Services:** EKS, VPC

> **Quick Answer:** When subnets run out of IPs, pods fail to start. Troubleshoot by checking subnet capacity and configuring custom networking (secondary CIDR) or prefix delegation to increase IP density per node.

<details>
<summary>Detailed Answer</summary>
The AWS VPC CNI allocates actual VPC IPs to pods.
1. Check `kubectl get pods -A | grep -i fail`.
2. Inspect AWS Console VPC subnets for "Available IPs".
3. **Fix 1 (Prefix Delegation):** Set `ENABLE_PREFIX_DELEGATION=true` in the `aws-node` DaemonSet. Instead of requesting single IPs per ENI, the CNI requests /28 prefixes (16 IPs), dramatically increasing the number of pods per node.
4. **Fix 2 (Custom Networking):** Add a secondary CIDR (e.g., 100.64.0.0/10) to the VPC. Configure the CNI `ENIConfig` to provision pod ENIs in subnets using this secondary, non-routable CIDR, preserving primary VPC IPs.
</details>

### Q5: Describe an EKS upgrade strategy with zero downtime.
**Level:** L4 | **Category:** practical
**Target Services:** EKS

> **Quick Answer:** Ensure high availability of workloads (PDBs, HPA, anti-affinity), upgrade the control plane, upgrade cluster add-ons, and perform a rolling update of worker nodes.

<details>
<summary>Detailed Answer</summary>
1. **Pre-flight:** Check for deprecated APIs using `pluto`. Update Helm charts/manifests.
2. **Control Plane:** Upgrade via the AWS Console or Terraform. This is zero downtime as AWS manages HA.
3. **Add-ons:** Update VPC CNI, CoreDNS, and kube-proxy to versions compatible with the new cluster version.
4. **Data Plane:**
   - Create a new Managed Node Group with the new Kubernetes version AMI.
   - Cordon and gracefully drain the old Node Group. Pod Disruption Budgets (PDBs) ensure sufficient replicas remain running.
   - Delete the old Node Group once empty.
</details>

### Q6: How does Calico Network Policy differ from AWS Security Groups in EKS?
**Level:** L3 | **Category:** networking/security
**Target Services:** EKS, VPC

> **Quick Answer:** Security Groups operate at the EC2 ENI level (node level, or pod level with Security Groups for Pods), while Calico operates at the Kubernetes abstraction level (L3/L4) using IPtables/eBPF to filter traffic between pods regardless of which node they reside on.

### Q7: What are Pod Disruption Budgets (PDB)?
**Level:** L3 | **Category:** architecture
**Target Services:** EKS

> **Quick Answer:** A PDB is a Kubernetes resource that limits the number of concurrently disrupted pods in a deployed application during voluntary disruptions (like node draining or upgrades), ensuring HA.

### Q8: How would you configure an HPA to scale based on an external metric (e.g., SQS Queue length)?
**Level:** L3 | **Category:** scaling
**Target Services:** EKS, CloudWatch, SQS

> **Quick Answer:** Deploy the KEDA (Kubernetes Event-driven Autoscaling) operator or the AWS CloudWatch Metrics Adapter to fetch the SQS `ApproximateNumberOfMessagesVisible` metric and feed it to the HPA.

### Q9: Explain how `kube-proxy` works in iptables mode.
**Level:** L3 | **Category:** networking
**Target Services:** EKS

> **Quick Answer:** `kube-proxy` watches the Kubernetes API for Service and Endpoint objects. It creates iptables rules on the worker node to capture traffic destined for a Service ClusterIP and NATs it to one of the healthy backend Pod IPs.

### Q10: What is the AWS Load Balancer Controller and target type `ip` vs `instance`?
**Level:** L3 | **Category:** networking
**Target Services:** EKS, ALB

> **Quick Answer:** `instance` mode routes ALB traffic to NodePorts on the EC2 instances, which then route to the pod. `ip` mode routes traffic directly from the ALB to the Pod's IP address (enabled by VPC CNI), eliminating an extra network hop.

### Q11: How do you enforce Pod Security Standards (PSS) in modern EKS?
**Level:** L3 | **Category:** security
**Target Services:** EKS

> **Quick Answer:** Use the built-in Pod Security Admission (PSA) controller by applying labels (e.g., `pod-security.kubernetes.io/enforce: restricted`) to Namespaces, replacing the deprecated Pod Security Policies (PSP).

### Q12: Why might a pod get `OOMKilled` when it hasn't reached its resource limit?
**Level:** L4 | **Category:** troubleshooting
**Target Services:** EKS

> **Quick Answer:** If the Node itself runs out of memory, the kubelet will evict pods to protect the system. It targets pods lacking resource requests, or pods using more memory than their request, even if under their specific limit.

### Q13: What is the EBS CSI driver, and why is it necessary?
**Level:** L3 | **Category:** storage
**Target Services:** EKS, EBS

> **Quick Answer:** The Container Storage Interface (CSI) driver enables EKS to manage the lifecycle (create, attach, delete) of EBS volumes. It moved out-of-tree from the core Kubernetes code for faster iteration.

### Q14: How do you implement cross-namespace communication restrictions?
**Level:** L3 | **Category:** security
**Target Services:** EKS

> **Quick Answer:** Define a default-deny Network Policy in each namespace that blocks all Ingress. Then, define explicit Network Policies that allow traffic from specific `namespaceSelectors`.

### Q15: How do you handle secrets management in EKS without storing them in etcd?
**Level:** L4 | **Category:** security
**Target Services:** EKS, Secrets Manager

> **Quick Answer:** Use the AWS Secrets and Configuration Provider (ASCP) with the Secrets Store CSI Driver to mount secrets from AWS Secrets Manager directly into the pod as a file, or sync them to Kubernetes Secrets securely.
