# **CS425 Assignment: DNS Resolver (Iterative & Recursive)**

## **Team**

| **Name**          | **Roll Number**     | **Email**          |
| ----------------- | ------------------- | ------------------ |
| Wattamwar Akanksha Balaji      | 221214     | akankshab22@iitk.ac.in      |
| Mahaarajan J | 220600 | mahaarajan22@iitk.ac.in |

## **Instructions**

To run the DNS resolver, follow these steps:

1. Ensure you have Python 3 installed along with the `dnspython` library. If not installed, run:

```bash
pip install dnspython
```

2. Run the script with either iterative or recursive mode:

```bash
python3 dnsresolver.py <iterative|recursive> <domain>
```

For example:

```bash
python3 dnsresolver.py iterative google.com
python3 dnsresolver.py recursive google.com
```

## **Features**

### Implemented Features

- Supports both **iterative** and **recursive** DNS resolution.
- Iterative resolution:
  - Starts at root DNS servers.
  - If a valid response with non-empty list then move to the next stage, else cycle through the ip addresses in the list
  - Queries the next level of servers iteratively until an answer is found.
- Recursive resolution:
  - Uses the system's DNS resolver to fetch the hostnames and ip adresses directly.
- Completing helper functions:
  - Writing snippets to complete the sending of dns queries and extracting hostnames
- Proper error handling:
  - Handles timeout, unreachable servers, and NXDOMAIN(Domain does not exist) cases.
  - Prints appropriate debug messages for each step.

### Not Implemented Features

- Support for record types other than A and NS.
- Caching of previously resolved queries.

## **Assumptions and Conventions**

- Root DNS servers are predefined in the script.
- The resolver assumes IPv4 (A records) for domain resolution.
- If a nameserver does not respond or the list of ip addresses extracted from the response is empty, the resolver tries the next available one.
- The script prints success or error messages along with resolution steps.

<!-- ## **Design Decisions**

### Iterative Resolver Flow

- **Decision:** Uses root servers as the starting point.
- **Reason:** This mimics how a real-world DNS resolver works, moving from root to TLD to authoritative servers iteratively.

### Recursive Resolver Flow

- **Decision:** Uses Python’s `dns.resolver.resolve()`.
- **Reason:** This relies on system-configured resolvers like Google DNS or ISP resolvers to fetch results.

### Error Handling

- **Decision:** Added exception handling for timeouts, NXDOMAIN errors, and network issues.
- **Reason:** Ensures the script does not crash and provides meaningful error messages. -->

## **Implementation**

### Key Functions

- `send_dns_query(server, domain)`: Sends a DNS query to a given server and returns the response.
- `extract_next_nameservers(response)`: Extracts NS records and resolves them to IP addresses.
- `iterative_dns_lookup(domain)`: Implements the iterative resolution process, following the DNS hierarchy.
- `recursive_dns_lookup(domain)`: Uses the system’s resolver to perform recursive resolution.

### Code Flow

1. The script reads the mode (`iterative` or `recursive`) and the target domain.
2. If **iterative mode**:
   - Starts with root servers.
   - Queries each level iteratively until an answer is found.
3. If **recursive mode**:
   - Uses the system's DNS resolver to fetch the result directly.
4. Errors are handled at each step.

## **Testing**

### Correctness Testing

- Verified iterative resolution using various domains (e.g., `abc.defg`, `google.com`,`microsoft.com`).
- Checked error handling for invalid and unreachable domains.

<!-- ## **Challenges and Solutions**

### Handling Timeouts

- **Issue:** Some nameservers do not respond within the timeout limit.
- **Solution:** Implemented fallback to the next available nameserver.

### Extracting Nameserver IPs

- **Issue:** Some NS records lack A records in the additional section.
- **Solution:** Added a separate query step to resolve NS hostnames to IPs. -->

## **Individual Contributions**

### Task-1: Implementation of the iterative and recursive DNS resolution logic.
| **Name**      | **Contribution** |  
|--------------|----------------|  
| Akanksha     | 50%            |  
| Mahaarajan   | 50%            | 

### Task-2: Implementation of the 2 helper functions
| **Name**          | **Contribution** |
|------------------|----------------|
| Akanksha     | 60%            |
| Mahaarajan | 40%            |

### Task-3: Preparing README and commenting the code
| **Name**          | **Contribution** |
|------------------|----------------|
| Akanksha       | 40%            |
| Mahaarajan | 60%            |


## **Sources**

- `dnspython` library documentation.
- Lecture notes from CS425.
- Stack Overflow discussions on DNS query handling.

## **Declaration**

We hereby declare that our code is original and does not involve plagiarism. The assignment was completed following the academic integrity guidelines.

## **Feedback**

This assignment provided a great learning experience in understanding DNS resolution mechanisms!


