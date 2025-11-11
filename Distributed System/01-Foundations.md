# 01-Distributed System Foundations

## Overview

A distributed system is a collection of autonomous computing nodes that communicate over a network to achieve a common goal. Unlike centralized systems, distributed systems face unique challenges arising from the lack of shared memory, independent node failures, unpredictable network delays, and the fundamental impossibility of perfect coordination. This document establishes the foundational concepts necessary for understanding and building distributed systems: defining characteristics, system models, failure modes, fundamental impossibility results, and key design principles.

## Table of Contents

1. [Defining Characteristics](#defining-characteristics)
2. [System Models](#system-models)
3. [Failure Models](#failure-models)
4. [The CAP Theorem](#the-cap-theorem)
5. [Fundamental Problems](#fundamental-problems)
6. [Consistency Models](#consistency-models)
7. [Replication and Fault Tolerance](#replication-and-fault-tolerance)
8. [Architectural Patterns](#architectural-patterns)
9. [Design Principles](#design-principles)
10. [Summary](#summary)

## Defining Characteristics

A distributed system is characterized by a set of core properties that distinguish it from centralized and parallel systems.

### Core Properties

**Interconnected Autonomous Nodes**

A distributed system is a collection of independent nodes, each with its own processor, memory, and local state, interconnected by a Local Area Network (LAN) or Wide Area Network (WAN). Each node operates autonomously and can make local decisions.

**No Shared Physical Memory**

Nodes do not share physical memory. All communication and coordination must occur through explicit message passing over the network. This fundamental constraint shapes the design of all distributed algorithms.

**Communication Time Dominance**

The time required for message communication between nodes (Tm) is significantly greater than the time to execute local computations (Te). This inequality, **Tm >> Te**, is the defining characteristic of distributed systems according to Lamport's definition:

> *"A system is distributed if the message transmission time is not negligible compared to the time between events in a single process."*

**Implications:** Because communication dominates, distributed algorithms must minimize message passing and maximize local computation. Even modern data center clusters qualify as distributed systems, as network latency remains orders of magnitude higher than local memory access.

**Partial Failure**

Individual nodes or network links can fail independently while the rest of the system continues operating. Unlike centralized systems where a single failure halts everything, distributed systems must gracefully handle partial failures.

**Concurrency**

Multiple nodes execute simultaneously, leading to inherent concurrency. Without perfect synchronization, different nodes may observe events in different orders, creating consistency challenges.

## System Models

System models define the assumptions about timing, synchronization, and behavior that algorithms can rely upon. The choice of model profoundly affects what is achievable.

### Timing Models

**Synchronous System**

A system where there exist known upper bounds on:
- Message delivery time
- Processing time for each step
- Clock drift rate

*Advantages:* Enables timeout-based failure detection. If a node doesn't respond within the bound, it can be declared failed with certainty.

*Disadvantages:* Difficult to achieve in practice, especially in WANs. Requires conservative bounds, leading to poor performance.

*Example:* Hard real-time systems, tightly-coupled clusters with reliable networks.

**Asynchronous System**

A system with no timing assumptions. Messages can be arbitrarily delayed, processes can be arbitrarily slow, and there are no clock bounds.

*Advantages:* Realistic model for the Internet and most distributed systems.

*Disadvantages:* Fundamentally limits what can be achieved. The FLP impossibility result shows that consensus is impossible in asynchronous systems with even one crash failure.

*Key Challenge:* Cannot distinguish between a slow node and a crashed node using timeouts alone.

**Partially Synchronous System**

A middle ground: the system behaves asynchronously during periods of instability but eventually stabilizes to synchronous behavior. Most real-world systems fall into this category.

*Characteristics:* Bounds exist but are unknown, or the system eventually satisfies bounds after an unknown stabilization period.

*Examples:* Modern cloud environments, Internet protocols with adaptive timeouts.

### Communication Models

**Reliable Communication**

Messages are eventually delivered without corruption, duplication, or reordering. Lost messages are automatically retransmitted by lower layers (e.g., TCP).

**Unreliable Communication**

Messages may be lost, duplicated, corrupted, or reordered. The application must handle these scenarios (e.g., UDP).

**Network Partitions**

The network may split into disconnected components, preventing communication between partitions. Nodes within a partition can communicate, but not across partitions.

## Failure Models

Failure models characterize the types of failures that can occur and define the behavior of faulty components.

### Crash Failures (Fail-Stop)

A node stops executing and never recovers. Once crashed, it sends no further messages and performs no further computations. This is the simplest and most commonly assumed failure model.

**Detection:** Difficult in asynchronous systems (indistinguishable from slow nodes) but straightforward in synchronous systems using timeouts.

**Recovery:** No recovery—the node is permanently failed. However, state may be recovered from persistent storage or replicas.

### Omission Failures

A node fails to send or receive messages, but otherwise continues executing correctly. Can be subdivided into:
- **Send omission:** Node fails to send some messages
- **Receive omission:** Node fails to receive some messages

**Relationship to Crash:** Crash failures are a special case where all subsequent sends and receives are omitted.

### Timing Failures

In synchronous systems, a node fails to respond within the expected time bounds. Examples include:
- Response arrives too late
- Clock drift exceeds allowed bounds

These are critical in real-time systems but less relevant in asynchronous models.

### Byzantine Failures (Arbitrary Failures)

The most severe failure model: a faulty node can exhibit arbitrary, even malicious, behavior. It may:
- Send incorrect or contradictory messages
- Collude with other faulty nodes
- Corrupt local state
- Impersonate other nodes

**Examples:** Security attacks, software bugs, hardware corruption, compromised nodes.

**Cost:** Byzantine fault tolerance requires significantly more resources (typically 3f+1 replicas to tolerate f failures, compared to f+1 for crash failures).

**Byzantine Generals Problem:** The classic formulation: how can loyal generals coordinate an attack when some generals may be traitors sending conflicting messages?

### Network Partition Failures

The network splits into disconnected subnetworks. Nodes within each partition can communicate, but not across partitions.

**Split-Brain Problem:** Each partition may independently elect a leader or modify state, leading to inconsistency when partitions heal.

**Common Causes:** Network cable cuts, router failures, firewall misconfigurations, geographic isolation.

## The CAP Theorem

The CAP theorem (also called Brewer's theorem) is a fundamental impossibility result stating that a distributed system cannot simultaneously guarantee all three of the following properties:

### The Three Properties

**Consistency (C)**

Every read receives the most recent write or an error. All nodes see the same data at the same time. Equivalent to linearizability or strong consistency.

**Availability (A)**

Every request (read or write) receives a non-error response, without guarantee that it contains the most recent write. The system remains operational for all requests.

**Partition Tolerance (P)**

The system continues to operate despite arbitrary message loss or network partitions. Nodes may be temporarily unable to communicate.

### The Impossibility

In the presence of a network partition (P), which is unavoidable in real-world distributed systems, you must choose between consistency (C) and availability (A):

**CP Systems (Consistency + Partition Tolerance)**

Sacrifice availability during partitions. Some nodes may refuse requests to maintain consistency.

*Examples:* HBase, MongoDB (with majority writes), Redis (with synchronous replication), distributed databases with strong consistency.

*Use Case:* Financial systems, inventory management, any system where returning stale data is unacceptable.

**AP Systems (Availability + Partition Tolerance)**

Sacrifice consistency during partitions. All nodes remain available but may return stale data.

*Examples:* Cassandra, DynamoDB, Riak, Couchbase, DNS.

*Use Case:* Social media feeds, content delivery networks, shopping carts, systems where availability trumps consistency.

**CA Systems (Consistency + Availability)**

Only possible without network partitions, which means the system is not truly distributed or operates within a single data center with reliable networking.

*Examples:* Traditional RDBMS (PostgreSQL, MySQL) on a single node or with synchronous replication in a tightly-coupled cluster.

### Practical Implications

**Networks are unreliable:** Partitions happen in practice, so P is not optional. The real choice is between C and A during partitions.

**Not binary:** Real systems often provide tunable consistency levels (e.g., Cassandra's quorum reads/writes) allowing applications to choose their trade-off point.

**Eventually consistent systems:** Many AP systems provide eventual consistency—if writes stop, all replicas eventually converge to the same state.

## Fundamental Problems

Certain problems are fundamental to distributed systems and have been extensively studied. Solutions to these problems form the building blocks of larger systems.

### Consensus

The consensus problem requires a group of processes to agree on a single value, despite failures and asynchrony.

**Properties:**
- **Agreement:** All non-faulty processes decide on the same value
- **Validity:** The decided value was proposed by some process
- **Termination:** All non-faulty processes eventually decide

**FLP Impossibility:** Fischer, Lynch, and Paterson proved that consensus is impossible in an asynchronous system with even one crash failure if we require deterministic termination.

**Practical Solutions:** Real systems circumvent FLP through:
- Randomization (e.g., Ben-Or algorithm)
- Partial synchrony assumptions (e.g., Paxos, Raft)
- Failure detectors (detecting suspected failures)

**Applications:** Leader election, atomic commit (2PC, 3PC), state machine replication.

### Leader Election

Select a single node from a group to coordinate actions, preventing conflicts and providing a single point of decision.

**Challenges:**
- Handling simultaneous elections
- Dealing with network partitions (split-brain)
- Detecting leader failures

**Algorithms:** Bully algorithm, Ring algorithm, Paxos-based election, Raft leader election.

**Use Cases:** Distributed lock managers, cluster coordination (e.g., Zookeeper), primary-backup replication.

### Distributed Transactions

Ensure atomicity across multiple nodes: either all operations commit or all abort.

**Two-Phase Commit (2PC):**
- Phase 1 (Prepare): Coordinator asks all participants if they can commit
- Phase 2 (Commit/Abort): Based on votes, coordinator tells all to commit or abort

*Problem:* Blocking protocol—if coordinator crashes after participants vote yes, they're stuck waiting.

**Three-Phase Commit (3PC):** Non-blocking variant that adds a pre-commit phase, but requires synchrony assumptions.

**Modern Approaches:** Eventual consistency, CRDTs (Conflict-free Replicated Data Types), consensus-based transactions (e.g., Spanner).

### Mutual Exclusion

Ensure that only one process accesses a critical section at a time, without shared memory.

**Approaches:**
- Token-based (circulating token)
- Permission-based (Ricart-Agrawala algorithm)
- Quorum-based
- Coordinator-based (centralized lock manager)

**Metrics:** Message complexity, latency, fault tolerance.

## Consistency Models

Consistency models define the guarantees about the order and visibility of operations in a distributed system. Stronger models are easier to reason about but harder to implement efficiently.

### Strong Consistency (Linearizability)

Operations appear to occur instantaneously at some point between invocation and completion. Equivalent to a single, global, correct order.

**Guarantee:** If operation A completes before operation B begins, then A appears before B in the global order.

**Cost:** High latency, reduced availability (requires coordination).

**Example:** Read returns the value of the most recent completed write.

### Sequential Consistency

Operations appear to execute in some sequential order, and operations of each process appear in program order.

**Weaker than linearizability:** Doesn't respect real-time ordering across processes.

**Example:** All processes see writes in the same order, but not necessarily the real-time order.

### Causal Consistency

Operations that are causally related must be seen in causal order by all processes. Concurrent operations may be seen in different orders by different processes.

**Based on:** Lamport's "Happened Before" relationship.

**Example:** If write W1 happens before write W2 (causally), all processes see W1 before W2. But if W1 and W2 are concurrent, different processes may see them in different orders.

### Eventual Consistency

If no new updates are made, all replicas eventually converge to the same state.

**Weakest useful model:** Provides no guarantees about the order or timing of convergence.

**Highly available:** No coordination required for reads or writes.

**Examples:** DNS, Amazon's shopping cart, Cassandra with eventual consistency settings.

**Challenges:** Application must handle stale reads, conflicts, and convergence detection.

## Replication and Fault Tolerance

Replication is the primary mechanism for achieving fault tolerance and high availability in distributed systems.

### Why Replicate?

**Fault Tolerance:** If one replica fails, others can continue serving requests.

**High Availability:** Distribute load across replicas, reducing latency and increasing throughput.

**Locality:** Place replicas geographically close to users for faster access.

### Replication Strategies

**Primary-Backup (Master-Slave)**

One primary replica handles all writes; backups passively replicate the primary's state.

*Advantages:* Simple, strong consistency.

*Disadvantages:* Primary is a bottleneck and single point of failure.

**Multi-Primary (Multi-Master)**

Multiple replicas can accept writes simultaneously.

*Advantages:* Higher write throughput, no single point of failure.

*Disadvantages:* Conflict resolution required, eventual consistency.

**State Machine Replication**

Replicas start in the same state and deterministically apply the same operations in the same order.

*Key Requirement:* Consensus on operation order (e.g., via Paxos or Raft).

*Advantages:* Strong consistency, fault tolerance.

### Quorum Systems

Require agreement from a majority (or weighted quorum) of replicas before completing operations.

**Read Quorum (R) + Write Quorum (W) > N:** Ensures reads see most recent writes.

**Example:** In a system with 5 replicas, W=3 and R=3 ensures consistency.

**Trade-off:** Tune R and W for consistency vs. availability. High W = strong consistency but lower write availability.

## Architectural Patterns

Common architectural patterns shape how distributed systems are structured.

### Client-Server

Clients request services from centralized servers. Servers manage state and provide responses.

**Advantages:** Simple, centralized control, easier to secure.

**Disadvantages:** Server is a bottleneck and single point of failure.

**Examples:** Web applications, database systems, traditional file servers.

### Peer-to-Peer (P2P)

All nodes are equal peers, both clients and servers. No central coordination.

**Advantages:** Highly scalable, no single point of failure, self-organizing.

**Disadvantages:** Complex coordination, challenging to secure, harder to maintain consistency.

**Examples:** BitTorrent, blockchain networks, distributed hash tables (Chord, Kademlia).

### Multi-Tier (N-Tier)

System is divided into layers: presentation tier (UI), application tier (business logic), data tier (storage).

**Advantages:** Separation of concerns, independent scaling of tiers, easier to maintain.

**Disadvantages:** Increased complexity, network latency between tiers.

**Examples:** Enterprise web applications, microservices architectures.

### Microservices

System is composed of small, independent services that communicate via APIs.

**Advantages:** Independent deployment, technology diversity, fault isolation.

**Disadvantages:** Distributed system complexity (consensus, consistency), operational overhead.

**Examples:** Netflix, Amazon, Uber, modern cloud-native applications.

## Design Principles

The fundamental characteristics of distributed systems lead to several important design principles:

### Minimize Communication

Since communication dominates computation time (Tm >> Te), algorithms should maximize local work and minimize message passing. Batch operations when possible.

### Embrace Asynchrony

Systems cannot rely on global clocks or instantaneous communication. Design for asynchronous message passing with unbounded delays. Use event-driven architectures.

### Design for Partial Failure

Individual components will fail independently. Systems must detect failures, isolate faulty components, and continue operating with reduced capacity.

**Techniques:** Health checks, timeouts, circuit breakers, graceful degradation.

### Avoid Distributed State When Possible

Shared mutable state across nodes is expensive to maintain consistently. Prefer:
- Immutable data
- Local state
- Eventual consistency where appropriate
- Stateless services

### Use Idempotent Operations

Operations that can be safely retried without changing the result. Critical for handling message duplication and failures.

**Example:** `SET x = 5` is idempotent, but `INCREMENT x` is not.

### Plan for Scalability

Design systems to scale horizontally (add more nodes) rather than vertically (larger nodes). Use partitioning/sharding to distribute data and load.

### Observe and Monitor

Distributed systems are inherently complex. Comprehensive logging, metrics, and distributed tracing are essential for understanding behavior and diagnosing issues.

### Accept Trade-offs

Perfect solutions don't exist. CAP theorem, FLP impossibility, and latency constraints force trade-offs between consistency, availability, performance, and simplicity. Choose trade-offs that align with application requirements.

## Summary

Distributed systems are characterized by autonomous nodes communicating over networks where message delays dominate computation time. The absence of shared memory, inevitability of partial failures, and impossibility of perfect coordination create fundamental challenges. System models define assumptions about timing and communication, while failure models characterize how components can fail, from simple crash failures to Byzantine faults.

The CAP theorem establishes that distributed systems must choose between consistency and availability during network partitions, which are unavoidable in practice. Fundamental problems like consensus, leader election, and distributed transactions form the building blocks of distributed systems, though impossibility results like FLP show that some problems cannot be solved perfectly in asynchronous systems.

Consistency models range from strong linearizability (expensive but simple to reason about) to eventual consistency (highly available but complex to use correctly). Replication is the primary mechanism for fault tolerance, with various strategies trading consistency for availability. Common architectural patterns like client-server, peer-to-peer, and microservices shape system structure, each with distinct trade-offs.

Successful distributed systems embrace these challenges through careful design: minimizing communication, designing for partial failure, avoiding shared state, using idempotent operations, and accepting that perfect solutions don't exist. The art of distributed systems lies in understanding these fundamental principles and making informed trade-offs that align with application requirements.

## References

- Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM*, 21(7), 558-565.
- Fischer, M. J., Lynch, N. A., & Paterson, M. S. (1985). "Impossibility of Distributed Consensus with One Faulty Process." *Journal of the ACM*, 32(2), 374-382.
- Gilbert, S., & Lynch, N. (2002). "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services." *ACM SIGACT News*, 33(2), 51-59.
- Brewer, E. A. (2000). "Towards Robust Distributed Systems." *Proceedings of the 19th Annual ACM Symposium on Principles of Distributed Computing*.
- Vogels, W. (2009). "Eventually Consistent." *Communications of the ACM*, 52(1), 40-44.
- Tanenbaum, A. S., & Van Steen, M. (2017). *Distributed Systems: Principles and Paradigms* (3rd ed.). CreateSpace Independent Publishing Platform.
- Graduate courses from Georgia Institute of Technology and Columbia University
