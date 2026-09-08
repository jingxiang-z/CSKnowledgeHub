# 02 Application Layer

## Table of Contents

1. [Overview](#overview)
2. [HTTP](#http)
3. [SMTP and Email Protocols](#smtp-and-email-protocols)
4. [DNS](#dns)
5. [P2P Networks](#p2p-networks)
6. [Content Delivery Networks](#content-delivery-networks)
7. [Summary](#summary)
8. [References](#references)

## Overview

The **application layer** is the topmost layer in the TCP/IP and OSI models, providing network services directly to end-user applications. It enables user interactions with network resources and facilitates communication between software applications.

### Key Characteristics

| Aspect | Description |
|--------|-------------|
| **Position** | Top layer (Layer 7 OSI, Layer 4 TCP/IP) |
| **Purpose** | Provide services to end-user applications |
| **Interface** | APIs, protocols (HTTP, SMTP, DNS, FTP) |
| **Data Unit** | Messages |

### Core Functions

1. **End-User Services:** Direct interaction with users and applications
2. **Data Presentation:** Format conversion, encryption, compression
3. **Session Management:** Establish, maintain, terminate connections
4. **Application Protocols:** Implement specific application services
5. **Port-Based Identification:** Use port numbers to identify services

### Common Application Protocols

| Protocol | Port | Purpose | Transport |
|----------|------|---------|-----------|
| **HTTP** | 80 | Web browsing | TCP |
| **HTTPS** | 443 | Secure web browsing | TCP |
| **SMTP** | 25 | Send email | TCP |
| **POP3** | 110 | Retrieve email | TCP |
| **IMAP** | 143 | Retrieve email (advanced) | TCP |
| **FTP** | 20/21 | File transfer | TCP |
| **DNS** | 53 | Name resolution | UDP/TCP |
| **SSH** | 22 | Secure remote access | TCP |
| **Telnet** | 23 | Remote access (insecure) | TCP |

## HTTP

**HyperText Transfer Protocol** is the foundation of data communication on the World Wide Web.

### HTTP Characteristics

**1. Client-Server Model:**
```
┌──────────┐                      ┌──────────┐
│  Client  │ ─── HTTP Request ──→ │  Server  │
│(Browser) │ ←── HTTP Response ─  │ (Apache) │
└──────────┘                      └──────────┘
```

**2. Stateless Protocol:**
- Each request is independent
- Server doesn't retain information between requests
- State maintained via cookies, sessions, or tokens

**3. Text-Based:**
- Human-readable protocol
- Headers and methods are plain text
- Supports various content types in body

### HTTP Request Structure

```
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
Accept-Language: en-US
Connection: keep-alive

[Optional Request Body]
```

**Components:**

1. **Request Line:**
   - Method (GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH)
   - URL/URI
   - HTTP Version (HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3)

2. **Headers:**
   - Host: Domain name
   - User-Agent: Client information
   - Accept: Acceptable content types
   - Content-Type: Body format (for POST/PUT)
   - Authorization: Authentication credentials
   - Cookie: Session/state information

3. **Body (optional):** Data payload for POST/PUT requests

### HTTP Response Structure

```
HTTP/1.1 200 OK
Date: Mon, 01 Nov 2025 12:00:00 GMT
Server: Apache/2.4.1
Content-Type: text/html; charset=UTF-8
Content-Length: 1234
Connection: keep-alive

<!DOCTYPE html>
<html>...
```

**Components:**

1. **Status Line:**
   - HTTP Version
   - Status Code
   - Reason Phrase

2. **Response Headers:**
   - Date, Server, Content-Type, Content-Length
   - Set-Cookie: Set client cookies
   - Cache-Control: Caching directives
   - Location: Redirect URL (for 3xx)

3. **Body:** Response data (HTML, JSON, XML, images, etc.)

### HTTP Status Codes

| Code Range | Category | Examples |
|------------|----------|----------|
| **1xx** | Informational | 100 Continue, 101 Switching Protocols |
| **2xx** | Success | 200 OK, 201 Created, 204 No Content |
| **3xx** | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| **4xx** | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| **5xx** | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### HTTP Methods

| Method | Purpose | Idempotent | Safe | Body |
|--------|---------|------------|------|------|
| **GET** | Retrieve resource | Yes | Yes | No |
| **POST** | Create resource | No | No | Yes |
| **PUT** | Update/replace resource | Yes | No | Yes |
| **DELETE** | Delete resource | Yes | No | No |
| **HEAD** | Retrieve headers only | Yes | Yes | No |
| **OPTIONS** | Get supported methods | Yes | Yes | No |
| **PATCH** | Partial update | No | No | Yes |

**Idempotent:** Multiple identical requests have same effect as single request
**Safe:** Read-only, doesn't modify server state

### Cookies and Sessions

**Cookies:** Small data stored on client to maintain state

```
Server Response:
Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure

Subsequent Client Request:
Cookie: sessionId=abc123
```

**Cookie Attributes:**
- Domain: Which domain can access cookie
- Path: Which paths can access cookie
- Expires/Max-Age: Cookie lifetime
- HttpOnly: Not accessible via JavaScript (XSS protection)
- Secure: Only sent over HTTPS

**Sessions:** Server-side state management
1. Server creates session, generates session ID
2. Session ID sent to client in cookie
3. Client sends session ID with each request
4. Server retrieves session data using session ID

### HTTP Caching

Reduces latency and server load by storing responses locally.

```
Client          Proxy Cache          Origin Server
  │                  │                     │
  ├───Request──────→ │                     │
  │                  ├──Check Cache────→   │
  │                  │  (Cache Miss)       │
  │                  ├───Forward Request──→│
  │                  │←──Response──────────┤
  │←──Response───────┤  (Store in cache)   │
  │                  │                     │
```

**Cache-Control Directives:**
- `max-age=3600`: Cache for 3600 seconds
- `no-cache`: Revalidate with server before using
- `no-store`: Don't cache at all
- `private`: Cache only in browser, not proxies
- `public`: Cache in shared caches

### HTTP Versions

| Version | Year | Key Features |
|---------|------|--------------|
| **HTTP/1.0** | 1996 | Basic functionality, one request per connection |
| **HTTP/1.1** | 1997 | Persistent connections, chunked transfer, pipelining |
| **HTTP/2** | 2015 | Binary protocol, multiplexing, server push, header compression |
| **HTTP/3** | 2020 | QUIC (UDP-based), improved performance over unreliable networks |

**HTTP/1.1 vs HTTP/2:**

```
HTTP/1.1 (Sequential):
Conn ═══[Req1]═══[Res1]═══[Req2]═══[Res2]═══[Req3]═══[Res3]═══

HTTP/2 (Multiplexed):
Conn ═══[Req1][Req2][Req3]═══[Res1][Res3][Res2]═══
         All interleaved on single connection
```

### HTTPS (HTTP Secure)

HTTP over TLS/SSL providing encryption and authentication.

```
Client                                    Server
  │                                         │
  ├────ClientHello─────────────────────────→│
  │                                         │
  │←───ServerHello, Certificate─────────────┤
  │                                         │
  ├────Key Exchange────────────────────────→│
  │                                         │
  │←───Finished──────────────────────────────┤
  │                                         │
  ├────Encrypted HTTP Request──────────────→│
  │                                         │
  │←───Encrypted HTTP Response──────────────┤
```

**Benefits:**
- Confidentiality: Data encrypted in transit
- Integrity: Detect tampering
- Authentication: Verify server identity (certificates)

## SMTP and Email Protocols

### SMTP (Simple Mail Transfer Protocol)

**SMTP** is used for sending email from client to server and between servers.

```
┌─────────┐     SMTP      ┌──────────┐    SMTP     ┌─────────┐
│  Sender │  ────────→    │  Sender  │  ────────→  │Receiver │
│  (MUA)  │   Port 25     │   Mail   │   Port 25   │  Mail   │
│         │               │  Server  │             │ Server  │
└─────────┘               └──────────┘             └─────────┘
                                                         ↑
                                                         │
                                            ┌─────────┐  │ POP3/IMAP
                                            │Receiver │  │
                                            │  (MUA)  │←─┘
                                            └─────────┘
```

**SMTP Session Example:**

```
S: 220 mail.example.com SMTP Server ready
C: HELO client.example.com
S: 250 Hello client.example.com
C: MAIL FROM:<sender@example.com>
S: 250 OK
C: RCPT TO:<recipient@example.com>
S: 250 OK
C: DATA
S: 354 Start mail input
C: From: sender@example.com
C: To: recipient@example.com
C: Subject: Test Email
C:
C: This is the email body.
C: .
S: 250 OK Message accepted
C: QUIT
S: 221 Closing connection
```

### Email Retrieval Protocols

**POP3 (Post Office Protocol version 3):**

- Downloads emails to local device
- Typically deletes from server after download
- Stateful protocol with three phases:
  1. Authorization (username/password)
  2. Transaction (retrieve, delete messages)
  3. Update (commit changes)

```
C: USER alice
S: +OK
C: PASS secret123
S: +OK User successfully logged in
C: LIST
S: +OK 2 messages (320 octets)
S: 1 120
S: 2 200
C: RETR 1
S: +OK 120 octets
[message content]
C: DELE 1
S: +OK message 1 deleted
C: QUIT
S: +OK Goodbye
```

**IMAP (Internet Message Access Protocol):**

- Keeps emails on server
- Allows folder management
- Supports multiple devices
- More features than POP3

```
C: A001 LOGIN alice secret123
S: A001 OK LOGIN completed
C: A002 SELECT INBOX
S: * 5 EXISTS
S: A002 OK SELECT completed
C: A003 FETCH 1 BODY[]
S: * 1 FETCH (BODY[] {320}
[message content]
S: A003 OK FETCH completed
C: A004 LOGOUT
S: A004 OK LOGOUT completed
```

**POP3 vs IMAP:**

| Feature | POP3 | IMAP |
|---------|------|------|
| **Email Storage** | Downloads to client | Kept on server |
| **Multiple Devices** | Difficult | Easy |
| **Folder Management** | No | Yes |
| **Offline Access** | Yes (local copy) | Partial (cached) |
| **Server Storage** | Minimal (deleted) | All emails stored |
| **Complexity** | Simple | More complex |

## DNS

**Domain Name System** translates human-readable domain names to IP addresses.

### DNS Hierarchy

```
                    Root (.)
                       │
      ┌────────────────┼────────────────┐
      │                │                │
     com              org              net
      │                │                │
   example          example          example
      │                │                │
   www,mail        www,mail         www,mail
```

**DNS Query Process:**

```
1. User types "www.example.com"

2. Client → Local DNS Resolver

3. Resolver → Root DNS Server
   Response: "Try .com TLD server"

4. Resolver → .com TLD Server
   Response: "Try example.com authoritative server"

5. Resolver → example.com Authoritative Server
   Response: "www.example.com = 93.184.216.34"

6. Resolver → Client
   Response: "93.184.216.34"

7. Client → 93.184.216.34 (HTTP request)
```

### DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| **A** | IPv4 address | example.com → 93.184.216.34 |
| **AAAA** | IPv6 address | example.com → 2606:2800:220:1:248:1893:25c8:1946 |
| **CNAME** | Alias (canonical name) | www → example.com |
| **MX** | Mail server | Mail → mail.example.com (priority 10) |
| **NS** | Name server | NS → ns1.example.com |
| **TXT** | Text information | SPF, DKIM records |
| **PTR** | Reverse DNS (IP→name) | 34.216.184.93.in-addr.arpa → example.com |
| **SOA** | Start of authority | Zone information |

### DNS Query Types

**1. Recursive Query:**
- Client expects complete answer
- DNS resolver does all the work

**2. Iterative Query:**
- Server returns referral to next server
- Client queries each server in chain

### DNS Caching

- Reduces query load and latency
- Each record has TTL (Time To Live)
- Cached at multiple levels: browser, OS, resolver, ISP

### DNS Security (DNSSEC)

Adds cryptographic signatures to DNS records to prevent spoofing and cache poisoning.

## P2P Networks

**Peer-to-Peer** networks distribute workload among peers rather than relying on centralized servers.

### P2P vs Client-Server

```
Client-Server:              P2P:
    [Server]              [Peer] ←→ [Peer]
      ↗ ↓ ↖                 ↕  ↖  ↗  ↕
  [C] [C] [C]            [Peer] ←→ [Peer]
```

| Aspect | Client-Server | P2P |
|--------|---------------|-----|
| **Scalability** | Limited by server | High (more peers = more capacity) |
| **Cost** | High (server infrastructure) | Low (distributed) |
| **Reliability** | Single point of failure | Redundant |
| **Control** | Centralized | Decentralized |
| **Examples** | Web, email | BitTorrent, Bitcoin |

### BitTorrent Protocol

Efficient P2P file sharing protocol.

**Key Concepts:**

1. **Torrent File (.torrent):** Metadata about file and trackers
2. **Tracker:** Coordinates peers (who has what pieces)
3. **Peer:** Downloads and uploads file pieces
4. **Seeder:** Has complete file, only uploads
5. **Leecher:** Downloading file, may also upload
6. **Pieces:** File divided into fixed-size chunks
7. **Swarm:** All peers sharing a specific file

**BitTorrent Workflow:**

```
1. User downloads .torrent file
2. Client contacts tracker(s)
3. Tracker returns list of peers
4. Client connects to peers
5. Client requests rarest pieces first
6. Upload to other peers while downloading (tit-for-tat)
7. Once complete, becomes seeder
```

**Advantages:**
- Efficient for popular files (many seeders)
- Distributed load
- Resilient to failures

**Challenges:**
- Slow for unpopular files (few seeders)
- Incentive issues (free-riding)
- Legal concerns (copyright infringement)

## Content Delivery Networks

**CDNs** distribute content across geographically dispersed servers to improve performance and availability.

### CDN Architecture

```
┌──────────────────────────────────────────────┐
│           Origin Server                      │
│        (Master content)                      │
└──────────┬───────────────────────────────────┘
           │
     ┌─────┴─────┬─────────┬─────────┐
     │           │         │         │
  ┌──┴───┐   ┌──┴───┐  ┌──┴───┐  ┌──┴───┐
  │ Edge │   │ Edge │  │ Edge │  │ Edge │
  │Server│   │Server│  │Server│  │Server│
  │(NYC) │   │(LON) │  │(TKO) │  │(SYD) │
  └───┬──┘   └───┬──┘  └───┬──┘  └───┬──┘
      │          │         │          │
   [Users]    [Users]   [Users]    [Users]
```

### CDN Benefits

| Benefit | Description |
|---------|-------------|
| **Reduced Latency** | Content served from nearby edge server |
| **Load Distribution** | Offload traffic from origin server |
| **High Availability** | Redundant servers, failover capability |
| **DDoS Protection** | Absorb and filter malicious traffic |
| **Bandwidth Savings** | Reduce origin server bandwidth costs |

### CDN Request Flow

```
1. User requests www.example.com/image.jpg
2. DNS returns IP of nearest CDN edge server
3. User connects to edge server
4. If cached: Edge server returns content
   If not cached:
   a. Edge server requests from origin
   b. Origin returns content
   c. Edge caches content
   d. Edge returns content to user
5. Subsequent requests served from cache (if not expired)
```

### Cache Strategies

**1. Push CDN:**
- Content uploaded to CDN manually
- Full control over what's cached
- Good for static, infrequently updated content

**2. Pull CDN:**
- Content fetched from origin on first request
- Automatic, lazy caching
- Good for dynamic content

### Popular CDNs

- Cloudflare
- Akamai
- Amazon CloudFront
- Fastly
- Google Cloud CDN

## Summary

The application layer provides network services directly to end users. Key protocols:

**HTTP/HTTPS:**
- Foundation of web communication
- Stateless, request-response model
- Versions: HTTP/1.1, HTTP/2, HTTP/3
- HTTPS adds encryption and authentication

**Email (SMTP, POP3, IMAP):**
- SMTP: Send mail (client→server, server→server)
- POP3: Download mail (simple)
- IMAP: Manage mail on server (advanced)

**DNS:**
- Hierarchical system for name resolution
- Distributed database
- Recursive and iterative queries
- Various record types (A, AAAA, CNAME, MX, etc.)

**P2P:**
- Decentralized architecture
- BitTorrent: Efficient file distribution
- Scalable but faces incentive challenges

**CDN:**
- Distributed content delivery
- Reduces latency, improves availability
- Essential for high-traffic websites

## References

**Course Materials:**
- CSEE 4119: An Introduction to Computer Networks - Columbia University

**Textbooks:**
- Kurose, James F., and Keith W. Ross. *Computer Networking: A Top-Down Approach*. 8th Edition, Pearson, 2021.

**RFCs:**
- RFC 2616: HTTP/1.1
- RFC 7540: HTTP/2
- RFC 9114: HTTP/3
- RFC 5321: SMTP
- RFC 1939: POP3
- RFC 3501: IMAP
- RFC 1035: DNS
- RFC 4034: DNSSEC
