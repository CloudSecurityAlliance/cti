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

TODO: add support for the following:

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

### Git Repository Setup for CTI Data Contributions

To contribute to the CTI repository:

1. **Fork the repository**:
   - Visit https://github.com/CloudSecurityAlliance/cti/
   - Click the "Fork" button in the upper right corner
   - This creates your own copy of the repository under your GitHub account

2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/cti.git
   cd cti
   ```

3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/CloudSecurityAlliance/cti.git
   ```
   This allows you to keep your fork synchronized with the main repository.

4. **Create a branch for your work**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make changes, commit, and push to your fork**:
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Visit your fork on GitHub
   - Click "Pull Request"
   - Select your branch and the main repository's main branch
   - Provide a description of your changes
   - Submit the pull request

### Using WG-CAVEaT Tools

The Cloud Security Alliance Working Group for CAVEaT provides a variety of tools to help with creating, validating, and managing STIX data for cloud threats:

1. **Access the tools repository**:
   - Visit https://github.com/CloudSecurityAlliance-WG/WG-CAVEaT
   - This repository contains tools, templates, and utilities specifically designed for working with cloud threat intelligence

2. **Set up local environment with Model Context Protocol**:
   - Follow the setup instructions in the WG-CAVEaT repository to configure AI assistants for local file access
   - This enables more efficient creation and validation of STIX objects

3. **Use the provided templates**:
   - The repository includes templates for common cloud attack patterns
   - These templates help ensure consistency across contributions

4. **Leverage the CAVEaT chatbot prompts**:
   - The repository contains specialized prompts for working with AI assistants
   - These prompts help guide the creation of well-structured STIX objects

For detailed instructions on using these tools, refer to the [WG-CAVEaT repository](https://github.com/CloudSecurityAlliance-WG/WG-CAVEaT).

## License

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication
