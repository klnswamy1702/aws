---
service: EKS
category: basics
difficulty_levels: [L1, L2]
aws_exam_relevance: [SAA-C03, DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - overview.md
---

# EKS Basics Interview Questions

### Q1: What is Amazon EKS?
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** Amazon Elastic Kubernetes Service (EKS) is a managed service that runs Kubernetes on AWS without requiring the user to install, operate, or maintain the Kubernetes control plane.

<details>
<summary>Detailed Answer</summary>
Amazon EKS provisions and scales the Kubernetes control plane (API servers, etcd) across multiple Availability Zones for high availability. It integrates deeply with AWS services like ALB for load balancing, IAM for authentication, and VPC for networking. Users only manage the data plane (worker nodes) and deployed applications.
</details>

### Q2: What are the components of the EKS Control Plane?
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** The EKS Control Plane consists of the Kubernetes API Server, etcd (key-value store), controller manager, and scheduler, all managed by AWS.

<details>
<summary>Detailed Answer</summary>
When you create an EKS cluster, AWS provisions at least two API servers and three etcd nodes across three Availability Zones. AWS is responsible for patching, scaling, and backing up these components. You cannot SSH into or directly access the control plane nodes.
</details>

### Q3: What is a Kubernetes Namespace?
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** A Namespace is a logical partition within a Kubernetes cluster that provides a scope for names and helps organize and divide cluster resources among multiple users or teams.

<details>
<summary>Detailed Answer</summary>
Namespaces allow you to implement soft multi-tenancy. You can apply Resource Quotas to a namespace to limit CPU and memory usage, and RBAC to restrict who can deploy or view resources within that specific namespace. `default`, `kube-system`, and `kube-public` are standard namespaces.
</details>

### Q4: Explain the difference between a Pod and a Node.
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** A Node is a physical or virtual machine (EC2 instance) that runs Kubernetes workloads. A Pod is the smallest deployable unit in Kubernetes, containing one or more containers that share storage and network resources, and runs on a Node.

### Q5: What is the VPC CNI?
**Level:** L2 | **Category:** networking
**Target Services:** EKS, VPC

> **Quick Answer:** The Amazon VPC CNI plugin assigns a primary or secondary IP address from the AWS VPC directly to a Kubernetes Pod.

<details>
<summary>Detailed Answer</summary>
Unlike overlay networks (like Flannel) that require encapsulation, the VPC CNI allows Pods to have native VPC IP addresses. This means Pods can communicate directly with other AWS services (like RDS) and can be easily routed to by ALBs or connected via Direct Connect, without NAT overhead.
</details>

### Q6: How do you authenticate to an EKS cluster?
**Level:** L2 | **Category:** security
**Target Services:** EKS, IAM

> **Quick Answer:** EKS uses AWS IAM to authenticate users via the `aws-iam-authenticator`. After authentication, Kubernetes RBAC (Role-Based Access Control) is used for authorization.

<details>
<summary>Detailed Answer</summary>
When you run `kubectl`, it executes the AWS CLI to generate a short-lived token using your IAM credentials. The EKS API server intercepts this token, validates it against IAM, maps the IAM user/role to a Kubernetes user/group using EKS Access Entries (or the legacy `aws-auth` ConfigMap), and then evaluates RBAC policies.
</details>

### Q7: What is an EKS Managed Node Group?
**Level:** L2 | **Category:** conceptual
**Target Services:** EKS, EC2

> **Quick Answer:** A Managed Node Group automates the provisioning and lifecycle management of EC2 worker nodes for an EKS cluster.

<details>
<summary>Detailed Answer</summary>
It handles creating the Auto Scaling Group (ASG), joining nodes to the cluster, gracefully draining nodes during termination, and applying rolling updates when upgrading the Kubernetes version or underlying AMI.
</details>

### Q8: What is AWS Fargate for EKS?
**Level:** L2 | **Category:** conceptual
**Target Services:** EKS, Fargate

> **Quick Answer:** AWS Fargate is a serverless compute engine for containers that works with EKS, allowing you to run Pods without managing underlying EC2 instances.

<details>
<summary>Detailed Answer</summary>
With Fargate, you define a Fargate Profile specifying which namespaces and labels should be scheduled on Fargate. EKS automatically provisions a right-sized, isolated compute environment for each Pod. You pay only for the vCPU and memory consumed by the Pod.
</details>

### Q9: What is a Kubernetes Service?
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** A Service provides a stable, static IP address and DNS name to abstract and load-balance traffic across a dynamic set of Pods.

<details>
<summary>Detailed Answer</summary>
Because Pod IPs change frequently (e.g., during scaling or crashes), Services provide reliable networking. Types include:
- **ClusterIP:** Internal only.
- **NodePort:** Exposes a port on every Node.
- **LoadBalancer:** Provisions a cloud provider load balancer (e.g., AWS NLB).
</details>

### Q10: What is an Ingress in Kubernetes?
**Level:** L2 | **Category:** networking
**Target Services:** EKS, ALB

> **Quick Answer:** An Ingress is an API object that manages external L7 (HTTP/HTTPS) access to Services within the cluster, providing URL routing, SSL termination, and name-based virtual hosting.

<details>
<summary>Detailed Answer</summary>
On EKS, you typically use the AWS Load Balancer Controller. When you create an Ingress resource, the controller provisions an Application Load Balancer (ALB) and configures listener rules to route traffic to your Pods based on the Ingress rules.
</details>

### Q11: What is a Deployment?
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** A Deployment provides declarative updates for Pods and ReplicaSets, ensuring a specified number of pod replicas are running and managing rolling updates.

### Q12: How do you scale a Deployment manually?
**Level:** L1 | **Category:** practical
**Target Services:** EKS

> **Quick Answer:** Use the command `kubectl scale deployment <name> --replicas=<number>`.

### Q13: What is HPA (Horizontal Pod Autoscaler)?
**Level:** L2 | **Category:** scaling
**Target Services:** EKS

> **Quick Answer:** HPA automatically scales the number of Pod replicas in a Deployment or StatefulSet based on observed CPU utilization, memory, or custom metrics.

### Q14: How does a Pod request storage in EKS?
**Level:** L2 | **Category:** storage
**Target Services:** EKS, EBS

> **Quick Answer:** A Pod uses a PersistentVolumeClaim (PVC). The EBS CSI driver dynamically provisions an Amazon EBS volume (PersistentVolume) to satisfy the claim.

### Q15: What is a DaemonSet?
**Level:** L2 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** A DaemonSet ensures that a copy of a specific Pod runs on all (or some) Nodes. It is typically used for cluster-wide services like log collection (Fluent Bit) or networking (kube-proxy).

### Q16: What is the purpose of CoreDNS?
**Level:** L2 | **Category:** networking
**Target Services:** EKS

> **Quick Answer:** CoreDNS is the default DNS server in EKS. It allows Pods to discover other Services by translating Service names (e.g., `my-svc.default.svc.cluster.local`) into ClusterIP addresses.

### Q17: How do you view Pod logs?
**Level:** L1 | **Category:** troubleshooting
**Target Services:** EKS

> **Quick Answer:** Run `kubectl logs <pod-name>`. For a multi-container pod, specify the container: `kubectl logs <pod-name> -c <container-name>`.

### Q18: What is a ConfigMap?
**Level:** L1 | **Category:** conceptual
**Target Services:** EKS

> **Quick Answer:** A ConfigMap is an API object used to store non-confidential data in key-value pairs. Pods can consume them as environment variables, command-line arguments, or configuration files in a volume.

### Q19: What is a Kubernetes Secret?
**Level:** L1 | **Category:** security
**Target Services:** EKS

> **Quick Answer:** A Secret is similar to a ConfigMap but designed to hold a small amount of sensitive data such as passwords, OAuth tokens, and SSH keys.

### Q20: What happens if a worker node crashes?
**Level:** L2 | **Category:** architecture
**Target Services:** EKS, EC2

> **Quick Answer:** The EKS control plane notices the Node is `NotReady`. The controller manager reschedules the Pods running on that node to other healthy nodes in the cluster.
