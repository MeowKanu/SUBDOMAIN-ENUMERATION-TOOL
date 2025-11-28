import requests
import threading

# ------------ CONFIGURATION --------------
domain = "microsoft.com"      # target domain
output_file = "discovered_subdomains.txt"
lock = threading.Lock()
discovered_subdomains = []

# ------------ SUBDOMAIN CHECKER ----------
def check_subdomain(subdomain):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 400:
            print(f"[FOUND] {url}")
            with lock:
                discovered_subdomains.append(url)
    except requests.ConnectionError:
        pass
    except requests.Timeout:
        pass

# ------------ MAIN PROGRAM ---------------
def main():
    # Load subdomains list
    try:
        with open("subdomains.txt") as f:
            subdomain_list = f.read().splitlines()
    except FileNotFoundError:
        print("subdomains.txt file missing!")
        return

    print(f"\nStarting enumeration on: {domain}")
    print(f"Total subdomains to test: {len(subdomain_list)}\n")

    threads = []

    # Create threads
    for sub in subdomain_list:
        t = threading.Thread(target=check_subdomain, args=(sub,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Save results
    if discovered_subdomains:
        with open(output_file, "w") as f:
            for sub in discovered_subdomains:
                f.write(sub + "\n")
        print(f"\nEnumeration complete! Found {len(discovered_subdomains)} subdomains.")
        print(f"Saved results to {output_file}")
    else:
        print("\nNo active subdomains found.")

if __name__ == "__main__":
    main()
