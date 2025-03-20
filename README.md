# Cloud Security Alliance CTI Repository

## Unique Approach to Cloud Threat Intelligence

Unlike traditional CTI, which often focuses primarily on indicators and general mitigations across hundreds of different security products, the Cloud Security Alliance CTI takes a distinct approach:

1. **Provider-Specific Remediation**: We focus on actionable, specific remediation steps for major cloud providers (AWS, Azure, GCP). Rather than generic advice, we provide exact console paths, CLI commands, API calls, and infrastructure-as-code examples to implement protections.

2. **Global Coverage**: Cloud environments enable global protective actions that simply aren't possible in traditional environments. A single AWS security policy or Azure control can protect resources worldwide, making remediation more powerful and comprehensive.

3. **Standardized Services**: Unlike the fragmented landscape of on-premises security products (hundreds of firewall vendors, IDS systems, etc.), cloud providers offer standardized services with consistent security interfaces, allowing for more precise and reliable remediation guidance.

4. **Detection as Code**: We provide actual detection implementations using cloud-native tools like AWS GuardDuty, Azure Sentinel, or GCP Security Command Center, rather than just conceptual detection strategies.

## STIX Format and Extensions

This repository contains Cloud Adversarial Vectors, Exploits, and Threats (CAVEaT) data in STIX format, with custom extensions to support:

- Cloud-specific tactics and techniques
- Provider-specific remediation steps
- Infrastructure-as-code examples for security controls
- Mappings to cloud provider security services
- Links to official documentation and service announcements

## CAVEaT Framework

Cloud Adversarial, Vectors, and Threats (CAVEaT) focuses on documented cloud attack vectors with evidence-based mitigations:

- [Main WG-CAVEaT Repository](https://github.com/CloudSecurityAlliance-WG/WG-CAVEaT)
- [WG-CAVEaT Working Group in Circle](https://circle.cloudsecurityalliance.org/community-home1?communitykey=cce2fd58-ba71-4280-9e3d-018c352d4100)
- [CAVEaT Chatbot v3](https://chatgpt.com/g/g-xXpnPwHaD-cloud-adversarial-vectors-and-threat-solutions-v3)
- [CAVEaT Chatbot v2](https://csaurl.org/CAVEaT-Chatbot)
- [Chatbot Data Repository](https://github.com/Cloudsecurityalliance-Chatbots/chatbot-CAVEaT-data)

An example of creating an entry using the chatbot: [https://chatgpt.com/share/67356abd-a78c-8013-91b1-473053aea9c2](https://chatgpt.com/share/67356abd-a78c-8013-91b1-473053aea9c2)

## Strategy: Evidence-Based Threat Identification

We identify significant cloud threats by observing where providers invest in security features. When cloud providers dedicate substantial resources (often hundreds of thousands or millions of dollars) to developing new security services, it signals threats serious enough to warrant attention.

Examples include:
- AWS GuardDuty Malware Protection for S3
- Microsoft Defender for Cloud
- GCP Security Command Center

These investments reveal the threats that security teams at major providers consider most critical.

## Sources We Monitor

- Official cloud provider security announcements and blogs
- API and IAM changes trackers:
  - [AWS API Changes](https://awsapichanges.com/)
  - [AWS IAM Changes](https://awsiamchanges.com/)
  - [GCP API Changes](https://gcpapichanges.com/)
  - [Azure IAM Changes](https://azureiamchanges.com/)
- Security blogs, especially product announcements (e.g., [Cloudflare Security](https://blog.cloudflare.com/tag/security/))
- CVEs specific to cloud services
- Security research publications on cloud vulnerabilities

## Contributing

We welcome contributions that enhance our cloud-specific threat intelligence. Please follow our contribution guidelines when submitting:
- New cloud attack vectors with evidence
- Provider-specific remediation steps with validation
- Detection implementations for cloud security services
- STIX-formatted data following our schema extensions

If you are interested in contributing to this project, please [sign up with your email address](https://csaurl.org/WG-CAVEaT-Form)

## License

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
