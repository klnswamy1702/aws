---
service: Route53
category: architecture
difficulty_levels: L4
aws_exam_relevance: high
maturity_tier: core
last_validated_date: 2026-08-29
version: 1.0
cross_references:
  - ../route-53/interview-questions-advanced.md
---
# Amazon Route 53 - Architecture Interview Questions

### Q1: Design a hybrid DNS architecture using Route 53 Resolver to allow on-premises servers to resolve AWS private domain names, and AWS resources to resolve on-premises corporate domains.
**Level:** L4 | **Category:** architecture
**Target Services:** Route 53 Resolver, Direct Connect / VPN

> **Quick Answer:** Use Route 53 Resolver Endpoints. Create an Inbound Endpoint to allow on-premise DNS servers to forward queries to AWS. Create an Outbound Endpoint with a Forwarding Rule to route queries for the corporate domain from AWS VPCs to the on-premise DNS servers.

#### Detailed Answer
In a hybrid enterprise environment, DNS must be unified.
1. **AWS to On-Premises (Outbound):** 
   - Deploy a Route 53 Resolver **Outbound Endpoint** across multiple Availability Zones in the VPC.
   - Create a **Resolver Rule** specifying that any DNS query for `corp.internal` should be forwarded to the IP addresses of the on-premises DNS servers.
   - Associate this rule with the VPCs that need access.
2. **On-Premises to AWS (Inbound):**
   - Deploy a Route 53 Resolver **Inbound Endpoint** across multiple AZs. This provides static IP addresses within the VPC.
   - Configure the on-premises DNS server (e.g., Active Directory DNS or BIND) to set up a conditional forwarder for your AWS domain (e.g., `aws.internal`). Forward those requests to the IP addresses of the Inbound Endpoint.
3. **Connectivity:** Ensure AWS Direct Connect or a Site-to-Site VPN is established, and security groups on the endpoints allow port 53 (TCP/UDP).

#### Follow-up Questions
- How do you share these Resolver Rules across a multi-account AWS environment using AWS RAM?
- How does Route 53 Resolver differ from a traditional EC2-based DNS forwarder?

### Q2: How does Route 53 Geoproximity routing differ from Geolocation routing, and how do you use Traffic Flow to manage it?
**Level:** L4 | **Category:** architecture
**Target Services:** Route 53 Traffic Flow

> **Quick Answer:** Geolocation routes users based exactly on their geographic location (e.g., continent, country, state) mapping to specific endpoints. Geoproximity routes traffic based on the physical distance between the user and your resources, and allows you to adjust the size of the geographic region that routes to a specific endpoint using "bias."

#### Detailed Answer
- **Geolocation:** Strict rules. "If user is in Europe, route to the `eu-central-1` ALB." If that ALB is down, and no failover is configured, the request fails.
- **Geoproximity:** Fluid routing. It calculates the distance. If you have an endpoint in US-East and US-West, users in the middle of the US will be routed to the mathematically closest one. 
  - **Bias:** You can shift traffic. If your US-East region has more capacity, you can increase the bias (+1 to +99) for US-East. This "expands" the catchment area of US-East, drawing in users who might physically be closer to US-West.
- **Traffic Flow:** Geoproximity routing MUST be configured using Route 53 Traffic Flow (a visual policy builder), which generates complex DNS decision trees.

#### Follow-up Questions
- How is Route 53 Traffic Flow billed compared to standard records?
- Can you use Geoproximity routing for resources that are not in AWS (e.g., an on-premises data center)?
