# Cloud Security Alliance CTI

## CAVEaT

Cloud Adversarial, Vectors, and Threats (CAVEaT) [Chatbot (v3) ](https://chatgpt.com/g/g-xXpnPwHaD-cloud-adversarial-vectors-and-threat-solutions-v3)

An example of creating an entry: https://chatgpt.com/share/67356abd-a78c-8013-91b1-473053aea9c2

## Strategy

Based on the fact that adding security features to Cloud services is not cheap (often hundreds of thousands or even millions of dollars to deploy a major feature or new security service) we can use the creation and enhancement of such services as a signal that something is enough of a problem to actual warrant spending money on fixing it.

One example of this is AWS S3 GuardDuty which provides integrated AV scanning of content uploaded to S3, Microsoft has a similar solution using Defender and while Google does not have an integrated solution they do have an official document describing how to build something using ClamAV.

Thus we want to make a list of sources to monitor, for example:

* AWS/Azure/GCE security announcements (blogs, API changes, CLI changes, etc.)
* Sites like https://awsapichanges.com/, https://awsiamchanges.com/, https://gcpapichanges.com/, https://azureiamchanges.com/ and so on
* Security blogs, especially product announcements: https://blog.cloudflare.com/tag/security/
