# 03 Transport Layer

## Table of Contents

1. [Overview](#overview)
2. [Multiplexing and Demultiplexing](#multiplexing-and-demultiplexing)
3. [UDP](#udp)
4. [Reliable Data Transfer Principles](#reliable-data-transfer-principles)
5. [TCP](#tcp)
6. [Summary](#summary)
7. [References](#references)

## Overview

The **transport layer** provides end-to-end communication services between applications running on different hosts. It serves as the bridge between the application layer and the network layer.

### Key Responsibilities

| Function | Description |
|----------|-------------|
| **Logical Communication** | Provides communication between processes (not just hosts) |
| **Multiplexing/Demultiplexing** | Multiple applications share network |
| **Segmentation** | Break application messages into segments |
| **Reassembly** | Reconstruct segments into messages |
| **Error Detection** | Detect transmission errors |
| **Reliability** | Ensure accurate delivery (TCP) |
| **Flow Control** | Prevent sender from overwhelming receiver |
| **Congestion Control** | Prevent network congestion |

### Transport vs Network Layer

| Aspect | Network Layer | Transport Layer |
|--------|---------------|-----------------|
| **Scope** | Host-to-host | Process-to-process |
| **Services** | Best-effort delivery | Reliability, flow/congestion control |
| **Addressing** | IP addresses | Port numbers |
| **Protocols** | IP, ICMP, routing | TCP, UDP |

### Transport Layer Protocols

**TCP (Transmission Control Protocol):**
- Connection-oriented
- Reliable, ordered delivery
- Flow control, congestion control
- Higher overhead
- Use cases: Web, email, file transfer

**UDP (User Datagram Protocol):**
- Connectionless
- Unreliable, unordered delivery
- No flow/congestion control
- Minimal overhead
- Use cases: DNS, streaming, gaming

## Multiplexing and Demultiplexing

**Multiplexing** at sender: Gather data from multiple sockets, add transport header, pass to network layer

**Demultiplexing** at receiver: Use header info to deliver segments to correct socket

```
Application Layer:
  [App 1]  [App 2]  [App 3]
     ↓        ↓        ↓
Transport Layer (Multiplexing):
  [Port 80][Port 443][Port 8080]
           ↓
     [TCP/UDP Segment]
           ↓
Network Layer:
      [IP Packet]
```

### Port Numbers

- **16-bit unsigned integer:** 0-65535
- **Well-Known Ports:** 0-1023 (HTTP=80, HTTPS=443, SMTP=25, DNS=53)
- **Registered Ports:** 1024-49151 (Application-specific)
- **Dynamic/Private Ports:** 49152-65535 (Temporary, ephemeral)

### Socket Identification

**UDP Socket:** Identified by 2-tuple (destination IP, destination port)

```
Host A (10.0.0.1)                Host B (10.0.0.2)
  App on port 5000                 App on port 9000
      ↓                                 ↑
  UDP segment                       UDP segment
  Src: 10.0.0.1:5000                Dst: 10.0.0.2:9000
  Dst: 10.0.0.2:9000   ─────────→   Src: 10.0.0.1:5000
```

**TCP Socket:** Identified by 4-tuple (source IP, source port, destination IP, destination port)

Allows multiple connections from same client IP to same server.

## UDP

**User Datagram Protocol** provides minimal, connectionless transport service.

### UDP Characteristics

| Feature | Description |
|---------|-------------|
| **Connectionless** | No handshake, no connection state |
| **Unreliable** | No delivery guarantees, no retransmission |
| **Unordered** | Segments may arrive out of order |
| **Lightweight** | Minimal header overhead (8 bytes) |
| **Fast** | No connection setup delay |
| **Multicast/Broadcast** | Supports one-to-many communication |

### UDP Segment Structure

```
 0                   16                  31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Source Port     | Destination Port  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Length        |     Checksum      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                         |
|             Data (Payload)              |
|                                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Header Fields:**

1. **Source Port (16 bits):** Sending application port
2. **Destination Port (16 bits):** Receiving application port
3. **Length (16 bits):** Length of UDP segment (header + data) in bytes
   - Minimum: 8 bytes (header only)
   - Maximum: 65,535 bytes
4. **Checksum (16 bits):** Error detection (optional but recommended)

### UDP Checksum

Detects errors in transmitted segment (bit flips).

**Calculation:**
1. Treat segment contents as sequence of 16-bit integers
2. Compute sum (with wraparound carry)
3. Compute 1's complement of sum
4. Result is checksum

**Verification:**
1. Add all 16-bit words including checksum
2. If result is all 1's → no errors detected
3. If result has 0's → error detected

**Limitation:** May not detect all errors (e.g., two bit flips that cancel out)

### Why Use UDP?

**Advantages:**
- **No connection establishment:** Reduced latency (no RTT delay)
- **No connection state:** Server can support more clients
- **Small header:** 8 bytes vs TCP's 20+ bytes
- **Fine-grained control:** Application controls when data is sent

**Use Cases:**

| Application | Reason |
|-------------|--------|
| **DNS** | Simple request-response, retries handled by application |
| **SNMP** | Network management queries |
| **RTP (streaming)** | Loss tolerant, rate sensitive |
| **Online gaming** | Low latency critical, some loss acceptable |
| **VoIP** | Real-time, loss tolerant |

## Reliable Data Transfer Principles

Building reliable communication over unreliable channel.

### RDT 1.0: Reliable Transfer over Reliable Channel

**Assumptions:**
- Underlying channel is perfectly reliable
- No bit errors, no packet loss

```
Sender:                Receiver:
  rdt_send(data)         rdt_rcv(packet)
      ↓                      ↓
  make_pkt(data)        extract(packet, data)
      ↓                      ↓
  udt_send(packet)      deliver_data(data)
```

**Analysis:** Trivial case, no error handling needed.

### RDT 2.0: Channel with Bit Errors

**Assumptions:**
- Bits in packet may be corrupted
- No packet loss

**Mechanisms:**
- **Error detection:** Checksum
- **Feedback:** Acknowledgments (ACKs/NAKs)
  - ACK: Receiver tells sender packet OK
  - NAK: Receiver tells sender packet had errors
- **Retransmission:** Sender retransmits on receiving NAK

```
Sender:                                Receiver:
  send pkt ─────────────────────────→   receive pkt
      ↓                                     ↓
  wait for ACK/NAK                     check checksum
      ↑                                     ↓
  ←─ ACK (if OK) or NAK (if error) ────────┘
      ↓
  if NAK: retransmit
  if ACK: send next packet
```

**Problem:** What if ACK/NAK corrupted?

### RDT 2.1: Handling Corrupted ACKs

**Solution:** Add **sequence numbers** to packets

- Sender adds sequence number to each packet
- Receiver discards duplicate packets
- For Stop-and-Wait: 1-bit sequence number suffices (0, 1, 0, 1, ...)

```
Sender State 0:                 Receiver State 0:
  send pkt 0                      expect seq 0
  wait for ACK                    if pkt 0 OK:
  if NAK or corrupt ACK:            send ACK
    resend pkt 0                    goto State 1
  if ACK:                          if pkt 0 error or pkt 1:
    goto State 1                     send NAK
                                     stay in State 0
```

### RDT 2.2: NAK-Free Protocol

**Improvement:** Replace NAKs with duplicate ACKs

- Receiver sends ACK for last correctly received packet
- Duplicate ACK indicates problem with next packet

```
Receiver:
  if pkt n OK and in-order:
    send ACK(n)
    deliver data
  if pkt n corrupted or out-of-order:
    send ACK(n-1)  [duplicate ACK]
```

### RDT 3.0: Channels with Errors and Loss

**New assumption:** Packets can be lost (dropped) in channel

**New mechanism:** **Timeout** - Sender waits reasonable amount of time for ACK

```
Sender:
  send pkt
  start timer
  if timeout:
    retransmit pkt
    restart timer
  if ACK received:
    stop timer
    send next packet
```

**Performance (Stop-and-Wait):**

```
Utilization = (L/R) / (RTT + L/R)

where:
  L = packet size (bits)
  R = transmission rate (bps)
  RTT = round-trip time

Example:
  L = 1 KB = 8,000 bits
  R = 1 Gbps
  RTT = 30 ms

  Utilization = (8,000 / 10^9) / (0.03 + 8,000/10^9)
               = 0.000008 / 0.030008
               = 0.027% (very inefficient!)
```

### Pipelined Protocols

**Solution:** Allow multiple unacknowledged packets in transit

```
Stop-and-Wait:
Time ─→
Send pkt 0 ───→ [wait RTT] ← ACK 0
Send pkt 1 ───→ [wait RTT] ← ACK 1
Send pkt 2 ───→ [wait RTT] ← ACK 2

Pipelined:
Time ─→
Send pkt 0 ───→
Send pkt 1 ───→                 ← ACK 0
Send pkt 2 ───→                 ← ACK 1
Send pkt 3 ───→                 ← ACK 2
```

**Benefits:**
- Increased utilization
- Higher throughput
- Better network resource utilization

**Requirements:**
- Range of sequence numbers must increase
- Sender and/or receiver must buffer packets

**Two approaches:** Go-Back-N, Selective Repeat

### Go-Back-N (GBN)

**Sender:**
- Window of up to N unacknowledged packets
- **Cumulative ACK:** ACK(n) acknowledges all packets up to sequence number n
- Timer for oldest unacknowledged packet
- On timeout: retransmit all unacknowledged packets

```
Sender Window (N=4):
[0][1][2][3]|4  5  6  7  8  9 ...
 └─────┬────┘
   Sent, unacked

After ACK(1):
    [2][3][4][5]|6  7  8  9 ...
     └─────┬────┘
       Sent, unacked
```

**Receiver:**
- Only sends cumulative ACK
- Discards out-of-order packets
- Simple: no buffering needed

**Example (packet loss):**
```
Sender transmits: 0, 1, 2, 3
Packet 1 lost
Receiver receives: 0, -, 2, 3
Receiver ACKs: ACK(0), [no ACK], discard 2, discard 3
Timeout on packet 1
Sender retransmits: 1, 2, 3 (Go-Back-N!)
```

**Performance:**
- Simple receiver
- Inefficient: may retransmit many correct packets

### Selective Repeat (SR)

**Sender:**
- Window of up to N unacknowledged packets
- **Individual ACK:** Each packet individually acknowledged
- Timer for each packet
- On timeout: retransmit only that packet

**Receiver:**
- Individually acknowledges all correctly received packets
- Buffers out-of-order packets
- Delivers in-order data to application

```
Sender Window (N=4):
[0][1][2][3]|4  5  6  7  8  9 ...

Receiver Window (N=4):
[0][1][2][3]|4  5  6  7  8  9 ...

Packet 1 lost:
Sender receives: ACK(0), -, ACK(2), ACK(3)
Receiver buffers: [0][–][2][3]
Timeout on packet 1
Sender retransmits: 1 only
Receiver: [0][1][2][3] → deliver all to application
```

**Performance:**
- More efficient: only retransmit lost packets
- More complex: receiver must buffer, reorder

### GBN vs Selective Repeat

| Aspect | Go-Back-N | Selective Repeat |
|--------|-----------|------------------|
| **ACK Type** | Cumulative | Individual |
| **Retransmit** | All from lost packet | Only lost packet |
| **Receiver Buffer** | No | Yes (out-of-order) |
| **Complexity** | Simple | More complex |
| **Efficiency** | Lower (many retransmits) | Higher (minimal retransmits) |
| **TCP Uses** | Modified GBN | - |

## TCP

**Transmission Control Protocol** provides reliable, ordered, connection-oriented transport.

### TCP Characteristics

| Feature | Description |
|---------|-------------|
| **Connection-Oriented** | 3-way handshake before data transfer |
| **Reliable** | Guarantees delivery, detects errors, retransmits |
| **Ordered** | Data delivered in sequence |
| **Full-Duplex** | Bidirectional data flow |
| **Flow Control** | Prevents overwhelming receiver |
| **Congestion Control** | Prevents overwhelming network |
| **Point-to-Point** | One sender, one receiver |

### TCP Segment Structure

```
 0                   16                  31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Source Port     | Destination Port  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Sequence Number               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        Acknowledgment Number            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Data |     |U|A|P|R|S|F|                 |
|Offset Res|R|C|S|S|Y|I|   Window Size    |
|     |     |G|K|H|T|N|N|                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Checksum        |  Urgent Pointer   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Options (if any)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                         |
|             Data (Payload)              |
|                                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Key Fields:**

1. **Sequence Number (32 bits):** Byte number of first data byte in segment
2. **Acknowledgment Number (32 bits):** Next byte expected from other side
3. **Data Offset (4 bits):** Header length in 32-bit words
4. **Flags (6 bits):**
   - URG: Urgent data
   - ACK: Acknowledgment valid
   - PSH: Push data immediately
   - RST: Reset connection
   - SYN: Synchronize sequence numbers
   - FIN: Finish, no more data
5. **Window Size (16 bits):** Flow control, receiver's buffer space
6. **Checksum (16 bits):** Error detection
7. **Options:** MSS, timestamps, window scaling, etc.

### TCP Connection Management

**Three-Way Handshake (Connection Establishment):**

```
Client                              Server
  │                                   │
  ├─── SYN (seq=x) ─────────────────→│
  │                                   │ (Server allocates
  │                                   │  resources)
  │←── SYN-ACK (seq=y, ack=x+1) ─────┤
  │                                   │
  │ (Client allocates                 │
  │  resources)                       │
  │                                   │
  ├─── ACK (ack=y+1) ───────────────→│
  │                                   │
  │   [Connection ESTABLISHED]        │
  │                                   │
  ├══ Data transfer ═════════════════┤
```

**Step 1:** Client sends SYN
- SYN flag set
- Initial sequence number (ISN) chosen

**Step 2:** Server responds with SYN-ACK
- SYN and ACK flags set
- Server's ISN chosen
- Acknowledges client's SYN

**Step 3:** Client sends ACK
- ACK flag set
- May contain data

**Four-Way Handshake (Connection Termination):**

```
Client                              Server
  │                                   │
  ├─── FIN (seq=x) ─────────────────→│
  │                                   │
  │←─── ACK (ack=x+1) ────────────────┤
  │                                   │
  │    [Half-close: Client→Server]   │
  │    [Server can still send data]  │
  │                                   │
  │←─── FIN (seq=y) ──────────────────┤
  │                                   │
  ├─── ACK (ack=y+1) ───────────────→│
  │                                   │
  │  [Connection CLOSED]              │
```

### TCP Reliability

**Mechanisms:**

1. **Checksums:** Detect bit errors
2. **Sequence Numbers:** Detect lost/duplicate/reordered segments
3. **Acknowledgments:** Confirm receipt
4. **Timeouts:** Detect lost segments, trigger retransmission
5. **Retransmission:** Resend lost segments

**Timeout Calculation:**

TCP uses **adaptive timeout** based on RTT measurements.

```
EstimatedRTT = (1-α) × EstimatedRTT + α × SampleRTT
              (typically α = 0.125)

DevRTT = (1-β) × DevRTT + β × |SampleRTT - EstimatedRTT|
         (typically β = 0.25)

TimeoutInterval = EstimatedRTT + 4 × DevRTT
```

**Fast Retransmit:**

If sender receives 3 duplicate ACKs for same data, resend segment before timeout.

```
Send seg 1 ───→
Send seg 2 ───→ (lost)
Send seg 3 ───→
             ←─── ACK 1 (expecting seg 2)
Send seg 4 ───→
             ←─── ACK 1 (dup 1)
Send seg 5 ───→
             ←─── ACK 1 (dup 2)
Send seg 6 ───→
             ←─── ACK 1 (dup 3)
[Fast retransmit seg 2]
Retransmit 2 →
             ←─── ACK 6 (all received!)
```

### TCP Flow Control

**Purpose:** Prevent sender from overwhelming receiver's buffer

**Mechanism:** Receiver advertises **receive window (rwnd)** in TCP header

```
Sender's Send Window = min(cwnd, rwnd)

where:
  cwnd = congestion window (congestion control)
  rwnd = receive window (flow control)
```

**Receiver Buffer:**

```
┌─────────────────────────────────────────┐
│  Application reads  │ Buffered │  Free  │
│     from buffer     │   Data   │ Space  │
└─────────────────────────────────────────┘
                      ←─ rwnd ──→
```

**Receiver calculates:**
```
rwnd = RcvBuffer - (LastByteRcvd - LastByteRead)
```

**Sender ensures:**
```
LastByteSent - LastByteAcked ≤ rwnd
```

### TCP Congestion Control

**Purpose:** Prevent sender from overwhelming the network

**Key Idea:** Probe for available bandwidth, adapt sending rate

**Congestion Window (cwnd):** Number of unacknowledged bytes sender can have in-flight

```
Effective Window = min(cwnd, rwnd)

Sending Rate ≈ cwnd / RTT
```

**TCP Congestion Control Algorithm:**

**1. Slow Start:**
- Begin with cwnd = 1 MSS
- Double cwnd every RTT (exponential growth)
- Continue until:
  - Loss detected, OR
  - cwnd reaches ssthresh (slow start threshold)

```
RTT 0: cwnd = 1 MSS
RTT 1: cwnd = 2 MSS
RTT 2: cwnd = 4 MSS
RTT 3: cwnd = 8 MSS
...
```

**2. Congestion Avoidance:**
- Increase cwnd by 1 MSS per RTT (linear growth)
- Continue until loss detected

```
cwnd = cwnd + MSS × (MSS / cwnd)
```

**3. Fast Recovery:**
- After fast retransmit (3 dup ACKs):
  - ssthresh = cwnd / 2
  - cwnd = ssthresh + 3 MSS
  - Increase cwnd by 1 MSS for each additional dup ACK
  - When new ACK arrives: cwnd = ssthresh (enter congestion avoidance)

**Loss Detection:**

- **Timeout:** Severe congestion
  - ssthresh = cwnd / 2
  - cwnd = 1 MSS
  - Enter slow start

- **3 Duplicate ACKs:** Mild congestion
  - ssthresh = cwnd / 2
  - cwnd = ssthresh + 3 MSS
  - Enter fast recovery

**TCP Congestion Control State Machine:**

```
                  ┌──────────────┐
                  │ Slow Start   │
                  │ (exp growth) │
                  └──────┬───────┘
                         │ cwnd ≥ ssthresh
                         ↓
                  ┌──────────────┐
          New ACK │  Congestion  │
        ┌─────────┤   Avoidance  │
        │         │ (lin growth) │
        │         └──────┬───────┘
        │                │
        │                │ 3 dup ACKs
        │                ↓
        │         ┌──────────────┐
        └─────────┤     Fast     │
                  │   Recovery   │
                  └──────────────┘
                         ↑
                         │ Timeout
                         │
                    (Reset to
                     Slow Start)
```

**TCP Variants:**

| Variant | Loss Signal | Characteristics |
|---------|-------------|-----------------|
| **TCP Tahoe** | Timeout or dup ACKs → slow start | Original, conservative |
| **TCP Reno** | Timeout → slow start<br>3 dup ACKs → fast recovery | Most common |
| **TCP NewReno** | Improved fast recovery | Better multiple loss handling |
| **TCP CUBIC** | Time-based growth | Better for high-speed networks |
| **TCP BBR** | Bottleneck bandwidth | Google's algorithm, probes bandwidth & RTT |

## Summary

The transport layer provides end-to-end communication between processes:

**Multiplexing/Demultiplexing:**
- Use port numbers to identify processes
- UDP: 2-tuple socket
- TCP: 4-tuple socket

**UDP:**
- Connectionless, unreliable, minimal overhead
- 8-byte header
- Use when speed > reliability

**Reliable Data Transfer:**
- RDT 1.0: Perfect channel
- RDT 2.x: Bit errors → checksums, ACKs/NAKs
- RDT 3.0: Loss → timeouts, retransmission
- Pipelining: GBN (cumulative ACK), SR (individual ACK)

**TCP:**
- Connection-oriented (3-way handshake, 4-way termination)
- Reliable (checksums, sequence numbers, ACKs, retransmission)
- Flow control (receive window, rwnd)
- Congestion control (cwnd, slow start, congestion avoidance, fast recovery)
- Adaptive timeout, fast retransmit

## References

**Course Materials:**
- CSEE 4119: An Introduction to Computer Networks - Columbia University

**Textbooks:**
- Kurose, James F., and Keith W. Ross. *Computer Networking: A Top-Down Approach*. 8th Edition, Pearson, 2021.

**RFCs:**
- RFC 768: User Datagram Protocol
- RFC 793: Transmission Control Protocol
- RFC 2001: TCP Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery
- RFC 5681: TCP Congestion Control
