import dns.message
import dns.query
import dns.rdatatype
import dns.resolver
import time

# readme me response ka struct explain karo

# Root DNS servers used to start the iterative resolution process
ROOT_SERVERS = {
    "198.41.0.4": "Root (a.root-servers.net)",
    "199.9.14.201": "Root (b.root-servers.net)",
    "192.33.4.12": "Root (c.root-servers.net)",
    "199.7.91.13": "Root (d.root-servers.net)",
    "192.203.230.10": "Root (e.root-servers.net)"
}

TIMEOUT = 3  # Timeout in seconds for each DNS query attempt

def send_dns_query(server, domain):
    """ 
    Sends a DNS query to the given server for an A record of the specified domain.
    Returns the response if successful, otherwise returns None.
    """
    try:
        query = dns.message.make_query(domain, dns.rdatatype.A)  # Construct the DNS query
        # TODO: Send the query using UDP 
        # Note that above TODO can be just a return statement with the UDP query!
        response = dns.query.udp(query, server, timeout=TIMEOUT) # Send the query using UDP
        return response  # Return the DNS response
    
    except Exception:
        return None  # If an error occurs (timeout, unreachable server, etc.), return None

def extract_next_nameservers(response):
    """ 
    Extracts nameserver (NS) records from the authority section of the response.
    Then, resolves those NS names to IP addresses.
    Returns a list of IPs of the next authoritative nameservers.
    """
    ns_ips = []  # List to store resolved nameserver IPs
    ns_names = []  # List to store nameserver domain names

    # Loop through the authority section to extract NS records
    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.NS:
            for rr in rrset:
                ns_name = rr.to_text()
                ns_names.append(ns_name)  # Extract nameserver hostname
                print(f"Extracted NS hostname: {ns_name}")

    # TODO: Resolve the extracted NS hostnames to IP addresses
    # To TODO, you would have to write a similar loop as above
    for ns_name in ns_names:
        try:
            answers = dns.resolver.resolve(ns_name, 'A')  # Query for A record (IPv4)
            ns_ips.extend([ip.address for ip in answers])  # Store all resolved IPs
            print(f"Resolved {ns_name} to {ns_ips[-1]}")   # printing the last IP address
        except Exception as e:
            print(f"Error resolving NS {ns_name}: {e}")

    return ns_ips  # Return list of resolved nameserver IPs

def iterative_dns_lookup(domain):
    """ 
    Performs an iterative DNS resolution starting from root servers.
    It queries root servers, then TLD servers, then authoritative servers,
    following the hierarchy until an answer is found or resolution fails.
    """
    print(f"[Iterative DNS Lookup] Resolving {domain}")

    next_ns_list = list(ROOT_SERVERS.keys())  # Start with the root server IPs
    stage = "ROOT"  # Track resolution stage (ROOT, TLD, AUTH)

    while next_ns_list:
        ns_ip = next_ns_list[0]  # Pick the first available nameserver to query
        response = send_dns_query(ns_ip, domain)

        if response: #checks if response is not NONE
            print(f"[DEBUG] Querying {stage} server ({ns_ip}) - SUCCESS")
            
            # If an answer is found, print and return
            if response.answer:
                print(f"[SUCCESS] {domain} -> {response.answer[0][0]}")
                return
            
            # If no answer, extract the next set of nameservers
            next_ns_list_new = extract_next_nameservers(response)
            if(not next_ns_list_new): #query next nameserver in the list if the list extracted is empty
                next_ns_list.pop(0)
                print("[EMPTY_LIST] Moving to the next nameserver in the list")
                continue
            # TODO: Move to the next resolution stage, i.e., it is either TLD, ROOT, or AUTH
            next_ns_list=next_ns_list_new #updating the list of nameservers if non-empty and moving to next stage
            if(stage=="ROOT"):
                stage="TLD"
            elif(stage=="TLD"):
                stage="AUTH"
            
        else:
            if(not next_ns_list):
                print(f"[ERROR] Query failed for {stage} {ns_ip}")
                return  # Stop resolution if a query fails
            next_ns_list.pop(0)  # Go to the next IP address in the list if the first query fails
            print("[ERROR] Moving to the next nameserver in the list")
    
    print("[ERROR] Resolution failed.")  # Final failure message if no nameservers respond with an non-empty list

def recursive_dns_lookup(domain):
    """ 
    Performs recursive DNS resolution using the system's default resolver.
    This approach relies on a resolver (like Google DNS or a local ISP resolver)
    to fetch the result recursively.
    """
    print(f"[Recursive DNS Lookup] Resolving {domain}")
    try:
        # TODO: Perform recursive resolution using the system's DNS resolver
        # Notice that the next line is looping through, therefore you should have something like answer = ??
        try:
            answer = dns.resolver.resolve(domain, "NS") # Getting the NS record recursively
            for rdata in answer:
                print(f"[SUCCESS] {domain} -> {rdata}")
        except Exception as e:
            pass

        answer = dns.resolver.resolve(domain, "A")
        for rdata in answer:
            print(f"[SUCCESS] {domain} -> {rdata}")
    except Exception as e:
        print(f"[ERROR] Recursive lookup failed: {e}")  # Handle resolution failure

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3 or sys.argv[1] not in {"iterative", "recursive"}:
        print("Usage: python3 dns_server.py <iterative|recursive> <domain>")
        sys.exit(1)

    mode = sys.argv[1]  # Get mode (iterative or recursive)
    domain = sys.argv[2]  # Get domain to resolve
    start_time = time.time()  # Record start time
    
    # Execute the selected DNS resolution mode
    if mode == "iterative":
        iterative_dns_lookup(domain)
    else:
        recursive_dns_lookup(domain)
    
    print(f"Time taken: {time.time() - start_time:.3f} seconds")  # Print execution time
        