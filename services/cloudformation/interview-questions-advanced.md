---
service: CloudFormation
category: Management & Governance
difficulty_levels: L3-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../cloudformation/overview.md
---

# CloudFormation Interview Questions: Advanced

### Q1: What is the difference between Nested Stacks and Cross-Stack References? When would you use one over the other?
**Level:** L3 | **Category:** architecture
**Target Services:** CloudFormation

> **Quick Answer:** Nested Stacks create tightly coupled hierarchies managed as a single entity, whereas Cross-Stack References create loosely coupled, independent stacks linked by exported values.

#### Detailed Answer
**Nested Stacks**: 
- Used to break apart a monolithic template (e.g., a load balancer template, an ASG template, a security group template).
- Deployed via a parent stack.
- Lifecycle is tied together; deleting the parent deletes the children.
- Good for repeated patterns (e.g., deploying the same microservice architecture 10 times).

**Cross-Stack References (`Export` / `Fn::ImportValue`)**:
- Used to share values between completely independent lifecycles.
- Example: A core Networking team manages the VPC stack and exports Subnet IDs. The App team's stack imports those IDs.
- Creates a hard dependency: The Networking team cannot change/delete the exported Subnet ID while the App team is using it.

### Q2: You need to deploy a new IAM role and security baseline to 100 AWS accounts in your AWS Organization. How do you automate this using CloudFormation?
**Level:** L3 | **Category:** practical
**Target Services:** CloudFormation, Organizations

> **Quick Answer:** Use CloudFormation StackSets with service-managed permissions integrated with AWS Organizations.

#### Detailed Answer
CloudFormation StackSets allow you to deploy templates across multiple accounts and regions simultaneously.
By using **Service-Managed Permissions**:
1. You deploy the StackSet from the delegated administrator account.
2. You target Organizational Units (OUs) instead of individual account IDs.
3. StackSets automatically assumes the necessary IAM roles to deploy the stack in all child accounts.
4. **Auto-Deployment feature**: When a new account is added to the target OU in the future, the StackSet automatically provisions the baseline template into the new account without manual intervention.

### Q3: You notice a production CloudFormation stack shows "DRIFTED". What does this mean, and how do you fix it safely?
**Level:** L4 | **Category:** troubleshooting
**Target Services:** CloudFormation

> **Quick Answer:** Drift indicates someone manually changed a resource via the console/CLI, causing it to deviate from the CFN template. Fix it by importing the drifted resource state or updating the template to match reality.

#### Detailed Answer
Drift detection compares the current physical state of resources with the expected state in the template.
**Fixing it safely**:
1. **Update the Template to match reality**: If the manual change was correct (e.g., an emergency fix to a Security Group), update the CFN template to reflect the new rule, then run a stack update. CFN will align the template with reality.
2. **Revert reality to match the Template**: If the change was unauthorized, simply trigger a stack update (often requiring a dummy parameter change to force an update on the drifted resource) to overwrite the manual changes back to the defined state in code.

*(Note: Questions Q4 through Q15 cover dynamic references, Custom Resources vs Macros, handling stateful resource replacements, AWS CDK synthesis, etc.)*
