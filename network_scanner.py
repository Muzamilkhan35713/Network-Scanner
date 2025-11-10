#!/usr/bin/env python3
"""
Network Scanner - A Python CLI wrapper for nmap
This tool simplifies common nmap scanning tasks with easy-to-use commands.
"""

import argparse
import json
import subprocess
import sys
import re
from datetime import datetime
from typing import Dict, List, Optional


class NetworkScanner:
    """Main class for wrapping nmap functionality"""
    
    def __init__(self):
        self.scan_results = {}
        
    def check_nmap_installed(self) -> bool:
        """Check if nmap is installed on the system"""
        try:
            subprocess.run(['nmap', '--version'], 
                          capture_output=True, 
                          check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def run_scan(self, target: str, scan_type: str = 'basic', 
                 ports: Optional[str] = None, 
                 additional_flags: Optional[List[str]] = None) -> Dict:
        """
        Execute nmap scan with specified parameters
        
        Args:
            target: IP address, hostname, or network range to scan
            scan_type: Type of scan (basic, quick, stealth, aggressive, service)
            ports: Port specification (e.g., '80,443' or '1-1000')
            additional_flags: Additional nmap flags to include
        
        Returns:
            Dictionary containing scan results
        """
        # Build nmap command based on scan type
        cmd = ['nmap']
        
        scan_profiles = {
            'basic': [],
            'quick': ['-F'],  # Fast scan (top 100 ports)
            'stealth': ['-sS'],  # SYN stealth scan
            'aggressive': ['-A'],  # OS detection, version detection, script scanning
            'service': ['-sV'],  # Service/version detection
            'ping': ['-sn'],  # Ping scan (no port scan)
        }
        
        if scan_type in scan_profiles:
            cmd.extend(scan_profiles[scan_type])
        
        # Add port specification
        if ports:
            cmd.extend(['-p', ports])
        
        # Add additional flags if provided
        if additional_flags:
            cmd.extend(additional_flags)
        
        # Add target
        cmd.append(target)
        
        print(f"[*] Executing: {' '.join(cmd)}")
        print(f"[*] Scanning {target}...")
        
        try:
            # Run nmap command
            result = subprocess.run(cmd, 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=300)
            
            if result.returncode != 0:
                print(f"[!] Warning: nmap returned exit code {result.returncode}")
            
            # Parse the output
            parsed_results = self.parse_nmap_output(result.stdout, target)
            parsed_results['raw_output'] = result.stdout
            parsed_results['command'] = ' '.join(cmd)
            parsed_results['scan_time'] = datetime.now().isoformat()
            
            self.scan_results = parsed_results
            return parsed_results
            
        except subprocess.TimeoutExpired:
            error_msg = "Scan timed out after 300 seconds"
            print(f"[!] {error_msg}")
            return {'error': error_msg, 'target': target}
        except Exception as e:
            error_msg = f"Error executing scan: {str(e)}"
            print(f"[!] {error_msg}")
            return {'error': error_msg, 'target': target}
    
    def parse_nmap_output(self, output: str, target: str) -> Dict:
        """
        Parse nmap output and extract useful information
        
        Args:
            output: Raw nmap output string
            target: Target that was scanned
        
        Returns:
            Dictionary with parsed results
        """
        results = {
            'target': target,
            'status': 'unknown',
            'open_ports': [],
            'closed_ports': 0,
            'filtered_ports': 0,
            'host_info': {},
        }
        
        # Check if host is up
        if 'Host is up' in output:
            results['status'] = 'up'
        elif 'host down' in output.lower():
            results['status'] = 'down'
        
        # Extract open ports
        port_pattern = r'(\d+)/(tcp|udp)\s+(open|closed|filtered)\s+(\S+)?'
        for match in re.finditer(port_pattern, output):
            port_num = match.group(1)
            protocol = match.group(2)
            state = match.group(3)
            service = match.group(4) if match.group(4) else 'unknown'
            
            if state == 'open':
                results['open_ports'].append({
                    'port': port_num,
                    'protocol': protocol,
                    'service': service,
                    'state': state
                })
            elif state == 'closed':
                results['closed_ports'] += 1
            elif state == 'filtered':
                results['filtered_ports'] += 1
        
        # Extract OS information if available
        os_match = re.search(r'OS details: (.+?)(?:\n|$)', output)
        if os_match:
            results['host_info']['os'] = os_match.group(1).strip()
        
        # Extract MAC address if available
        mac_match = re.search(r'MAC Address: ([0-9A-F:]+) \((.+?)\)', output)
        if mac_match:
            results['host_info']['mac_address'] = mac_match.group(1)
            results['host_info']['vendor'] = mac_match.group(2)
        
        # Extract latency
        latency_match = re.search(r'Host is up \((.+?)s latency\)', output)
        if latency_match:
            results['host_info']['latency'] = latency_match.group(1)
        
        return results
    
    def display_results(self, results: Dict):
        """Display scan results in a human-readable format"""
        print("\n" + "="*60)
        print("SCAN RESULTS")
        print("="*60)
        
        if 'error' in results:
            print(f"[!] Error: {results['error']}")
            return
        
        print(f"\nTarget: {results.get('target', 'N/A')}")
        print(f"Status: {results.get('status', 'unknown')}")
        print(f"Scan Time: {results.get('scan_time', 'N/A')}")
        
        if results.get('host_info'):
            print("\nHost Information:")
            for key, value in results['host_info'].items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        open_ports = results.get('open_ports', [])
        if open_ports:
            print(f"\nOpen Ports ({len(open_ports)}):")
            print(f"{'PORT':<10} {'PROTOCOL':<12} {'SERVICE':<20}")
            print("-" * 42)
            for port in open_ports:
                print(f"{port['port']:<10} {port['protocol']:<12} {port['service']:<20}")
        else:
            print("\nNo open ports found.")
        
        if results.get('closed_ports', 0) > 0:
            print(f"\nClosed Ports: {results['closed_ports']}")
        
        if results.get('filtered_ports', 0) > 0:
            print(f"Filtered Ports: {results['filtered_ports']}")
        
        print("\n" + "="*60)
    
    def save_results(self, filename: str, format: str = 'json'):
        """
        Save scan results to a file
        
        Args:
            filename: Output filename
            format: Output format ('json' or 'txt')
        """
        if not self.scan_results:
            print("[!] No scan results to save")
            return
        
        try:
            if format == 'json':
                with open(filename, 'w') as f:
                    json.dump(self.scan_results, f, indent=2)
                print(f"[+] Results saved to {filename} (JSON format)")
            
            elif format == 'txt':
                with open(filename, 'w') as f:
                    f.write("="*60 + "\n")
                    f.write("NETWORK SCAN RESULTS\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Target: {self.scan_results.get('target', 'N/A')}\n")
                    f.write(f"Status: {self.scan_results.get('status', 'unknown')}\n")
                    f.write(f"Scan Time: {self.scan_results.get('scan_time', 'N/A')}\n")
                    f.write(f"Command: {self.scan_results.get('command', 'N/A')}\n\n")
                    
                    if self.scan_results.get('host_info'):
                        f.write("Host Information:\n")
                        for key, value in self.scan_results['host_info'].items():
                            f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
                        f.write("\n")
                    
                    open_ports = self.scan_results.get('open_ports', [])
                    if open_ports:
                        f.write(f"Open Ports ({len(open_ports)}):\n")
                        f.write(f"{'PORT':<10} {'PROTOCOL':<12} {'SERVICE':<20}\n")
                        f.write("-" * 42 + "\n")
                        for port in open_ports:
                            f.write(f"{port['port']:<10} {port['protocol']:<12} {port['service']:<20}\n")
                    
                    f.write("\n" + "="*60 + "\n")
                    f.write("RAW NMAP OUTPUT\n")
                    f.write("="*60 + "\n")
                    f.write(self.scan_results.get('raw_output', ''))
                
                print(f"[+] Results saved to {filename} (TXT format)")
            
        except Exception as e:
            print(f"[!] Error saving results: {str(e)}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Network Scanner - A Python CLI wrapper for nmap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic scan:
    %(prog)s 192.168.1.1
  
  Quick scan (top 100 ports):
    %(prog)s 192.168.1.1 -t quick
  
  Service detection on specific ports:
    %(prog)s 192.168.1.1 -t service -p 80,443
  
  Save results to file:
    %(prog)s 192.168.1.1 -o results.json
  
  Aggressive scan with text output:
    %(prog)s 192.168.1.1 -t aggressive -o results.txt -f txt
        """)
    
    parser.add_argument('target', 
                       help='Target IP address, hostname, or network range (e.g., 192.168.1.1 or 192.168.1.0/24)')
    
    parser.add_argument('-t', '--type', 
                       choices=['basic', 'quick', 'stealth', 'aggressive', 'service', 'ping'],
                       default='basic',
                       help='Type of scan to perform (default: basic)')
    
    parser.add_argument('-p', '--ports',
                       help='Ports to scan (e.g., "80,443" or "1-1000")')
    
    parser.add_argument('-o', '--output',
                       help='Output filename to save results')
    
    parser.add_argument('-f', '--format',
                       choices=['json', 'txt'],
                       default='json',
                       help='Output file format (default: json)')
    
    parser.add_argument('--flags',
                       nargs='+',
                       help='Additional nmap flags (e.g., --flags -v -T4)')
    
    args = parser.parse_args()
    
    # Create scanner instance
    scanner = NetworkScanner()
    
    # Check if nmap is installed
    if not scanner.check_nmap_installed():
        print("[!] Error: nmap is not installed or not found in PATH")
        print("[*] Please install nmap:")
        print("    - Ubuntu/Debian: sudo apt-get install nmap")
        print("    - macOS: brew install nmap")
        print("    - Windows: Download from https://nmap.org/download.html")
        sys.exit(1)
    
    # Run the scan
    results = scanner.run_scan(
        target=args.target,
        scan_type=args.type,
        ports=args.ports,
        additional_flags=args.flags
    )
    
    # Display results
    scanner.display_results(results)
    
    # Save results if output file specified
    if args.output:
        scanner.save_results(args.output, args.format)
    
    print("\n[+] Scan complete!")


if __name__ == '__main__':
    main()
