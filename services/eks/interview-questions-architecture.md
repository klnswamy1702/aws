---
service: EKS
category: architecture
difficulty_levels: [L4]
aws_exam_relevance: [SAP-C02, DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - overview.md
---

# EKS Architecture Interview Questions

### Q1: How do you design a multi-cluster EKS strategy for a global application?
**Level:** L4 | **Category:** architecture
**Target Services:** EKS, Route 53, Global Accelerator

> **Quick Answer:** A multi-cluster strategy involves deploying EKS clusters in multiple AWS regions, using Route 53 for latency-based routing or Global Accelerator for anycast IP routing, and syncing workloads using a GitOps controller like ArgoCD.

<details>
<summary>Detailed Answer</summary>
When designing a multi-cluster global architecture:
1. **Traffic Routing:** Use AWS Global Accelerator for a static anycast IP that routes user traffic to the nearest healthy region. Alternatively, use Route 53 latency-based or geolocation routing.
2. **State Management:** Keep clusters stateless where possible. Replicate stateful data using global databases like DynamoDB Global Tables or Aurora Global Database.
3. **Cluster Sync:** Use GitOps (ArgoCD or Flux) tied to a central repository to ensure all clusters run identical workloads.
4. **Service Mesh:** Implement a multi-cluster service mesh (like Istio) if cross-cluster pod-to-pod communication is required.
</details>

### Q2: How do you implement a zero-trust network in EKS using a Service Mesh?
**Level:** L4 | **Category:** security/architecture
**Target Services:** EKS, App Mesh, Istio

> **Quick Answer:** Deploy a service mesh like Istio or AWS App Mesh to enforce mTLS between all pods, using SPIFFE for identity, and implementing strict authorization policies for pod-to-pod communication.

<details>
<summary>Detailed Answer</summary>
A zero-trust architecture on EKS requires that no communication is trusted by default, even inside the cluster.
1. **mTLS:** The service mesh sidecar proxies intercept all traffic and encrypt it via mutual TLS.
2. **Identity:** Each pod receives a cryptographic identity (SPIFFE ID).
3. **Authorization:** Define `AuthorizationPolicies` in Istio to explicitly allow traffic only between specific identities (e.g., frontend can talk to backend, but backend cannot talk to frontend).
4. **Network Policies:** Layer Calico network policies beneath the service mesh to block traffic at the L3/L4 level as defense-in-depth.
</details>

### Q3: Design a GitOps pipeline for managing 100+ EKS clusters across multiple AWS accounts.
**Level:** L4 | **Category:** architecture
**Target Services:** EKS, ArgoCD, Flux

> **Quick Answer:** Implement an ArgoCD ApplicationSet or Flux Kustomization architecture with a hub-and-spoke model, where a central management cluster pushes configurations or distinct ArgoCD instances pull from centralized Git repositories organized by environment and region.

<details>
<summary>Detailed Answer</summary>
1. **Hub and Spoke:** Deploy a "Management" EKS cluster hosting ArgoCD. Register the 100+ target clusters as ArgoCD managed clusters.
2. **ApplicationSets:** Use ArgoCD ApplicationSets to dynamically generate ArgoCD Applications based on cluster labels or Git directory structures.
3. **Repository Structure:** Separate infrastructure code (Terraform for EKS creation) from workload manifests. Use Helm charts or Kustomize to patch environment-specific values.
4. **Security:** Use cross-account IAM roles to allow the management cluster to securely authenticate to the API servers of the spoke clusters.
</details>

### Q4: How do you architect a multi-tenant EKS cluster for isolated development teams?
**Level:** L4 | **Category:** architecture
**Target Services:** EKS, IAM, Fargate

> **Quick Answer:** Use soft multi-tenancy with Kubernetes Namespaces, RBAC, Network Policies, and Resource Quotas. For stricter isolation, map teams to distinct Fargate profiles or separate Node Groups using taints and tolerations.

<details>
<summary>Detailed Answer</summary>
1. **Namespaces:** Assign one or more namespaces per team.
2. **Access Control:** Map AWS IAM roles to Kubernetes RBAC via EKS Access Entries so teams can only manage resources in their namespaces.
3. **Resource Quotas:** Apply `ResourceQuota` and `LimitRange` objects to prevent a single team's workloads from consuming all cluster resources.
4. **Network Isolation:** Implement default-deny Network Policies per namespace, only allowing ingress from an ingress controller or specific trusted namespaces.
5. **Compute Isolation:** If teams run untrusted code, use AWS Fargate (which provides VM-level isolation per pod) or dedicated EC2 Node Groups tainted for specific teams.
</details>

### Q5: What is your disaster recovery (DR) strategy for a mission-critical EKS cluster?
**Level:** L4 | **Category:** architecture
**Target Services:** EKS, Velero, S3

> **Quick Answer:** Rely on GitOps to restore workloads and use Velero to backup and restore stateful Kubernetes resources and persistent volumes to an S3 bucket in a secondary region.

<details>
<summary>Detailed Answer</summary>
1. **Stateless Recovery:** Because the cluster infrastructure is defined in Terraform and workloads in Git (GitOps), rebuilding a cluster and restoring stateless apps simply requires running the CI/CD pipeline against a new region.
2. **Stateful Recovery:** Use Velero configured with an AWS plugin. Velero backups Kubernetes objects (like ConfigMaps and Secrets) and triggers EBS snapshots.
3. **Cross-Region Replication:** Replicate the Velero S3 bucket and EBS snapshots to the DR region.
4. **RTO/RPO:** For strict RTO, maintain a "pilot light" EKS cluster in the secondary region with GitOps actively syncing, keeping the replica count to zero until a failover is declared.
</details>

### Q6: How do you integrate an on-premise Kubernetes cluster with AWS EKS?
**Level:** L4 | **Category:** architecture
**Target Services:** EKS Anywhere, Direct Connect

> **Quick Answer:** Use EKS Anywhere for consistent tooling on-premise, connect the environments using AWS Direct Connect or Site-to-Site VPN, and use the EKS Connector to view the on-premise cluster in the AWS Console.

<details>
<summary>Detailed Answer</summary>
1. **Consistent Plane:** Deploy EKS Anywhere on VMware vSphere or bare metal on-premise. This uses the same EKS Distro as AWS, ensuring version compatibility.
2. **Network Connectivity:** Establish a highly available AWS Direct Connect to allow private communication between on-premise and AWS VPCs.
3. **Management:** Use the EKS Connector (an agent running on-prem) to register the cluster with the AWS EKS console.
4. **Traffic Management:** Use an external DNS provider or Route 53 with inbound/outbound endpoints to route hybrid traffic.
</details>

### Q7: Architect a highly scalable ingress solution for EKS handling millions of requests per minute.
**Level:** L4 | **Category:** architecture
**Target Services:** EKS, ALB, NLB, Nginx Ingress

> **Quick Answer:** Front the cluster with an AWS Network Load Balancer (NLB) routing traffic to an Nginx Ingress Controller deployed as a DaemonSet or highly scaled Deployment, bypassing `kube-proxy` for lower latency.

<details>
<summary>Detailed Answer</summary>
For massive scale, the AWS ALB Ingress Controller can hit AWS API rate limits if managing thousands of ingress rules.
1. **L4 Load Balancing:** Provision an AWS NLB pointing to the EKS worker nodes.
2. **In-cluster Ingress:** Deploy Nginx Ingress Controller or HAProxy inside the cluster. Use `externalTrafficPolicy: Local` to preserve client IPs and reduce network hops.
3. **Scaling the Controller:** Run the ingress controller as a DaemonSet (one per node) or a heavily scaled Deployment with HPA based on custom metrics (like request rate).
4. **Caching & WAF:** Place Amazon CloudFront and AWS WAF in front of the NLB to absorb DDoS attacks and cache static assets.
</details>

### Q8: How would you design logging and observability for a heavily regulated financial EKS environment?
**Level:** L4 | **Category:** architecture/security
**Target Services:** EKS, CloudWatch, OpenSearch, Fluent Bit

> **Quick Answer:** Use Fluent Bit as a DaemonSet for log shipping to Amazon OpenSearch or CloudWatch, enable EKS control plane audit logs, and use AWS X-Ray and Prometheus for distributed tracing and metrics, encrypting all data in transit and at rest.

<details>
<summary>Detailed Answer</summary>
1. **Audit Logs:** Enable EKS Control Plane Logging (API, Audit, Authenticator) sent to CloudWatch Logs. Set a retention policy and export to S3 via Kinesis Firehose for long-term immutable storage (Glacier Vault Lock).
2. **App Logging:** Deploy Fluent Bit as a DaemonSet. Configure it to enrich logs with Kubernetes metadata and forward them to an encrypted Amazon OpenSearch cluster.
3. **Metrics:** Deploy Amazon Managed Service for Prometheus (AMP) to scrape metrics without managing storage infrastructure, visualized via Amazon Managed Grafana.
4. **Compliance:** Ensure all storage backends use customer-managed KMS keys.
</details>

### Q9: Describe an architecture for running ML training workloads on EKS.
**Level:** L4 | **Category:** architecture
**Target Services:** EKS, EC2 GPU, FSx for Lustre

> **Quick Answer:** Use Karpenter to dynamically provision GPU-optimized EC2 instances (e.g., P4/P5), schedule workloads using Kubeflow or Volcano, and mount Amazon FSx for Lustre via the CSI driver for high-performance dataset access.

<details>
<summary>Detailed Answer</summary>
1. **Compute:** Configure Karpenter with NodePools targeting GPU instances. Enable scale-to-zero so expensive GPUs are terminated immediately after training jobs complete.
2. **Storage:** ML training requires high throughput. Use the Amazon FSx for Lustre CSI driver to mount datasets directly into training pods, caching data from S3.
3. **Orchestration:** Deploy Kubeflow or the Volcano batch scheduler to manage complex gang-scheduling requirements for distributed training jobs.
4. **Networking:** For multi-node distributed training, enable EFA (Elastic Fabric Adapter) on the EC2 instances and pods for microsecond latency.
</details>

### Q10: How do you architect a CI/CD pipeline that builds and tests containers securely before deploying to EKS?
**Level:** L4 | **Category:** architecture
**Target Services:** ECR, CodePipeline, EKS

> **Quick Answer:** Use CodeBuild to build images, scan them with ECR basic/enhanced scanning or a 3rd party tool, sign the image with AWS Signer, and use an admission controller (like Kyverno or Gatekeeper) on EKS to reject unsigned or vulnerable images.

<details>
<summary>Detailed Answer</summary>
1. **Build:** Dev commits code. CodePipeline triggers CodeBuild to run unit tests and build the Docker image.
2. **Scan:** Push the image to Amazon ECR. Trigger an ECR Enhanced Scan (Inspector). If Critical/High vulnerabilities are found, fail the pipeline.
3. **Sign:** Use AWS Signer (Notation) to cryptographically sign the approved image.
4. **Deploy:** Update the image tag in the GitOps repository. ArgoCD syncs the cluster.
5. **Enforce:** A Kubernetes Admission Controller (e.g., Kyverno) intercepts the pod creation request, verifies the image signature via AWS Signer, and blocks deployment if the signature is invalid or missing.
</details>
