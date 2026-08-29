---
service: Meta
category: Interview Preparation
difficulty_levels: L3-L4
aws_exam_relevance: SAP, DOP
maturity_tier: advanced
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../day-1-to-day-30/day-08.md
  - ../day-1-to-day-30/day-27.md
---

# AWS DevOps Mock Interview Scripts

This document provides 5 complete, 60-minute mock interview simulations designed for L3-L4 (Senior/Lead) DevOps Engineers, Cloud Architects, and SREs. Each simulation includes the exact questions, expected answers, live scenarios, and scoring rubrics.

## Interview 1: DevOps Lead - CI/CD & Infrastructure as Code (60 min)

### Q1: [Opening] Background & Experience (5 min)
**Level:** L3-L4 | **Category:** conceptual
**Target Services:** General

> **Quick Answer:** Briefly walk me through a recent complex deployment pipeline you designed and what challenges you faced.

#### Expected Answer & Scoring
- **Score 5:** Articulates a complex multi-stage pipeline, mentions specific tooling (e.g., CodePipeline, Jenkins, GitLab), addresses security (SAST/DAST), and discusses a specific challenge (e.g., deployment speed, flaky tests) and its resolution.
- **Red Flags:** Focuses only on pushing code, doesn't mention testing or security, cannot articulate a specific technical challenge.

### Q2: [Round 1] CI/CD Pipeline Design (15 min)
**Level:** L3-L4 | **Category:** architecture
**Target Services:** CodePipeline, CodeBuild, CodeDeploy

> **Quick Answer:** Design a CI/CD pipeline for a microservices architecture deployed to Amazon EKS, including automated testing and rollback strategies.

#### Detailed Answer
A strong design should include:
- **Source:** CodeCommit or GitHub, triggering on PRs and merges.
- **Build:** CodeBuild for container image building, running unit tests, and pushing to ECR. Mention image scanning in ECR.
- **Deploy:** GitOps (ArgoCD/Flux) or CodeDeploy for blue/green or canary deployments to EKS.
- **Testing:** Integration tests running against a staging environment.
- **Rollback:** Automated rollbacks triggered by CloudWatch alarms monitoring error rates or latency during deployment.

#### Follow-up Questions
- How do you handle database schema changes in this pipeline?
- How do you ensure secrets are not leaked during the build process?

### Q3: [Round 2] IaC Deep Dive (15 min)
**Level:** L4 | **Category:** conceptual/practical
**Target Services:** CloudFormation, Terraform

> **Quick Answer:** Compare CloudFormation and Terraform for an enterprise multi-cloud strategy. How do you handle state management and drift detection?

#### Detailed Answer
- **Comparison:** CloudFormation is AWS-native, excellent for AWS-only shops, integrates deeply with AWS services. Terraform is cloud-agnostic (via providers), uses HCL, and is preferred for multi-cloud.
- **State Management:** Terraform requires backend state (S3 + DynamoDB for locking). CloudFormation manages state internally.
- **Drift Detection:** CloudFormation has native drift detection. Terraform uses `terraform plan` to detect drift against the state file.

#### Follow-up Questions
- How do you structure Terraform modules for reuse across multiple teams?
- Explain how you would recover a corrupted Terraform state file.

### Q4: [Round 3] Live Troubleshooting (15 min)
**Level:** L3-L4 | **Category:** troubleshooting
**Target Services:** CodeBuild, IAM

> **Quick Answer:** A developer reports that CodeBuild is failing to push a Docker image to ECR with an "Access Denied" error. How do you troubleshoot?

#### Detailed Answer
- Check the IAM role assigned to the CodeBuild project.
- Verify the role has `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:CompleteLayerUpload`, `ecr:InitiateLayerUpload`, and `ecr:PutImage`.
- Check if the ECR repository has a resource-based policy blocking the role.
- Verify the AWS CLI/SDK commands in the `buildspec.yml` to ensure they are targeting the correct region and account.

### Q5: [Round 4] Architecture - Multi-Account CI/CD (10 min)
**Level:** L4 | **Category:** architecture
**Target Services:** AWS Organizations, IAM, CodePipeline

> **Quick Answer:** Design a CI/CD strategy for an organization with separate Development, Staging, and Production AWS accounts.

#### Detailed Answer
- Centralized tooling account hosting the CodePipeline, CodeBuild, and ECR.
- Cross-account IAM roles in Dev, Staging, and Prod accounts that trust the tooling account.
- CodePipeline assumes these cross-account roles to deploy resources (e.g., via CloudFormation or Terraform) into the target accounts.

---

## Interview 2: Senior SRE - Observability & Incident Response (60 min)

### Q1: Observability Strategy (15 min)
**Level:** L4 | **Category:** architecture
**Target Services:** CloudWatch, X-Ray

> **Quick Answer:** How would you design comprehensive observability for a distributed microservices application on AWS?

#### Detailed Answer
- **Metrics:** CloudWatch metrics for infrastructure (CPU, memory) and custom application metrics (business KPIs).
- **Logs:** Centralized logging to CloudWatch Logs or OpenSearch, using structured logging (JSON).
- **Traces:** AWS X-Ray for distributed tracing across microservices to identify bottlenecks.
- **Alerting:** CloudWatch Alarms triggering EventBridge rules, routing to SNS and PagerDuty.

### Q2: Incident Response & Post-Mortem (15 min)
**Level:** L3-L4 | **Category:** process
**Target Services:** General

> **Quick Answer:** Walk me through your incident response process for a critical severity outage.

#### Detailed Answer
- **Triage:** Acknowledge the alert, declare an incident, assign roles (Incident Commander, Scribe, Resolvers).
- **Mitigation:** Focus on restoring service quickly (e.g., rollback, failover), not necessarily finding the root cause immediately.
- **Resolution:** Apply the permanent fix.
- **Post-Mortem:** Blameless review. Identify timeline, root cause (5 Whys), and action items to prevent recurrence.

### Q3: Live Scenario - Production Outage (30 min)
**Level:** L4 | **Category:** troubleshooting
**Target Services:** ALB, EC2, CloudWatch

> **Quick Answer:** Scenario: The ALB is returning 502 Bad Gateway errors. Walk me through your debugging steps.

#### Detailed Answer
1. Check ALB metrics in CloudWatch (`HTTPCode_ELB_502_Count`, `TargetResponseTime`).
2. Check Target Group health status. Are targets failing health checks?
3. If targets are unhealthy, check the EC2 instances. Are they running? Is the application process running?
4. Check security groups. Did someone modify the SG blocking traffic from ALB to EC2?
5. Check application logs via CloudWatch Logs or SSM Run Command. Is the app crashing or OOM?

---

## Interview 3: Cloud Architect - Networking & Security (60 min)

### Q1: Multi-Region Architecture (20 min)
**Level:** L4 | **Category:** architecture
**Target Services:** Route 53, CloudFront, DynamoDB, Aurora

> **Quick Answer:** Design an active-active multi-region architecture for a high-traffic web application.

#### Detailed Answer
- **DNS:** Route 53 with Latency-based or Geolocation routing.
- **CDN:** CloudFront for edge caching.
- **Compute:** Auto Scaling groups behind ALBs in multiple regions (or EKS/ECS).
- **Database:** DynamoDB Global Tables or Aurora Global Database for cross-region replication.
- **State:** S3 cross-region replication for static assets/uploads.

### Q2: Network Security (20 min)
**Level:** L3-L4 | **Category:** security
**Target Services:** VPC, Transit Gateway, WAF, Shield

> **Quick Answer:** How do you secure a multi-VPC environment and protect against DDoS and application-layer attacks?

#### Detailed Answer
- **Network Routing:** AWS Transit Gateway for centralized routing.
- **Inspection:** Transit Gateway routing traffic to a central Inspection VPC with AWS Network Firewall or third-party NGFWs.
- **Edge Protection:** AWS Shield Advanced for DDoS protection.
- **App Protection:** AWS WAF attached to CloudFront or ALBs to block SQLi, XSS, and rate limit malicious IPs.

### Q3: IAM Architecture (20 min)
**Level:** L4 | **Category:** security
**Target Services:** IAM, Identity Center, SCPs

> **Quick Answer:** Design a centralized IAM and access management strategy for 50 AWS accounts.

#### Detailed Answer
- Use AWS Organizations to group accounts into OUs.
- Apply Service Control Policies (SCPs) to enforce guardrails (e.g., restrict regions, prevent disabling CloudTrail).
- Use AWS IAM Identity Center (formerly SSO) integrated with an external IdP (Okta, Entra ID) for federated access.
- Implement least privilege and Attribute-Based Access Control (ABAC).

---

## Interview 4: Container Platform Lead - EKS & ECS (60 min)

### Q1: EKS vs ECS (15 min)
**Level:** L3-L4 | **Category:** architecture
**Target Services:** EKS, ECS

> **Quick Answer:** When would you choose EKS over ECS, and vice versa?

#### Detailed Answer
- **ECS:** Simpler, AWS-native, lower operational overhead. Best when teams don't have Kubernetes expertise and want tight AWS integration.
- **EKS:** Kubernetes ecosystem, portable, multi-cloud strategy, complex orchestration requirements (e.g., Helm, Operators, Service Meshes).

### Q2: EKS Security & Scaling (20 min)
**Level:** L4 | **Category:** security/architecture
**Target Services:** EKS, IRSA, Karpenter

> **Quick Answer:** How do you implement least privilege for Pods in EKS, and how do you handle cluster autoscaling?

#### Detailed Answer
- **Security:** IAM Roles for Service Accounts (IRSA) via OIDC provider. Pods assume specific IAM roles rather than using the Node instance profile.
- **Scaling:** Use Karpenter instead of Cluster Autoscaler for faster, more efficient node provisioning. Use HPA (Horizontal Pod Autoscaler) for scaling Pods based on metrics.

### Q3: Live Troubleshooting - Pod Scheduling (25 min)
**Level:** L3-L4 | **Category:** troubleshooting
**Target Services:** EKS

> **Quick Answer:** Scenario: Pods are stuck in a `Pending` state. How do you troubleshoot?

#### Detailed Answer
1. Run `kubectl describe pod <pod-name>`.
2. Check for resource constraints (CPU/Memory).
3. Check for matching Node Selectors, Taints, and Tolerations.
4. Check if the cluster autoscaler (or Karpenter) is failing to provision new nodes (e.g., ASG max size reached, AWS service limits).
5. Check VPC CNI limits (max ENIs/IPs per node instance type).

---

## Interview 5: Principal Engineer - System Design & Cost Optimization (60 min)

### Q1: System Design (30 min)
**Level:** L4 | **Category:** architecture
**Target Services:** General

> **Quick Answer:** Design a globally distributed, auto-scaling video streaming platform (like Netflix).

#### Detailed Answer
- **Ingestion/Transcoding:** MediaConvert, S3, Step Functions.
- **Storage:** S3 for video files, tiered storage.
- **Delivery:** CloudFront for edge delivery.
- **Metadata/Users:** DynamoDB global tables.
- **Compute:** EKS or ECS across multiple regions.
- **Resiliency:** Chaos engineering, cellular architecture.

### Q2: FinOps & Cost Optimization (15 min)
**Level:** L4 | **Category:** cost-optimization
**Target Services:** Compute Optimizer, Cost Explorer

> **Quick Answer:** You inherit an AWS bill of $500K/month that has doubled in 6 months. How do you optimize it?

#### Detailed Answer
- **Visibility:** Use Cost Explorer and Cost & Usage Reports (CUR). Tagging strategy enforcement.
- **Compute:** Right-size instances (Compute Optimizer), use Graviton processors, implement Savings Plans / RIs. Spot instances for stateless workloads.
- **Storage:** S3 Intelligent-Tiering, delete unattached EBS volumes, lifecycle policies.
- **Network:** Optimize data transfer costs, keep traffic within AZs/Regions where possible, use VPC endpoints.

### Q3: Disaster Recovery (15 min)
**Level:** L4 | **Category:** architecture
**Target Services:** Route 53, RDS, S3

> **Quick Answer:** Design a DR strategy with RPO=0 and RTO<15 minutes.

#### Detailed Answer
- RPO=0 requires synchronous replication. Multi-AZ is essential.
- For cross-region RTO<15m, use Pilot Light or Warm Standby architecture.
- Aurora Global Database (sub-second RPO cross-region).
- Route 53 health checks and automated failover routing.
- Infrastructure fully codified (Terraform/CFN) for rapid deployment.

---
## Grading Rubric (For All Interviews)
- **1 - Novice:** Fails to answer basic concepts. Deal-breaker for senior roles.
- **2 - Intermediate:** Knows the theory but lacks practical implementation details.
- **3 - Proficient:** Solid answers, covers edge cases. (Passing for L3).
- **4 - Advanced:** Deep dive into internals, cites real-world examples and trade-offs. (Passing for L4).
- **5 - Expert:** Teaches the interviewer something new, flawless architecture design considering cost, security, and scale.
