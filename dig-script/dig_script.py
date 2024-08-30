# Author: Prashant Singh

import sys
import os
import string
import csv
import dns.resolver

def banner():
    print("*****" * 20)

def write_host_file(domain_name, value):
    headers = ['Hostname', 'Dig Result']
    data = [[domain_name, value],]

    # Check output file's existence and set headers
    file_path = "dig_result.csv"
    file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0
    
    with open(file_path, 'a', newline='') as file:
        file = csv.writer(file)
        if not file_exists:
            file.writerow(headers)
        file.writerows(data)

def dig_domain_name(domain_name,dns_server):
    # Create a dns resolver instance and set nameserver
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_server]

    # DNS lookup operation below
    try:
        # DNS lookup for domain's CNAME record
        response = resolver.resolve(domain_name, 'CNAME')
        for cname in response:
            print(f"CNAME record for {domain_name} is: {cname}")
            write_host_file(domain_name, cname)
        banner()
    except dns.resolver.NoAnswer:
        print(f"No CNAME record found for {domain_name}")
        try:
            # If no CNAME found, DNS lookup for domain's A record
            response = resolver.resolve(domain_name, 'A')
            for ip in response:
                print(f"A record for {domain_name} is: {ip}")
                write_host_file(domain_name, ip)
            banner()
        except dns.resolver.NoAnswer:
            print(f"No A record found for {domain_name}")
            try:
                # If no CNAME found, DNS lookup for domain's A record
                response = resolver.resolve(domain_name, 'AAAA')
                for ip in response:
                    print(f"AAAA record for {domain_name} is: {ip}")
                    write_host_file(domain_name, ip)
                banner()
            except dns.resolver.NoAnswer:
                print(f"No A record found for {domain_name}")
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain_name} does not exist!")

def host_list(dns_server):
    # Read hostnames list from input file
    with open('dig_hosts.txt', 'r') as file:
        for domain_name in file:
            # From domain list avoid using any non-printable characters
            domain_name = ''.join(char for char in domain_name if char in string.printable and char not in string.whitespace)
            
            dig_domain_name(domain_name,dns_server)

def main():
    # Define Nameserver to used for dig operation
    dns_server = sys.argv[1]
    host_list(dns_server)

if __name__ == "__main__":
    main()