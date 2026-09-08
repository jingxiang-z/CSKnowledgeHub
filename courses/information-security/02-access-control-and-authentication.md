# 02 Access Control and Authentication

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Authentication Factors](#authentication-factors)
4. [Authentication Protocols](#authentication-protocols)
5. [Access Control Models](#access-control-models)
6. [Authorization Mechanisms](#authorization-mechanisms)
7. [Identity and Access Management (IAM)](#identity-and-access-management-iam)
8. [Single Sign-On (SSO)](#single-sign-on-sso)
9. [Federated Identity](#federated-identity)
10. [Best Practices](#best-practices)

## Overview

**Authentication** and **access control** are fundamental security mechanisms that determine who can access systems and what they can do once authenticated.

**Key Concepts:**

- **Identification**: Claiming an identity (e.g., username)
- **Authentication**: Proving the claimed identity
- **Authorization**: Granting or denying access to resources
- **Accountability**: Tracking and logging user actions

### Authentication vs. Authorization

**Authentication** ("Who are you?"): Verifies identity, validates credentials, happens first (e.g., login)

**Authorization** ("What can you do?"): Grants permissions, checks access rights, happens after authentication (e.g., admin panel access)

## Authentication

**Authentication** is the process of verifying the identity of a user, device, or system.

### Password-Based Authentication

The most common authentication method, relying on shared secrets.

**Password Security Requirements:**
- **Length**: 12-16+ characters (brute-force resistance)
- **Complexity**: Mix of letters, numbers, symbols
- **Uniqueness**: Different per service (limits breach impact)
- **Storage**: Hashed with salt (bcrypt, Argon2)

**Password Attacks**: Brute force, dictionary, rainbow tables, credential stuffing, phishing

**Defenses**: Rate limiting, hashing with salt (Argon2/bcrypt), strength meters, breach detection, MFA

### Certificate-Based Authentication

Uses digital certificates issued by a Certificate Authority (CA).

**Public Key Infrastructure (PKI)**: Certificate Authority issues certificates to clients, who use them for mutual TLS authentication with servers

**Advantages**: Strong cryptographic authentication, non-repudiation, scalable, supports mTLS

**Use Cases**: VPN, smart cards, IoT device authentication, code signing

### Biometric Authentication

Authentication based on physical (fingerprint, iris, face) or behavioral (keystroke, gait, voice) characteristics.

**Advantages**: Cannot be lost/forgotten, difficult to forge, user-friendly

**Challenges**: Privacy concerns, cannot be changed if compromised, environmental sensitivity, expensive, potential discrimination

**Best Practices**: Use as part of MFA (not sole factor), store encrypted templates (not raw data), implement liveness detection

## Authentication Factors

Authentication strength increases by combining multiple factors.

### The Five Factors

1. **Something You Know**: Passwords, PINs (vulnerable to phishing)
2. **Something You Have**: Tokens, smart cards, mobile devices (risk of theft)
3. **Something You Are**: Biometrics (cannot be changed if compromised)
4. **Somewhere You Are**: Geolocation, IP address (can be spoofed)
5. **Something You Do**: Behavioral biometrics (requires continuous monitoring)

### Multi-Factor Authentication (MFA)

**MFA** requires two or more authentication factors from different categories.

**Common MFA Methods**: SMS OTP (low strength, SIM swapping risk), TOTP apps (medium), hardware tokens (high), push notifications (medium-high), biometric + PIN (high)

**Time-Based One-Time Password (TOTP):**
```
User Device                    Auth Server
    │                              │
    │  Shared Secret Key (K)       │ Shared Secret Key (K)
    │  Current Time (T)            │ Current Time (T)
    │        ↓                     │        ↓
    │  HMAC(K, T) → OTP            │  HMAC(K, T) → Expected OTP
    │                              │
    │────────── OTP ──────────────→│
    │                              │ Verify: OTP == Expected OTP
    │←────── Access Granted ───────│
```

**FIDO2/WebAuthn**: Modern passwordless standard using public key cryptography, hardware-backed security (TPM), phishing-resistant

## Authentication Protocols

### Kerberos

Network authentication protocol using symmetric-key cryptography and trusted third party (Key Distribution Center).

**Flow**: Client requests TGT from AS → receives encrypted TGT → requests service ticket from TGS → accesses service with ticket

**Components**: AS (issues TGTs), TGS (issues service tickets), Principals (users/services), Realm (domain)

**Advantages**: SSO, mutual authentication, no passwords over network, replay protection

**Limitations**: Requires clock synchronization, single point of failure, complex configuration

### OAuth 2.0

Authorization framework enabling third-party applications to obtain limited access to user accounts.

**Roles**: Resource Owner (user), Client (app), Authorization Server (issues tokens), Resource Server (hosts resources)

**Authorization Code Flow**: Client requests authorization → user authenticates & consents → client receives code → exchanges code for access token → accesses resources with token

**Grant Types**: Authorization Code (web apps), Client Credentials (service-to-service), Refresh Token (renew access)

**Security**: Use PKCE for mobile/SPA, validate redirect URIs, use state parameter (CSRF protection), short-lived access tokens, secure token storage

### SAML (Security Assertion Markup Language)

XML-based standard for exchanging authentication/authorization data between identity providers and service providers.

**Flow**: User requests SP resource → SP redirects to IdP → IdP authenticates → returns signed SAML assertion → SP grants access

**SAML vs. OAuth**: SAML (enterprise SSO, XML, high complexity) vs. OAuth 2.0 (API authorization, JSON, mobile-friendly)

### OpenID Connect (OIDC)

Identity layer on OAuth 2.0, adding authentication to authorization.

**OIDC Additions**: ID Token (JWT with user identity), UserInfo endpoint, standard scopes (openid, profile, email)

**ID Token**: JWT containing issuer, subject, audience, expiration, user claims (email, etc.)

## Access Control Models

Access control models define how permissions are granted to users.

### Discretionary Access Control (DAC)

Resource owner decides who can access the resource using Access Control Lists (ACLs). Common in file systems (Unix, NTFS).

**Example**: Unix permissions `-rwxr-xr--` (owner: read/write/execute, group: read/execute, others: read)

**Weaknesses**: Users may grant excessive permissions, hard to enforce policies, vulnerable to Trojan horse attacks

### Mandatory Access Control (MAC)

System enforces access rules based on security classifications. Centrally controlled, users cannot change permissions. Common in military/government.

**Bell-LaPadula (Confidentiality)**: No Read Up, No Write Down (prevents leakage)

**Biba (Integrity)**: No Read Down, No Write Up (prevents contamination)

**Security Labels:**
```
Top Secret
    ↑
  Secret
    ↑
Confidential
    ↑
Unclassified
```

### Role-Based Access Control (RBAC)

Permissions assigned to roles, users assigned to roles.

**RBAC Model:**
```
Users ──→ User-Role Assignment ──→ Roles ──→ Permission-Role Assignment ──→ Permissions
```

**Components**: Users, Roles (job functions), Permissions (operations), Sessions

**Example**: DBA role has permissions (read records, modify schema, backup/restore, grant permissions). Users Alice and Bob assigned to DBA role.

**Advantages**: Simplifies management, aligns with org structure, reduces overhead, supports separation of duties

**Constraints**: Mutually exclusive roles, cardinality limits, role prerequisites

### Attribute-Based Access Control (ABAC)

Access decisions based on attributes: subject (department, clearance), resource (classification, owner), action (read/write), environment (time, location)

**Example Policy**: ALLOW READ IF user.department == resource.department AND user.clearance >= resource.classification AND current_time IN business_hours

**XACML**: Standard for expressing ABAC policies

**Advantages**: Fine-grained, flexible, dynamic, context-aware, reduces role explosion

**Challenges**: Complex policy management, performance overhead, difficult auditing

## Authorization Mechanisms

### Access Control Lists (ACLs)

Lists attached to resources specifying permissions per user/group. Example: File Q4.pdf (Alice: read/write, Bob: read, Finance group: read)

**Advantages**: Fine-grained per-resource control, easy to understand, simple auditing

**Disadvantages**: Hard to answer "what can user access", scalability issues, management overhead

### Capability-Based Security

Users possess unforgeable tokens granting specific access rights. Transferable, system verifies capabilities (e.g., Unix file descriptors).

**ACLs vs. Capabilities**: ACLs (attached to resources, answers "who can access?", easy revocation) vs. Capabilities (attached to subjects, answers "what can access?", easy delegation)

## Identity and Access Management (IAM)

**IAM** is a framework of policies, processes, and technologies for managing digital identities and access rights.

### IAM Components

1. **Identity Lifecycle**: Provisioning, maintenance, deprovisioning
2. **Authentication**: Verify identity, support multiple methods, enforce MFA
3. **Authorization**: Determine permissions, enforce policies, support multiple models
4. **Directory Services**: Centralized repository (Active Directory, LDAP, Azure AD)
5. **Audit and Compliance**: Log events, generate reports, forensic support

### IAM Best Practices

Least privilege, zero trust, regular access reviews, automated provisioning/deprovisioning, privileged access management (PAM), identity governance

## Single Sign-On (SSO)

**SSO** allows users to authenticate once and access multiple applications without re-authenticating.

### SSO Benefits

Reduced password fatigue, improved security (fewer passwords), increased productivity, centralized management

### SSO Architectures

**Enterprise SSO**: User authenticates once to IdP → IdP issues tokens/assertions → grants access to multiple apps (A, B, C)

**Web SSO**: Session-based (shared cookies across subdomains, e.g., Google services) or Token-based (JWT/SAML, stateless, cross-domain)

### SSO Challenges and Mitigations

**Challenges**: Single point of failure (IdP outage), security risk (compromised account), session management complexity, legacy integration

**Mitigations**: High availability IdP, MFA, session timeouts, continuous authentication, break-glass procedures

## Federated Identity

**Federated identity** allows users from one domain to access resources in another domain without separate authentication.

### Federation Models

**Cross-Organization**: Org A IdP trusts Org B IdP → User A authenticates at IdP A → accesses App B (authorized by IdP B)

**Use Cases**: B2B partnerships, cloud services, academic collaborations, government services

### Federation Standards

SAML 2.0 (mature, enterprise), OAuth 2.0 + OIDC (modern, API-friendly), WS-Federation (Microsoft)

### Trust Models

Bilateral (direct trust), Multilateral (trust broker), Transitive (A trusts B, B trusts C → A trusts C)

### Federation Challenges

Trust establishment (legal/technical agreements), attribute mapping (schema differences), privacy (information sharing control), liability (authentication responsibility)

## Best Practices

### Authentication Best Practices

Enforce MFA (especially for privileged accounts), strong password policies (length > complexity), account lockout (prevent brute-force), secure credential storage (Argon2/bcrypt), breach monitoring, CAPTCHA, TLS/HTTPS only

### Authorization Best Practices

Default deny, least privilege, separation of duties, time-limited access, regular access reviews, centralized policy management (IAM systems)

### Session Management Best Practices

Secure session IDs (cryptographically random), session timeouts (idle + absolute), secure cookie flags (HttpOnly, Secure, SameSite), session invalidation on logout/password change, concurrent session limits, prevent session fixation (regenerate ID after auth)
