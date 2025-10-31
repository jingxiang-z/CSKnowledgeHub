# 04 Network Layer

## Table of Contents

1. [Overview](#overview)
2. [IP Addressing](#ip-addressing)
3. [IPv4 Datagram](#ipv4-datagram)
4. [IPv6](#ipv6)
5. [Routing Fundamentals](#routing-fundamentals)
6. [Routing Algorithms](#routing-algorithms)
7. [Intra-AS Routing](#intra-as-routing)
8. [Inter-AS Routing](#inter-as-routing)
9. [ICMP](#icmp)
10. [NAT](#nat)
11. [Summary](#summary)
12. [References](#references)

## Overview

The **network layer** provides host-to-host communication, routing packets across networks from source to destination.

### Key Responsibilities

| Function | Description |
|----------|-------------|
| **Addressing** | Logical addressing (IP addresses) |
| **Routing** | Determine path from source to destination |
| **Forwarding** | Move packets from input to output port |
| **Fragmentation** | Break packets to fit link MTU |
| **Error Reporting** | ICMP messages |

### Network Layer Services

**Data Plane:** Per-router functions, determines how packet arriving on input port is forwarded to output port

**Control Plane:** Network-wide logic, determines how packets are routed among routers along end-to-end path

### Network Layer Protocols

- **IP (Internet Protocol):** Addressing, datagram format, packet handling
- **ICMP (Internet Control Message Protocol):** Error reporting, diagnostics
- **Routing Protocols:** OSPF, RIP, BGP

## IP Addressing

### IPv4 Addresses

**32-bit identifier** for host or router interface.

**Dotted-Decimal Notation:**
```
192.168.1.1
= 11000000.10101000.00000001.00000001 (binary)
```

**Interface:** Connection between host/router and physical link
- Router: Multiple interfaces
- Host: Typically one or two interfaces (Ethernet, WiFi)

### Classful Addressing (Historical)

| Class | First Bits | Range | Default Mask | Hosts per Network |
|-------|-----------|-------|--------------|-------------------|
| **A** | 0 | 0.0.0.0 - 127.255.255.255 | 255.0.0.0 (/8) | 16,777,214 |
| **B** | 10 | 128.0.0.0 - 191.255.255.255 | 255.255.0.0 (/16) | 65,534 |
| **C** | 110 | 192.0.0.0 - 223.255.255.255 | 255.255.255.0 (/24) | 254 |
| **D** | 1110 | 224.0.0.0 - 239.255.255.255 | N/A | Multicast |
| **E** | 1111 | 240.0.0.0 - 255.255.255.255 | N/A | Reserved |

**Problems:** Inflexible, address space exhaustion

### CIDR (Classless Inter-Domain Routing)

**Notation:** a.b.c.d/x where x is number of network bits

**Example:**
```
200.23.16.0/23
Network: 200.23.16.0 - 200.23.17.255 (512 addresses)
Hosts: 510 (minus network and broadcast addresses)

Binary:
11001000.00010111.0001000|0.00000000
                        ↑
                   23 bits for network
```

**Subnet Mask Calculation:**
```
/24 = 255.255.255.0
/23 = 255.255.254.0
/22 = 255.255.252.0
/16 = 255.255.0.0
/8  = 255.0.0.0
```

### Subnetting

Divide network into smaller subnetworks.

**Example: Subnet 200.23.16.0/23 into 4 subnets**

```
Original: 200.23.16.0/23 (512 addresses)

Subnet 1: 200.23.16.0/25   (128 addresses)
Subnet 2: 200.23.16.128/25 (128 addresses)
Subnet 3: 200.23.17.0/25   (128 addresses)
Subnet 4: 200.23.17.128/25 (128 addresses)

Each subnet:
- Network address: First address
- Broadcast address: Last address
- Usable hosts: Middle addresses
```

**Subnetting Steps:**
1. Determine number of subnets needed
2. Calculate subnet bits: ⌈log₂(subnets)⌉
3. New prefix length = original + subnet bits
4. Calculate subnet addresses

### Special IP Addresses

| Address | Purpose |
|---------|---------|
| **0.0.0.0** | This host, this network |
| **127.0.0.0/8** | Loopback (127.0.0.1) |
| **10.0.0.0/8** | Private (Class A) |
| **172.16.0.0/12** | Private (Class B) |
| **192.168.0.0/16** | Private (Class C) |
| **169.254.0.0/16** | Link-local (APIPA) |
| **224.0.0.0/4** | Multicast |
| **255.255.255.255** | Limited broadcast |

### DHCP (Dynamic Host Configuration Protocol)

Automatically assigns IP addresses to hosts.

```
Client                           DHCP Server
  │                                   │
  ├──DHCP Discover (broadcast)──────→│
  │                                   │
  │←──DHCP Offer (available IP)───────┤
  │                                   │
  ├──DHCP Request (accept IP)───────→│
  │                                   │
  │←──DHCP ACK (confirm)──────────────┤
  │                                   │
  [Client uses IP address]
```

**DHCP provides:**
- IP address
- Subnet mask
- Default gateway
- DNS server addresses
- Lease time

## IPv4 Datagram

### Datagram Structure

```
 0                   16                  31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|  Total  |
| (4)   |  (4)  |     (8)       | Length  |
|       |       |               |  (16)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    Identification (16)    |Flags| Frag  |
|                           | (3) | Offset|
|                           |     | (13)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to  |   Protocol    |   Header    |
|  Live(8)  |      (8)      | Checksum(16)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Source IP Address (32)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Destination IP Address (32)        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Options (if any)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|             Data (Payload)              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Key Header Fields

**Version (4 bits):** IP version (4 for IPv4)

**IHL (Internet Header Length, 4 bits):** Header length in 32-bit words
- Minimum: 5 (20 bytes)
- Maximum: 15 (60 bytes)

**Type of Service (8 bits):** QoS, priority

**Total Length (16 bits):** Entire packet size (header + data)
- Maximum: 65,535 bytes

**Identification (16 bits):** Uniquely identifies datagram

**Flags (3 bits):**
- Bit 0: Reserved
- Bit 1: Don't Fragment (DF)
- Bit 2: More Fragments (MF)

**Fragment Offset (13 bits):** Position of fragment in original datagram

**Time to Live (TTL, 8 bits):** Maximum hops
- Decremented at each router
- Packet discarded when TTL = 0

**Protocol (8 bits):** Upper layer protocol
- 1 = ICMP
- 6 = TCP
- 17 = UDP

**Header Checksum (16 bits):** Error detection for header only

**Source/Destination IP Address (32 bits each)**

### IP Fragmentation

When datagram too large for link MTU (Maximum Transmission Unit).

**Example:**
```
Original: 4000 byte datagram, MTU = 1500 bytes

Fragment 1:
  Length = 1500, MF = 1, Offset = 0
  Data = bytes 0-1479

Fragment 2:
  Length = 1500, MF = 1, Offset = 185 (1480/8)
  Data = bytes 1480-2959

Fragment 3:
  Length = 1040, MF = 0, Offset = 370 (2960/8)
  Data = bytes 2960-3999
```

**Offset in 8-byte units:** Offset = byte_position / 8

**Reassembly:** Performed at destination only

## IPv6

**128-bit addresses** to solve IPv4 address exhaustion.

### IPv6 Address Format

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334

Compressed:
2001:db8:85a3::8a2e:370:7334
(leading zeros omitted, consecutive zeros replaced with ::)
```

### IPv6 Datagram Header

**Simplified compared to IPv4:**

```
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version| Traffic Class |   Flow Label    |
|  (4)  |      (8)      |      (20)       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Payload Length    |  Next Header(8) |
|         (16)          |   Hop Limit(8)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                         |
|      Source Address (128 bits)          |
|                                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                         |
|    Destination Address (128 bits)       |
|                                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Key Changes from IPv4:**
- No header checksum (faster processing)
- No fragmentation at routers
- Fixed 40-byte header (no options in main header)
- Flow label for QoS

### IPv4 to IPv6 Transition

**Dual Stack:** Nodes run both IPv4 and IPv6

**Tunneling:** IPv6 datagram carried as payload in IPv4 datagram

```
IPv6 → [IPv4 Header][IPv6 Datagram] → IPv6
```

## Routing Fundamentals

### Routing vs Forwarding

**Forwarding:** Move packet from input port to output port (data plane, nanoseconds)

**Routing:** Determine route taken by packets (control plane, seconds)

### Routing Table

Maps destination addresses to next-hop routers.

```
Destination Network    Next Hop       Interface
192.168.1.0/24        192.168.1.1    eth0
10.0.0.0/8            10.1.1.1       eth1
default (0.0.0.0/0)   192.168.1.1    eth0
```

**Longest Prefix Match:** Use most specific route

```
Packet to 192.168.1.50:
  Matches: 192.168.1.0/24, 0.0.0.0/0
  Use: 192.168.1.0/24 (longest prefix)
```

### Routing Metrics

| Metric | Description |
|--------|-------------|
| **Hop Count** | Number of routers to destination |
| **Bandwidth** | Link capacity |
| **Delay** | Propagation + transmission + queueing |
| **Cost** | Administrative weight |
| **Load** | Link utilization |
| **Reliability** | Error rate, availability |

## Routing Algorithms

### Graph Abstraction

```
Network as graph:
Nodes = Routers
Edges = Links
Weights = Cost (delay, bandwidth, etc.)

    1
  A───B
  │ 2 │ 5
  │   │
  3   C
  │   │ 3
  │   │
  D───E
    1
```

### Link-State Routing

**Dijkstra's Algorithm** - Computes least-cost paths from one node to all others.

**Algorithm:**
```
1. Initialize:
   - dist[source] = 0
   - dist[all others] = ∞
   - unvisited = all nodes

2. While unvisited not empty:
   - u = node in unvisited with minimum dist
   - remove u from unvisited
   - for each neighbor v of u:
       alt = dist[u] + cost(u,v)
       if alt < dist[v]:
           dist[v] = alt
           prev[v] = u
```

**Example:**

```
Step-by-step from A:

Initial: A=0, B=∞, C=∞, D=∞, E=∞

Step 1: Visit A
  Update: B=1, D=3

Step 2: Visit B (dist=1)
  Update: C=6

Step 3: Visit D (dist=3)
  Update: E=4

Step 4: Visit E (dist=4)
  Update: C=7 (no change, 6 < 7)

Step 5: Visit C (dist=6)

Result:
  A→B: 1 (direct)
  A→C: 6 (A→B→C)
  A→D: 3 (direct)
  A→E: 4 (A→D→E)
```

**Characteristics:**
- **Complexity:** O(n²) or O(n log n) with priority queue
- **Message Complexity:** O(n × E) messages
- **Convergence:** Fast
- **Oscillation:** Possible with load-based costs

### Distance-Vector Routing

**Bellman-Ford Algorithm** - Distributed, iterative, asynchronous.

**Bellman-Ford Equation:**
```
dx(y) = min{c(x,v) + dv(y)}
        over all neighbors v

where:
  dx(y) = cost of least-cost path from x to y
  c(x,v) = cost from x to neighbor v
  dv(y) = distance from v to y
```

**Algorithm:**
```
Each node:
1. Initialize own distance vector
2. Send distance vector to neighbors
3. Receive distance vectors from neighbors
4. Recompute own distance vector using Bellman-Ford
5. If distance vector changed, notify neighbors
6. Repeat until convergence
```

**Example:**

```
Network:    A---1---B
            |       |
            2       3
            |       |
            C---1---D

Initial:
A: {A:0, B:∞, C:∞, D:∞}
B: {A:∞, B:0, C:∞, D:∞}
C: {A:∞, B:∞, C:0, D:∞}
D: {A:∞, B:∞, C:∞, D:0}

After exchanges and updates:
A: {A:0, B:1, C:2, D:3}
B: {A:1, B:0, C:3, D:3}
C: {A:2, B:3, C:0, D:1}
D: {A:3, B:3, C:1, D:0}
```

**Count-to-Infinity Problem:**

```
Good news travels fast, bad news travels slow.

A---1---B---1---C

If A-B link fails:
- B updates: B→A = ∞
- But C tells B: C→A = 2
- B thinks: B→C→A = 3
- B tells C: B→A = 3
- C thinks: C→B→A = 4
- Continues until reaches ∞
```

**Solutions:**
- **Poisoned Reverse:** If B routes through C, B tells C distance is ∞
- **Split Horizon:** Don't advertise route back to source
- **Limit:** Set ∞ to reasonable value (e.g., 16 for RIP)

### Link-State vs Distance-Vector

| Aspect | Link-State | Distance-Vector |
|--------|------------|-----------------|
| **Algorithm** | Dijkstra | Bellman-Ford |
| **Knowledge** | Complete topology | Only neighbors' distances |
| **Messages** | Flood link states | Exchange distance vectors |
| **Computation** | Each node computes independently | Iterative, distributed |
| **Convergence** | Fast | Slow (count-to-infinity) |
| **Complexity** | O(n²) or O(n log n) | O(n × iterations) |
| **Robustness** | More robust | Less robust |
| **Examples** | OSPF, IS-IS | RIP, BGP |

## Intra-AS Routing

**Autonomous System (AS):** Collection of routers under same administrative control.

**Intra-AS Routing (IGP - Interior Gateway Protocol):** Routing within AS.

### RIP (Routing Information Protocol)

**Distance-vector protocol** based on hop count.

**Characteristics:**
- Metric: Hop count (max 15, 16 = ∞)
- Updates: Every 30 seconds
- Timers: Invalid (180s), Holddown (180s), Flush (240s)
- Uses UDP port 520

**RIP Message:**
```
Command | Version | Zero
Entry 1: Address Family | Route Tag | IP Address | Mask | Next Hop | Metric
Entry 2: ...
...
(up to 25 routes)
```

**Example:**
```
Router A's Table:
Destination    Metric    Next Hop
192.168.1.0/24   1       direct
192.168.2.0/24   2       RouterB
192.168.3.0/24   3       RouterB
```

**Limitations:**
- Slow convergence
- Count-to-infinity problem
- Limited to small networks (max 15 hops)

### OSPF (Open Shortest Path First)

**Link-state protocol** using Dijkstra's algorithm.

**Characteristics:**
- Metric: Cost (can be based on bandwidth, delay)
- Updates: Triggered by topology changes
- Area hierarchy for scalability
- Uses IP protocol 89

**OSPF Areas:**
```
         Area 0 (Backbone)
    ┌──────────┬──────────┐
    │          │          │
  Area 1     Area 2     Area 3
```

**OSPF Message Types:**
1. **Hello:** Discover/maintain neighbors
2. **Database Description:** Summary of link-state database
3. **Link-State Request:** Request specific link-state records
4. **Link-State Update:** Flood link-state advertisements
5. **Link-State Acknowledgment:** Acknowledge LSAs

**OSPF Cost Calculation:**
```
Cost = Reference Bandwidth / Interface Bandwidth

Default Reference = 100 Mbps

Examples:
  10 Gbps link: 100/10000 = 0.01 → 1 (minimum)
  1 Gbps link:  100/1000 = 0.1 → 1
  100 Mbps:     100/100 = 1
  10 Mbps:      100/10 = 10
```

**Advantages over RIP:**
- Fast convergence
- Scalability (hierarchical areas)
- Load balancing (equal-cost multi-path)
- Authentication
- Efficient use of bandwidth

## Inter-AS Routing

**Border Gateway Protocol (BGP)** - Routing between autonomous systems.

### BGP Characteristics

- **Path-vector protocol:** Avoids loops by including full AS path
- **Policy-based routing:** ASes control traffic flow based on agreements
- **Scalability:** Handles entire Internet routing table
- **Uses TCP port 179:** Reliable transport

### BGP Sessions

**eBGP (External BGP):** Between routers in different ASes

**iBGP (Internal BGP):** Between routers within same AS

```
AS 100          AS 200          AS 300
[R1]──eBGP──[R2]──eBGP──[R3]
  │           │           │
 iBGP        iBGP        iBGP
  │           │           │
[R4]        [R5]        [R6]
```

### BGP Messages

1. **OPEN:** Establish BGP session
2. **UPDATE:** Advertise/withdraw routes
3. **KEEPALIVE:** Maintain session
4. **NOTIFICATION:** Error, close session

### BGP Route Advertisement

```
AS Path: Sequence of ASes to reach destination

Example:
AS 100 advertises: 200.23.0.0/16 via [AS100]
AS 200 advertises: 200.23.0.0/16 via [AS200, AS100]
AS 300 advertises: 200.23.0.0/16 via [AS300, AS200, AS100]
```

**Loop Prevention:** If AS sees itself in AS path, rejects route

### BGP Route Selection

When multiple routes to destination, prefer in order:
1. **Local preference:** Administratively set
2. **AS path length:** Shorter is better
3. **Origin type:** IGP > EGP > Incomplete
4. **MED (Multi-Exit Discriminator):** Preferred entry point to AS
5. **eBGP over iBGP**
6. **IGP cost to next hop**
7. **Router ID**

### BGP Policy Example

```
ISP A's Policy:
- Accept routes from customers (make money)
- Accept routes from peers (settlement-free)
- Don't transit traffic between peers/providers
  (only for customers)

Result: Customer routes preferred over peer/provider routes
```

## ICMP

**Internet Control Message Protocol** - Error reporting and diagnostics.

### ICMP Messages

Carried in IP datagrams (Protocol = 1).

```
┌────────────────────────────────────┐
│        IP Header                   │
├────────────────────────────────────┤
│ Type | Code | Checksum             │
├────────────────────────────────────┤
│        Message-specific data       │
└────────────────────────────────────┘
```

### Common ICMP Types

| Type | Code | Description | Use |
|------|------|-------------|-----|
| 0 | 0 | Echo Reply | ping response |
| 3 | 0-15 | Destination Unreachable | Network/host/port unreachable |
| 5 | 0-3 | Redirect | Better route available |
| 8 | 0 | Echo Request | ping |
| 11 | 0 | Time Exceeded (TTL) | traceroute |
| 11 | 1 | Fragment Reassembly Timeout | Fragmentation issue |

### Traceroute

Uses ICMP Time Exceeded messages to discover route.

```
Send UDP packets with increasing TTL:

TTL=1 → Router 1 → ICMP Time Exceeded (identifies Router 1)
TTL=2 → Router 2 → ICMP Time Exceeded (identifies Router 2)
TTL=3 → Router 3 → ICMP Time Exceeded (identifies Router 3)
...
TTL=n → Destination → ICMP Port Unreachable (reached destination)
```

## NAT

**Network Address Translation** - Maps private IPs to public IPs.

### NAT Operation

```
Private Network          NAT Router       Public Internet
(10.0.0.0/8)         (138.76.29.7)

[10.0.0.1]                   │
[10.0.0.2]  ──────→  [NAT]  ──────→  Internet
[10.0.0.3]          Translation

NAT Translation Table:
Private IP:Port     Public IP:Port
10.0.0.1:3345  ←→  138.76.29.7:5001
10.0.0.2:3346  ←→  138.76.29.7:5002
10.0.0.3:3347  ←→  138.76.29.7:5003
```

### NAT Types

**1. Static NAT:** One-to-one mapping
```
10.0.0.1 ←→ 138.76.29.7
```

**2. Dynamic NAT:** Pool of public IPs
```
10.0.0.1 → 138.76.29.7 (from pool)
10.0.0.2 → 138.76.29.8 (from pool)
```

**3. PAT (Port Address Translation / NAPT):** Many-to-one with ports
```
10.0.0.1:3345 → 138.76.29.7:5001
10.0.0.2:3346 → 138.76.29.7:5002
```

### NAT Advantages

- **Address conservation:** Many private IPs share few public IPs
- **Security:** Hides internal network structure
- **Flexibility:** Change internal IPs without affecting external

### NAT Disadvantages

- **Violates end-to-end principle:** Modifies packets
- **Port exhaustion:** Limited to 65,535 ports
- **Breaks some protocols:** FTP, SIP, IPsec
- **Complicates server hosting:** Port forwarding needed

## Summary

The network layer provides host-to-host communication:

**IP Addressing:**
- IPv4: 32-bit, dotted-decimal, CIDR notation
- IPv6: 128-bit, hexadecimal, simplified header
- Subnetting: Divide networks into subnetworks
- DHCP: Dynamic address assignment

**IP Datagram:**
- Header: Version, TTL, protocol, checksum, addresses
- Fragmentation: Split packets for MTU
- Best-effort delivery: No guarantees

**Routing:**
- Forwarding: Data plane, fast (ns)
- Routing: Control plane, slow (s)
- Longest prefix match in routing tables

**Routing Algorithms:**
- Link-State: Dijkstra, complete topology, fast convergence (OSPF)
- Distance-Vector: Bellman-Ford, neighbor info, slow convergence (RIP)

**Inter/Intra-AS:**
- Intra-AS (IGP): RIP, OSPF within AS
- Inter-AS (EGP): BGP between ASes, policy-based

**ICMP:** Error reporting, diagnostics (ping, traceroute)

**NAT:** Map private to public IPs, conserve addresses

## References

**Course Materials:**
- CSEE 4119: An Introduction to Computer Networks - Columbia University

**Textbooks:**
- Kurose, James F., and Keith W. Ross. *Computer Networking: A Top-Down Approach*. 8th Edition, Pearson, 2021.

**RFCs:**
- RFC 791: Internet Protocol (IPv4)
- RFC 2460: Internet Protocol Version 6 (IPv6)
- RFC 2131: DHCP
- RFC 792: ICMP
- RFC 2453: RIP Version 2
- RFC 2328: OSPF Version 2
- RFC 4271: BGP-4
- RFC 3022: Traditional NAT
