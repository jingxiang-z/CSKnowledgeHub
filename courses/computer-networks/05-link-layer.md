# 05 Link Layer

## Table of Contents

1. [Overview](#overview)
2. [Error Detection](#error-detection)
3. [Multiple Access Protocols](#multiple-access-protocols)
4. [MAC Addresses](#mac-addresses)
5. [ARP](#arp)
6. [Ethernet](#ethernet)
7. [Switches](#switches)
8. [Wi-Fi](#wi-fi)
9. [Summary](#summary)
10. [References](#references)

## Overview

The **link layer** (Data Link Layer) transfers frames between adjacent nodes over a link. It provides services to the network layer above and uses services from the physical layer below.

### Link Layer Services

| Service | Description |
|---------|-------------|
| **Framing** | Encapsulate network layer datagram into frame |
| **Link Access** | Coordinate access to shared medium (MAC) |
| **Reliable Delivery** | Detect and correct errors (optional) |
| **Error Detection** | Detect bit errors in frames |
| **Error Correction** | Correct detected errors (FEC) |
| **Flow Control** | Pace sender/receiver |

### Link Layer Implementation

**Where:** Network adapter (NIC - Network Interface Card) or chip

```
┌──────────────────────────────────────────┐
│          Host/Router                     │
│  ┌────────────────────────────────────┐  │
│  │    Application, Transport,         │  │
│  │    Network Layers (software)       │  │
│  └────────────┬───────────────────────┘  │
│               │                          │
│  ┌────────────┴───────────────────────┐  │
│  │  Link Layer (NIC/adapter)          │  │
│  │  • Frame formatting                │  │
│  │  • Error detection                 │  │
│  │  • MAC addressing                  │  │
│  └────────────┬───────────────────────┘  │
└───────────────┼──────────────────────────┘
                │ Physical medium
                ↓
```

### Frame Structure

```
┌──────────┬─────────┬─────────┬────────┬─────────┐
│ Preamble │ Header  │ Payload │ Trailer│   IFG   │
└──────────┴─────────┴─────────┴────────┴─────────┘

Header typically contains:
- Destination MAC address
- Source MAC address
- Type/Length field

Trailer typically contains:
- Frame Check Sequence (FCS) for error detection
```

## Error Detection

Detect errors in transmitted frames.

### Parity Bit

**Single-bit parity:** Add 1 bit to make number of 1s even (or odd).

```
Data: 1011001 (four 1s)
Even parity: 10110010 (add 0 to keep even)

Data: 1011000 (three 1s)
Even parity: 10110001 (add 1 to make even)
```

**Limitation:** Cannot detect even number of bit errors

### Two-Dimensional Parity

Arrange bits in grid, compute parity for each row and column.

```
Data bits (12 bits):
  1 0 1 1 | 0   ← row parity
  0 1 0 1 | 0
  1 1 1 0 | 1
  ─ ─ ─ ─   ─
  0 0 0 0   0   ← column parity

Can detect and correct single-bit errors
Can detect (but not correct) some multi-bit errors
```

### Checksum

Sum of data treated as integers, then complement.

**Example (16-bit checksum):**
```
Data words:
  0x1234
  0x5678
+ 0x9ABC
─────────
  0x22768 → wrap around carry: 0x2768 + 2 = 0x276A

Checksum = ~0x276A = 0xD895

Verification: Sum all words including checksum
  0x1234 + 0x5678 + 0x9ABC + 0xD895 = 0xFFFF
  (all 1s → no error detected)
```

**Used in:** IP, TCP, UDP

**Weakness:** Simple errors can cancel out

### CRC (Cyclic Redundancy Check)

Most powerful error detection, widely used in link layer.

**Key Idea:** Treat bit string as polynomial, divide by generator polynomial.

**Process:**

1. **Sender:**
   - Data bits: D
   - Generator: G (r+1 bits)
   - Compute R = remainder of (D × 2^r) / G
   - Send: D concatenated with R

2. **Receiver:**
   - Receive: D' concatenated with R'
   - Compute: (D' × 2^r + R') / G
   - If remainder = 0 → no error detected
   - If remainder ≠ 0 → error detected

**Example:**

```
Data D = 101110 (6 bits)
Generator G = 1001 (4 bits, r=3)

Step 1: Append r zeros to D
  101110000

Step 2: Divide by G (XOR)
         101011
      ──────────
1001 │ 101110000
       1001
       ─────
        0101
        0000
        ─────
         1011
         1001
         ─────
          0100
          0000
          ─────
           1000
           1001
           ─────
            0010  ← Remainder R

Step 3: Transmit D + R = 101110010
```

**Standard Generators:**
- **CRC-8:** x^8 + x^2 + x + 1
- **CRC-16:** x^16 + x^15 + x^2 + 1
- **CRC-32 (Ethernet):** x^32 + x^26 + x^23 + ... + 1

**Properties:**
- Detects all burst errors ≤ r bits
- Detects all odd number of bit errors (if G has factor x+1)
- High probability of detecting other errors

## Multiple Access Protocols

**Problem:** How to coordinate access to shared broadcast channel?

### Channel Partitioning

**1. TDMA (Time Division Multiple Access)**

Divide time into slots, each node gets fixed slot.

```
Time slots:  1   2   3   4   5   6   1   2   3 ...
           │ A │ B │ C │ D │   │   │ A │ B │ C │

Node A transmits in slots 1, 7, 13, ...
Node B transmits in slots 2, 8, 14, ...
```

**Pros:** No collisions, fair
**Cons:** Unused slots wasted, node must wait for its slot

**2. FDMA (Frequency Division Multiple Access)**

Divide spectrum into frequency bands, each node gets fixed band.

```
Frequency
    ↑
   F4 │████████████████████ Node D
   F3 │████████████████████ Node C
   F2 │████████████████████ Node B
   F1 │████████████████████ Node A
      └────────────────────→ Time
```

**Pros:** No collisions, simultaneous transmission
**Cons:** Unused bandwidth wasted

**3. CDMA (Code Division Multiple Access)**

All nodes transmit simultaneously on same frequency, but with different codes.

- Encode data with unique code
- Receiver decodes with same code
- Other signals appear as noise

Used in: Cellular networks (3G, 4G)

### Random Access

Nodes transmit at full channel rate, collisions possible.

**1. ALOHA**

Simply transmit when you have data.

```
Node A: ────█████──────────█████────
Node B: ──────█████──────────────────
         Collision! ↑
```

**Pure ALOHA:**
- No coordination
- If collision, wait random time and retransmit
- Efficiency: ~18%

**Slotted ALOHA:**
- Time divided into slots
- Nodes transmit only at slot beginning
- Efficiency: ~37%

**2. CSMA (Carrier Sense Multiple Access)**

**Listen before transmit:** If channel idle, transmit; if busy, defer.

```
Node A: ████████──────────────────
Node B: ───↑ Senses channel busy
          waits until idle
```

**Collision still possible:** Due to propagation delay

```
t=0: A starts transmitting
t=1: B senses idle (A's signal hasn't arrived yet)
t=1: B starts transmitting
t=2: Collision!
```

**3. CSMA/CD (with Collision Detection)**

Used in **Ethernet**.

**Detect collision while transmitting, abort immediately.**

```
Algorithm:
1. Sense channel
   - If idle: transmit
   - If busy: wait
2. While transmitting:
   - Monitor channel
   - If collision detected:
     a. Abort transmission
     b. Send jam signal
     c. Wait random backoff time
     d. Retry
```

**Binary Exponential Backoff:**
```
After n collisions:
  Wait random time from {0, 1, 2, ..., 2^n - 1} × slot time
  (n capped at 10)
```

**Efficiency:**
```
E = 1 / (1 + 5d/T)

where:
  d = max propagation delay
  T = time to transmit max-size frame
```

**4. CSMA/CA (with Collision Avoidance)**

Used in **Wi-Fi** (wireless can't detect collisions during transmission).

**Algorithm:**
```
1. Sense channel
   - If idle for DIFS time: transmit
   - If busy: wait

2. Before transmitting:
   - Wait random backoff time
   - Backoff counter decrements while channel idle
   - Freeze counter when channel busy

3. After successful transmission:
   - Receiver sends ACK after SIFS time

4. If no ACK received:
   - Double backoff window
   - Retry
```

**Optional RTS/CTS (for hidden terminal problem):**
```
Sender → RTS (Request to Send) → Receiver
Sender ← CTS (Clear to Send) ← Receiver
Sender → Data → Receiver
Sender ← ACK ← Receiver

All nodes hearing CTS stay silent
```

### Taking Turns

**1. Polling**

Master node invites slave nodes to transmit.

```
Master: "Node 1, send"
Node 1: [transmits]
Master: "Node 2, send"
Node 2: [transmits]
...
```

**Pros:** No collisions, efficient at high load
**Cons:** Polling overhead, single point of failure (master)

**2. Token Passing**

Token circulates among nodes, node can transmit when it has token.

```
Token → Node A → Node B → Node C → Node D → Node A ...
        (sends)  (passes) (sends)  (passes)
```

**Pros:** Decentralized, no collisions
**Cons:** Token overhead, failure can disrupt entire ring

## MAC Addresses

**Media Access Control (MAC) address** is a 48-bit identifier for network interface.

**Format:**
```
6 bytes = 12 hex digits
Example: 1A:2B:3C:4D:5E:6F

1A-2B-3C-4D-5E-6F  (also common)
```

**Structure:**
```
┌─────────────────────┬─────────────────────┐
│   OUI (24 bits)     │   NIC (24 bits)     │
│ Organizationally    │  Device-specific    │
│ Unique Identifier   │                     │
└─────────────────────┴─────────────────────┘

First byte contains:
  Bit 0 (LSB): I/G bit (0=Individual, 1=Group/Multicast)
  Bit 1: U/L bit (0=Universally administered, 1=Locally administered)
```

**Special Addresses:**
- **Broadcast:** FF:FF:FF:FF:FF:FF (all devices)
- **Multicast:** First bit = 1

**MAC vs IP:**

| Aspect | MAC Address | IP Address |
|--------|-------------|------------|
| **Layer** | Link (Layer 2) | Network (Layer 3) |
| **Scope** | Local link | Global (internetwork) |
| **Portability** | Stays with device | Changes with location |
| **Assignment** | Burned into NIC (usually) | Configured (DHCP, manual) |
| **Format** | 48-bit, hex | 32-bit (IPv4), dotted-decimal |

## ARP

**Address Resolution Protocol** maps IP addresses to MAC addresses.

### ARP Operation

```
┌──────────────────────────────────────────────┐
│            Same LAN                          │
│  ┌────────┐              ┌────────┐          │
│  │ Host A │              │ Host B │          │
│  │ IP: .1 │              │ IP: .2 │          │
│  │ MAC: AA│              │ MAC: BB│          │
│  └────────┘              └────────┘          │
└──────────────────────────────────────────────┘

A wants to send to B (.2), but only knows IP, not MAC.

Step 1: A broadcasts ARP Request
  "Who has IP 192.168.1.2? Tell 192.168.1.1 (MAC AA)"
  Destination: FF:FF:FF:FF:FF:FF (broadcast)

Step 2: B receives request, replies
  "192.168.1.2 is at MAC BB"
  Destination: AA (unicast to A)

Step 3: A caches mapping in ARP table
  192.168.1.2 → BB (valid for ~20 minutes)

Step 4: A sends frame to B using MAC BB
```

### ARP Table

Each host maintains ARP cache.

```
IP Address       MAC Address        TTL
192.168.1.1      AA:AA:AA:AA:AA:AA  120 sec
192.168.1.2      BB:BB:BB:BB:BB:BB  95 sec
192.168.1.3      CC:CC:CC:CC:CC:CC  200 sec
```

**Entries time out** to handle changes (device replaced, IP reassigned).

### ARP Across Subnets

If destination on different subnet, ARP for **gateway router**.

```
Host A (192.168.1.10) → Router (192.168.1.1) → Host B (10.0.0.20)

Step 1: A determines B is on different subnet
Step 2: A ARPs for default gateway (192.168.1.1)
Step 3: A sends frame to router's MAC
Step 4: Router forwards to B's subnet
Step 5: Router ARPs for B on its subnet
Step 6: Router sends frame to B's MAC
```

## Ethernet

**Dominant wired LAN technology.**

### Ethernet Standards

| Standard | Speed | Medium | Max Distance |
|----------|-------|--------|--------------|
| **10BASE-T** | 10 Mbps | Cat 3 UTP | 100m |
| **100BASE-TX** | 100 Mbps | Cat 5 UTP | 100m |
| **1000BASE-T** | 1 Gbps | Cat 5e UTP | 100m |
| **10GBASE-T** | 10 Gbps | Cat 6a UTP | 100m |
| **100GBASE-SR4** | 100 Gbps | Multimode fiber | 100m |

### Ethernet Frame Structure

```
 8 bytes  |6 bytes|6 bytes|2 bytes| 46-1500 bytes |4 bytes
┌─────────┬───────┬───────┬───────┬───────────────┬───────┐
│Preamble │  Dest │  Src  │ Type  │    Payload    │  FCS  │
│  + SFD  │  MAC  │  MAC  │       │               │ (CRC) │
└─────────┴───────┴───────┴───────┴───────────────┴───────┘

Minimum frame: 64 bytes (including header + FCS)
Maximum frame: 1518 bytes
MTU (Maximum Transmission Unit): 1500 bytes
```

**Fields:**

1. **Preamble (7 bytes):** 10101010... for synchronization
2. **SFD (1 byte):** Start Frame Delimiter, 10101011
3. **Destination MAC (6 bytes)**
4. **Source MAC (6 bytes)**
5. **Type (2 bytes):** Protocol type (0x0800 = IPv4, 0x86DD = IPv6)
6. **Payload (46-1500 bytes):** Data from network layer
7. **FCS (4 bytes):** Frame Check Sequence (CRC-32)

**Minimum payload:** 46 bytes (padded if necessary)
- Ensures collision detection works correctly
- Minimum frame 64 bytes ensures collision detected before transmission finishes

### Ethernet Evolution

**Half-Duplex (Legacy):**
- CSMA/CD
- Shared medium (hub)
- Collisions possible

**Full-Duplex (Modern):**
- Point-to-point links (switch)
- Simultaneous send/receive
- No collisions, no CSMA/CD needed

```
Half-Duplex (Hub):               Full-Duplex (Switch):
     [Hub]                            [Switch]
    /  |  \                          /   |   \
  [A] [B] [C]                      [A]  [B]  [C]
Shared medium                   Dedicated links
```

## Switches

**Link-layer device:** Operates at Layer 2, forwards frames based on MAC addresses.

### Switch Functions

**1. Forwarding:** Use switch table to selectively forward frames

**2. Learning:** Build switch table by examining source MAC addresses

### Switch Table

```
MAC Address       Interface    TTL
AA:AA:AA:AA:AA:AA    1         60 sec
BB:BB:BB:BB:BB:BB    2         45 sec
CC:CC:CC:CC:CC:CC    3         120 sec
```

### Switch Learning

```
Initially: Switch table empty

Frame arrives on interface 1:
  Src MAC: AA, Dst MAC: BB

Step 1 (Learn): Add "AA on interface 1" to table

Step 2 (Forward):
  - If BB in table: forward to BB's interface
  - If BB not in table: flood to all interfaces except 1

Frame arrives on interface 2:
  Src MAC: BB, Dst MAC: AA

Step 1 (Learn): Add "BB on interface 2" to table

Step 2 (Forward):
  - AA in table (interface 1): forward to interface 1 only
```

### Self-Learning Example

```
Network:
  [A]──1───[Switch]───2──[B]
            │
            3
            │
           [C]

Initial: Table empty

1. A→B frame arrives on interface 1:
   Learn: A on 1
   Forward: Flood to 2, 3 (B unknown)

2. B→A frame arrives on interface 2:
   Learn: B on 2
   Forward: To interface 1 only (A known)

3. C→B frame arrives on interface 3:
   Learn: C on 3
   Forward: To interface 2 only (B known)

Final Table:
  A → 1
  B → 2
  C → 3
```

### Switch vs Router

| Aspect | Switch | Router |
|--------|--------|--------|
| **Layer** | Link (Layer 2) | Network (Layer 3) |
| **Addressing** | MAC addresses | IP addresses |
| **Forwarding** | Learns via flooding | Computes via routing algorithms |
| **Configuration** | Plug-and-play | Requires configuration |
| **Isolation** | Same broadcast domain | Separate broadcast domains |
| **Use** | Within LAN | Between networks |

### VLANs

**Virtual LANs** partition switch into multiple virtual switches.

```
Physical Switch:
┌─────────────────────────────────┐
│ Port 1-8: VLAN 10 (Engineering) │
│ Port 9-16: VLAN 20 (Sales)      │
│ Port 17-24: VLAN 30 (Management)│
└─────────────────────────────────┘

Benefits:
- Logical separation without physical switches
- Security isolation
- Traffic management
- Broadcast domain control
```

## Wi-Fi

**Wireless LAN based on IEEE 802.11 standards.**

### Wi-Fi Standards

| Standard | Year | Frequency | Max Speed | Indoor Range |
|----------|------|-----------|-----------|--------------|
| **802.11b** | 1999 | 2.4 GHz | 11 Mbps | 35m |
| **802.11a** | 1999 | 5 GHz | 54 Mbps | 35m |
| **802.11g** | 2003 | 2.4 GHz | 54 Mbps | 38m |
| **802.11n** (Wi-Fi 4) | 2009 | 2.4/5 GHz | 600 Mbps | 70m |
| **802.11ac** (Wi-Fi 5) | 2013 | 5 GHz | 1.3 Gbps | 35m |
| **802.11ax** (Wi-Fi 6) | 2019 | 2.4/5 GHz | 9.6 Gbps | 30m |

### Wi-Fi Architecture

**Infrastructure Mode:**

```
┌──────────────────────────────────────┐
│   Basic Service Set (BSS)            │
│                                      │
│  [STA]   [STA]   [STA]               │
│    \       |      /                  │
│     \      |     /                   │
│      \     |    /                    │
│        [Access Point (AP)]           │
│              |                       │
└──────────────┼───────────────────────┘
               │
               ↓
         Distribution System
         (Wired Network)
```

**Ad-Hoc Mode:** Devices communicate directly (no AP)

### CSMA/CA in Wi-Fi

**Problem:** Can't detect collisions during transmission (wireless)

**Solution:** Avoid collisions proactively

**CSMA/CA Algorithm:**
```
1. If channel idle for DIFS:
   - Transmit frame
   - Wait for ACK

2. If channel busy:
   - Wait until idle
   - Random backoff
   - Transmit

3. If no ACK:
   - Increase backoff window
   - Retransmit
```

**IFS (Inter-Frame Spacing):**
- **SIFS** (Short IFS): ~10μs, for ACKs, CTS
- **DIFS** (DCF IFS): ~50μs, for data frames

### Hidden Terminal Problem

```
Range of A:  ─────────────
Range of B:        ─────────────
Range of C:               ─────────────

[A]        [B]        [C]

A and C both in range of B, but not each other.
A transmits to B.
C can't sense A's transmission.
C transmits, causing collision at B.
```

**Solution: RTS/CTS**
```
A → RTS → B
A ← CTS ← B (heard by C)
A → Data → B
A ← ACK ← B

C hears CTS, defers transmission
```

### Wi-Fi Frame

```
┌──────┬────┬────┬─────┬─────┬─────┬─────┬────┬─────┐
│Frame │Dur │Addr│Addr │Addr │Seq  │Addr │Data│ FCS │
│Ctrl  │    │ 1  │ 2   │ 3   │Ctrl │ 4   │    │     │
│(2B)  │(2B)│(6B)│(6B) │(6B) │(2B) │(6B) │    │(4B) │
└──────┴────┴────┴─────┴─────┴─────┴─────┴────┴─────┘

Up to 4 MAC addresses (depending on topology):
- Destination
- Source
- Receiver (AP)
- Transmitter (AP)
```

### Wi-Fi Security

**Evolution:**
1. **WEP (Wired Equivalent Privacy):** Broken, insecure
2. **WPA (Wi-Fi Protected Access):** Better, but flawed
3. **WPA2:** Strong (AES encryption)
4. **WPA3:** Strongest (2018, mandatory since 2020)

**WPA2 Authentication:**
- **Pre-Shared Key (PSK):** Password-based
- **Enterprise (802.1X):** RADIUS server authentication

## Summary

The link layer handles communication between adjacent nodes on a link:

**Error Detection:**
- Parity: Simple, limited
- Checksum: Medium strength
- CRC: Strong, widely used in link layer

**Multiple Access:**
- Channel partitioning: TDMA, FDMA (no collisions but waste capacity)
- Random access: ALOHA, CSMA, CSMA/CD, CSMA/CA (efficient but collisions)
- Taking turns: Polling, token passing (efficient, complex)

**MAC Addresses:**
- 48-bit physical address
- Identifies network interface
- ARP maps IP to MAC

**Ethernet:**
- Dominant wired LAN
- Frame: Preamble, addresses, type, payload, FCS
- Modern: Full-duplex, switched, no collisions

**Switches:**
- Layer 2 forwarding
- Self-learning via flooding
- Plug-and-play operation

**Wi-Fi (802.11):**
- Wireless LAN
- CSMA/CA (collision avoidance)
- Hidden terminal problem → RTS/CTS
- Security: WPA2/WPA3

## References

**Course Materials:**
- CSEE 4119: An Introduction to Computer Networks - Columbia University

**Textbooks:**
- Kurose, James F., and Keith W. Ross. *Computer Networking: A Top-Down Approach*. 8th Edition, Pearson, 2021.

**Standards:**
- IEEE 802.3: Ethernet
- IEEE 802.11: Wi-Fi
- IEEE 802.1Q: VLANs
