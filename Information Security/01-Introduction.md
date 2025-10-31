# 01 Information Security Introduction

## Table of Contents

1. [Overview](#overview)
2. [The CIA Triad](#the-cia-triad)
3. [Core Security Principles](#core-security-principles)
4. [Threat Modeling](#threat-modeling)
5. [Attack Surfaces and Vectors](#attack-surfaces-and-vectors)
6. [Security Domains](#security-domains)
7. [Common Security Threats](#common-security-threats)
8. [Security Mechanisms](#security-mechanisms)
9. [Security Lifecycle](#security-lifecycle)
10. [Risk Management](#risk-management)

## Overview

**Information Security** (InfoSec) is the practice of protecting information by mitigating information risks. It involves protecting information and information systems from unauthorized access, use, disclosure, disruption, modification, or destruction to ensure confidentiality, integrity, and availability.

### Primary Goals

Information security aims to protect information assets through:

- **Prevention**: Implementing controls to prevent security incidents
- **Detection**: Identifying security breaches and anomalies
- **Response**: Reacting to security incidents effectively
- **Recovery**: Restoring systems and data after security incidents

### Why Information Security Matters

- **Data Breaches**: Exposure of sensitive information
- **Financial Loss**: Theft, ransomware, recovery costs, legal penalties
- **Reputation Damage**: Loss of customer trust
- **Operational Disruption**: Downtime and productivity loss
- **Legal Compliance**: Violations of regulations (GDPR, HIPAA, PCI DSS)
- **IP Theft**: Loss of competitive advantage

## The CIA Triad

The **CIA Triad** is the foundational model for information security policies and implementations.

### Confidentiality

Ensures information is accessible only to authorized entities.

**Mechanisms**: Encryption, access control lists, authentication, physical security, data masking

**Threats**: Eavesdropping, social engineering, insider threats, unauthorized access

### Integrity

Ensures information remains accurate and unmodified except by authorized processes.

**Mechanisms**: Hash functions (SHA-256), digital signatures, MACs, input validation, database constraints

**Threats**: Man-in-the-middle attacks, data tampering, SQL injection, malware

### Availability

Ensures information and systems are accessible to authorized users when needed.

**Mechanisms**: Redundancy, load balancing, DDoS protection, backups, disaster recovery

**Threats**: DoS/DDoS attacks, hardware failures, natural disasters, ransomware

### Extended Models

Modern security frameworks extend the CIA triad:

- **Authenticity**: Verifying the genuineness of information and its source
- **Non-repudiation**: Ensuring that actions cannot be denied after the fact
- **Accountability**: Tracing actions to responsible entities

## Core Security Principles

### 1. Least Privilege

Users and processes should have only the minimum access rights necessary to perform their functions.

**Benefits:**
- Reduces attack surface
- Limits damage from compromised accounts
- Simplifies security auditing

**Implementation:**
- Role-Based Access Control (RBAC)
- Just-In-Time (JIT) access provisioning
- Regular access reviews

### 2. Defense in Depth

Implement multiple layers of security controls throughout an IT system.

**Layered Approach:**
```
┌─────────────────────────────────────┐
│    Physical Security                │
│  ┌──────────────────────────────┐   │
│  │  Perimeter Security          │   │
│  │ ┌────────────────────────┐   │   │
│  │ │ Network Security       │   │   │
│  │ │ ┌──────────────────┐   │   │   │
│  │ │ │ Host Security    │   │   │   │
│  │ │ │ ┌────────────┐   │   │   │   │
│  │ │ │ │ Application│   │   │   │   │
│  │ │ │ │   Data     │   │   │   │   │
│  │ │ │ └────────────┘   │   │   │   │
│  │ │ └──────────────────┘   │   │   │
│  │ └────────────────────────┘   │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 3. Separation of Duties

Critical tasks should require multiple parties to complete, preventing fraud and errors.

**Examples:**
- Code review before deployment
- Multi-signature approval for financial transactions
- Separate roles for development, testing, and production

### 4. Fail-Safe Defaults

Systems should default to a secure state when errors occur.

**Principles:**
- Deny access by default; explicitly grant permissions
- Fail closed rather than open
- Disable unnecessary services and features

### 5. Complete Mediation

Every access to every resource must be checked for authorization.

**Implementation:**
- Avoid caching authorization decisions
- Validate permissions on each request
- Implement centralized authorization services

### 6. Open Design

Security should not depend on secrecy of implementation (Kerckhoffs's principle).

**Implications:**
- Use peer-reviewed cryptographic algorithms
- Avoid security through obscurity
- Open-source security tools benefit from community review

### 7. Psychological Acceptability

Security mechanisms should be usable and not unduly interfere with legitimate work.

**Considerations:**
- Balance security with user experience
- Provide clear security indicators
- Minimize friction in authentication flows

## Threat Modeling

**Threat modeling** is the systematic process of identifying and evaluating potential threats to a system.

### STRIDE Framework

A Microsoft-developed threat classification model:

| Threat | Security Property Violated | Example |
|--------|---------------------------|---------|
| **Spoofing** | Authentication | Impersonating another user |
| **Tampering** | Integrity | Modifying data in transit or at rest |
| **Repudiation** | Non-repudiation | Denying performed actions |
| **Information Disclosure** | Confidentiality | Exposing sensitive information |
| **Denial of Service** | Availability | Making systems unavailable |
| **Elevation of Privilege** | Authorization | Gaining unauthorized permissions |

### Threat Modeling Process

1. **Identify Assets**: Determine what needs protection (data, systems, services)
2. **Create Architecture Overview**: Document system components and data flows
3. **Identify Threats**: Use frameworks like STRIDE or PASTA
4. **Assess Risk**: Evaluate likelihood and impact
5. **Identify Mitigations**: Design controls to address threats
6. **Validate**: Test that mitigations are effective

### Attack Trees

Hierarchical diagrams representing how an asset might be attacked. Example: Goal (Steal User Data) can be achieved through Exploit Web App (SQL Injection, XSS) or Social Engineering (Phishing, Pretexting).

## Attack Surfaces and Vectors

### Attack Surface

The **attack surface** is the sum of all points where an unauthorized user can try to enter or extract data.

**Types:**
- **Network attack surface**: Open ports, services, protocols
- **Physical attack surface**: Access to hardware, USB ports
- **Software attack surface**: Applications, libraries, OS
- **Human attack surface**: Social engineering targets

**Reducing Attack Surface:**
- Disable unnecessary services
- Minimize exposed APIs
- Implement network segmentation
- Regular security patching

### Attack Vectors

**Attack vectors** are the paths or means by which attackers gain unauthorized access.

| Vector | Description | Example |
|--------|-------------|---------|
| **Email** | Malicious attachments or links | Phishing, malware distribution |
| **Web Applications** | Exploiting vulnerabilities | SQL injection, XSS |
| **Networks** | Intercepting or manipulating traffic | Man-in-the-middle, packet sniffing |
| **Physical** | Direct access to systems | Stolen devices, USB attacks |
| **Supply Chain** | Compromising third-party components | Malicious libraries, backdoored hardware |
| **Insider Threats** | Malicious or negligent insiders | Data exfiltration, sabotage |

## Security Domains

1. **Physical Security**: Access control, surveillance, environmental controls
2. **Network Security**: Firewalls, IDS/IPS, VPNs, TLS/SSL
3. **Application Security**: Secure SDLC, input validation, security testing
4. **Data Security**: Encryption, DLP, key management, data classification
5. **Identity and Access Management (IAM)**: Authentication, authorization, SSO
6. **Endpoint Security**: Antivirus, EDR, device encryption, MDM

## Common Security Threats

### Malware

**Malware** (malicious software) is software designed to disrupt, damage, or gain unauthorized access to computer systems.

| Type | Behavior | Impact |
|------|----------|--------|
| **Virus** | Self-replicating code attached to files | Data corruption, system slowdown |
| **Worm** | Self-replicating over networks | Network congestion, mass infection |
| **Trojan** | Disguised as legitimate software | Backdoors, data theft |
| **Ransomware** | Encrypts data, demands payment | Data unavailability, financial loss |
| **Spyware** | Monitors user activity | Privacy violation, credential theft |
| **Rootkit** | Hides presence and activities | Persistent access, difficult removal |

### Social Engineering

Exploits human psychology: Phishing, spear phishing, pretexting, baiting, quid pro quo, tailgating

### Web Application Attacks

SQL Injection, XSS, CSRF, remote code execution, directory traversal

### Network Attacks

Man-in-the-Middle (MitM), DNS spoofing, ARP poisoning, session hijacking, DoS/DDoS

## Security Mechanisms

### Cryptography

Mathematical techniques for secure communication in the presence of adversaries.

**Core Services:**
- **Confidentiality**: Encryption algorithms (AES, ChaCha20)
- **Integrity**: Hash functions (SHA-256, SHA-3)
- **Authentication**: Message Authentication Codes (HMAC)
- **Non-repudiation**: Digital signatures (RSA, ECDSA)

### Firewalls

Network security devices that monitor and control traffic based on security rules.

**Types:**
- **Packet-filtering**: Inspects packet headers
- **Stateful inspection**: Tracks connection states
- **Application-layer**: Deep packet inspection, protocol-aware
- **Next-generation**: Includes IPS, application awareness, threat intelligence

### Intrusion Detection Systems (IDS)

Monitors network or system activities for malicious activities or policy violations.

**Detection Methods:**
- **Signature-based**: Matches known attack patterns
- **Anomaly-based**: Detects deviations from normal behavior
- **Stateful protocol analysis**: Tracks protocol states

**Deployment:**
- **Network-based (NIDS)**: Monitors network traffic
- **Host-based (HIDS)**: Monitors individual hosts

### Multi-Factor Authentication (MFA)

Authentication using two or more verification factors:

1. **Something you know**: Password, PIN
2. **Something you have**: Token, smart card, mobile device
3. **Something you are**: Biometrics (fingerprint, facial recognition)
4. **Somewhere you are**: Geolocation
5. **Something you do**: Behavioral biometrics

## Security Lifecycle

Information security is an ongoing process, not a one-time implementation.

### Security Development Lifecycle

1. **Planning**: Requirements, risk assessment, policies
2. **Design**: Threat modeling, architecture, control selection
3. **Implementation**: Secure coding, testing, code reviews
4. **Testing**: Vulnerability scanning, penetration testing, audits
5. **Deployment**: Configuration, hardening, monitoring
6. **Operations**: Monitoring, incident response, patch management
7. **Decommissioning**: Data disposal, asset retirement, access revocation

**Continuous Security**: Ongoing monitoring, assessment, and improvement based on evolving threats

## Risk Management

**Risk management** is the process of identifying, assessing, and controlling threats to an organization's assets.

### Risk Assessment Process

1. **Identify Assets**: Catalog systems, data, and services
2. **Identify Threats**: Determine potential threats to assets
3. **Identify Vulnerabilities**: Find weaknesses that threats can exploit
4. **Assess Likelihood**: Estimate probability of threat occurrence
5. **Assess Impact**: Evaluate potential damage
6. **Calculate Risk**: Risk = Likelihood × Impact

### Risk Treatment Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Avoidance** | Eliminate the risk by removing the activity | Risk exceeds benefit |
| **Mitigation** | Implement controls to reduce risk | Cost-effective controls exist |
| **Transfer** | Shift risk to third party (insurance) | Risk is external or insurable |
| **Acceptance** | Accept the risk without action | Risk is within acceptable tolerance |

### Risk Metrics

- **Annualized Loss Expectancy (ALE)**: Expected annual loss from a risk
  - ALE = Single Loss Expectancy × Annual Rate of Occurrence
- **Return on Security Investment (ROSI)**: Justifying security spending
- **Mean Time to Detect (MTTD)**: Average time to identify incidents
- **Mean Time to Respond (MTTR)**: Average time to contain incidents

## Summary

Information security protects information assets through core principles (CIA triad, defense in depth, least privilege), threat awareness, layered defenses across multiple domains, and continuous risk management. Effective security requires technical controls, organizational policies, and security-aware culture that adapts to evolving threats.

## Related Topics

- [Access Control and Authentication](02-Access-Control-and-Authentication.md)
- [Cryptography](03-Cryptography.md)
- [Web Security](04-Web-Security.md)
- [Network Security](05-Network-Security.md)
- [Database Security](06-Database-Security.md)

## References

- Anderson, R. (2020). *Security Engineering: A Guide to Building Dependable Distributed Systems* (3rd ed.)
- Stallings, W., & Brown, L. (2018). *Computer Security: Principles and Practice* (4th ed.)
- NIST Special Publication 800-53: Security and Privacy Controls
- OWASP (Open Web Application Security Project) - Security Knowledge Framework
- ISO/IEC 27001: Information Security Management Systems
- SANS Institute - Information Security Resources
