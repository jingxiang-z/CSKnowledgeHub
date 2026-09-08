# 05 Network Security

## Table of Contents

1. [Overview](#overview)
2. [Network Security Fundamentals](#network-security-fundamentals)
3. [Firewalls](#firewalls)
4. [Virtual Private Networks (VPN)](#virtual-private-networks-vpn)
5. [Transport Layer Security (TLS/SSL)](#transport-layer-security-tlsssl)
6. [Network Segmentation](#network-segmentation)
7. [Intrusion Detection and Prevention](#intrusion-detection-and-prevention)
8. [DDoS Protection](#ddos-protection)
9. [Wireless Security](#wireless-security)
10. [DNS Security](#dns-security)
11. [Network Protocol Security](#network-protocol-security)

## Overview

**Network Security** protects the integrity, confidentiality, and availability of data as it is transmitted across or accessed through networks. It encompasses both hardware and software technologies and addresses threats at multiple layers of the network stack.

### Network Security Objectives

| Objective | Description | Mechanisms |
|-----------|-------------|------------|
| **Confidentiality** | Prevent unauthorized access to network traffic | Encryption, VPNs, TLS/SSL |
| **Integrity** | Ensure data is not modified in transit | Message authentication codes, digital signatures |
| **Availability** | Maintain network accessibility | DDoS protection, redundancy, failover |
| **Authentication** | Verify identity of communicating parties | Certificates, Kerberos, 802.1X |
| **Non-repudiation** | Prove message origin and delivery | Digital signatures, audit logs |

### Defense in Depth for Networks

Multiple security layers: Perimeter Security (Firewalls, IDS/IPS) → Network Segmentation (VLANs, DMZ) → Encrypted Communications (TLS, VPN) → Access Control (NAC, 802.1X) → Monitoring & Detection (SIEM)

## Network Security Fundamentals

### The OSI Model and Security

Security mechanisms operate at different layers of the OSI model:

| Layer | Security Concerns | Security Mechanisms |
|-------|------------------|---------------------|
| **7. Application** | Application-level attacks, data validation | WAF, application-layer firewalls, input validation |
| **6. Presentation** | Data format attacks, encoding issues | Data encryption, SSL/TLS |
| **5. Session** | Session hijacking, session fixation | Session management, secure cookies |
| **4. Transport** | Port scanning, TCP attacks | TLS/SSL, stateful firewalls |
| **3. Network** | IP spoofing, routing attacks | IPsec, packet filtering, DNSSEC |
| **2. Data Link** | MAC spoofing, ARP poisoning | 802.1X, port security, VLAN segmentation |
| **1. Physical** | Physical access, wiretapping | Physical security, fiber optics (harder to tap) |

### Common Network Threats

**Passive Attacks (Eavesdropping):**
- **Traffic Analysis**: Inferring information from traffic patterns
- **Packet Sniffing**: Capturing network traffic
- **Port Scanning**: Discovering open ports and services

**Active Attacks:**
- **IP Spoofing**: Forging source IP addresses
- **Man-in-the-Middle (MitM)**: Intercepting and potentially altering communications
- **Session Hijacking**: Taking over authenticated sessions
- **Replay Attacks**: Retransmitting captured legitimate messages
- **Denial of Service (DoS)**: Overwhelming resources
- **ARP Poisoning**: Redirecting traffic on local networks
- **DNS Spoofing**: Redirecting domain name resolution

## Firewalls

**Firewalls** are network security devices that monitor and control incoming and outgoing network traffic based on predetermined security rules.

### Firewall Types

#### 1. Packet-Filtering Firewalls

Inspect individual packets based on header information (source/destination IP, port, protocol).

**Characteristics**: Stateless, fast, cannot inspect payload, vulnerable to IP spoofing

**Example Rules**: Allow TCP 443 from 192.168.1.0/24, Allow UDP 53 to specific server, Deny Telnet (23), Deny all else

**Limitations**: No connection state tracking, difficult with dynamic ports, cannot detect application-layer attacks

#### 2. Stateful Inspection Firewalls

Track the state of network connections and make decisions based on connection context.

**Connection State Table:**
```
Source IP    | Dest IP      | Src Port | Dst Port | State       | Timeout
-------------|--------------|----------|----------|-------------|--------
192.168.1.5  | 93.184.216.34| 52341    | 443      | ESTABLISHED | 3600s
192.168.1.7  | 8.8.8.8      | 51923    | 53       | UDP         | 120s
```

**Advantages**: Understands connection context, better security than packet filtering, handles dynamic ports, protects against certain DoS attacks

**TCP Handshake Tracking**: Firewall tracks connection states (NEW → ESTABLISHED) through SYN, SYN+ACK, ACK sequence

#### 3. Application-Layer Firewalls (Proxy Firewalls)

Operate at the application layer, inspecting complete application protocol messages.

**Deep Packet Inspection (DPI)**: Examines payload, understands application protocols, blocks specific content, provides logging/filtering

**Proxy Functionality**: Intercepts client requests, inspects for attacks/malware, forwards to server, scans responses before returning to client

**Advantages**: Strongest security, protocol-aware, content inspection, malware scanning, user authentication

**Disadvantages**: Performance overhead, complex configuration, may break applications, privacy concerns

#### 4. Next-Generation Firewalls (NGFW)

Combine traditional firewall capabilities with additional features:

**NGFW Features**: Application control, integrated IPS, SSL/TLS inspection, user/identity awareness, threat intelligence, cloud sandboxing, advanced malware protection

### Firewall Architectures

#### Screened Subnet (DMZ)

```
Internet
   │
   ↓
[Firewall 1] ← External Firewall
   │
   ↓
[  DMZ   ] ← Web Servers, Mail Servers (public-facing)
   │
   ↓
[Firewall 2] ← Internal Firewall
   │
   ↓
Internal Network ← Database Servers, Application Servers
```

**Benefits**: Isolates public services, two protection layers for internal network, DMZ breach doesn't compromise internal network

**Dual-Homed Host**: Single firewall with multiple interfaces separating trusted/untrusted networks

**Bastion Host**: Hardened server in DMZ with minimal services, extensive logging, regular updates

## Virtual Private Networks (VPN)

**VPNs** create secure, encrypted tunnels over untrusted networks (typically the Internet).

### VPN Types

| Type | Use Case | Protocol | Layer |
|------|----------|----------|-------|
| **Remote Access VPN** | Employees connecting to corporate network | SSL/TLS, IPsec | 3-4 |
| **Site-to-Site VPN** | Connecting branch offices | IPsec | 3 |
| **Client-to-Site VPN** | Individual devices to network | OpenVPN, WireGuard | 3-4 |

### IPsec (Internet Protocol Security)

A protocol suite for securing IP communications through authentication and encryption.

**IPsec Components:**

1. **Authentication Header (AH)**
   - Provides integrity and authentication
   - Does not provide confidentiality
   - Protects against replay attacks

2. **Encapsulating Security Payload (ESP)**
   - Provides confidentiality (encryption)
   - Also provides integrity and authentication
   - Most commonly used

**IPsec Modes:**

**Transport Mode:**
```
Original IP Packet:
[IP Header][TCP Header][Data]

IPsec Transport Mode (ESP):
[IP Header][ESP Header][TCP Header][Data][ESP Trailer][ESP Auth]
            └────────── Encrypted ──────────┘
```
- Only payload is encrypted
- IP header remains visible
- Used for end-to-end communication

**Tunnel Mode:**
```
Original IP Packet:
[IP Header][TCP Header][Data]

IPsec Tunnel Mode (ESP):
[New IP Header][ESP Header][Original IP Header][TCP Header][Data][ESP Trailer][ESP Auth]
                          └──────────────── Encrypted ────────────────┘
```
- Entire original packet is encrypted
- New IP header added
- Used for site-to-site VPNs
- Hides internal network topology

**IPsec Connection Establishment (IKE):**

```
Phase 1: IKE SA (Security Association)
  - Establish secure channel for negotiation
  - Authenticate peers
  - Agree on encryption/hashing algorithms
  - Diffie-Hellman key exchange

Phase 2: IPsec SA
  - Negotiate IPsec parameters
  - Establish IPsec tunnel
  - Generate session keys for ESP/AH
```

### SSL/TLS VPN

Uses SSL/TLS protocol for VPN connections.

**Advantages over IPsec:**
- Works through most firewalls (uses TCP 443)
- No special client software (browser-based option)
- Easier to configure for end users
- Granular application-level access control

**Disadvantages:**
- Typically higher overhead
- May offer lower performance
- Limited to TCP-based applications (for browser-based)

### WireGuard

Modern VPN protocol designed for simplicity and performance.

**Features:**
- Minimal codebase (~4,000 lines vs. OpenVPN's ~100,000)
- Strong cryptography (ChaCha20, Curve25519)
- Excellent performance
- Built into Linux kernel
- Simplified configuration

## Transport Layer Security (TLS/SSL)

**TLS** (Transport Layer Security) is the cryptographic protocol that provides secure communication over networks.

### TLS Handshake

```
Client                                                Server
  │                                                     │
  │─────────── ClientHello ──────────────────────────→ │
  │  (Supported cipher suites, TLS version, random)    │
  │                                                     │
  │ ←────────── ServerHello ──────────────────────────│
  │  (Selected cipher suite, TLS version, random)      │
  │ ←────────── Certificate ───────────────────────────│
  │ ←────────── ServerKeyExchange ─────────────────────│ (if needed)
  │ ←────────── ServerHelloDone ───────────────────────│
  │                                                     │
  │─────────── ClientKeyExchange ─────────────────────→│
  │  (Premaster secret, encrypted with server's        │
  │   public key)                                       │
  │─────────── ChangeCipherSpec ──────────────────────→│
  │─────────── Finished ───────────────────────────────→│
  │  (Encrypted with session key)                       │
  │                                                     │
  │ ←────────── ChangeCipherSpec ──────────────────────│
  │ ←────────── Finished ───────────────────────────────│
  │  (Encrypted with session key)                       │
  │                                                     │
  │═══════════ Application Data ═══════════════════════│
```

### TLS 1.3 Improvements

**Key Changes:**
- **Faster handshake**: 1-RTT vs. 2-RTT (0-RTT for resumed sessions)
- **Removed weak algorithms**: RC4, SHA-1, MD5, DES, 3DES
- **Forward secrecy**: Mandatory (Diffie-Hellman required)
- **Encrypted handshake**: More of the handshake is encrypted
- **Simplified cipher suites**: Reduced from hundreds to five

**TLS 1.3 Handshake (1-RTT):**
```
Client                                      Server
  │                                            │
  │─ClientHello + KeyShare ───────────────────→│
  │                                            │
  │←─ServerHello + KeyShare───────────────────│
  │  {EncryptedExtensions}                     │
  │  {Certificate}                             │
  │  {CertificateVerify}                       │
  │  {Finished}                                │
  │                                            │
  │─{Finished}─────────────────────────────────→│
  │                                            │
  │═Application Data══════════════════════════│
```

### Certificate Validation

**X.509 Certificate Chain:**
```
┌──────────────────────┐
│ Root CA              │ ← Self-signed, trusted by OS/browser
└──────────┬───────────┘
           │ Signs
           ↓
┌──────────────────────┐
│ Intermediate CA      │
└──────────┬───────────┘
           │ Signs
           ↓
┌──────────────────────┐
│ example.com          │ ← Server certificate
│ (End Entity)         │
└──────────────────────┘
```

**Validation Steps:**
1. Verify certificate signature using issuer's public key
2. Check certificate validity period (notBefore, notAfter)
3. Verify domain name matches (Common Name or Subject Alternative Name)
4. Check Certificate Revocation List (CRL) or OCSP
5. Validate entire chain to trusted root CA

### Common TLS Attacks and Mitigations

| Attack | Description | Mitigation |
|--------|-------------|------------|
| **BEAST** | Exploits CBC mode in TLS 1.0 | Use TLS 1.2+ |
| **POODLE** | Exploits SSLv3 fallback | Disable SSLv3 |
| **Heartbleed** | OpenSSL vulnerability | Update OpenSSL |
| **FREAK** | Forces weak export ciphers | Disable export ciphers |
| **Logjam** | Weakens Diffie-Hellman | Use strong DH parameters (2048-bit+) |
| **DROWN** | Attacks SSLv2 | Disable SSLv2 |
| **CRIME/BREACH** | TLS compression attacks | Disable TLS compression |

## Network Segmentation

**Network segmentation** divides a network into smaller, isolated segments to limit the spread of attacks.

### Segmentation Strategies

#### 1. VLANs (Virtual LANs)

Logically segment a network at Layer 2.

```
Physical Switch
┌────────────────────────────────────────┐
│  VLAN 10: Management                   │
│  VLAN 20: Employees                    │
│  VLAN 30: Guests                       │
│  VLAN 40: IoT Devices                  │
└────────────────────────────────────────┘
```

**Benefits:**
- Broadcast domain isolation
- Improved performance
- Easier management
- Enhanced security (inter-VLAN routing can be controlled)

**VLAN Hopping Attack Prevention:**
- Disable unused ports
- Change native VLAN from default (VLAN 1)
- Use VLAN Access Control Lists (VACLs)

#### 2. Subnetting

Divide IP address space into smaller networks.

**Example:**
```
Corporate Network: 10.0.0.0/8
  ├─ Data Center: 10.1.0.0/16
  ├─ Office Network: 10.2.0.0/16
  │   ├─ Engineering: 10.2.1.0/24
  │   ├─ Sales: 10.2.2.0/24
  │   └─ HR: 10.2.3.0/24
  └─ Guest Network: 10.3.0.0/16
```

#### 3. Zero Trust Network Architecture

"Never trust, always verify" - assume breach and verify every access request.

**Principles:**
- Verify explicitly (authenticate and authorize every request)
- Use least privilege access
- Assume breach (minimize blast radius)
- Micro-segmentation (isolate workloads)

**Implementation:**
- Software-Defined Perimeter (SDP)
- Micro-segmentation with next-gen firewalls
- Identity-based access control
- Continuous monitoring and analytics

### DMZ (Demilitarized Zone)

Isolated network segment for public-facing services.

```
Internet
   │
   ↓
[External Firewall]
   │
   ├─→ [DMZ: Web Servers, Mail Servers]
   │
   ↓
[Internal Firewall]
   │
   ↓
[Internal Network: Databases, Application Servers]
```

**DMZ Best Practices:**
- Place only necessary public services in DMZ
- No direct connections from DMZ to internal network
- All DMZ traffic to internal network goes through firewall
- Harden DMZ systems
- Monitor DMZ extensively

## Intrusion Detection and Prevention

### Intrusion Detection Systems (IDS)

**IDS** monitor network traffic for suspicious activity and generate alerts.

**Detection Methods:**

1. **Signature-Based Detection**
   - Matches traffic against known attack patterns
   - Low false positives
   - Cannot detect new/unknown attacks
   - Requires regular signature updates

2. **Anomaly-Based Detection**
   - Establishes baseline of normal behavior
   - Detects deviations from baseline
   - Can detect zero-day attacks
   - Higher false positive rate

3. **Stateful Protocol Analysis**
   - Compares traffic against expected protocol behavior
   - Understands protocol semantics
   - Detects protocol violations and anomalies

**Deployment Types:**

**Network-based IDS (NIDS):**
```
Internet ─→ [Firewall] ─→ [Switch with SPAN port]
                                  │
                                  ↓ (mirrored traffic)
                            [NIDS Sensor]
                                  │
                                  ↓
                         [Management Console]
```

- Monitors network traffic
- Passive (out-of-band) or inline
- Strategic placement: perimeter, DMZ, critical subnets

**Host-based IDS (HIDS):**
- Monitors individual hosts
- Analyzes system calls, file integrity, logs
- Detects local attacks and policy violations
- Examples: OSSEC, Tripwire

### Intrusion Prevention Systems (IPS)

**IPS** actively blocks detected threats (inline deployment).

**IDS vs. IPS:**

| Feature | IDS | IPS |
|---------|-----|-----|
| **Deployment** | Passive (out-of-band) | Active (inline) |
| **Action** | Alert only | Alert and block |
| **Performance Impact** | Minimal | Can introduce latency |
| **False Positive Risk** | Annoying alerts | Blocked legitimate traffic |

**IPS Actions:**
- **Alert**: Generate alert (like IDS)
- **Drop**: Silently discard malicious packets
- **Reset**: Send TCP reset to terminate connection
- **Quarantine**: Isolate affected host
- **Rate Limit**: Throttle suspicious traffic

**Best Practices:**
- Start in IDS mode, tune, then enable IPS blocking
- Carefully review and update signatures
- Monitor false positives
- Ensure IPS doesn't become single point of failure
- Maintain high availability configuration

## DDoS Protection

**Distributed Denial of Service (DDoS)** attacks overwhelm resources with malicious traffic from multiple sources.

### DDoS Attack Types

| Layer | Attack Type | Mechanism | Mitigation |
|-------|-------------|-----------|------------|
| **Application (L7)** | HTTP flood, Slowloris | Exhaust application resources | Rate limiting, CAPTCHA, WAF |
| **Transport (L4)** | SYN flood, UDP flood | Exhaust connection table | SYN cookies, connection limits |
| **Network (L3)** | ICMP flood, IP fragment | Consume bandwidth | Traffic filtering, blackholing |
| **Amplification** | DNS, NTP, memcached | Amplify attack traffic | Rate limiting, BCP38 (ingress filtering) |

### DDoS Mitigation Strategies

**1. Traffic Scrubbing:**
```
Legitimate Traffic        Attack Traffic
        ↓                        ↓
        └────────┬───────────────┘
                 ↓
    [DDoS Mitigation Service]
         (Scrubbing Center)
                 │
        Clean Traffic Only
                 ↓
         [Protected Server]
```

**2. Anycast Network:**
- Distribute traffic across multiple locations
- Absorb large-scale attacks
- Used by CDNs and DNS providers

**3. Rate Limiting:**
- Limit requests per IP address/user
- Token bucket or leaky bucket algorithms
- Adaptive rate limiting based on behavior

**4. Challenge-Response:**
- CAPTCHA for human verification
- JavaScript challenges
- Proof-of-work challenges

**5. Traffic Analysis:**
- Distinguish legitimate from malicious traffic
- Machine learning for anomaly detection
- Behavioral analysis

### Amplification Attack Prevention

**DNS Amplification Example:**
```
Attacker sends small DNS query (60 bytes)
  with spoofed source IP (victim's IP)
    ↓
Open DNS Resolver
    ↓
Sends large DNS response (3000 bytes)
    ↓
Victim (50x amplification)
```

**Prevention:**
- **For resolvers**: Disable recursion for external queries
- **For networks**: Implement BCP38 (prevent IP spoofing)
- **For services**: Rate limit responses

## Wireless Security

### Wi-Fi Security Protocols

| Protocol | Year | Encryption | Security Level | Notes |
|----------|------|------------|---------------|-------|
| **WEP** | 1997 | RC4 | Broken | Never use |
| **WPA** | 2003 | TKIP | Weak | Deprecated |
| **WPA2** | 2004 | AES-CCMP | Good | Still widely used |
| **WPA3** | 2018 | AES-GCMP | Best | Recommended |

### WPA2 (802.11i)

**Authentication Modes:**

1. **WPA2-Personal (PSK)**
   - Pre-Shared Key
   - Single password for all users
   - Suitable for home/small office

2. **WPA2-Enterprise (802.1X)**
   - Individual user authentication
   - RADIUS server
   - Centralized management
   - Suitable for organizations

**4-Way Handshake:**
```
Client (Supplicant)          Access Point (Authenticator)
  │                                    │
  │←─────── ANonce ────────────────────│ (Message 1)
  │                                    │
  │─── SNonce + MIC ──────────────────→│ (Message 2)
  │ (Derives PTK)                      │ (Derives PTK)
  │                                    │
  │←─────── GTK + MIC ─────────────────│ (Message 3)
  │                                    │
  │─────────── ACK ────────────────────→│ (Message 4)
  │                                    │
  │═══════ Encrypted Communication ════│
```

**KRACK Attack (Key Reinstallation Attack):**
- Exploits WPA2 handshake
- Forces reuse of encryption keys
- Mitigation: Update devices, use WPA3

### WPA3 Improvements

**Key Features:**

1. **SAE (Simultaneous Authentication of Equals)**
   - Replaces PSK 4-way handshake
   - Resistant to offline dictionary attacks
   - Forward secrecy

2. **Individualized Data Encryption**
   - OWE (Opportunistic Wireless Encryption)
   - Encrypted traffic even on open networks

3. **192-bit Security Suite**
   - For government and enterprise
   - Stronger encryption algorithms

4. **Easy Connect**
   - QR code-based onboarding
   - Simplified IoT device setup

### Wireless Security Best Practices

- **Use WPA3** (or WPA2 if WPA3 unavailable)
- **Strong passwords**: Long, complex passphrases
- **Hide SSID**: Minor security benefit, but helps
- **MAC filtering**: Limited effectiveness (MAC can be spoofed)
- **Disable WPS**: Vulnerable to brute-force attacks
- **Network segmentation**: Separate guest and corporate networks
- **Regular firmware updates**: Patch vulnerabilities
- **Monitor for rogue APs**: Detect unauthorized access points

## DNS Security

### DNS Vulnerabilities

| Vulnerability | Attack | Impact |
|---------------|--------|--------|
| **Cache Poisoning** | Inject fake DNS records | Redirect users to malicious sites |
| **DNS Tunneling** | Exfiltrate data via DNS queries | Data theft, C&C communication |
| **DDoS** | Overwhelm DNS servers | Service unavailability |
| **DNS Hijacking** | Modify DNS settings | Redirect all traffic |
| **Subdomain Takeover** | Claim abandoned subdomains | Phishing, malware distribution |

### DNSSEC (DNS Security Extensions)

Adds cryptographic signatures to DNS records to ensure authenticity and integrity.

**DNSSEC Record Types:**
- **RRSIG**: Contains digital signature
- **DNSKEY**: Public key for verification
- **DS**: Delegation Signer (links child zone to parent)
- **NSEC/NSEC3**: Authenticated denial of existence

**DNSSEC Validation Chain:**
```
. (Root)
 └─ Signed by root KSK
    ↓
.com (TLD)
 └─ DS record in root zone
    └─ Signed by .com KSK
       ↓
example.com
 └─ DS record in .com zone
    └─ Signed by example.com KSK
       ↓
www.example.com
 └─ A record signed by example.com ZSK
```

**DNSSEC Limitations:**
- Does not provide confidentiality (no encryption)
- Increases DNS response size
- Complex key management
- Not widely deployed

### DNS over HTTPS (DoH) and DNS over TLS (DoT)

**Traditional DNS:**
```
Client ──UDP/53 (plaintext)──→ DNS Resolver
```
- Vulnerable to eavesdropping
- ISP can see all DNS queries
- Subject to manipulation

**DoT (DNS over TLS):**
```
Client ──TLS/853 (encrypted)──→ DNS Resolver
```

**DoH (DNS over HTTPS):**
```
Client ──HTTPS/443 (encrypted)──→ DNS Resolver
```

**DoH vs. DoT:**

| Feature | DoH | DoT |
|---------|-----|-----|
| **Port** | 443 (HTTPS) | 853 (dedicated) |
| **Protocol** | HTTPS | TLS |
| **Firewall Visibility** | Hard to block (port 443) | Easy to identify (port 853) |
| **Network Monitoring** | More difficult | Easier |
| **Browser Support** | Excellent | Limited |

## Network Protocol Security

### Secure Protocol Alternatives

| Insecure Protocol | Port | Secure Alternative | Port | Encryption |
|-------------------|------|-------------------|------|------------|
| **HTTP** | 80 | **HTTPS** | 443 | TLS |
| **FTP** | 21 | **SFTP** | 22 | SSH |
| **Telnet** | 23 | **SSH** | 22 | SSH |
| **SMTP** | 25 | **SMTPS** | 465/587 | TLS |
| **POP3** | 110 | **POP3S** | 995 | TLS |
| **IMAP** | 143 | **IMAPS** | 993 | TLS |
| **LDAP** | 389 | **LDAPS** | 636 | TLS |
| **DNS** | 53 | **DoT/DoH** | 853/443 | TLS |

### Protocol-Specific Security

**SSH (Secure Shell):**
- Public key authentication preferred over passwords
- Disable root login
- Use fail2ban to prevent brute-force
- Keep host keys secure
- Disable weak ciphers and MACs

**HTTPS:**
- Use TLS 1.2 or 1.3
- Strong cipher suites (AES-GCM, ChaCha20-Poly1305)
- Enable HSTS (HTTP Strict Transport Security)
- Implement Certificate Transparency
- Use OCSP stapling

**IPsec:**
- Use IKEv2 (not IKEv1)
- Strong encryption (AES-256)
- Perfect Forward Secrecy (PFS)
- Regular key rotation

### BGP Security

**Border Gateway Protocol (BGP)** is vulnerable to:
- **Route hijacking**: Announcing unauthorized IP prefixes
- **Route leaks**: Incorrectly propagating routes
- **DDoS amplification**: Exploiting BGP UPDATE messages

**BGP Security Measures:**
- **RPKI (Resource Public Key Infrastructure)**: Cryptographically validate route origins
- **BGP Route Filtering**: Filter invalid announcements
- **Prefix Limit**: Limit number of prefixes from peers
- **BGP Community Tags**: Control route propagation
- **IRR (Internet Routing Registry)**: Document routing policies
