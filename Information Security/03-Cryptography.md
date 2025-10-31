# 03 Cryptography

## Table of Contents

1. [Overview](#overview)
2. [Cryptographic Primitives](#cryptographic-primitives)
3. [Symmetric Cryptography](#symmetric-cryptography)
4. [Asymmetric Cryptography](#asymmetric-cryptography)
5. [Hash Functions](#hash-functions)
6. [Message Authentication Codes](#message-authentication-codes)
7. [Digital Signatures](#digital-signatures)
8. [Key Management](#key-management)
9. [Cryptographic Protocols](#cryptographic-protocols)
10. [Practical Security Considerations](#practical-security-considerations)
11. [Post-Quantum Cryptography](#post-quantum-cryptography)

## Overview

**Cryptography** is the mathematical science of securing information through encoding and decoding techniques. Modern cryptography provides the foundational security services that protect data confidentiality, integrity, and authenticity in digital systems.

### Security Services

- **Confidentiality**: Preventing unauthorized disclosure (encryption)
- **Integrity**: Detecting unauthorized modification (hash functions, MACs)
- **Authentication**: Verifying identity (digital signatures, MACs)
- **Non-repudiation**: Preventing denial of actions (digital signatures)

### Kerckhoffs's Principle

> "A cryptosystem should be secure even if everything about the system, except the key, is public knowledge."

This principle, established in 1883, remains fundamental to modern cryptography. Security should depend solely on the secrecy of the key, not on the secrecy of the algorithm.

## Cryptographic Primitives

Cryptographic primitives are the basic building blocks used to construct security protocols.

### Primitive Categories

**Encryption**: Symmetric (single key: AES, ChaCha20), Asymmetric (public/private keys: RSA, ECC)

**Authentication**: Hash functions (SHA-256, SHA-3), MACs (HMAC), Digital signatures (RSA, ECDSA)

**Key Establishment**: Key exchange (Diffie-Hellman), Key encapsulation (RSA-KEM)

## Symmetric Cryptography

**Symmetric cryptography** uses a single shared secret key for both encryption and decryption.

### Symmetric Encryption Model

```
Plaintext (M) + Key (K)  →  [Encryption]  →  Ciphertext (C)
Ciphertext (C) + Key (K)  →  [Decryption]  →  Plaintext (M)
```

### Block Ciphers

**Block ciphers** encrypt fixed-size blocks of data (typically 128 bits).

#### Advanced Encryption Standard (AES)

AES is the current standard for symmetric encryption, adopted by NIST in 2001.

**Parameters**: Block size 128 bits, Key sizes 128/192/256 bits, Rounds 10/12/14, Structure: SPN

**Operations**: SubBytes (S-box substitution), ShiftRows (row shifting), MixColumns (column mixing), AddRoundKey (XOR with key)

**Security**: No practical attacks on full AES, brute force infeasible (2^256), quantum-resistant (2^128 with Grover's), hardware-accelerated (AES-NI)

#### Data Encryption Standard (DES) - Legacy

**Parameters**: Block 64 bits, Key 56 bits, 16 rounds, Feistel network

**[BROKEN]** (1998 brute-force), do not use. Triple DES (3DES): 112-bit effective strength, **deprecated** (NIST 2023), use AES

### Block Cipher Modes of Operation

Block ciphers operate on fixed-size blocks; modes of operation enable encryption of arbitrary-length messages.

#### Electronic Codebook (ECB)

Each block encrypted independently. Identical plaintext → identical ciphertext. **[INSECURE]**: reveals patterns

#### Cipher Block Chaining (CBC)

Each block XORed with previous ciphertext. Requires unpredictable IV. **[SECURE]** with proper IV. **[WARNING]** Padding oracle attacks possible. Used in TLS 1.0-1.2

#### Counter (CTR)

Converts block cipher to stream cipher. Parallelizable, no padding needed, random access. **[SECURE]** with unique IV/counter

#### Galois/Counter Mode (GCM)

CTR mode + GMAC authentication. **AEAD** (Authenticated Encryption with Associated Data): provides confidentiality + integrity. Parallelizable, hardware-accelerated. Industry standard (TLS 1.3, IPsec). **Critical**: unique nonce per encryption (reuse breaks security)

### Stream Ciphers

**Stream ciphers** generate a keystream that is XORed with plaintext.

#### ChaCha20

Modern stream cipher (256-bit key, 96-bit nonce). **ChaCha20-Poly1305**: AEAD like GCM. Used in TLS 1.3, SSH, VPNs. Better than AES on devices without hardware acceleration (no timing attacks, faster in software)

### Symmetric Key Management Challenge

**Problem**: How to securely share secret keys? Pre-shared keys (not scalable), key distribution center (single point of failure). **Solution**: Asymmetric cryptography for key exchange

## Asymmetric Cryptography

**Asymmetric cryptography** uses a pair of mathematically related keys: public key (shared openly) and private key (kept secret).

### Asymmetric Encryption Model

```
Encryption:  Plaintext + Public Key (PK)  → Ciphertext
Decryption:  Ciphertext + Private Key (SK) → Plaintext
```

### RSA (Rivest-Shamir-Adleman)

RSA is the most widely deployed public-key cryptosystem, based on the difficulty of factoring large integers.

#### RSA Key Generation & Operations

**Generation**: Select primes p, q → compute n = p×q, φ(n) = (p-1)(q-1) → choose e (commonly 65537) → compute d = e^(-1) mod φ(n). Public key (e, n), Private key (d, n)

**Encryption**: C = M^e mod n (public key)
**Decryption**: M = C^d mod n (private key)

#### RSA Security

Based on hard factoring problem. **Key sizes**: 1024-bit (insecure, do not use), 2048-bit (minimum), 3072-bit (long-term), 4096-bit (high security)

**Vulnerabilities**: Textbook RSA insecure (use OAEP padding), timing attacks, quantum computers (Shor's algorithm breaks RSA)

**Padding**: PKCS#1 v1.5 (vulnerable), OAEP (secure, recommended)

### Diffie-Hellman Key Exchange

Protocol for two parties to establish a shared secret over an insecure channel.

#### Diffie-Hellman Protocol

Alice & Bob exchange public values (A = g^a mod p, B = g^b mod p) → both compute shared secret s = g^(ab) mod p

**Security**: Based on Discrete Logarithm Problem. **[WARNING]** Vulnerable to MitM (mitigate with authentication)

**ECDH**: Same concept using elliptic curves. Shorter keys, preferred in modern protocols (TLS 1.3)

### Elliptic Curve Cryptography (ECC)

ECC provides equivalent security to RSA with much shorter keys.

**Security Comparison:**

| ECC Key Size | RSA Equivalent | Quantum Security (bits) |
|-------------|----------------|------------------------|
| 256 bits    | 3072 bits      | 128 bits              |
| 384 bits    | 7680 bits      | 192 bits              |
| 521 bits    | 15360 bits     | 256 bits              |

**Advantages:**
- Smaller keys → less storage, faster computation
- Better performance on mobile and IoT devices
- Lower bandwidth requirements

**Commonly Used Curves:**
- **NIST P-256** (secp256r1): Widely deployed, some concerns about NSA involvement
- **Curve25519**: Modern, fast, designed to avoid implementation pitfalls
- **secp384r1**: Higher security level

**Applications:**
- TLS/SSL (ECDHE key exchange)
- Bitcoin and cryptocurrencies (ECDSA signatures)
- SSH
- Signal Protocol (X25519)

## Hash Functions

**Cryptographic hash functions** map arbitrary-length input to fixed-length output (digest).

### Hash Function Properties

**Required Properties:**

1. **Preimage Resistance** (One-way):
   - Given hash h, computationally infeasible to find message m such that H(m) = h
   - Prevents password recovery from hashes

2. **Second Preimage Resistance** (Weak collision resistance):
   - Given message m1, computationally infeasible to find m2 ≠ m1 such that H(m1) = H(m2)
   - Prevents substitution attacks

3. **Collision Resistance** (Strong collision resistance):
   - Computationally infeasible to find any m1 ≠ m2 such that H(m1) = H(m2)
   - Required for digital signatures

**Desirable Properties:**
- **Deterministic**: Same input always produces same output
- **Fast computation**: Efficient to compute
- **Avalanche effect**: Small change in input drastically changes output
- **Fixed output size**: Regardless of input size

### SHA Family (Secure Hash Algorithm)

#### SHA-1 (Legacy)

- **Output**: 160 bits (20 bytes)
- **Status**: Broken (practical collision attacks demonstrated in 2017)
- **History**: Designed by NSA, published 1995
- **Attacks**: SHAttered attack produced identical SHA-1 hashes for different PDFs
- **Do not use**: Replaced by SHA-2

#### SHA-2 Family

| Algorithm | Output Size | Block Size | Security Level |
|-----------|-------------|------------|---------------|
| SHA-224   | 224 bits    | 512 bits   | 112 bits      |
| SHA-256   | 256 bits    | 512 bits   | 128 bits      |
| SHA-384   | 384 bits    | 1024 bits  | 192 bits      |
| SHA-512   | 512 bits    | 1024 bits  | 256 bits      |

- **Status**: Secure, widely deployed
- **Design**: Merkle-Damgård construction
- **Applications**: Digital signatures, certificate authorities, blockchain
- **Performance**: Hardware-accelerated on modern CPUs

#### SHA-3 (Keccak)

- **Output sizes**: 224, 256, 384, 512 bits
- **Design**: Sponge construction (different from SHA-2)
- **Status**: Secure, but less widely adopted than SHA-2
- **Advantage**: Different design provides diversity (hedging against SHA-2 vulnerabilities)
- **Performance**: Slower than SHA-2 in software, faster in hardware

### Hash Function Applications

**Password Storage:**
```
Insecure: Store password directly
Better:   Store H(password)
Secure:   Store H(password || salt) using Argon2/bcrypt
```

**Digital Signatures:**
```
Sign H(message) instead of message (efficiency)
```

**Data Integrity:**
```
File download: Provide SHA-256 hash for verification
Git commits: Identified by SHA-1 hash of contents
```

**Blockchain:**
```
Bitcoin: Double SHA-256 for proof-of-work
Merkle trees: Efficient verification of transaction inclusion
```

### Birthday Paradox and Collision Resistance

**Birthday Attack:**
- With n-bit hash, collision found in ~2^(n/2) attempts
- Example: SHA-256 (256 bits) requires ~2^128 attempts for collision
- Implication: Hash should be twice as long as desired security level

## Message Authentication Codes

**Message Authentication Codes (MACs)** provide both integrity and authentication using a shared secret key.

### MAC Construction

```
Tag = MAC(Key, Message)
Verification: Compare received tag with computed tag
```

**Properties:**
- Only parties with the key can create valid tags
- Detects any modification of message
- Does not provide non-repudiation (both parties have the key)

### HMAC (Hash-based MAC)

**HMAC Construction:**
```
HMAC(K, M) = H((K ⊕ opad) || H((K ⊕ ipad) || M))

Where:
  K = secret key (padded to block size)
  M = message
  H = hash function (e.g., SHA-256)
  opad = outer padding (0x5c repeated)
  ipad = inner padding (0x36 repeated)
  || = concatenation
```

**Properties:**
- Proven secure if underlying hash function is secure
- No known attacks on HMAC-SHA256
- Widely used in TLS, IPsec, SSH

**Common Variants:**
- HMAC-SHA256: 256-bit output
- HMAC-SHA512: 512-bit output
- HMAC-SHA1: Legacy, still used in some protocols

### Encrypt-then-MAC

**Authenticated Encryption Approaches:**

1. **Encrypt-and-MAC** (E&M): C = Enc(K1, M), T = MAC(K2, M)
   - Potential security issues

2. **MAC-then-Encrypt** (MtE): C = Enc(K1, M || MAC(K2, M))
   - Used in TLS 1.0-1.2, vulnerable to padding oracle attacks

3. **Encrypt-then-MAC** (EtM): C = Enc(K1, M), T = MAC(K2, C)
   - Provably secure, recommended approach
   - Used in IPsec

**Modern Alternative:**
- Use AEAD modes (GCM, ChaCha20-Poly1305) instead of separate MAC

## Digital Signatures

**Digital signatures** provide authentication, integrity, and non-repudiation using asymmetric cryptography.

### Digital Signature Model

```
Signing:    Signature = Sign(Private Key, Message)
Verification: Valid = Verify(Public Key, Message, Signature)
```

**Properties:**
- Only holder of private key can create signature
- Anyone with public key can verify
- Signature is specific to message (tamper-evident)
- Non-repudiation: Signer cannot deny signing

### RSA Signatures

**Signing (using private key):**
```
1. Compute hash: h = H(M)
2. Sign hash: s = h^d mod n
```

**Verification (using public key):**
```
1. Compute h' = H(M)
2. Recover h = s^e mod n
3. Check if h' == h
```

**Padding Schemes:**
- **PKCS#1 v1.5**: Legacy, vulnerable
- **PSS (Probabilistic Signature Scheme)**: Secure, recommended

### DSA (Digital Signature Algorithm)

Based on discrete logarithm problem, designed specifically for signatures.

**Parameters:**
- Prime p (2048-3072 bits)
- Prime q (divides p-1, 256 bits)
- Generator g

**Advantages:**
- Faster signature generation than RSA
- Shorter signatures than RSA

**Disadvantages:**
- Requires secure random number generation
- Reusing random value k exposes private key (Sony PlayStation 3 hack)

### ECDSA (Elliptic Curve DSA)

- DSA adapted to elliptic curves
- Shorter keys and signatures
- Widely used: Bitcoin, TLS, SSH

**Vulnerability:**
- Same k reuse vulnerability as DSA
- Requires high-quality random number generation

### EdDSA (Edwards-curve DSA)

Modern signature scheme based on Ed25519 curve.

**Advantages over ECDSA:**
- Deterministic (no random number generation required)
- Faster than ECDSA
- Easier to implement securely
- Recommended for new applications

**Applications:**
- SSH (Ed25519 keys)
- Signal Protocol
- Tor
- Cryptocurrencies (Monero, Cardano)

## Key Management

Key management is often the weakest link in cryptographic systems.

### Key Generation

**Requirements:**
- **Randomness**: Cryptographically secure random number generator (CSRNG)
- **Entropy**: Sufficient unpredictability
- **Sufficient length**: Meet security requirements

**Random Number Generation:**
```
Insecure:  rand(), Math.random(), time-based seeds
Secure:    /dev/urandom, CryptGenRandom, crypto.getRandomValues()
```

**Key Derivation:**
- Never use passwords directly as keys
- Use Key Derivation Functions (KDFs)

### Key Derivation Functions (KDFs)

**Password-Based KDFs:**

**PBKDF2 (Password-Based Key Derivation Function 2):**
```
Key = PBKDF2(password, salt, iterations, key_length)
```
- Vulnerable to GPU/ASIC attacks
- Still acceptable with high iteration count (>100,000)

**bcrypt:**
- Designed for password hashing
- Adaptive: Can increase computational cost over time
- Good for password storage

**scrypt:**
- Memory-hard function (resistant to hardware attacks)
- Better than PBKDF2 against parallelization

**Argon2:**
- Winner of Password Hashing Competition (2015)
- Best current practice for password hashing
- Three variants: Argon2d, Argon2i, Argon2id (hybrid, recommended)

**General KDFs (for non-password keys):**

**HKDF (HMAC-based KDF):**
```
PRK = HKDF-Extract(salt, IKM)  # Extract pseudo-random key
OKM = HKDF-Expand(PRK, info, L) # Expand to desired length
```
- Used in TLS 1.3, Signal Protocol
- Efficient and provably secure

### Key Storage

**Software Storage:**
- Encrypt keys at rest
- Use OS key storage (Keychain, Credential Manager)
- Limit access permissions

**Hardware Storage:**
- **Hardware Security Modules (HSMs)**: Enterprise-grade
- **Trusted Platform Module (TPM)**: Device-integrated
- **Smart cards**: Portable
- **Secure enclaves**: Mobile devices (ARM TrustZone, Intel SGX)

**Key Protection Hierarchy:**
```
Master Key (hardware-protected)
   ↓ (encrypts)
Key Encryption Keys (KEK)
   ↓ (encrypts)
Data Encryption Keys (DEK)
```

### Key Distribution

**Pre-Shared Keys (PSK):**
- Out-of-band distribution (physical meeting, secure courier)
- Does not scale

**Key Distribution Center (KDC):**
- Trusted third party distributes keys (Kerberos)
- Single point of failure

**Public Key Infrastructure (PKI):**
- Certificate Authorities issue digital certificates
- Scalable but complex

**Key Agreement Protocols:**
- Diffie-Hellman, ECDH
- Parties derive shared secret without transmitting it

### Key Rotation

**Best Practices:**
- Regularly rotate keys (frequency depends on usage and sensitivity)
- Automate rotation when possible
- Maintain key versioning
- Securely destroy old keys after rotation period

## Cryptographic Protocols

### TLS/SSL

**TLS Handshake (simplified):**
1. Client → Server: ClientHello (supported ciphers)
2. Server → Client: ServerHello (selected cipher), Certificate
3. Key Exchange: ECDH or RSA
4. Both derive session keys
5. Encrypted application data

**TLS 1.3 Improvements:**
- Faster handshake (1-RTT)
- Forward secrecy mandatory
- Removed weak ciphers
- Encrypted handshake

See [Network Security](05-Network-Security.md) for comprehensive TLS coverage.

### Key Exchange Protocols

**Station-to-Station (STS) Protocol:**
- Authenticated Diffie-Hellman
- Prevents Man-in-the-Middle attacks

**Perfect Forward Secrecy (PFS):**
- Compromise of long-term keys doesn't compromise past sessions
- Achieved using ephemeral Diffie-Hellman keys

## Practical Security Considerations

### Common Cryptographic Mistakes

1. **Using ECB mode**: Reveals patterns
2. **Reusing IVs/nonces**: Breaks security
3. **Using weak keys**: Insufficient entropy
4. **Rolling your own crypto**: Extremely difficult to get right
5. **Ignoring side-channels**: Timing, power analysis

### Side-Channel Attacks

**Timing Attacks:**
- Measure execution time to infer secret information
- Example: RSA timing attack, AES cache timing
- **Mitigation**: Constant-time implementations

**Power Analysis:**
- Measure power consumption during crypto operations
- **Simple Power Analysis (SPA)**: Direct observation
- **Differential Power Analysis (DPA)**: Statistical analysis
- **Mitigation**: Power consumption randomization, masking

**Cache Attacks:**
- Exploit CPU cache behavior (Spectre, Meltdown)
- **Mitigation**: Cache-timing-resistant algorithms

### Random Number Generation

**Failure Cases:**
- Debian OpenSSL (2008): Poor entropy, predictable keys
- Dual_EC_DRBG: NSA backdoor in NIST standard
- Android Bitcoin wallets: Weak randomness led to key recovery

**Best Practices:**
- Use OS-provided CSRNG (/dev/urandom, CryptGenRandom)
- Avoid user-space RNG implementations
- Continuously seed from hardware entropy

### Cryptographic Agility

**Design for algorithm replacement:**
- Algorithms have limited lifetimes
- SHA-1 broken, MD5 broken, DES broken
- Design systems to support multiple algorithms
- Use protocol versioning

## Post-Quantum Cryptography

**Quantum Threat:**
- **Shor's Algorithm**: Breaks RSA, ECC, Diffie-Hellman in polynomial time
- Large-scale quantum computers expected within 10-20 years
- **Harvest now, decrypt later**: Adversaries storing encrypted data for future decryption

### NIST Post-Quantum Standards (2022-2024)

**Public-Key Encryption/Key Establishment:**
- **CRYSTALS-Kyber**: Lattice-based, selected for standardization

**Digital Signatures:**
- **CRYSTALS-Dilithium**: Lattice-based
- **FALCON**: Lattice-based (NTRU)
- **SPHINCS+**: Hash-based

**Transition Strategy:**
- **Hybrid approach**: Use both classical and post-quantum algorithms
- Update critical systems first
- Plan multi-year migration

## Applications

### Secure Communication

**Email Encryption:**
- PGP/GPG: End-to-end encryption
- S/MIME: Certificate-based

**Messaging:**
- Signal Protocol: Double Ratchet, forward secrecy
- WhatsApp, Signal, Wire

**VPNs:**
- IPsec: Network-layer encryption
- WireGuard: Modern, efficient VPN protocol

### Data Protection

**Disk Encryption:**
- Full disk encryption (BitLocker, FileVault, LUKS)
- AES-XTS mode for disk encryption

**Database Encryption:**
- Transparent Data Encryption (TDE)
- Application-level encryption

### Blockchain and Cryptocurrencies

- **Bitcoin**: ECDSA signatures, SHA-256 proof-of-work
- **Ethereum**: Keccak-256 hashing
- **Smart contracts**: Cryptographic verification

### Authentication

**Password Hashing:**
- Argon2, bcrypt, scrypt
- Salt + hash, never plain passwords

**Multi-Factor Authentication:**
- TOTP (Time-based OTP): HMAC-SHA1
- FIDO2/WebAuthn: Public-key authentication

## Best Practices

### Algorithm Selection

**Recommended Algorithms (2024):**

| Purpose | Algorithm | Key Size | Notes |
|---------|-----------|----------|-------|
| **Symmetric Encryption** | AES-GCM | 256 bits | Use unique nonces |
| | ChaCha20-Poly1305 | 256 bits | Alternative to AES |
| **Asymmetric Encryption** | RSA-OAEP | 3072+ bits | Or use ECC |
| | ECDH (X25519) | 256 bits | For key exchange |
| **Digital Signatures** | RSA-PSS | 3072+ bits | Or use EdDSA |
| | EdDSA (Ed25519) | 256 bits | Recommended |
| **Hash Functions** | SHA-256 | - | Minimum |
| | SHA-512 | - | Higher security |
| **Password Hashing** | Argon2id | - | Best practice |
| | bcrypt | - | Acceptable alternative |

### Implementation Guidelines

1. **Use established libraries**: OpenSSL, libsodium, Bouncy Castle
2. **Never implement crypto yourself** unless you're a cryptographer
3. **Follow standards**: Use NIST, IETF recommendations
4. **Constant-time operations**: Prevent timing attacks
5. **Secure defaults**: Force users to make security-positive choices
6. **Fail securely**: Errors should not leak information
7. **Defense in depth**: Multiple layers of cryptographic protection

### Security Checklist

**Encryption:**
- Use authenticated encryption (GCM, ChaCha20-Poly1305)
- Never reuse IVs/nonces with the same key
- Use sufficiently long keys (AES-256, RSA-3072+)
- Avoid ECB mode
- Don't use DES, 3DES, RC4

**Hashing:**
- Use SHA-256 or SHA-3 for integrity
- Use Argon2 for passwords
- Don't use MD5 or SHA-1

**Random Numbers:**
- Use CSRNG for all cryptographic purposes
- Don't use time-based seeds or pseudo-RNGs

**Keys:**
- Protect keys with hardware when possible
- Rotate keys regularly
- Use KDFs for deriving keys from passwords
- Don't hardcode keys in source code
