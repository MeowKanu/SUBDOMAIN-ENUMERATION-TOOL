# 🕵️‍♂️ Subdomain Enumeration Tool  
A fast and simple **Python-based multithreaded subdomain scanner** that checks for active subdomains using HTTP requests. This project is beginner-friendly and ideal for cybersecurity students, CEH learners, or anyone practicing information gathering & recon.

---

## 🚀 Features
- 🔍 Enumerates subdomains using HTTP GET requests  
- ⚡ Multithreaded (much faster than sequential scanning)  
- 📁 Reads subdomains from `subdomains.txt`  
- 📝 Saves results to `discovered_subdomains.txt`  
- 🧱 Simple, clean, and beginner-friendly Python code  
- ✔ Works on Windows, Linux, and macOS  

---

## 📂 Project Structure

```
SUBDOMAIN-ENUMERATION-TOOL/
│── enumeration_tool.py
│── subdomains.txt
│── discovered_subdomains.txt   (generated after running)
│── README.md
```

---

## 🖥 Requirements

Make sure you have:
- Python 3.x installed  
- `requests` library  
  ```
  pip install requests
  ```

---

## 🛠 How It Works

1. The tool reads a list of possible subdomains from `subdomains.txt`.  
2. Each subdomain is combined with the target domain, e.g.:
   ```
   api.microsoft.com
   mail.microsoft.com
   dev.microsoft.com
   ```
3. Each full URL is tested with an HTTP request.  
4. Valid (reachable) subdomains are printed and saved.  
5. Multithreading drastically increases speed.  

---

## ▶️ Usage

### 1. Add subdomains to `subdomains.txt`

Example:

```
www
mail
api
test
dev
admin
login
```

### 2. Run the script

```
python enumeration_tool.py
```

### 3. Output Example

```
Starting enumeration on: microsoft.com
Total subdomains to test: 20

[FOUND] http://www.microsoft.com
[FOUND] http://login.microsoft.com

Enumeration complete! Found 2 subdomains.
Saved results to discovered_subdomains.txt
```

---

## 📜 Code (enumeration_tool.py)

```python
import requests
import threading

domain = "microsoft.com"     
output_file = "discovered_subdomains.txt"
lock = threading.Lock()
discovered_subdomains = []

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

def main():
    try:
        with open("subdomains.txt") as f:
            subdomain_list = f.read().splitlines()
    except FileNotFoundError:
        print("subdomains.txt file missing!")
        return

    print(f"\nStarting enumeration on: {domain}")
    print(f"Total subdomains to test: {len(subdomain_list)}\n")

    threads = []

    for sub in subdomain_list:
        t = threading.Thread(target=check_subdomain, args=(sub,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

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
```

---

## 📘 Notes & Tips
- Some domains block or redirect HTTP requests — try HTTPS if needed.  
- Larger wordlists = more results but slower scan.  
- You can expand this tool to:
  - 🔹 Save status codes  
  - 🔹 Add color output  
  - 🔹 Use asynchronous requests  
  - 🔹 Scan ports  
  - 🔹 Support HTTPS  

---

## 🏁 Future Improvements (Optional)
- Add command-line arguments  
- Add progress bar  
- Add logging system  
- Add DNS resolution before HTTP requests  
- GUI version using Tkinter or PyQt  
- Export results in JSON format  

---

## 📜 License
This project is open-source and free to use for learning and ethical cybersecurity research.

---

## 👤 Author
**Kanak **   

🔗 *More projects coming soon!*  

---

# ⭐ If this project helped you…
Please give a **star ⭐ on GitHub** — it motivates me to build more tools!
