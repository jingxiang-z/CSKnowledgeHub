# 04 Storage and I/O Systems

## Table of Contents
1. [Introduction](#introduction)
2. [Storage Technologies](#storage-technologies)
3. [I/O Systems and Buses](#io-systems-and-buses)
4. [RAID Systems](#raid-systems)
5. [System Dependability](#system-dependability)
6. [References](#references)

## Introduction

Storage and I/O systems form the foundation for persistent data management and external communication in computer systems. While processors and memory focus on computation speed, storage systems prioritize capacity, cost-per-bit, and reliability. The performance gap between compute/memory and storage is vast—orders of magnitude—making efficient storage architecture critical.

### Storage Hierarchy Context

Storage devices occupy the bottom tiers of the memory hierarchy:

| Level | Technology | Capacity | Access Time | Cost/GB | Volatile |
|-------|-----------|----------|-------------|---------|----------|
| **DRAM** | Main Memory | 8-128 GB | ~100 ns | $3-5 | Yes |
| **SSD** | Flash NAND | 256 GB-4 TB | ~100 μs | $0.10-0.20 | No |
| **HDD** | Magnetic Disk | 1-20 TB | ~5-10 ms | $0.01-0.03 | No |
| **Tape** | Magnetic Tape | 10-100 TB | ~60 s | $0.001-0.005 | No |

**Key Distinction**: Non-volatile storage persists data after power loss, making it essential for long-term data retention despite being 100,000× slower than DRAM.

## Storage Technologies

### Hard Disk Drives (HDD)

Magnetic disk storage has been the dominant secondary storage technology for decades.

#### Physical Structure

**Components**:
- **Platters**: Rotating magnetic disks (typically 2-5 platters per drive)
- **Spindle**: Motor rotating platters at constant speed (5,400-15,000 RPM)
- **Read/Write Heads**: Electromagnetic heads that float nanometers above platter surface
- **Actuator Arm**: Moves heads radially across platters
- **Controller**: Electronics managing I/O, caching, and error correction

**Data Organization**:
```
Platter Surface:
┌─────────────────────────────────────┐
│        Track (concentric ring)      │
│  ┌─────────────────────────────┐    │
│  │    Sector (512B-4KB)        │    │
│  │  ┌─────────────┐             │    │
│  │  │   Data      │             │    │
│  │  └─────────────┘             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Cylinder: same track on all platters│
└─────────────────────────────────────┘
```

- **Sector**: Smallest addressable unit (historically 512 bytes, now 4 KB)
- **Track**: Concentric ring of sectors on a platter surface
- **Cylinder**: All tracks at the same radial position across all platters

#### Access Time Components

Total access time = Seek Time + Rotational Latency + Transfer Time

**Seek Time**: Time to move heads to target track
- **Average**: 4-10 ms (desktop), 3-5 ms (enterprise)
- **Full stroke**: 8-15 ms
- Dominates access time for random I/O

**Rotational Latency**: Time for target sector to rotate under head
- **Average**: 1/2 rotation
- 7,200 RPM: 60s/7200 rev = 8.33 ms/rev → 4.2 ms average
- 15,000 RPM: 2 ms average

**Transfer Time**: Time to read/write data
- Modern HDDs: 100-250 MB/s sequential
- For 4 KB sector: ~20 μs (negligible compared to seek)

**Random vs. Sequential**:
- **Random 4KB reads**: ~100-200 IOPS (I/O operations per second)
- **Sequential reads**: 100-250 MB/s (~25,000+ IOPS for 4KB blocks)
- **Ratio**: Sequential is 100-250× faster

#### HDD Characteristics

**Advantages**:
- High capacity (up to 20 TB single drive)
- Very low cost per GB ($0.01-0.03/GB)
- Mature, reliable technology
- Good sequential performance

**Disadvantages**:
- High latency (milliseconds)
- Poor random I/O performance
- Mechanical parts subject to wear and failure
- Sensitive to shock and vibration
- High power consumption

**Use Cases**: Bulk storage, archival, sequential workloads, cost-sensitive applications

### Solid-State Drives (SSD)

Flash-based storage using NAND memory cells has revolutionized storage performance.

#### Technology

**NAND Flash Types**:
- **SLC (Single-Level Cell)**: 1 bit/cell, fastest, most durable, expensive
- **MLC (Multi-Level Cell)**: 2 bits/cell, balanced performance and cost
- **TLC (Triple-Level Cell)**: 3 bits/cell, cheaper, slower, less durable
- **QLC (Quad-Level Cell)**: 4 bits/cell, highest density, lowest endurance

**Internal Architecture**:
```
SSD Controller
├── Host Interface (NVMe/SATA)
├── Flash Translation Layer (FTL)
│   └── Logical-to-Physical mapping
├── Wear Leveling
├── Garbage Collection
└── Multiple NAND Flash Channels
    ├── Channel 0: [Die 0][Die 1]...[Die N]
    ├── Channel 1: [Die 0][Die 1]...[Die N]
    └── ...
```

**Key Operations**:
- **Read**: Fast (~25-100 μs per page)
- **Program (Write)**: Slower (~200-1000 μs per page)
- **Erase**: Slowest (~1-3 ms per block), required before reprogramming
- **Granularity**: Read/write by page (4-16 KB), erase by block (256 KB-4 MB)

#### Flash Translation Layer (FTL)

Maps logical block addresses to physical flash locations:
- **Wear Leveling**: Distributes writes evenly to prevent premature wear
- **Garbage Collection**: Reclaims blocks with invalid data
- **Write Amplification**: Internal writes exceed host writes (affects endurance)

#### SSD Characteristics

**Advantages**:
- Low latency (50-100 μs, 50-100× faster than HDD)
- High random I/O (50,000-500,000 IOPS)
- High bandwidth (500 MB/s SATA, 3-7 GB/s NVMe)
- No moving parts (shock resistant)
- Low power consumption
- Consistent performance (no seek/rotation)

**Disadvantages**:
- Higher cost per GB ($0.10-0.20/GB)
- Limited write endurance (P/E cycles)
- Write amplification reduces performance and lifespan
- Capacity generally lower than HDDs (though improving)

**Use Cases**: OS and applications, databases, latency-sensitive workloads, mobile devices

### NVMe (Non-Volatile Memory Express)

Modern storage protocol designed specifically for SSDs, replacing legacy SATA.

**Benefits over SATA**:
- Direct PCIe connection (bypasses slower SATA controller)
- Parallel queues (65,536 queues × 65,536 commands each)
- Lower latency (no SATA translation overhead)
- Higher bandwidth (PCIe 4.0 x4: up to 8 GB/s)

## I/O Systems and Buses

I/O systems manage communication between the CPU and external devices.

### I/O Device Categories

**Block Devices**: Transfer data in blocks (e.g., HDDs, SSDs)
- Random access
- Buffering and caching applicable

**Character Devices**: Transfer data as streams of bytes (e.g., keyboards, serial ports)
- Sequential access
- No seeking

**Network Devices**: Transfer data packets (e.g., NICs)
- Asynchronous, packetized

### I/O Communication Methods

#### Programmed I/O (Polling)

CPU repeatedly checks device status:
```c
while (device_busy)
    ;  // Busy wait
read_data_from_device();
```

**Pros**: Simple
**Cons**: Wastes CPU cycles

#### Interrupt-Driven I/O

Device signals CPU via interrupt when ready:
```
1. CPU initiates I/O
2. CPU continues other work
3. Device completes → generates interrupt
4. CPU handles interrupt, processes data
```

**Pros**: CPU free during I/O
**Cons**: Interrupt overhead, still requires CPU for data transfer

#### Direct Memory Access (DMA)

Dedicated hardware transfers data directly between device and memory:
```
1. CPU programs DMA controller (source, dest, count)
2. DMA controller transfers data (no CPU involvement)
3. DMA signals CPU via interrupt when complete
```

**Pros**: Minimal CPU involvement, high throughput
**Cons**: More complex hardware

### Bus Architectures

**System Bus Hierarchy**:
```
┌────────┐
│  CPU   │
└───┬────┘
    │ (Front-Side Bus / System Bus)
┌───┴────────┬──────────┐
│  Memory    │  PCIe    │
│  Controller│  Root    │
│            │  Complex │
└────────────┴─────┬────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
   GPU (x16)    SSD (x4)    NIC (x4)
```

**PCIe (Peripheral Component Interconnect Express)**:
- Point-to-point serial links (lanes)
- Configurations: x1, x4, x8, x16 lanes
- Generations:
  - PCIe 3.0: ~1 GB/s per lane
  - PCIe 4.0: ~2 GB/s per lane
  - PCIe 5.0: ~4 GB/s per lane

**USB (Universal Serial Bus)**:
- Serial bus for peripherals
- USB 3.2 Gen 2: 10 Gb/s (1.25 GB/s)
- USB4: 40 Gb/s (5 GB/s)

## RAID Systems

**RAID (Redundant Array of Independent Disks)** combines multiple physical disks into a logical unit to improve performance, reliability, or both.

### RAID Levels

#### RAID 0: Striping

**Mechanism**: Data is striped (divided) across N disks without redundancy.

```
Disk 0: [A1][A3][A5][A7]
Disk 1: [A2][A4][A6][A8]
Disk 2: [A3][A5][A7][A9]

File A split across all disks
```

**Performance**:
- **Read Throughput**: N × single disk
- **Write Throughput**: N × single disk
- **Parallelism**: Multiple disks accessed simultaneously

**Fault Tolerance**: **None**
- Failure of any single disk results in total data loss
- **Reliability**: 1/N of single disk (worse than single disk!)

**Capacity Overhead**: 0% (full capacity available)

**Use Case**: High-performance temporary storage where data loss is acceptable (e.g., video editing scratch disk)

#### RAID 1: Mirroring

**Mechanism**: Data is duplicated on N disks (typically N=2).

```
Disk 0: [A1][A2][A3][A4]
Disk 1: [A1][A2][A3][A4]  ← Identical copy

Each block written to both disks
```

**Performance**:
- **Read Throughput**: N × single disk (can read from any mirror)
- **Write Throughput**: 1 × single disk (must write to all mirrors)
- **Latency**: Same as single disk

**Fault Tolerance**: **High**
- Tolerates failure of N-1 disks
- Data can be reconstructed from any surviving disk

**Capacity Overhead**: 50% (for 2-way mirroring)

**Use Case**: High-reliability applications (databases, critical systems) where availability is paramount

#### RAID 4: Block-Interleaved Parity

**Mechanism**: Data striped across N-1 disks, with a dedicated parity disk.

```
Disk 0: [A1][A4][A7][A10]  ← Data
Disk 1: [A2][A5][A8][A11]  ← Data
Disk 2: [A3][A6][A9][A12]  ← Data
Disk 3: [P1][P2][P3][P4]   ← Parity (XOR of corresponding blocks)

P1 = A1 ⊕ A2 ⊕ A3
```

**Parity Calculation**: XOR of data blocks
- If any one disk fails, data can be reconstructed using parity
- Example: If Disk 1 fails, A2 = P1 ⊕ A1 ⊕ A3

**Performance**:
- **Read Throughput**: (N-1) × single disk (parity disk not read)
- **Write Throughput**: **Poor** (parity disk bottleneck)
  - Every write requires: read old data + read old parity + write new data + write new parity
  - Parity disk becomes a bottleneck (all writes touch it)

**Fault Tolerance**: Tolerates failure of any one disk

**Capacity Overhead**: 1/N (one disk worth of parity)

**Drawback**: Parity disk bottleneck makes this impractical

#### RAID 5: Distributed Block-Interleaved Parity

**Mechanism**: Same as RAID 4, but parity blocks are distributed across all disks.

```
Disk 0: [A1][A4][A7][P4]
Disk 1: [A2][A5][P3][A10]
Disk 2: [A3][P2][A8][A11]
Disk 3: [P1][A6][A9][A12]

Parity rotated across disks
```

**Performance**:
- **Read Throughput**: N × single disk (all disks can serve reads)
- **Write Throughput**: Better than RAID 4 (no single parity disk bottleneck)
  - Still requires read-modify-write for small writes
  - Full-stripe writes avoid parity read

**Fault Tolerance**: Tolerates failure of any one disk

**Capacity Overhead**: 1/N

**Use Case**: Good balance of performance, capacity, and reliability for general-purpose servers

**Popular Configuration**: Most common RAID level for medium-sized arrays (4-12 disks)

#### RAID 6: Dual Parity

**Mechanism**: Uses two different parity calculations (e.g., P and Q parity) to protect against two simultaneous disk failures.

```
Disk 0: [A1][A4][P3][Q4]
Disk 1: [A2][P2][A7][A10]
Disk 2: [P1][A5][A8][A11]
Disk 3: [Q1][A6][A9][A12]

Two independent parity schemes
```

**Parity Schemes**:
- **P parity**: Simple XOR (same as RAID 5)
- **Q parity**: Reed-Solomon code (more complex math)

**Performance**:
- **Read Throughput**: N × single disk
- **Write Throughput**: Slower than RAID 5 (two parities to compute and write)
- **Rebuild**: Slower due to complex Q parity

**Fault Tolerance**: **High**
- Tolerates simultaneous failure of any two disks
- Critical for large arrays where rebuild time is long

**Capacity Overhead**: 2/N

**Use Case**: Large storage arrays where likelihood of simultaneous failures during rebuild is significant

**Importance**: As disk sizes grow (10+ TB), rebuild times can exceed 24 hours, increasing the probability of a second failure during rebuild

### RAID Comparison

| RAID Level | Capacity | Read Performance | Write Performance | Fault Tolerance | Best Use Case |
|------------|----------|------------------|-------------------|-----------------|---------------|
| **RAID 0** | N × disk | Excellent (N×) | Excellent (N×) | None | Temp storage, performance |
| **RAID 1** | N/2 | Good (N×) | Moderate (1×) | N-1 failures | Critical data, databases |
| **RAID 4** | (N-1) × disk | Good ((N-1)×) | Poor (bottleneck) | 1 failure | Rarely used |
| **RAID 5** | (N-1) × disk | Excellent (N×) | Good | 1 failure | General servers |
| **RAID 6** | (N-2) × disk | Excellent (N×) | Moderate | 2 failures | Large arrays |

### Nested RAID

Combine RAID levels for specific benefits:

**RAID 10 (1+0)**: Mirror of stripes
```
RAID 1      RAID 1
  ↓           ↓
[D0][D1]  [D2][D3]  ← Mirrors
  └─────┬─────┘
      RAID 0 Stripe
```
- Excellent performance and reliability
- 50% capacity overhead
- Tolerates multiple failures (if not in same mirror group)

**RAID 50 (5+0)**: Stripe of RAID 5 arrays
- Better performance than RAID 5
- Better fault tolerance than RAID 5

**RAID 60 (6+0)**: Stripe of RAID 6 arrays
- Maximum protection for very large arrays

### Hardware vs. Software RAID

**Hardware RAID**:
- Dedicated RAID controller with processor and battery-backed cache
- **Pros**: Better performance, offloads CPU, cache survives power loss
- **Cons**: Expensive, vendor lock-in

**Software RAID**:
- OS-level RAID implementation (e.g., Linux md, Windows Storage Spaces)
- **Pros**: Flexible, no special hardware, can span different controllers
- **Cons**: CPU overhead, no battery-backed cache

## System Dependability

Dependability is the quality of a system that justifies relying on it. It encompasses reliability, availability, and fault tolerance.

### Reliability and Availability

**Reliability**: Continuous service accomplishment
- **MTTF (Mean Time To Failure)**: Average time until first failure
- **MTBF (Mean Time Between Failures)**: MTTF + MTTR

**Availability**: Fraction of time system provides correct service

$$
Availability = \frac{MTTF}{MTTF + MTTR}
$$

Where:
- **MTTF**: Mean Time To Failure
- **MTTR**: Mean Time To Repair

**Example**:
- Disk MTTF: 1,000,000 hours (~114 years)
- Disk MTTR: 4 hours

$$
Availability = \frac{1,000,000}{1,000,000 + 4} = 99.9996\%
$$

**For RAID 5 with 10 disks**:
- Probability of one failure is higher (10× more disks)
- But can tolerate one failure
- Availability increases if rebuild time < MTTF of remaining disks

### Fault, Error, and Failure

**Fault**: Underlying defect (e.g., cosmic ray bit flip, hardware defect)

**Error**: Deviation from correct state (e.g., incorrect bit value)

**Failure**: Deviation from specified system behavior (e.g., data corruption visible to user)

**Chain**: Fault → Error → Failure

**Goal**: Break this chain through fault tolerance

### Fault Tolerance Techniques

#### Redundancy

**N-Module Redundancy (NMR)**: Use N identical modules and vote on outputs
- **TMR (Triple-Module Redundancy)**: N=3, can mask one faulty module
- **Cost**: 3× hardware overhead
- **Benefit**: No downtime on single fault

#### Error-Correcting Codes (ECC)

Used extensively in memory systems:

**SECDED (Single-Error Correction, Double-Error Detection)**:
- Adds extra bits (e.g., 8 bits for 64-bit word)
- Can correct 1-bit error, detect 2-bit error
- Overhead: ~12.5% for 64-bit words

**Chipkill**: Advanced ECC protecting against entire memory chip failure
- Used in high-reliability servers
- Higher overhead but protects against worst-case failures

#### Checksums and CRCs

**Checksum**: Simple sum of data blocks (detects errors)
**CRC (Cyclic Redundancy Check)**: Polynomial-based error detection
- Used in networking, storage
- Can detect burst errors

### Dependability in Storage

**RAID**: Provides fault tolerance (covered above)

**Scrubbing**: Periodic background verification
- Reads all data, checks parity/ECC
- Corrects silent errors before they accumulate

**SMART (Self-Monitoring, Analysis and Reporting Technology)**:
- Drives monitor their own health
- Report predictive failures (temperature, reallocated sectors, etc.)
- Allows proactive replacement

## References

- CS 6290: High Performance Computer Architecture: Georgia Tech OMSCS
