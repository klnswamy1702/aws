---
service: EKS
category: hands-on
difficulty_levels: [L2, L3, L4]
aws_exam_relevance: [SAA-C03, SAP-C02, DOP-C02]
maturity_tier: core
last_validated_date: 2026-08-29
version: "1.30"
cross_references:
  - overview.md
---

# EKS Hands-on Labs

## Lab 1: Deploy an EKS Cluster with Terraform
**Objective:** Stand up an EKS cluster with managed node groups using the official AWS EKS Terraform module.

<details>
<summary>Step-by-Step Guide</summary>

1. Initialize your Terraform workspace:
```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "my-eks-cluster"
  cluster_version = "1.30"

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets

  eks_managed_node_groups = {
    initial = {
      instance_types = ["m5.large"]
      min_size     = 1
      max_size     = 3
      desired_size = 2
    }
  }
}
```
2. Run `terraform init` and `terraform apply`.
3. Update local kubeconfig:
```bash
aws eks update-kubeconfig --region us-east-1 --name my-eks-cluster
```
</details>

## Lab 2: Configure IRSA for an Application
**Objective:** Grant an application pod read-only access to an S3 bucket using IAM Roles for Service Accounts.

<details>
<summary>Step-by-Step Guide</summary>

1. Create an OIDC provider for your cluster (usually handled by the Terraform module).
2. Create an IAM policy and role for S3 ReadOnly access, establishing a trust relationship with the OIDC provider.
3. Annotate the Kubernetes Service Account:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-reader-sa
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/s3-reader-role
```
4. Deploy a test pod using the `s3-reader-sa` service account and verify access using the AWS CLI inside the pod.
</details>

## Lab 3: Set up Karpenter for Autoscaling
**Objective:** Replace Cluster Autoscaler with Karpenter for faster, provisioner-based scaling.

<details>
<summary>Step-by-Step Guide</summary>

1. Ensure the Karpenter Node Role is created.
2. Install Karpenter via Helm:
```bash
helm upgrade --install karpenter oci://public.ecr.aws/karpenter/karpenter \
  --namespace karpenter --create-namespace \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=${KARPENTER_IAM_ROLE_ARN} \
  --set settings.aws.clusterName=my-eks-cluster
```
3. Create a Karpenter `NodePool` and `EC2NodeClass` YAML configuration to define where and how Karpenter can provision instances.
4. Scale up a deployment to trigger Karpenter provisioning.
</details>

## Lab 4: Implement Calico Network Policies
**Objective:** Restrict traffic to a backend database pod so only the frontend pod can reach it.

<details>
<summary>Step-by-Step Guide</summary>

1. Ensure Calico network policy engine is installed (or use VPC CNI's network policy support).
2. Apply the following policy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-to-backend
  namespace: app
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 5432
```
3. Verify that the frontend pod can connect to the backend, but other pods time out.
</details>

## Lab 5: Deploy App with ALB Ingress Controller
**Objective:** Expose a web application to the internet using an Application Load Balancer.

<details>
<summary>Step-by-Step Guide</summary>

1. Install the AWS Load Balancer Controller using Helm (ensure IRSA is configured).
2. Deploy a sample deployment and service (type `NodePort` or `ClusterIP`).
3. Create an Ingress resource:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```
4. Verify the ALB is created in the AWS Console and access the DNS name.
</details>
