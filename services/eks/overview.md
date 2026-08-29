---
service: EKS
category: overview
difficulty_levels: [L1, L2, L3, L4]
aws_exam_relevance: [SAA-C03, SAP-C02, DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - ../vpc/overview.md
  - ../iam/overview.md
---

# Amazon Elastic Kubernetes Service (EKS) Overview

Amazon EKS is a managed Kubernetes service that makes it easy to run Kubernetes on AWS without needing to stand up or maintain your own Kubernetes control plane.

## EKS Architecture
- **Control Plane:** Fully managed by AWS. Runs across multiple Availability Zones to ensure high availability. AWS automatically manages the scaling and health of the API servers and etcd nodes.
- **Data Plane (Worker Nodes):**
  - **Managed Node Groups:** Automates the provisioning and lifecycle management of nodes (Amazon EC2 instances).
  - **Self-Managed Nodes:** You manage the EC2 instances, registering them to the EKS cluster.
  - **AWS Fargate:** Serverless compute for containers. EKS automatically provisions the underlying infrastructure based on pod CPU and memory requirements.

## Networking
- **VPC CNI:** The default networking plugin for EKS. It assigns an IP address from your VPC directly to a Pod, making Pods first-class citizens in the VPC network.
- **Pod Networking:** Every pod gets a routable IP within the VPC, facilitating direct communication without NAT.
- **Calico Network Policies:** While VPC CNI handles routing, Calico (or VPC CNI's native support for network policies) is used to enforce granular network access rules (ingress/egress) at the pod level.

## Identity and Access Management
- **IRSA (IAM Roles for Service Accounts):** Maps AWS IAM roles to Kubernetes Service Accounts using an OIDC identity provider. Allows pods to access AWS resources with least privilege.
- **EKS Pod Identities:** A newer, simplified mechanism for granting AWS permissions to pods without needing complex OIDC federation setup on the cluster.

## EKS Add-ons
- **CoreDNS:** Handles cluster DNS resolution.
- **kube-proxy:** Maintains network rules on nodes.
- **VPC CNI:** Manages pod networking.
- **EBS CSI Driver:** Allows EKS clusters to manage the lifecycle of Amazon EBS volumes for persistent storage.

## Scaling
- **Cluster Autoscaler:** Watches for pods that fail to schedule due to resource constraints and scales the ASG (Auto Scaling Group) up. Scales down when nodes are underutilized.
- **Karpenter:** A flexible, high-performance Kubernetes cluster autoscaler built with AWS. It bypasses ASGs and directly provisions EC2 instances that closely match pod requirements, optimizing cost and scaling speed.

## EKS Blueprints & GitOps
- **EKS Blueprints:** Infrastructure as Code (Terraform/CDK) modules to rapidly bootstrap EKS clusters with operational software (monitoring, ingress, logging).
- **GitOps (Flux/ArgoCD):** Recommended approach for deploying workloads to EKS. Cluster state is defined in Git, and agents (like ArgoCD) continuously reconcile the cluster state with the Git repository.

## Security
- **PSS/PSA (Pod Security Standards / Admissions):** Built-in Kubernetes mechanisms to restrict pod behaviors (e.g., preventing privileged containers).
- **OPA/Gatekeeper:** Policy-as-code engine for advanced, dynamic admission control.
- **Falco:** Threat detection engine that monitors container and node behavior for anomalous activity.

## Service Mesh
- **App Mesh:** AWS-native service mesh for observing and controlling microservices.
- **Istio:** Popular open-source service mesh frequently deployed on EKS for advanced traffic management, mTLS, and observability.

## Hybrid and Edge Deployments
- **EKS Anywhere:** Deploy EKS on your own on-premises infrastructure (vSphere, bare metal).
- **EKS on Outposts:** Run EKS locally on AWS Outposts for ultra-low latency or local data processing requirements.

## Legacy Notes (Day 22 Content)
For legacy configurations, initial EKS setup walkthroughs, basic OIDC configurations, ALB controller deployments, and sample application manifests, refer to the [Day 22 Archive](../../day-22/).
