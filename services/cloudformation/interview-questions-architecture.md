---
service: CloudFormation
category: Management & Governance
difficulty_levels: L4
aws_exam_relevance: Solutions Architect Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudformation/overview.md
---

# CloudFormation Interview Questions: Architecture

### Q1: You are designing an IaC strategy for a heavily regulated financial institution. They require strict segregation of duties: Developers can write templates, but Security must approve any IAM roles created, and Operations must review any stateful data stores (RDS). How do you enforce this natively with CloudFormation?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudFormation, IAM, Service Catalog

> **Quick Answer:** Use AWS Service Catalog integrated with CloudFormation. Pre-approve templates as Service Catalog Products and use IAM boundary policies. Alternatively, use CloudFormation Macros/Hooks to validate resources programmatically before deployment.

#### Detailed Answer
To enforce strict compliance at scale:
1. **AWS Service Catalog**: The central team (Security/Ops) authors and reviews CloudFormation templates and publishes them as "Products" in a portfolio. Developers are granted access to launch these products. The products use a Launch Constraint (an IAM role) to provision the resources, meaning developers don't need underlying AWS permissions, they only need permission to use Service Catalog.
2. **CloudFormation Hooks**: Write custom AWS CloudFormation Hooks (using Python/Java) that run synchronously before a resource is created or updated. For example, a hook can inspect the template to ensure all S3 buckets have encryption enabled or that IAM roles don't have wildcard permissions. If the hook fails, the stack deployment fails.
3. **Permissions Boundaries**: Require developers to attach a predefined IAM Permissions Boundary to any IAM roles they create within their templates.

#### Follow-up Questions
- What is the difference between AWS Config rules and CloudFormation Hooks? (Hooks prevent non-compliant resources from being deployed; Config is generally reactive, detecting non-compliance after deployment).

### Q2: A global application requires a multi-region Active-Active architecture with Route 53 latency-based routing. How do you structure the CloudFormation templates and CI/CD pipeline to deploy this reliably?
**Level:** L4 | **Category:** architecture
**Target Services:** CloudFormation, Route 53, CodePipeline

> **Quick Answer:** Decouple the architecture into regional stacks (VPC, App) and global stacks (Route 53, IAM). Use StackSets or a multi-region CI/CD pipeline to deploy the regional stacks concurrently, then deploy the global stack using exported values.

#### Detailed Answer
1. **Template Structure**:
   - `Global-IAM.yaml`: IAM roles, Route 53 Hosted Zones (deployed once in `us-east-1`).
   - `Regional-Base.yaml`: VPCs, Subnets (deployed in both `us-east-1` and `eu-west-1`).
   - `Regional-App.yaml`: ALBs, ASGs, DynamoDB Global Tables (deployed in both regions).
2. **Deployment Strategy**:
   - Use **CloudFormation StackSets** targeting the specific regions for the regional templates.
   - Alternatively, use **AWS CodePipeline** with a multi-region setup. The pipeline has a "Deploy-Region1" action and "Deploy-Region2" action running in parallel.
3. **Routing Integration**: The regional stacks create ALBs and output their ARNs/DNS names. A final Custom Resource or SDK script in the pipeline updates the Route 53 Latency Records to point to the newly deployed regional ALBs.

#### Follow-up Questions
- How do you handle DynamoDB Global Table provisioning in CloudFormation without race conditions? (Define the Global Table in a single template deployed to one region; CFN handles the replication automatically).
