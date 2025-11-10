# Network-Scanner

This is a Python-based command-line interface (CLI) that wraps around the powerful nmap network scanner. It simplifies common scanning tasks and adds basic parsing and output-saving features, making it easier for beginners and professionals to run scans and interpret results.

## Features

- 🎯 **Simple CLI Interface**: Easy-to-use command-line interface for nmap
- 🔍 **Multiple Scan Types**: Support for basic, quick, stealth, aggressive, service, and ping scans
- 📊 **Smart Parsing**: Automatically parses nmap output to extract useful information
- 💾 **Save Results**: Export scan results in JSON or TXT format
- 🚀 **Fast & Efficient**: Wraps nmap directly for optimal performance
- 📝 **Detailed Output**: Displays open ports, services, host information, and more

## Prerequisites

- Python 3.6 or higher
- nmap installed on your system

### Installing nmap

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install nmap
```

**macOS:**
```bash
brew install nmap
```

**Windows:**
Download and install from [https://nmap.org/download.html](https://nmap.org/download.html)

## Installation

### Option 1: Direct Usage
Simply download and run the script:
```bash
chmod +x network_scanner.py
./network_scanner.py <target>
```

### Option 2: Install as Package
```bash
pip install -e .
network-scanner <target>
```

## Usage

### Basic Scan
Scan a single host with default settings:
```bash
python3 network_scanner.py 192.168.1.1
```

### Quick Scan (Top 100 Ports)
Fast scan of the most common ports:
```bash
python3 network_scanner.py 192.168.1.1 -t quick
```

### Service Detection
Detect services and versions on specific ports:
```bash
python3 network_scanner.py 192.168.1.1 -t service -p 80,443,8080
```

### Stealth Scan
Perform a SYN stealth scan:
```bash
python3 network_scanner.py 192.168.1.1 -t stealth
```

### Aggressive Scan
OS detection, version detection, and script scanning:
```bash
python3 network_scanner.py 192.168.1.1 -t aggressive
```

### Ping Scan (No Port Scan)
Check if hosts are alive without port scanning:
```bash
python3 network_scanner.py 192.168.1.0/24 -t ping
```

### Save Results
Save scan results to a file:
```bash
# Save as JSON (default)
python3 network_scanner.py 192.168.1.1 -o results.json

# Save as TXT
python3 network_scanner.py 192.168.1.1 -o results.txt -f txt
```

### Custom Port Range
Scan specific ports or port ranges:
```bash
python3 network_scanner.py 192.168.1.1 -p 1-1000
python3 network_scanner.py 192.168.1.1 -p 22,80,443,3306
```

### Additional nmap Flags
Pass additional nmap flags:
```bash
python3 network_scanner.py 192.168.1.1 --flags -v -T4
```

## Command-Line Options

```
positional arguments:
  target                Target IP address, hostname, or network range

optional arguments:
  -h, --help            Show help message and exit
  -t, --type {basic,quick,stealth,aggressive,service,ping}
                        Type of scan to perform (default: basic)
  -p, --ports PORTS     Ports to scan (e.g., "80,443" or "1-1000")
  -o, --output OUTPUT   Output filename to save results
  -f, --format {json,txt}
                        Output file format (default: json)
  --flags FLAGS [FLAGS ...]
                        Additional nmap flags
```

## Scan Types

| Type | Description | nmap Flags |
|------|-------------|------------|
| **basic** | Standard scan | (none) |
| **quick** | Fast scan of top 100 ports | `-F` |
| **stealth** | SYN stealth scan | `-sS` |
| **aggressive** | OS/version detection + scripts | `-A` |
| **service** | Service/version detection | `-sV` |
| **ping** | Ping scan only (no ports) | `-sn` |

## Output Format

### Console Output
The tool displays results in a clean, formatted table:
```
============================================================
SCAN RESULTS
============================================================

Target: 192.168.1.1
Status: up
Scan Time: 2025-11-10T06:15:00

Host Information:
  Latency: 0.0050
  Mac Address: AA:BB:CC:DD:EE:FF
  Vendor: Vendor Name

Open Ports (3):
PORT       PROTOCOL     SERVICE            
------------------------------------------
22         tcp          ssh                
80         tcp          http               
443        tcp          https              

============================================================
```

### JSON Output
Structured data format for programmatic use:
```json
{
  "target": "192.168.1.1",
  "status": "up",
  "open_ports": [
    {
      "port": "22",
      "protocol": "tcp",
      "service": "ssh",
      "state": "open"
    }
  ],
  "host_info": {
    "latency": "0.0050"
  },
  "scan_time": "2025-11-10T06:15:00",
  "command": "nmap 192.168.1.1"
}
```

## Examples

### Example 1: Basic Network Scan
```bash
python3 network_scanner.py 192.168.1.1
```

### Example 2: Scan Multiple Hosts
```bash
python3 network_scanner.py 192.168.1.0/24 -t quick
```

### Example 3: Web Server Analysis
```bash
python3 network_scanner.py example.com -t service -p 80,443,8080,8443 -o web_scan.json
```

### Example 4: Complete Security Audit
```bash
python3 network_scanner.py 192.168.1.1 -t aggressive -o security_audit.txt -f txt
```

## Security & Legal Notice

⚠️ **Important**: Only scan networks and systems you own or have explicit permission to scan. Unauthorized network scanning may be illegal in your jurisdiction.

This tool is for:
- ✅ Security auditing your own networks
- ✅ Penetration testing with authorization
- ✅ Educational purposes in controlled environments
- ✅ Network administration and troubleshooting

## Limitations

- Requires nmap to be installed on the system
- Some scan types require root/administrator privileges
- Scan timeout is set to 300 seconds (5 minutes)
- Stealth and aggressive scans may be detected by intrusion detection systems

## Troubleshooting

### "nmap is not installed"
Install nmap using your system's package manager (see Prerequisites section).

### Permission Denied
Some scan types (stealth, OS detection) require root privileges:
```bash
sudo python3 network_scanner.py 192.168.1.1 -t stealth
```

### Scan Times Out
For large networks or comprehensive scans, consider:
- Using `-t quick` for faster scans
- Scanning specific port ranges with `-p`
- Breaking large networks into smaller subnets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built on top of [nmap](https://nmap.org/) - the industry-standard network scanner
- Inspired by the need for simpler nmap interfaces
