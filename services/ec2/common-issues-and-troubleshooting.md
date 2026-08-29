---
service: EC2
category: Compute
difficulty_levels: L2-L4
aws_exam_relevance: Solutions Architect Professional, DevOps Engineer Professional
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../ec2/overview.md
---

# EC2 Common Issues & Troubleshooting

## 1. Instance Unreachable (Status Check Failed)
- **System Status Check Failure**: Indicates an issue with the underlying AWS hardware. Stop and start the instance to migrate it to healthy hardware.
- **Instance Status Check Failure**: Indicates an issue within the OS (e.g., kernel panic, exhausted memory, misconfigured network).
  - *Troubleshooting*: Check system logs via EC2 console, or use EC2 Serial Console. Reboot if necessary.

## 2. SSH Connection Issues
- **Timeouts**: Usually caused by Security Group rules, Network ACLs, or route tables not allowing traffic on port 22.
- **Connection Refused**: SSH daemon is not running on the instance.
- **Permission Denied (publickey)**: Wrong private key, or the permissions on `~/.ssh/authorized_keys` are incorrect.

## 3. Insufficient Capacity Errors (`InsufficientInstanceCapacity`)
- **Cause**: AWS does not have enough available On-Demand capacity in the targeted Availability Zone for the requested instance type.
- **Solution**: 
  - Wait and try again later.
  - Launch in a different Availability Zone.
  - Choose a different instance type.

## 4. Instance Immediately Terminates (`Server.InternalError` or `Client.VolumeLimitExceeded`)
- **Cause**: Reaching EBS volume limits, missing AMI parts, or encrypted AMI KMS key access issues.
- **Troubleshooting**: Check the AWS CloudTrail events for `RunInstances` and decode the error message. Use the State Transition Reason in the EC2 console.

## 5. Cannot Access Internet from EC2 in Private Subnet
- **Troubleshooting Checklist**:
  - Ensure the subnet has a route to a NAT Gateway or NAT Instance.
  - Ensure the NAT Gateway is in a public subnet with a route to an Internet Gateway (IGW).
  - Verify Security Groups allow outbound HTTP/HTTPS.
  - Verify Network ACLs allow outbound traffic and return ephemeral port traffic.
