---
service: EC2
category: Compute
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# EC2 Interview Questions: Advanced

### Q1: Explain how you would safely migrate a legacy application from a static IP structure to an Auto Scaling, highly available architecture on EC2.
**Level:** L4 | **Category:** architecture
**Target Services:** EC2, Auto Scaling, ELB

> **Quick Answer:** Decouple state from instances, use an Application Load Balancer to distribute traffic, bake the application into an AMI or configure it via User Data, and implement Auto Scaling based on relevant CloudWatch metrics.

#### Detailed Answer
Migrating a legacy application bound to static IPs involves several structural changes:
1. **Statelessness**: Move local state (sessions, files) to shared services like ElastiCache, EFS, or S3.
2. **Database Decoupling**: If a DB runs locally, migrate it to Amazon RDS.
3. **AMI Baking vs. Bootstrapping**: Create a golden AMI via Packer for immutable infrastructure, or use EC2 User Data/Systems Manager to bootstrap at launch.
4. **Load Balancing**: Place the instances in an Auto Scaling Group (ASG) behind an Application Load Balancer (ALB). The ALB handles the static entry point (via DNS/Route 53) while the instances scale dynamically.
5. **DNS**: Point the legacy application domain to the ALB Alias record rather than a static IP.

#### Follow-up Questions
- How do you handle legacy applications that hardcode IP addresses for licensing? (Use Elastic IPs attached to secondary ENIs if absolutely necessary, but prefer refactoring).
- How do you minimize deployment time for the ASG instances? (Pre-bake AMIs).

#### Related Services
- Auto Scaling, ELB, Route 53

### Q2: How does IMDSv2 prevent Server-Side Request Forgery (SSRF), and how would you enforce its use across an AWS Organization?
**Level:** L3 | **Category:** security
**Target Services:** EC2, IAM, Organizations

> **Quick Answer:** IMDSv2 uses session-based authentication requiring a PUT request to fetch a token before retrieving metadata. It can be enforced using SCPs at the Organization level or IAM condition keys.

#### Detailed Answer
IMDSv1 allowed simple GET requests to `169.254.169.254`. If an application had an SSRF vulnerability, an attacker could trick the app into fetching temporary IAM credentials. 
IMDSv2 mitigates this by requiring a session token:
```bash
# 1. Get Token
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
# 2. Use Token
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
```
To enforce IMDSv2:
- **IAM Policy/SCP**: 
```json
{
  "Effect": "Deny",
  "Action": "ec2:RunInstances",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "ec2:MetadataHttpTokens": "required"
    }
  }
}
```
- Existing instances can be modified via the AWS CLI to require IMDSv2.

#### Follow-up Questions
- How do you detect if applications are still using IMDSv1 before enforcing v2? (Use the `MetadataNoToken` CloudWatch metric).

#### Related Services
- IAM, AWS Organizations

*(Note: Questions Q3 through Q15 would cover Spot Fleets, Placement Groups in-depth, ENA/EFA tuning for HPC, Dedicated Hosts vs Dedicated Instances, hibernation mechanics, cross-account AMI sharing and encryption, etc.)*
