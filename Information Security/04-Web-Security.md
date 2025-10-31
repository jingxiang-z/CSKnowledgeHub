# 04 Web Security

## Table of Contents

1. [Overview](#overview)
2. [Web Application Security Fundamentals](#web-application-security-fundamentals)
3. [Common Web Vulnerabilities](#common-web-vulnerabilities)
4. [API Security](#api-security)
5. [Session Management](#session-management)
6. [Web Authentication Considerations](#web-authentication-considerations)
7. [HTTPS and Transport Security](#https-and-transport-security)
8. [Content Security Policy](#content-security-policy)
9. [Web Security Headers](#web-security-headers)
10. [Best Practices](#best-practices)

## Overview

**Web Security** focuses on protecting web applications, APIs, and websites from attacks that exploit vulnerabilities in web technologies, protocols, and application logic. Unlike network or system security, web security operates primarily at the application layer (Layer 7) and deals with HTTP/HTTPS, browsers, APIs, and user interactions.

### The Web Security Challenge

Web applications present unique security challenges:
- **Public exposure**: Accessible from anywhere on the internet
- **Complex attack surface**: Client-side code, server-side logic, databases, APIs
- **User input**: Untrusted data from users is the primary attack vector
- **Browser as platform**: Security relies on browser implementations and user behavior
- **Rapid development cycles**: Security often sacrificed for speed

## Web Application Security Fundamentals

### The OWASP Top 10

The Open Web Application Security Project (OWASP) maintains a list of the most critical web application security risks:

| Rank | Vulnerability | Description |
|------|--------------|-------------|
| **A01** | Broken Access Control | Failures that allow unauthorized access to resources |
| **A02** | Cryptographic Failures | Weak encryption or exposed sensitive data |
| **A03** | Injection | SQL, NoSQL, OS command, LDAP injection attacks |
| **A04** | Insecure Design | Missing or ineffective security controls |
| **A05** | Security Misconfiguration | Default configs, unnecessary features enabled |
| **A06** | Vulnerable Components | Using libraries/frameworks with known vulnerabilities |
| **A07** | Authentication Failures | Broken authentication and session management |
| **A08** | Software/Data Integrity | Insecure CI/CD, unsigned updates, compromised dependencies |
| **A09** | Logging/Monitoring Failures | Insufficient logging and incident response |
| **A10** | Server-Side Request Forgery | Web app fetches remote resources without validation |

### Secure Development Lifecycle for Web Apps

1. **Requirements**: Define security requirements (authentication, authorization, data protection)
2. **Design**: Threat modeling, secure architecture design
3. **Implementation**: Secure coding practices, input validation, output encoding
4. **Testing**: SAST, DAST, penetration testing, security code review
5. **Deployment**: Secure configuration, HTTPS enforcement, security headers
6. **Maintenance**: Patch management, security monitoring, incident response

## Common Web Vulnerabilities

### 1. Cross-Site Scripting (XSS)

**XSS** allows attackers to inject malicious scripts into web pages viewed by other users.

**Types of XSS:**

**Reflected XSS:**
```
Attacker crafts malicious URL:
https://example.com/search?q=<script>steal_cookies()</script>

Victim clicks link → Script executes in victim's browser
```

**Stored XSS:**
```
1. Attacker posts comment with malicious script
2. Script stored in database
3. Every user viewing the comment executes the script
```

**DOM-based XSS:**
```javascript
// Vulnerable JavaScript code
let username = location.hash.substring(1);
document.getElementById('welcome').innerHTML = 'Hello ' + username;

// Attack: https://example.com/#<img src=x onerror=alert(1)>
```

**Impact:**
- Cookie theft and session hijacking
- Keylogging
- Phishing (displaying fake login forms)
- Website defacement
- Malware distribution

**Prevention:**
- **Output encoding**: Encode user input before displaying (HTML entity encoding, JavaScript encoding, URL encoding)
- **Content Security Policy (CSP)**: Restrict script sources
- **HTTPOnly cookies**: Prevent JavaScript access to cookies
- **Input validation**: Validate and sanitize user input
- **Use frameworks**: Modern frameworks (React, Angular) provide automatic XSS protection

### 2. Cross-Site Request Forgery (CSRF)

**CSRF** forces authenticated users to perform unwanted actions on web applications.

**Attack Scenario:**
```
1. User logs into bank.com (authenticated session established)
2. User visits attacker's site evil.com
3. evil.com contains hidden form:
   <form action="https://bank.com/transfer" method="POST">
     <input name="to" value="attacker_account">
     <input name="amount" value="10000">
   </form>
   <script>document.forms[0].submit();</script>
4. Form auto-submits using victim's authenticated session
5. Bank transfers money to attacker
```

**Prevention:**
- **CSRF Tokens**: Include random, unpredictable tokens in forms
  ```html
  <form action="/transfer" method="POST">
    <input type="hidden" name="csrf_token" value="abc123xyz...">
    <input name="amount" value="100">
    <button type="submit">Transfer</button>
  </form>
  ```
- **SameSite Cookie Attribute**: `Set-Cookie: session=abc; SameSite=Strict`
- **Custom Headers**: Require custom header that CSRF can't add (e.g., X-Requested-With)
- **Double Submit Cookies**: Send token in both cookie and request parameter
- **Re-authentication**: Require password for sensitive operations

### 3. SQL Injection

**SQL Injection** allows attackers to manipulate database queries by injecting malicious SQL code.

**Vulnerable Code:**
```python
# VULNERABLE - Never do this!
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
db.execute(query)
```

**Attack:**
```
Username: admin' OR '1'='1' --
Password: anything

Resulting query:
SELECT * FROM users WHERE username='admin' OR '1'='1' --' AND password='anything'
                                         ↑ Always true     ↑ Comment out rest
```

**Prevention:**
- **Parameterized Queries (Prepared Statements):**
  ```python
  # SECURE
  query = "SELECT * FROM users WHERE username=? AND password=?"
  db.execute(query, (username, password))
  ```
- **ORM Frameworks**: Use ORMs that automatically parameterize queries
- **Stored Procedures**: Encapsulate SQL logic (still need parameterization)
- **Input Validation**: Whitelist allowed characters
- **Least Privilege**: Database user should have minimal permissions
- **WAF (Web Application Firewall)**: Detect and block SQL injection attempts

For detailed SQL injection prevention, see [Database Security](06-Database-Security.md).

### 4. Insecure Deserialization

Exploiting flaws in how applications deserialize (unpack) untrusted data.

**Impact:**
- Remote code execution
- Replay attacks
- Injection attacks
- Privilege escalation

**Prevention:**
- Avoid deserializing untrusted data
- Use data formats that don't support object types (JSON without complex types)
- Implement integrity checks (digital signatures, HMACs)
- Restrict deserialization to specific classes
- Monitor deserialization exceptions

### 5. XML External Entity (XXE) Attacks

Exploiting XML parsers that process external entity references.

**Vulnerable XML:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user><name>&xxe;</name></user>
```

**Prevention:**
- Disable XML external entity processing
- Use less complex data formats (JSON)
- Update XML parsers
- Input validation

### 6. Server-Side Request Forgery (SSRF)

Web application fetches remote resources without validating user-supplied URLs.

**Attack:**
```
Request: GET /fetch?url=http://169.254.169.254/latest/meta-data/
Server fetches internal AWS metadata (credentials, keys)
```

**Prevention:**
- Whitelist allowed domains/IPs
- Validate and sanitize URLs
- Disable unnecessary URL schemas (file://, gopher://)
- Network segmentation
- Use authentication for internal services

## API Security

APIs (Application Programming Interfaces) are critical components of modern web applications but present unique security challenges.

### API Authentication Methods

| Method | Security Level | Use Case | Notes |
|--------|---------------|----------|-------|
| **API Keys** | Low-Medium | Public APIs, rate limiting | Simple but easily leaked |
| **Basic Auth** | Low | Legacy systems | Base64-encoded, not encrypted (use with HTTPS) |
| **OAuth 2.0** | High | Third-party access, delegated auth | Industry standard (see [02-Access-Control](02-Access-Control-and-Authentication.md#oauth-20)) |
| **JWT** | Medium-High | Stateless APIs, microservices | Self-contained tokens (see [02-Access-Control](02-Access-Control-and-Authentication.md#openid-connect-oidc)) |
| **mTLS** | Very High | Service-to-service | Mutual certificate authentication |

### Web-Specific Token Security

When using OAuth 2.0 and JWT in web applications, additional considerations apply:

**Token Storage in Browsers:**

| Storage Method | XSS Vulnerable | CSRF Vulnerable | Notes |
|----------------|----------------|-----------------|-------|
| **localStorage** | Yes | No | Accessible via JavaScript, survives page reload |
| **sessionStorage** | Yes | No | Accessible via JavaScript, cleared on tab close |
| **Cookies (HttpOnly)** | No | Yes | Not accessible via JavaScript, needs CSRF protection |
| **In-memory** | No | No | Lost on page reload, best security |

**Recommendation:**
- **Access tokens**: Store in-memory or HttpOnly cookies with SameSite attribute
- **Refresh tokens**: HttpOnly, Secure, SameSite=Strict cookies only
- **Never** store tokens in localStorage for sensitive applications

**OAuth 2.0 for Single-Page Applications (SPAs):**
- Use **Authorization Code Flow with PKCE** (Proof Key for Code Exchange)
- Avoid Implicit Flow (deprecated due to token leakage risks)
- Short-lived access tokens (5-15 minutes)
- Refresh tokens stored securely

For comprehensive OAuth 2.0 details, see [02-Access-Control-and-Authentication](02-Access-Control-and-Authentication.md#oauth-20).

### API Security Best Practices

1. **Rate Limiting**: Prevent abuse and DoS attacks
2. **Input Validation**: Validate all input parameters
3. **Output Encoding**: Encode responses to prevent injection
4. **Authentication Required**: Require authentication for all non-public endpoints
5. **HTTPS Only**: Enforce TLS for all API traffic
6. **Versioning**: API versioning for backward compatibility and security updates
7. **Error Handling**: Don't leak sensitive information in error messages
8. **CORS Configuration**: Properly configure Cross-Origin Resource Sharing

## Session Management

**Session management** secures the interaction between user and application after authentication.

### Session Lifecycle

```
1. User authenticates
2. Server creates session
3. Server sends session ID to client (cookie)
4. Client includes session ID in subsequent requests
5. Server validates session ID
6. Session expires (timeout or logout)
7. Session destroyed
```

### Session Security Best Practices

**Secure Session Cookies:**
```
Set-Cookie: sessionid=abc123xyz;
  Secure;              ← Only sent over HTTPS
  HttpOnly;            ← Not accessible via JavaScript
  SameSite=Strict;     ← CSRF protection
  Path=/;              ← Cookie scope
  Max-Age=3600;        ← Expiration (1 hour)
  Domain=example.com   ← Domain restriction
```

**Session Fixation Prevention:**
- Regenerate session ID after successful login
- Invalidate old session ID
- Don't accept session IDs from URL parameters

**Session Hijacking Prevention:**
- Use HTTPS exclusively
- Bind sessions to IP address (careful with mobile users)
- User-Agent validation
- Implement session timeout (idle and absolute)
- Multi-factor authentication for sensitive operations

**Session Timeout Strategy:**
- **Idle timeout**: 15-30 minutes of inactivity
- **Absolute timeout**: 8-12 hours maximum
- **Extend on activity**: Reset idle timeout on user action
- **Warn before expiration**: Give user chance to extend session

## Web Authentication Considerations

While comprehensive authentication is covered in [02-Access-Control-and-Authentication](02-Access-Control-and-Authentication.md), web applications have specific considerations:

### Browser-Based Authentication Challenges

1. **Credential Storage**: Browsers store passwords (encrypted, but target for malware)
2. **Password Managers**: Vary in security, some vulnerable to extraction
3. **Autocomplete**: Convenience vs. security on shared computers
4. **Browser Extensions**: Can intercept credentials
5. **Bookmarked URLs**: May contain session tokens

### Login Security Best Practices

**Secure Login Form:**
```html
<form action="/login" method="POST" autocomplete="off">
  <input type="text" name="username" autocomplete="username">
  <input type="password" name="password" autocomplete="current-password">
  <input type="hidden" name="csrf_token" value="...">
  <button type="submit">Log In</button>
</form>
```

**Login Protection Mechanisms:**
- **Rate limiting**: Limit login attempts per IP/username
- **Account lockout**: Temporarily lock after N failed attempts
- **CAPTCHA**: After several failed attempts
- **Notification**: Email user about failed login attempts
- **MFA**: Require second factor for sensitive accounts
- **Passwordless**: Consider WebAuthn/FIDO2 for high-security scenarios

**Account Recovery Security:**
- Don't reveal whether email exists in system
- Time-limited password reset tokens (15-30 minutes)
- One-time use tokens
- Invalidate all sessions on password change
- Require old password for password change
- Notify user of password changes via email

## HTTPS and Transport Security

### Why HTTPS Matters for Web Applications

HTTPS provides:
- **Confidentiality**: Encryption prevents eavesdropping
- **Integrity**: Prevents tampering with data in transit
- **Authentication**: Verifies server identity

**HTTPS Everywhere:**
- All pages should use HTTPS, not just login/checkout
- Mixed content (HTTPS page loading HTTP resources) degrades security
- HTTP Strict Transport Security (HSTS) enforces HTTPS

### HTTPS Downgrade Attacks

**SSL Stripping Attack:**
```
1. User on public WiFi types "http://bank.com"
2. Attacker intercepts, proxies connection
3. Attacker maintains HTTPS to bank.com (user sees HTTP)
4. User enters credentials over unencrypted HTTP
5. Attacker captures credentials
```

**Prevention:**
- **HSTS Header**: Force browser to always use HTTPS
  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  ```
- **HSTS Preload List**: Browsers have built-in list of HSTS sites
- **Always redirect**: HTTP → HTTPS (server-side)

For comprehensive TLS/SSL details, see [05-Network-Security](05-Network-Security.md#transport-layer-security-tlsssl).

## Content Security Policy

**Content Security Policy (CSP)** is a security mechanism that helps prevent XSS and data injection attacks by specifying trusted content sources.

### CSP Directives

```
Content-Security-Policy:
  default-src 'self';                    ← Default policy
  script-src 'self' https://apis.example.com;  ← Script sources
  style-src 'self' 'unsafe-inline';      ← CSS sources
  img-src 'self' data: https:;           ← Image sources
  connect-src 'self' https://api.example.com;  ← AJAX/WebSocket
  font-src 'self';                       ← Font sources
  object-src 'none';                     ← Plugins (Flash, etc.)
  base-uri 'self';                       ← <base> tag
  form-action 'self';                    ← Form submission
  frame-ancestors 'none';                ← Embedding in frames
```

### CSP Implementation Strategy

**Level 1: Report Only**
```
Content-Security-Policy-Report-Only: default-src 'self';
  report-uri /csp-violation-report
```
- Monitor violations without breaking functionality
- Analyze reports to refine policy

**Level 2: Enforce**
```
Content-Security-Policy: default-src 'self';
  script-src 'self' 'nonce-abc123';
```
- Enforce policy after testing
- Use nonces for inline scripts

**Level 3: Strict Policy**
```
Content-Security-Policy:
  default-src 'none';
  script-src 'nonce-random123';
  style-src 'nonce-random456';
  connect-src 'self';
  img-src 'self' https:;
```

### CSP Nonces

Nonces (number used once) allow specific inline scripts while blocking others:

```html
<!-- Server generates random nonce per request -->
<script nonce="randomvalue123">
  // This inline script is allowed
  console.log("Trusted script");
</script>

<script>
  // This script is blocked (no nonce)
  console.log("Blocked script");
</script>
```

## Web Security Headers

Security headers instruct browsers to enable built-in security features.

### Essential Security Headers

| Header | Purpose | Example |
|--------|---------|---------|
| **Strict-Transport-Security** | Force HTTPS | `max-age=31536000; includeSubDomains` |
| **Content-Security-Policy** | Prevent XSS, injection | `default-src 'self'; script-src 'self'` |
| **X-Content-Type-Options** | Prevent MIME sniffing | `nosniff` |
| **X-Frame-Options** | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| **X-XSS-Protection** | Enable browser XSS filter | `1; mode=block` (legacy) |
| **Referrer-Policy** | Control referrer information | `strict-origin-when-cross-origin` |
| **Permissions-Policy** | Control browser features | `geolocation=(), microphone=()` |

### Clickjacking Prevention

**Clickjacking** tricks users into clicking hidden elements.

**Attack:**
```html
<!-- Attacker's page -->
<iframe src="https://bank.com/transfer" style="opacity:0; position:absolute; top:0; left:0;"></iframe>
<button style="position:absolute; top:100px; left:100px;">
  Click to win prize!
</button>
<!-- User thinks they're clicking prize button, actually clicking bank transfer -->
```

**Prevention:**
```
X-Frame-Options: DENY                    ← Never allow framing
X-Frame-Options: SAMEORIGIN              ← Allow same-origin framing
Content-Security-Policy: frame-ancestors 'none'  ← CSP alternative
```

### Subresource Integrity (SRI)

Ensures external resources (scripts, stylesheets) haven't been tampered with.

```html
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
  crossorigin="anonymous">
</script>
```

If the file is modified, the browser refuses to execute it.

## Best Practices

### Secure Development Checklist

**Input Handling:**
- Validate all input (whitelist, not blacklist)
- Sanitize and encode output for context (HTML, JavaScript, URL, CSS)
- Use parameterized queries for database access
- Limit file upload sizes and types
- Validate file uploads (don't trust MIME type)

**Authentication & Authorization:**
- Use strong password policies
- Implement MFA for sensitive accounts
- Secure session management (HttpOnly, Secure, SameSite cookies)
- Regenerate session ID on login
- Implement proper access controls
- Check authorization on every request

**Data Protection:**
- Use HTTPS everywhere
- Implement HSTS
- Encrypt sensitive data at rest
- Use secure password hashing (Argon2, bcrypt)
- Don't log sensitive data (passwords, credit cards, PII)

**Security Headers:**
- Implement CSP
- Set X-Content-Type-Options: nosniff
- Set X-Frame-Options or CSP frame-ancestors
- Set Referrer-Policy
- Set Permissions-Policy

**Error Handling:**
- Don't expose stack traces to users
- Generic error messages for failed logins
- Log detailed errors server-side
- Implement proper exception handling

**Security Testing:**
- Automated security scans (SAST, DAST)
- Dependency scanning for vulnerable libraries
- Regular penetration testing
- Security code reviews
- Bug bounty program

### Security Tools

**Static Analysis (SAST):**
- SonarQube
- Checkmarx
- Veracode
- Semgrep

**Dynamic Analysis (DAST):**
- OWASP ZAP
- Burp Suite
- Acunetix
- Netsparker

**Dependency Scanning:**
- Snyk
- OWASP Dependency-Check
- npm audit / pip-audit
- GitHub Dependabot

**Web Application Firewall (WAF):**
- ModSecurity
- Cloudflare WAF
- AWS WAF
- Imperva
