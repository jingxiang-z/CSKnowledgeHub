# 01 Computer Network Introduction

## Table of Contents

1. [Overview](#overview)
2. [Network Architecture](#network-architecture)
3. [Network Types and Topologies](#network-types-and-topologies)
4. [Data Switching Methods](#data-switching-methods)
5. [Network Performance Metrics](#network-performance-metrics)
6. [Protocol Layers](#protocol-layers)
7. [Summary](#summary)
8. [References](#references)

## Overview

A **computer network** is a collection of interconnected computing devices that exchange data and share resources. Networks form the foundation of modern computing infrastructure including the internet, enterprise systems, cloud computing, and IoT ecosystems.

### Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Connectivity** | Physical (Ethernet, fiber) and logical (VPNs, virtual networks) connections |
| **Resource Sharing** | Hardware, software, and data sharing across devices |
| **Scalability** | Support for network growth from PANs to global networks |
| **Reliability** | Fault tolerance through redundancy and error correction |

### Primary Functions

| Function | Description | Implementation |
|----------|-------------|----------------|
| **Data Communication** | Transfer information between devices | TCP/IP, UDP protocols |
| **Resource Sharing** | Shared access to resources | File/print servers |
| **Distributed Processing** | Divide tasks across nodes | Cloud computing, distributed systems |
| **Reliability** | Maintain operations despite failures | Redundancy, failover mechanisms |

## Network Architecture

Network architecture defines the structure and design of a network, including physical and logical components.

### Network Edges and Core

```
┌─────────────────────────────────────────────────┐
│  NETWORK EDGE (End Devices + Access Networks)  │
│  [PC] [Laptop] [Phone] [Server]                │
│       ↓         ↓        ↓       ↓              │
│  [Ethernet] [WiFi AP] [DSL/Cable Modem]        │
└───────────────────┬─────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  NETWORK CORE (ISP Infrastructure)              │
│     [Router]────[Router]────[Router]            │
│        │           │           │                │
│     [Router]────[Router]────[Router]            │
│  • High-speed backbone links                    │
│  • Internet Exchange Points (IXPs)              │
│  • Tier 1/2/3 ISPs                             │
└─────────────────────────────────────────────────┘
```

**Network Edge Components:**
- **End Devices:** Clients, servers, IoT devices, edge computing nodes
- **Access Networks:** DSL, cable, FTTH, Ethernet, Wi-Fi, cellular (4G/5G)
- **Access Points:** Switches, wireless APs, modems, SOHO routers

**Network Core Components:**
- **Core Routers:** High-capacity packet switches (Tbps throughput)
- **Backbone Networks:** Fiber optic links (10G, 40G, 100G, 400G Ethernet)
- **ISP Hierarchy:**
  - **Tier 1:** Global reach, peer with other Tier 1, no transit payments
  - **Tier 2:** Regional/national, purchase transit from Tier 1
  - **Tier 3:** Local access, purchase transit from Tier 2
- **IXPs:** Direct peering infrastructure between ISPs
- **Network Services:** DNS, DHCP, CDNs, firewalls

## Network Types and Topologies

### Classification by Scope

| Type | Range | Characteristics | Examples |
|------|-------|-----------------|----------|
| **PAN** | 0-10m | Personal devices, low power | Bluetooth, USB, NFC |
| **LAN** | 10m-1km | Single building/campus, high speed | Ethernet, Wi-Fi |
| **MAN** | 1-50km | City-wide, fiber backbone | Metro Ethernet |
| **WAN** | 50km+ | Long distance, interconnects LANs | Internet, MPLS |

### Common Topologies

**Bus Topology:**
```
[Node A]──[Node B]──[Node C]──[Node D]
          Shared Bus
```
- **Pros:** Simple, low cost
- **Cons:** Single point of failure, limited scalability

**Star Topology:**
```
       [Central Switch]
        /    |    \
    [A]    [B]    [C]
```
- **Pros:** Easy management, fault isolation
- **Cons:** Central device is single point of failure

**Ring Topology:**
```
[A]→[B]→[C]→[D]→[A]
```
- **Pros:** Predictable performance
- **Cons:** Break disrupts entire network

**Mesh Topology:**
```
[A]─┬─[B]
 │ ×│× │
[D]─┴─[C]
```
- **Pros:** High reliability, multiple paths
- **Cons:** Complex, expensive

## Data Switching Methods

### Circuit Switching

Establishes a dedicated communication path for the entire connection duration.

```
Setup → Data Transfer (Dedicated Path) → Teardown
```

**Characteristics:**
- Connection-oriented with call setup
- Reserved bandwidth for entire duration
- Constant delay, guaranteed QoS
- Inefficient resource utilization (idle periods waste capacity)

**Examples:** PSTN, ISDN

### Packet Switching

Data divided into packets, independently routed through the network.

```
Message: "HELLO" → Packets: [HE][LL][O]
Each packet routed independently
May arrive out of order → Reassemble at destination
```

**Characteristics:**
- Connectionless (datagram) or connection-oriented (virtual circuit)
- Statistical multiplexing (shared resources)
- Store-and-forward at routers
- Variable delay, efficient resource use

**Packet Structure:**
```
┌──────────────┬─────────────────┐
│   Header     │    Payload      │
├──────────────┼─────────────────┤
│ • Src Addr   │                 │
│ • Dst Addr   │  Application    │
│ • Seq #      │     Data        │
│ • Protocol   │                 │
│ • Checksum   │                 │
└──────────────┴─────────────────┘
```

**Examples:** Internet (TCP/IP), Ethernet

### Comparison

| Aspect | Circuit Switching | Packet Switching |
|--------|------------------|------------------|
| **Connection** | Dedicated | Shared |
| **Resource Allocation** | Fixed (entire duration) | Dynamic (on-demand) |
| **Efficiency** | Low (idle resources wasted) | High (statistical multiplexing) |
| **Delay** | Constant, predictable | Variable (congestion-dependent) |
| **Setup** | Required | Minimal/none |
| **Best For** | Voice, continuous data | Bursty data (web, email) |
| **Failure Impact** | Entire call disrupted | Packets reroute |

## Network Performance Metrics

### Latency

Total time for data to travel from source to destination.

**Components:**

```
Total Latency = Transmission Delay + Propagation Delay +
                Processing Delay + Queueing Delay
```

**1. Transmission Delay:** Time to push bits onto link
```
T_trans = L / R
where L = packet size (bits), R = bandwidth (bps)
```

**Example:** 1500 bytes, 100 Mbps → 0.12 ms

**2. Propagation Delay:** Time for signal to travel through medium
```
T_prop = D / S
where D = distance, S = propagation speed
```

**Propagation speeds:**
- Copper/Fiber: ~2 × 10⁸ m/s (2/3 speed of light)
- Wireless: ~3 × 10⁸ m/s (speed of light)

**Example:** 3000 km fiber → 15 ms

**3. Processing Delay:** Router processing time (μs to ms)

**4. Queueing Delay:** Wait time in router queues (most variable)

**Round-Trip Time (RTT):** Time for packet + acknowledgment return

### Throughput

Actual data transfer rate achieved.

```
Throughput = Data Transferred / Time
```

**Bottleneck Link:** Slowest link limits end-to-end throughput

```
Link 1: 10 Mbps → Link 2: 100 Mbps → Link 3: 1 Mbps → Link 4: 10 Mbps
                        Bottleneck ↑
End-to-end throughput ≈ 1 Mbps
```

**Factors affecting throughput:**
- Bandwidth, latency, packet loss
- Protocol overhead
- Network congestion
- TCP window size

### Bandwidth

Maximum data transfer capacity of a link.

**Bandwidth-Delay Product (BDP):**
```
BDP = Bandwidth × RTT
```

Represents amount of data "in flight" on the network.

**Example:** 100 Mbps × 50 ms = 625 KB in flight

### Packet Loss and Jitter

**Packet Loss:** Percentage of packets that fail to reach destination
```
Loss Rate = (Packets Lost / Total Sent) × 100%
```

**Causes:** Buffer overflow, transmission errors, routing failures

**Jitter:** Variation in packet delay over time

Important for real-time applications (VoIP, video conferencing)

## Protocol Layers

### OSI Model (7 Layers)

```
┌────────────────────────────────────────────────┐
│ 7. APPLICATION    │ HTTP, FTP, SMTP, DNS       │
├────────────────────────────────────────────────┤
│ 6. PRESENTATION   │ SSL/TLS, JPEG, encryption  │
├────────────────────────────────────────────────┤
│ 5. SESSION        │ NetBIOS, RPC               │
├────────────────────────────────────────────────┤
│ 4. TRANSPORT      │ TCP, UDP                   │
├────────────────────────────────────────────────┤
│ 3. NETWORK        │ IP, ICMP, routing          │
├────────────────────────────────────────────────┤
│ 2. DATA LINK      │ Ethernet, Wi-Fi, MAC       │
├────────────────────────────────────────────────┤
│ 1. PHYSICAL       │ Cables, fiber, radio       │
└────────────────────────────────────────────────┘
```

### TCP/IP Model (4 Layers)

```
┌────────────────────────────────────────────────┐
│ 4. APPLICATION    │ HTTP, FTP, SMTP, DNS       │
│                   │ (Combines OSI 5, 6, 7)     │
├────────────────────────────────────────────────┤
│ 3. TRANSPORT      │ TCP, UDP                   │
├────────────────────────────────────────────────┤
│ 2. INTERNET       │ IP, ICMP, routing          │
├────────────────────────────────────────────────┤
│ 1. LINK           │ Ethernet, Wi-Fi            │
│                   │ (Combines OSI 1, 2)        │
└────────────────────────────────────────────────┘
```

### Model Comparison

| Aspect | OSI Model | TCP/IP Model |
|--------|-----------|--------------|
| **Layers** | 7 | 4 |
| **Origin** | Theoretical (ISO) | Practical (Internet) |
| **Adoption** | Less common | Dominant |

### Encapsulation

Data gains headers as it moves down the protocol stack:

```
Application:  [Data]
Transport:    [TCP][Data]
Network:      [IP][TCP][Data]
Data Link:    [Eth][IP][TCP][Data][FCS]
Physical:     01001011010...
```

Each layer adds its header; receiving end reverses the process (decapsulation).

### Network Security Fundamentals

**Security Objectives:**

1. **Confidentiality:** Encryption (SSL/TLS, IPsec)
2. **Integrity:** Checksums, digital signatures
3. **Authentication:** Certificates, passwords
4. **Availability:** DDoS protection, redundancy
5. **Non-repudiation:** Digital signatures

**Common Threats:**

| Threat | Description | Mitigation |
|--------|-------------|------------|
| **Eavesdropping** | Traffic interception | Encryption |
| **Man-in-the-Middle** | Intercept and alter | Authentication + encryption |
| **Denial of Service** | Resource exhaustion | Rate limiting, filtering |
| **IP Spoofing** | Forge source address | Ingress filtering |

**Security Mechanisms:**
- **Firewalls:** Packet filtering, stateful inspection
- **VPNs:** Encrypted tunnels over public networks
- **IDS/IPS:** Intrusion detection/prevention
- **Encryption:** SSL/TLS, IPsec, WPA2/WPA3

## Summary

Computer networks enable communication and resource sharing between distributed devices. Key concepts:

**Architecture:**
- Network edge: end devices and access networks
- Network core: routers, ISPs, backbone links
- Hierarchical ISP structure (Tier 1/2/3)

**Switching:**
- Circuit switching: dedicated path, constant delay, inefficient
- Packet switching: shared resources, variable delay, efficient

**Performance:**
- Latency: sum of transmission, propagation, processing, queueing delays
- Throughput: limited by bottleneck link
- Bandwidth: maximum link capacity
- Packet loss and jitter affect quality

**Protocol Layers:**
- OSI: 7-layer theoretical model
- TCP/IP: 4-layer practical model
- Encapsulation: adding headers at each layer

**Security:**
- Objectives: confidentiality, integrity, authentication, availability
- Threats: eavesdropping, MITM, DoS, spoofing
- Mechanisms: firewalls, VPNs, encryption, IDS/IPS

## References

**Course Materials:**
- CSEE 4119: An Introduction to Computer Networks - Columbia University

**Textbooks:**
- Kurose, James F., and Keith W. Ross. *Computer Networking: A Top-Down Approach*. 8th Edition, Pearson, 2021.

**Standards:**
- RFC 791: Internet Protocol
- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol
- ISO/IEC 7498-1: OSI Reference Model
