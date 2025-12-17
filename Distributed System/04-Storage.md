# 03-Distributed Storage Systems

## Overview

This document explores two complementary approaches to building distributed storage systems: Distributed Memory and Distributed File Systems. Both exploit the collective resources of a cluster to overcome the limitations of individual nodes. The central theme is using network communication to provide powerful new abstractions—whether creating the illusion of shared memory across physically separate machines, or building high-performance, scalable file systems from commodity hardware. By leveraging advances in network technology that make remote memory access faster than local disk access, these systems trade network communication for disk I/O to deliver impressive performance improvements.

## Table of Contents

1. [Distributed Memory Systems](#distributed-memory-systems)
   - [Global Memory Systems (GMS)](#global-memory-systems-gms)
   - [Distributed Shared Memory (DSM)](#distributed-shared-memory-dsm)
2. [Distributed File Systems](#distributed-file-systems)
   - [Key Enabling Technologies](#key-enabling-technologies)
   - [xFS Architecture](#xfs-architecture-and-innovations)
   - [Data Structures and File Access](#data-structures-and-file-access-paths)
3. [Summary](#summary)

## Distributed Memory Systems

### Global Memory Systems (GMS)

The core proposition of a Global Memory System is to leverage the idle physical memory of peer nodes in a cluster as a fast, network-accessible paging device, serving as an intermediate tier in the memory hierarchy between a node's local memory and its local disk.

#### System Architecture and Core Concepts

**Objective**

To trade slower disk I/O for faster network communication when handling page faults. With gigabit and 10-gigabit LANs, fetching a page from a remote node's memory is substantially faster than retrieving it from an electromechanical disk, which incurs seek and rotational latency.

**Dynamic Memory Partition**

The physical memory of each node in the GMS is dynamically divided into two parts:

- **Local:** Contains the working set of processes currently executing on that node. The size of this partition grows or shrinks based on the node's memory pressure.

- **Global:** Contains "clean" (non-dirty) pages paged out by peer nodes. This partition serves as a community resource, acting as a cache for the cluster. An idle node's `local` part shrinks, allowing its `global` part to expand, effectively turning it into a "memory server."

**Reliability**

GMS does not introduce new failure concerns. The disk is always considered to hold a complete and authoritative copy of all pages. The `global` memory partitions only hold clean copies, so a node crash results only in the loss of a cached page, which can be retrieved from disk.

#### Page Fault Handling Mechanisms

GMS employs a community-based service for handling page faults, with behavior depending on the location of the faulted page and the memory pressure on the involved nodes. The key nodes are the faulting node (**P**), the node supplying the page (**Q**), and the node holding the globally oldest page (**R**).

| Case                 | Scenario                                                     | Actions & Impact                                             |
|----------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| **1. Common Case**   | Page `X` is found in the `global` cache of node **Q**.       | **Q** sends `X` to **P**. **P**'s `local` memory increases by one page to accommodate `X`. To make space, **P** evicts its oldest `global` page, `Y`, and sends it to **Q**. The `local`/`global` split on **P** shifts; on **Q**, it remains unchanged as `Y` replaces `X`. |
| **2. High Pressure** | **P**'s `global` cache is empty (all memory is `local`). It faults on page `X`. | **Q** sends `X` to **P**. **P** must now evict a page from its own `local` working set (its oldest page, `Y`) to make room for `X`, sending `Y` to **Q**. The `local`/`global` split on both **P** and **Q** remains unchanged. |
| **3. Disk Fetch**    | Page `X` is not in any cluster memory and must be fetched from disk. | **P** fetches `X` from disk, increasing its `local` memory. It evicts a `global` page, `Y`, to make room. `Y` is sent to node **R**, which holds the globally oldest page (`Z`). To store `Y`, **R** must discard `Z`. If `Z` was in **R**'s `global` cache, it is simply dropped (as it's a clean copy). If `Z` was in **R**'s `local` cache and dirty, it must be written to disk first. |
| **4. Shared Page**   | Page `X` is actively shared and is in the `local` working set of **Q**. **P** faults on `X`. | **Q** sends a *copy* of `X` to **P** but retains its own copy. The total memory pressure on the cluster increases. **P**'s `local` memory grows, so it evicts a `global` page `Y`. `Y` is sent to node **R** (with the globally oldest page), which must discard its oldest page to make room for `Y`, potentially writing it to disk. GMS does not manage coherence for shared pages; this is an application-level concern. |

#### Age Management: The "Geriatrics" Algorithm

To approximate a global LRU policy without excessive overhead, GMS uses an epoch-based distributed algorithm to identify the oldest pages in the cluster.

**Epochs**

Management work is divided into epochs, defined by a maximum time duration (`T`, e.g., a few seconds) or a maximum number of page replacements (`M`, e.g., thousands).

**Initiator Role**

At the start of each epoch, one node acts as the initiator (manager):

1. All nodes send age information for their resident pages to the initiator.
2. The initiator identifies the `M` oldest pages across the entire cluster. It calculates **MinAge**, the age of the youngest page within this `M`-page set. Any page older than `MinAge` is a replacement candidate.
3. The initiator calculates a weight vector (`W`), where `Wi` is the expected fraction of the `M` replacements that will come from node `Ni`.
4. The initiator broadcasts `MinAge` and the full weight vector `W` to all nodes.

**Local Decision Making ("Think Globally, Act Locally")**

For the duration of the epoch, each node acts locally using the global information:

- When a node must evict a page, it checks the page's age against `MinAge`. If `age > MinAge`, the page is a candidate for global replacement and is simply discarded.

- If `age < MinAge`, the page is considered active and must be preserved. It is sent to a peer node selected probabilistically based on the weight vector `W`.

**Dynamic Manager Selection**

To distribute the management burden, the initiator for the *next* epoch is the node with the highest weight in the current epoch, as this node is predicted to be the least active. This decision is made locally by all nodes, as they all possess the weight vector.

#### Implementation and Data Structures

GMS was implemented by modifying the OSF/1 operating system, demonstrating significant "heavy lifting" to integrate the concept into a real system.

**OS Integration**

GMS intercepts page fault handling from both the **Virtual Memory (VM)** system (for anonymous process pages) and the **Unified Buffer Cache (UBC)** (for file system pages). Instead of going to disk, these subsystems query GMS.

**Distributed Data Structures**

- **Universal ID (UID):** A globally unique identifier for a virtual page, derived from the node's IP address, disk partition, i-node, and page offset.

- **Page Ownership Directory (POD):** A replicated data structure on every node that maps a UID to its "owner" node—the node holding the GCD entry.

- **Global Cache Directory (GCD):** A distributed hash table, partitioned across owner nodes. It maps a UID to the node that currently holds the PFD entry (i.e., the node where the page physically resides).

- **Page Frame Directory (PFD):** A per-node data structure, analogous to a page table, that maps a UID to a local physical page frame.

**Page Fault Lookup Path**

On a page fault, a node converts the virtual address to a UID. It consults its local POD to find the owner. It then sends a network message to the owner, which consults its GCD partition to find the node hosting the page. Finally, a message is sent to the hosting node to retrieve the page.

For the common case of non-shared pages, the faulting node, owner node, and hosting node are often the same, minimizing network communication.

### Distributed Shared Memory (DSM)

DSM systems create the abstraction of a single, coherent shared memory address space on a cluster of nodes that have physically separate memories. This simplifies parallel programming by allowing developers to use familiar constructs like shared pointers, locks, and barriers, as opposed to the more complex message-passing paradigm.

#### Memory Consistency Models: SC vs. RC

The memory consistency model is a contract defining *when* a write to a shared location by one processor becomes visible to others. The choice of model has profound performance implications.

**Sequential Consistency (SC)**

The strictest model. It requires that all memory operations appear to execute in some single global sequential order, and the operations of any individual processor appear in its program order.

*Implication:* The system must perform a coherence action (e.g., sending invalidation or update messages) and wait for it to complete for *every* shared memory access. This creates significant overhead and hinders scalability.

*Example:*
```
P1: Write(X) -> Write(Y)
P2: Read(Y) -> Read(X)

SC guarantees: If P2 reads Y=new, then P2 must also read X=new
```

**Release Consistency (RC)**

A relaxed model that leverages the common programming pattern of protecting shared data with synchronization operations (e.g., locks).

*Concept:* It distinguishes between normal data accesses and synchronization accesses (`acquire` and `release`).

*Mechanism:* Coherence is not enforced on every data write. Instead, all pending writes by a processor are guaranteed to be globally visible only when that processor performs a `release` operation (e.g., unlocking a mutex). An `acquire` operation ensures that the processor sees all writes from the preceding `release`.

*Advantage:* This allows the system to overlap computation with the communication required for coherence actions, significantly improving performance.

*Example:*
```
P1: Write(X) -> Write(Y) -> Release(Lock)
P2: Acquire(Lock) -> Read(X) -> Read(Y)

RC guarantees: Coherence only at synchronization points
P1 can continue computing while coherence messages propagate
```

#### Lazy Release Consistency (LRC): An Optimization

LRC further postpones coherence actions to reduce network traffic.

**Eager RC (Vanilla RC)**

At a `release`, modifications are "pushed" to all other processors that might have a copy of the data. This can involve unnecessary broadcast messages.

**Lazy RC (LRC)**

At a `release`, no coherence actions are taken. Instead, when another processor performs an `acquire` on the same lock, it "pulls" only the necessary modifications from the previous lock holder.

*Advantage:* This changes the communication pattern from broadcast to point-to-point, reducing the number of messages and the amount of data transferred. It effectively procrastinates coherence actions until they are absolutely necessary.

*Comparison:*
```
Eager RC:  Release -> Broadcast updates to all potential sharers
Lazy RC:   Release -> No action
           Acquire -> Pull updates only from last releaser

Message reduction: O(N) broadcasts -> O(1) point-to-point
```

#### Implementation: Page-Based DSM with a Multiple-Writer Protocol

Software DSM is typically implemented at the granularity of virtual memory pages, using the OS and MMU hardware to trap on accesses.

**The False Sharing Problem**

A major issue with page-based coherence is *false sharing*. This occurs when two unrelated data objects, accessed by different processors, happen to reside on the same page. A write to one object by one processor will trigger an invalidation of the entire page for the other processor, even though its data was not actually modified. This leads to pages "ping-ponging" between nodes.

*Example:*
```
Page contains: [Object A | Object B]
P1 writes to Object A
P2 writes to Object B
Result: Page bounces between P1 and P2, even though no actual sharing
```

**Multiple-Writer Protocol**

To combat false sharing, systems like TreadMarks use a multiple-writer protocol combined with LRC:

1. Multiple processors are allowed to simultaneously write to their own copies of the same page.

2. When a processor first writes to a shared page, the OS creates a pristine copy called a **twin**.

3. At a `release` operation, the system compares the modified page with its twin to generate a **diff**—a record of the changes made. The twin is then discarded.

4. At a subsequent `acquire` of the same lock, the DSM software invalidates the local copies of pages that the previous lock holder modified.

5. When the acquiring processor faults on an invalidated page, the DSM software retrieves the necessary diff(s) from the previous writer(s) of that lock and applies them to its local page to bring it up-to-date.

**Garbage Collection**

Over time, numerous diffs can accumulate across the system. Periodically, a garbage collection process applies these diffs to the master copy of the page at its owner node, allowing the old diffs to be discarded.

*Diff Lifecycle:*
```
Write -> Create Twin -> Modify Page -> Release
  -> Generate Diff -> Store Diff -> Discard Twin
Acquire -> Invalidate Pages -> Fault -> Fetch Diff -> Apply Diff
GC -> Consolidate Diffs -> Update Master -> Discard Old Diffs
```

## Distributed File Systems

Distributed File Systems aim to solve the performance and scalability bottlenecks of a centralized file server (like traditional NFS) by distributing file storage, metadata management, and caching across an entire cluster. This section examines the xFS prototype from UC Berkeley, which exemplifies innovative approaches to building scalable, high-performance distributed storage systems.

### Key Enabling Technologies

#### Log-Structured File System (LFS)

Solves the "small write problem" common in file systems. Instead of performing many small, random writes to disk (which are inefficient), LFS buffers writes (for multiple files) in memory into a contiguous **log segment**. This large segment is then written to disk sequentially, which is much faster. Files are reconstructed from these logs on read.

**Traditional File System:**
```
Write file A -> Seek + Write inode -> Seek + Write data block
Write file B -> Seek + Write inode -> Seek + Write data block
Result: Multiple seeks, low throughput
```

**Log-Structured File System:**
```
Buffer writes to A, B, C in memory
Write [A_inode | A_data | B_inode | B_data | C_inode | C_data] sequentially
Result: Single sequential write, high throughput
```

#### Software RAID

xFS stripes these log segments across the disks of multiple storage server nodes in the cluster. This parallelizes disk I/O, dramatically increasing the aggregate I/O bandwidth available to clients.

**Benefits:**
- Parallel disk access across multiple servers
- Fault tolerance through redundancy
- Increased aggregate bandwidth: N servers → N × single-server bandwidth

#### Stripe Groups

Rather than striping every log segment across all available servers, xFS stripes a segment across a smaller, predefined **stripe group** (a subset of servers). This allows multiple clients to write to different stripe groups in parallel, increasing system throughput and availability.

**Advantages:**
- Multiple concurrent write streams
- Improved availability (failure of one stripe group doesn't affect others)
- Better load balancing
- Reduced coordination overhead

**Example:**
```
Cluster: 12 storage servers
Stripe group size: 4 servers
Possible stripe groups: 3 concurrent groups
→ 3 clients can write simultaneously to different groups
```

### xFS Architecture and Innovations

xFS builds on these technologies to create a scalable, serverless file system where all cluster nodes participate in storage and management.

#### Dynamic Management of Data and Metadata

Unlike in NFS where the manager of a file is the server that stores it, xFS decouples these roles:

- The node responsible for a file's metadata (**manager**) can be different from the storage servers that hold its data blocks
- This allows the system to distribute management load and avoid hotspots
- Manager responsibilities can be dynamically reassigned based on access patterns

**Benefits:**
- Load balancing of metadata operations
- Avoids single point of contention
- Scalability: Management work distributed across all nodes

#### Cooperative Caching

xFS leverages the memory of client nodes as a large, distributed file cache, turning client RAM into a valuable cluster resource.

**Coherence Protocol**

A single-writer, multiple-reader protocol is maintained at the file-block level:
- Multiple clients can cache the same block for reading
- Only one client can have write permission for a block at a time
- Manager tracks which clients cache each block

**Operation**

*Write Request:*
1. Client requests write permission from the file's manager
2. Manager sends invalidation messages to all other clients caching that block
3. After receiving acknowledgments, manager grants write permission
4. Client can now modify the block locally

*Cache Miss (Read):*
1. Client requests block from the file's manager
2. Manager checks if any client has a dirty cached copy
3. If yes, manager directs requesting client to fetch from peer's cache
4. If no, manager directs client to storage servers
5. Manager updates cache directory to track new copy

**Advantages:**
- Fast reads from peer memory (faster than disk)
- Reduced load on storage servers
- Leverages aggregate cluster memory

#### Distributed Log Cleaning

As files are updated, blocks in older log segments become obsolete, creating "holes." A **log cleaning** process is required to read the live blocks from multiple old segments, coalesce them into a new segment, and reclaim the disk space from the old ones. xFS distributes this responsibility:

- Each stripe group has a leader responsible for coordinating cleaning within its set of servers
- Clients, as the mutators of the file system, help track segment utilization
- Cleaning can proceed in background, overlapped with normal operations

**Cleaning Process:**
```
1. Identify segments with low utilization (many dead blocks)
2. Read live blocks from old segments
3. Write live blocks to new segment
4. Update metadata to point to new locations
5. Reclaim space from old segments
```

**Distributed Approach:**
- Leader per stripe group prevents centralized bottleneck
- Clients provide segment utilization information
- Cleaning parallelized across stripe groups

### Data Structures and File Access Paths

xFS relies on a set of distributed data structures to locate files and manage metadata efficiently.

#### Core Data Structures

**Manager Map:**
- Replicated map on all nodes
- Maps a file's i-number to its current manager node
- Allows any node to quickly locate who manages a given file
- Updated when manager responsibilities are reassigned

**Manager Data Structures:**
Each manager maintains:
- `File Directory`: Maps filename → i-number
- `i-map`: Maps i-number → i-node address (location in log)
- `Stripe Group Map`: Locates the log segments on storage servers
- `Cache Directory`: Tracks which clients have cached which blocks

#### File Access Paths

A client reading a file block follows one of three paths, from fastest to slowest:

**1. Local Cache Hit (Fastest)**

The block is found in the client's own memory. This is the expected common case.

```
Client checks local cache → Hit → Return data
Latency: ~100 ns (memory access)
```

**2. Peer Cache Hit (Medium)**

The block is not local. The client contacts the file's manager, which directs it to retrieve the block from another client's cache. This involves network communication but is faster than disk access.

```
Client checks local cache → Miss
→ Contact manager
→ Manager checks cache directory
→ Manager returns peer address
→ Client fetches from peer cache
Latency: ~10-100 μs (network + memory)
```

**3. Disk Access (Slowest)**

The block is not in any client cache. The client contacts the manager, which then uses its internal maps to locate the correct log segment on the appropriate storage server(s) and retrieve the block from disk.

```
Client checks local cache → Miss
→ Contact manager
→ Manager checks cache directory → Not cached
→ Manager consults i-map and stripe group map
→ Manager returns storage server addresses
→ Client fetches from storage servers
Latency: ~1-10 ms (network + disk I/O)
```

#### Performance Characteristics

| Access Path     | Latency    | Bandwidth      | Common Case |
|-----------------|------------|----------------|-------------|
| Local Cache     | ~100 ns    | Memory speed   | 80-90%      |
| Peer Cache      | ~10-100 μs | Network speed  | 5-15%       |
| Disk Access     | ~1-10 ms   | Disk speed     | 5-10%       |

The key to xFS performance is maximizing the local cache hit rate through cooperative caching and coherence protocols.

## Summary

Distributed storage systems leverage cluster resources through two complementary approaches:

**Distributed Memory Systems:** Global Memory Systems treat collective idle memory as a high-speed paging device, using sophisticated distributed algorithms like "geriatrics" for global LRU approximation. Distributed Shared Memory provides the illusion of shared memory across physically separate machines, with the evolution from Sequential Consistency to Lazy Release Consistency demonstrating how relaxing consistency models can yield significant performance gains. The multiple-writer protocol addresses the false sharing problem inherent in page-based implementations.

**Distributed File Systems:** xFS demonstrates how to build a scalable distributed file system by distributing all aspects of file management across a cluster. Key innovations include log-structured storage to solve the small-write problem, software RAID with stripe groups for parallelization, dynamic metadata management to distribute load, cooperative caching leveraging client memory, and distributed log cleaning to prevent bottlenecks. The xFS architecture represents a "serverless" approach where all nodes are peers, eliminating traditional client-server bottlenecks.

Both approaches exemplify the principle of trading fast network communication for slow disk I/O, a trade-off that becomes increasingly attractive as network speeds continue to improve. The concepts from these systems have influenced modern distributed storage platforms including Google File System (GFS), Hadoop Distributed File System (HDFS), and cloud storage services.

## References

- Feeley, M. J., et al. (1995). "Implementing Global Memory Management in a Workstation Cluster." *Proceedings of the 15th ACM Symposium on Operating Systems Principles*.
- Keleher, P., et al. (1994). "TreadMarks: Distributed Shared Memory on Standard Workstations and Operating Systems." *Proceedings of the Winter 1994 USENIX Conference*.
- Adve, S. V., & Gharachorloo, K. (1996). "Shared Memory Consistency Models: A Tutorial." *Computer*, 29(12), 66-76.
- Anderson, T. E., et al. (1995). "Serverless Network File Systems." *Proceedings of the 15th ACM Symposium on Operating Systems Principles*, 109-126.
- Rosenblum, M., & Ousterhout, J. K. (1992). "The Design and Implementation of a Log-Structured File System." *ACM Transactions on Computer Systems*, 10(1), 26-52.
- Thekkath, C. A., et al. (1997). "Frangipani: A Scalable Distributed File System." *Proceedings of the 16th ACM Symposium on Operating Systems Principles*.
- Graduate courses from Georgia Institute of Technology and Columbia University
