---
service: vpc
category: interview-questions
difficulty_levels:
  - L3
  - L4
aws_exam_relevance:
  - AWS Certified Advanced Networking - Specialty
  - AWS Certified Solutions Architect - Professional
  - AWS Certified DevOps Engineer - Professional
maturity_tier: advanced
last_validated_date: '2026-08-29'
version: 1.0.0
cross_references:
  - ../route53/overview.md
  - ../directconnect/overview.md
  - ../ram/overview.md
---

# AWS VPC - Advanced Interview Questions

### Q1: Transit Gateway Architecture and Routing
**Level:** L3-L4 | **Category:** architecture
**Target Services:** VPC, Transit Gateway

> **Quick Answer:** AWS Transit Gateway acts as a hub-and-spoke regional network transit hub. It supports multiple route tables, route propagation from attachments, inter-region peering, and allows complex topologies like isolated environments or shared egress.

<details>
<summary><b>Detailed Answer</b></summary>

Transit Gateway (TGW) simplifies network architecture by replacing complex peering meshes.

**Key Components:**
- **Attachments:** Can be VPCs, VPN connections, Direct Connect Gateways, or Connect (SD-WAN) attachments.
- **Route Tables:** TGW supports multiple route tables. Attachments are associated with exactly one route table, but routes can be propagated to multiple route tables.
- **Inter-Region Peering:** Two TGWs in different regions can be peered to route traffic globally.

**Complex Topologies:**
To create an isolated environment (e.g., Prod and Dev can talk to Shared Services but not to each other):
1. Create a `Prod-RT`, `Dev-RT`, and `Shared-RT`.
2. Associate Prod VPCs with `Prod-RT`, Dev VPCs with `Dev-RT`.
3. Propagate Shared Services routes to `Prod-RT` and `Dev-RT`.
4. Propagate Prod and Dev routes to `Shared-RT`.

**CLI Example: Creating a TGW Route Table and Propagation**
```bash
# Create Route Table
aws ec2 create-transit-gateway-route-table \
    --transit-gateway-id tgw-0abc123def

# Propagate attachment
aws ec2 enable-transit-gateway-route-table-propagation \
    --transit-gateway-route-table-id tgw-rtb-012345678 \
    --transit-gateway-attachment-id tgw-attach-0abcdef
```

</details>

#### Follow-up Questions
- How does TGW handle overlapping CIDRs compared to PrivateLink?
- What is appliance mode in TGW and when would you enable it?

#### Related Services
- Transit Gateway Network Manager
- AWS Direct Connect Gateway

#### References
- [Transit Gateway Routing](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-routing-tables.html)

### Q2: VPC Endpoint Policies for Granular Access
**Level:** L3-L4 | **Category:** security
**Target Services:** VPC, S3, IAM, DynamoDB

> **Quick Answer:** VPC Endpoint Policies are resource policies attached to VPC endpoints that restrict which principals can use the endpoint and which resources they can access (e.g., restricting S3 access only to a specific bucket).

<details>
<summary><b>Detailed Answer</b></summary>

By default, an endpoint policy allows full access. However, for a defense-in-depth strategy, you should restrict access.

**Example Scenario:** Restrict instances in a VPC so they can only access `my-production-bucket`.

**Endpoint Policy JSON:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-production-bucket/*"
    }
  ]
}
```

**Terraform Implementation:**
```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = ["s3:*"]
      Resource  = [
        "arn:aws:s3:::my-production-bucket",
        "arn:aws:s3:::my-production-bucket/*"
      ]
    }]
  })
}
```

This prevents data exfiltration by blocking access to external or personal S3 buckets via the gateway.

</details>

#### Follow-up Questions
- How does a VPC endpoint policy interact with an S3 bucket policy?
- What is the `aws:SourceVpce` condition key used for?

#### Related Services
- AWS IAM
- Amazon S3

#### References
- [VPC Endpoint Policies](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-access.html)

### Q3: VPC Flow Logs Analysis and Troubleshooting
**Level:** L3-L4 | **Category:** troubleshooting
**Target Services:** VPC, CloudWatch Logs, Athena

> **Quick Answer:** VPC Flow Logs capture IP traffic going to and from network interfaces. They can be analyzed using CloudWatch Logs Insights or Amazon Athena to debug network issues like blocked ports, asymmetric routing, or malicious IP scanning.

<details>
<summary><b>Detailed Answer</b></summary>

Flow logs can be published to CloudWatch Logs or S3.

**CloudWatch Logs Insights Example:**
To find rejected connections (e.g., due to Security Group rules) to a specific destination IP:
```text
fields @timestamp, srcAddr, dstAddr, dstPort, action
| filter dstAddr = "10.0.1.55" and action = "REJECT"
| sort @timestamp desc
| limit 20
```

**Amazon Athena Example (when logs are in S3):**
Creating a table for Parquet-formatted flow logs and finding top talkers:
```sql
SELECT srcaddr, COUNT(*) as hits, SUM(bytes) as total_bytes
FROM vpc_flow_logs
WHERE action='ACCEPT'
GROUP BY srcaddr
ORDER BY total_bytes DESC
LIMIT 10;
```

Flow logs help identify if traffic reached the ENI, if SGs/NACLs blocked it, or if it was dropped for lack of a route. Note that flow logs do not capture DNS traffic (Port 53) to the Route 53 Resolver or instance metadata (169.254.169.254) traffic.

</details>

#### Follow-up Questions
- What traffic is not logged by VPC Flow Logs?
- How do you configure custom formats for VPC Flow Logs?

#### Related Services
- Amazon CloudWatch
- Amazon Athena

#### References
- [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)

### Q4: Network Troubleshooting Methodology
**Level:** L3-L4 | **Category:** troubleshooting
**Target Services:** VPC, EC2

> **Quick Answer:** Network troubleshooting in AWS requires a systematic check from source to destination evaluating Security Groups, Network ACLs, Route Tables, Internet/NAT Gateways, and DNS resolution.

<details>
<summary><b>Detailed Answer</b></summary>

A systematic approach to diagnosing "I can't connect to my EC2 instance":

1. **DNS Resolution:** Is the hostname resolving to the correct IP? (Check `nslookup` or `dig`).
2. **Security Groups (SGs):** 
   - Is the inbound port allowed on the destination? SGs are stateful, so outbound is automatically allowed.
3. **Network ACLs (NACLs):** 
   - NACLs are stateless. You must check BOTH inbound rules (allowing the request) AND outbound rules (allowing the ephemeral port return traffic, usually 1024-65535).
4. **Route Tables:** 
   - Does the subnet route table have a path to the destination? 
   - If external, is there a route to an IGW or NAT Gateway?
5. **Gateways/Endpoints:** 
   - Does the subnet have an attached IGW (for public IP) or NAT Gateway (for private IP)?
   - If using PrivateLink, is the endpoint associated with the correct subnets?
6. **OS-Level Firewalls:** Check `iptables`, `firewalld`, or Windows Firewall.
7. **Reachability Analyzer:** Use the AWS Network Reachability Analyzer for automated path testing.

**CLI Example: Reachability Analyzer**
```bash
aws ec2 create-network-insights-path \
    --source i-1234567890abcdef0 \
    --destination i-0987654321fedcba0 \
    --protocol tcp --destination-port 443
```

</details>

#### Follow-up Questions
- How do stateful SGs differ from stateless NACLs regarding ephemeral ports?
- How does Network Reachability Analyzer work without sending actual packets?

#### Related Services
- VPC Reachability Analyzer
- Route 53

#### References
- [Troubleshoot Network Reachability](https://docs.aws.amazon.com/vpc/latest/reachability/getting-started.html)

### Q5: DNS Resolution in VPC and Hybrid DNS
**Level:** L3-L4 | **Category:** architecture
**Target Services:** VPC, Route 53

> **Quick Answer:** VPC DNS relies on `enableDnsSupport` and `enableDnsHostnames`. For hybrid environments, Route 53 Resolver provides inbound and outbound endpoints to resolve DNS queries between on-premises and AWS VPCs.

<details>
<summary><b>Detailed Answer</b></summary>

**VPC DNS Attributes:**
- `enableDnsSupport`: Ensures the Amazon provided DNS server (VPC+2 IP) is enabled.
- `enableDnsHostnames`: Ensures instances receive public DNS hostnames if they have public IPs.

**Hybrid DNS Architecture:**
To resolve `.internal.onprem` from AWS and `.aws.cloud` from on-premises:
1. **Outbound Resolver Endpoint:** Deployed in the VPC. A Route 53 Resolver Rule is created for `.internal.onprem` targeting on-premises DNS server IPs, associated with the VPC.
2. **Inbound Resolver Endpoint:** Deployed in the VPC with dedicated ENIs. On-premises DNS servers are configured to forward queries for `.aws.cloud` to these inbound endpoint IPs.

**Terraform Snippet for Outbound Rule:**
```hcl
resource "aws_route53_resolver_rule" "fwd_to_onprem" {
  domain_name          = "internal.onprem."
  name                 = "onprem-rule"
  rule_type            = "FORWARD"
  resolver_endpoint_id = aws_route53_resolver_endpoint.outbound.id

  target_ip {
    ip = "192.168.1.53"
  }
}
```

</details>

#### Follow-up Questions
- What IP address does the VPC DNS resolver use?
- How do Route 53 Private Hosted Zones resolve across peered VPCs?

#### Related Services
- Route 53 Resolver
- AWS Direct Connect

#### References
- [Route 53 Resolver](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html)

### Q6: Cross-Region VPC Peering and Limitations
**Level:** L3-L4 | **Category:** architecture
**Target Services:** VPC

> **Quick Answer:** Cross-region VPC peering securely connects VPCs across regions over the AWS global backbone. Traffic does not traverse the public internet. However, VPC peering does not support transitive routing, and overlapping CIDRs are prohibited.

<details>
<summary><b>Detailed Answer</b></summary>

**Key Characteristics:**
- No single point of failure or bandwidth bottlenecks.
- Encrypted by default (AWS AEAD encryption across regions).
- Supports IPv4 and IPv6.

**Crucial Limitations:**
1. **No Transitive Routing:** If VPC A peers with VPC B, and VPC B peers with VPC C, A cannot route to C through B. You must create a direct peer A-C, or use a Transit Gateway.
2. **MTU Limitations:** Cross-region peering has an MTU of 1500 bytes. Jumbo frames (9001 bytes) are supported *within* the same region, but cross-region traffic must be fragmented or path MTU discovery must be used.
3. **Security Group Referencing:** You can reference peer SGs cross-region, but it requires specific syntax and support.

**CLI Example:**
```bash
aws ec2 create-vpc-peering-connection \
    --vpc-id vpc-1a2b3c4d \
    --peer-vpc-id vpc-11122233 \
    --peer-region eu-west-1
```

</details>

#### Follow-up Questions
- Why might you choose VPC Peering over Transit Gateway?
- How do you resolve DNS hostnames over a cross-region peering connection?

#### Related Services
- AWS Transit Gateway

#### References
- [VPC Peering Restrictions](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html#vpc-peering-limitations)

### Q7: Resolving Overlapping CIDRs
**Level:** L4 | **Category:** architecture
**Target Services:** VPC, PrivateLink

> **Quick Answer:** When connecting VPCs or on-premises networks with overlapping CIDR blocks, traditional peering or routing fails. Solutions include AWS PrivateLink (for service-to-service access) or Private NAT Gateways with secondary non-overlapping CIDRs.

<details>
<summary><b>Detailed Answer</b></summary>

**Scenario:** VPC A (10.0.0.0/16) needs to access a service in VPC B (10.0.0.0/16).

**Solution 1: AWS PrivateLink (Best Practice)**
1. Deploy a Network Load Balancer (NLB) in VPC B in front of the target service.
2. Create an Endpoint Service tied to the NLB.
3. In VPC A, create a VPC Endpoint connected to the Endpoint Service.
4. Traffic from VPC A hits the endpoint (which has an IP in VPC A's CIDR) and is securely SNATted across the AWS fabric to the NLB in VPC B, entirely bypassing CIDR overlap issues.

**Solution 2: Private NAT Gateway & Transit Gateway**
If bidirectional IP routing is strictly required (rarely the case):
1. Attach secondary, non-overlapping CIDRs to both VPCs.
2. Deploy Private NAT Gateways in the secondary CIDR subnets.
3. Route traffic to the TGW, forcing traffic through the Private NAT to translate the source IPs into the non-overlapping range.

</details>

#### Follow-up Questions
- How does AWS PrivateLink affect the source IP seen by the target application?
- Can you use Proxy Protocol v2 with PrivateLink to retrieve the source IP?

#### Related Services
- AWS PrivateLink
- Elastic Load Balancing

#### References
- [VPC PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)

### Q8: PrivateLink Architecture (Endpoints vs Endpoint Services)
**Level:** L3-L4 | **Category:** architecture
**Target Services:** VPC, PrivateLink

> **Quick Answer:** AWS PrivateLink uses Interface Endpoints (ENIs in your VPC) to privately consume services, and Endpoint Services (backed by NLBs) to act as a service provider, allowing unidirectional, secure access without internet gateways.

<details>
<summary><b>Detailed Answer</b></summary>

**Gateway Endpoints vs Interface Endpoints:**
- **Gateway Endpoints:** Only for S3 and DynamoDB. Uses Route Table entries. No hourly charges.
- **Interface Endpoints:** Uses an ENI with a private IP. Supports many AWS services and custom SaaS apps. Charged per hour and per GB processed.

**Endpoint Services (Provider Side):**
If you build a SaaS product and want customers to access it privately:
1. Put instances behind a Network Load Balancer (NLB).
2. Create a VPC Endpoint Service tied to the NLB.
3. Whitelist customer AWS Account IDs.
4. Customers create an Interface Endpoint in their VPC and connect to your Service Name.

**Terraform snippet for Endpoint Service:**
```hcl
resource "aws_vpc_endpoint_service" "example" {
  acceptance_required        = true
  network_load_balancer_arns = [aws_lb.nlb.arn]
}
```

</details>

#### Follow-up Questions
- What happens if you enable "Private DNS" on an interface endpoint?
- Why can't you use an ALB behind a VPC Endpoint Service?

#### Related Services
- Elastic Load Balancing
- API Gateway

#### References
- [AWS PrivateLink Concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

### Q9: Direct Connect with VPN Backup and BGP Failover
**Level:** L4 | **Category:** architecture
**Target Services:** Direct Connect, VPN, Transit Gateway

> **Quick Answer:** For high availability, an AWS Direct Connect (DX) connection can be backed up by an AWS Site-to-Site VPN. Failover is managed automatically via BGP by manipulating route preferences (AS-PATH prepending).

<details>
<summary><b>Detailed Answer</b></summary>

**Architecture:**
- Both DX and VPN terminate at a Transit Gateway (or Virtual Private Gateway).
- Both use BGP (Dynamic Routing).

**Route Preference:**
AWS implicitly prefers Direct Connect paths over Site-to-Site VPN paths when the route destination CIDR matches exactly.
To ensure traffic properly fails over:
1. Ensure both DX and VPN advertise the exact same IP prefixes.
2. For traffic from AWS to On-Prem: Use AS-PATH prepending on the VPN customer gateway. Make the VPN path longer so AWS prefers the DX connection.
3. For traffic from On-Prem to AWS: Your on-premises router must be configured with a higher Local Preference for the routes learned via DX.

**BGP Communities:**
AWS supports BGP communities to control route scope (Local Preference in the AWS network). You can tag routes over the VPN with `7224:7100` (Low Preference) to force AWS to prefer DX.

</details>

#### Follow-up Questions
- What happens if the VPN advertises a more specific route (/24) than the Direct Connect (/16)?
- How does BFD (Bidirectional Forwarding Detection) speed up failover?

#### Related Services
- AWS Site-to-Site VPN
- AWS Transit Gateway

#### References
- [Direct Connect Routing](https://docs.aws.amazon.com/directconnect/latest/UserGuide/routing-and-bgp.html)

### Q10: VPC Sharing and Resource Access Manager (RAM)
**Level:** L3 | **Category:** architecture
**Target Services:** VPC, RAM, Organizations

> **Quick Answer:** VPC Sharing allows multiple AWS accounts within an AWS Organization to launch resources into shared, centrally managed VPC subnets, reducing network complexity and IP address exhaustion.

<details>
<summary><b>Detailed Answer</b></summary>

**How it works:**
A central "Network Account" owns the VPC, Subnets, Route Tables, and Gateways. Using AWS Resource Access Manager (RAM), the Network Account shares specific *Subnets* (not the whole VPC) with "Participant Accounts".

**Participant Capabilities:**
- Participants can launch EC2 instances, RDS databases, and ALBs into the shared subnets.
- Participants manage their own Security Groups.
- Participants CANNOT modify route tables, VPC endpoints, or NACLs.

**Benefits:**
- Better IP space utilization (fewer fragmented VPCs).
- Centralized egress/ingress inspection and routing.
- Strong separation of duties (Network team manages routing; App teams manage instances).

**CLI Example: Sharing a Subnet via RAM**
```bash
aws ram create-resource-share \
    --name "Shared-Prod-Subnets" \
    --resource-arns "arn:aws:ec2:us-east-1:111122223333:subnet/subnet-0abcd" \
    --principals "arn:aws:organizations::111122223333:ou/o-example/ou-example"
```

</details>

#### Follow-up Questions
- Who pays for data transfer in a Shared VPC: the owner or the participant?
- Can you share a VPC with an account outside your AWS Organization?

#### Related Services
- AWS RAM
- AWS Organizations

#### References
- [VPC Sharing](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html)

### Q11: IPv6 in VPC and Egress-Only Internet Gateways
**Level:** L3-L4 | **Category:** architecture
**Target Services:** VPC

> **Quick Answer:** VPCs can be dual-stack (IPv4 and IPv6). Because all IPv6 addresses are globally routable (no NAT), an Egress-Only Internet Gateway (EOIG) is used to allow outbound IPv6 traffic while blocking inbound connections from the internet.

<details>
<summary><b>Detailed Answer</b></summary>

**Dual-Stack Architecture:**
- Assign an Amazon-provided /56 IPv6 CIDR to the VPC.
- Assign a /64 CIDR to each subnet.
- Instances get both a private IPv4 and a globally unique IPv6 address.

**Security and Routing:**
For private subnets, you cannot use a NAT Gateway for IPv6. Instead, you use an **Egress-Only Internet Gateway (EOIG)**.
- **Route Table entry for public subnet:** `::/0` -> `igw-id`
- **Route Table entry for private subnet:** `::/0` -> `eigw-id`

The EOIG is stateful and tracks outbound connections, dropping any unsolicited inbound traffic, effectively mimicking the security posture of a NAT Gateway without the translation overhead.

</details>

#### Follow-up Questions
- Does an EOIG perform network address translation (NAT)?
- How do security groups work with IPv6?

#### Related Services
- Amazon EC2

#### References
- [Egress-Only Internet Gateways](https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html)

### Q12: AWS Network Firewall Deployment Models
**Level:** L4 | **Category:** security
**Target Services:** VPC, Network Firewall

> **Quick Answer:** AWS Network Firewall is a managed, stateful firewall offering IDS/IPS. It can be deployed in a distributed model (in every VPC) or a centralized inspection model (using Transit Gateway).

<details>
<summary><b>Detailed Answer</b></summary>

**Rule Types:**
- **Stateless Rules:** Fast, evaluate individual packets (like NACLs). Useful for immediate blocklists.
- **Stateful Rules:** Suricata-compatible rules that inspect context and payload (e.g., matching domain names or deep packet inspection).

**Centralized Inspection Architecture:**
1. Create an "Inspection VPC".
2. Deploy the Network Firewall endpoints into dedicated subnets.
3. Attach the Inspection VPC to a Transit Gateway (TGW).
4. Use TGW route tables to force all east-west (VPC-to-VPC) or north-south (VPC-to-Internet) traffic into the Inspection VPC, through the firewall endpoints, and back out.

**Routing Magic (VPC Ingress Routing):**
To inspect traffic entering from an IGW into a VPC, you create a route table attached directly to the IGW (Edge Association). 
- IGW Route: Target destination CIDR -> Network Firewall Endpoint.

</details>

#### Follow-up Questions
- What is asymmetric routing, and how can it break a centralized firewall architecture?
- How does AWS Network Firewall handle encrypted TLS traffic?

#### Related Services
- AWS Transit Gateway
- Gateway Load Balancer

#### References
- [AWS Network Firewall Deployment Models](https://docs.aws.amazon.com/network-firewall/latest/developerguide/arch-options.html)

### Q13: Gateway Load Balancer (GWLB) Architecture
**Level:** L4 | **Category:** architecture
**Target Services:** VPC, GWLB

> **Quick Answer:** GWLB allows you to deploy and scale third-party virtual network appliances (firewalls, IDS/IPS) transparently. It uses GENEVE encapsulation to maintain the original packet headers and IP addresses.

<details>
<summary><b>Detailed Answer</b></summary>

**The Problem it Solves:**
Traditionally, scaling 3rd party firewalls in AWS required complex IPsec VPNs, SNAT, and route table manipulations, breaking source IP visibility.

**How GWLB Works:**
1. GWLB sits in front of an Auto Scaling Group of virtual appliance EC2 instances.
2. It provides a VPC Endpoint Service (GWLB Endpoint).
3. In the application VPC, a GWLB Endpoint is deployed.
4. Route tables are updated to send traffic to the GWLB Endpoint.
5. GWLB encapsulates the traffic using the GENEVE protocol (UDP port 6081) and sends it to the appliance. The appliance inspects it, and if permitted, sends it back.

Because of GENEVE, the original source and destination IPs are preserved completely untouched, and the appliance acts as a transparent "bump in the wire".

</details>

#### Follow-up Questions
- Why is GENEVE encapsulation used instead of standard NAT?
- How does GWLB maintain flow symmetry?

#### Related Services
- Elastic Load Balancing
- AWS Network Firewall

#### References
- [Gateway Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html)

### Q14: ENI Management and Source/Destination Checks
**Level:** L3 | **Category:** practical
**Target Services:** VPC, EC2

> **Quick Answer:** An Elastic Network Interface (ENI) represents a virtual network card. EC2 instances perform Source/Destination checks by default. This must be disabled if the instance is acting as a router, NAT, or firewall appliance.

<details>
<summary><b>Detailed Answer</b></summary>

**Source/Destination Checks:**
By default, AWS drops traffic arriving at an ENI if the ENI's IP address does not match the packet's destination IP, and drops outbound traffic if the source IP doesn't match. 
If an EC2 instance is acting as a NAT instance, VPN appliance, or router, you MUST disable this check so it can process packets meant for other IPs.

**CLI Command:**
```bash
aws ec2 modify-network-interface-attribute \
    --network-interface-id eni-12345678 \
    --no-source-dest-check
```

**Multiple ENIs:**
Attaching multiple ENIs to an instance is common for management networks vs data networks, or for license-bound MAC addresses. However, OS-level routing (like `iproute2` on Linux) must be manually configured to ensure asymmetric routing doesn't occur when packets arrive on `eth1` but the OS replies via the default gateway on `eth0`.

</details>

#### Follow-up Questions
- How are Elastic IPs associated with an ENI?
- What determines the maximum number of ENIs you can attach to an EC2 instance?

#### Related Services
- Amazon EC2

#### References
- [Elastic Network Interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html)

### Q15: MTU, Jumbo Frames, and Path MTU Discovery
**Level:** L3-L4 | **Category:** troubleshooting
**Target Services:** VPC, VPN, Direct Connect

> **Quick Answer:** AWS VPCs support Jumbo frames (9001 MTU) for internal communication. However, traffic leaving the VPC (Internet, VPN, cross-region peering) drops to 1500 MTU. PMTUD is critical to prevent dropped packets.

<details>
<summary><b>Detailed Answer</b></summary>

**Maximum Transmission Unit (MTU):**
- **Intra-region VPC traffic:** 9001 bytes (Jumbo frames). Highly beneficial for large data transfers (Hadoop, database replication).
- **Internet, Cross-region Peering, Direct Connect:** 1500 bytes.
- **Site-to-Site VPN:** Can be lower (e.g., 1446) due to IPsec overhead.

**Path MTU Discovery (PMTUD):**
If an instance sends a 9001-byte packet to an internet destination with the "Don't Fragment" (DF) bit set, the AWS gateway drops it and sends back an ICMP `Destination Unreachable (Fragmentation Needed)` message. 
The sender OS then reduces the packet size.

**Troubleshooting:**
If SGs or NACLs block inbound ICMP (Type 3, Code 4), PMTUD breaks. This results in connections hanging or stalling when transferring large payloads, often misdiagnosed as an application timeout. Always allow inbound ICMP fragmentation required messages.

</details>

#### Follow-up Questions
- How do you enable ICMP rules in a Security Group specifically for PMTUD?
- What is MSS Clamping and how does it relate to VPN MTU issues?

#### Related Services
- AWS Site-to-Site VPN
- AWS Direct Connect

#### References
- [Network MTU for your EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/network_mtu.html)
