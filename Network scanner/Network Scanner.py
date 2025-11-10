#!/usr/bin/env python3
import subprocess
import shutil
import os
import sys
import shlex
import re

def check_nmap():
    if shutil.which("nmap") is None:
        print("Error: nmap is not installed or not in PATH.")
        sys.exit(1)

def is_root_unix():
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Windows: no geteuid
        return False

def run_and_print(cmd, save_file=None):
    """
    Run subprocess.run with text output, print the CompletedProcess object,
    and also print stdout/stderr for readability (similar to your style).
    Optionally save raw stdout to save_file.
    """
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("Error: command not found:", cmd[0])
        return None

    # Print CompletedProcess-like object (so it looks like your original print(re))
    print(proc)

    # Also print readable output
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    print("=== STDOUT ===")
    print(stdout or "<no stdout>")
    print("=== STDERR ===")
    print(stderr or "<no stderr>")
    print("Return code:", proc.returncode)

    if save_file and stdout:
        try:
            with open(save_file, "w", encoding="utf-8") as f:
                f.write(stdout + "\n")
            print(f"Saved stdout to {save_file}")
        except Exception as e:
            print("Failed to save output:", e)

    return proc

def extract_live_hosts_from_nmap_sn(output):
    """
    Parse nmap -sn output to get live IPs.
    Example line:
      Nmap scan report for 192.168.1.1
      Host is up (0.0010s latency).
    """
    hosts = []
    for line in output.splitlines():
        m = re.search(r"Nmap scan report for ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", line)
        if m:
            hosts.append(m.group(1))
    return hosts

def extract_open_ports_simple(output):
    """
    Very simple parsing to show open ports from nmap normal output.
    It looks for lines like:
      PORT     STATE SERVICE
      22/tcp   open  ssh
    This is a heuristic and won't cover every nmap output format.
    """
    open_ports = {}
    lines = output.splitlines()
    port_section = False
    for line in lines:
        if re.match(r"PORT\s+STATE\s+SERVICE", line):
            port_section = True
            continue
        if port_section:
            if line.strip() == "" or line.startswith("Nmap done:"):
                port_section = False
                continue
            m = re.match(r"\s*([0-9]+)/(tcp|udp)\s+(\S+)\s+(.+)", line)
            if m:
                port = m.group(1)
                proto = m.group(2)
                state = m.group(3)
                svc = m.group(4).strip()
                if state.lower() == "open":
                    # attempt to find the host from prior context: search backwards for "Nmap scan report for"
                    host = "<unknown>"
                    idx = lines.index(line)
                    for b in range(idx-1, max(-1, idx-10), -1):
                        mh = re.search(r"Nmap scan report for ([^\s]+)", lines[b])
                        if mh:
                            host = mh.group(1)
                            break
                    open_ports.setdefault(host, []).append(f"{port}/{proto} {svc}")
    return open_ports

def ask_save_filename():
    save = input("Save raw nmap stdout to file? [y/N]: ").strip().lower()
    if save == "y":
        fname = input("Enter filename (e.g. results.txt): ").strip()
        return fname or None
    return None

def menu_once():
    print()
    print("1. Find the host (ping sweep)")
    print("2. Find the OS (OS detection)")
    print("3. Find open ports (scan all TCP ports)")
    print("4. SYN scan (requires root on Unix)")
    print("5. Scan with -Pn (skip host discovery)")
    print("6. Custom flags (enter full nmap flags)")
    print("7. Exit")
    print()
    choice = input("Choose the option (1-7): ").strip()
    return choice

def main():
    check_nmap()
    print("Simple Nmap wrapper — use responsibly. (Only scan machines you own or have permission to test.)")

    try:
        while True:
            choice = menu_once()

            if choice == "1":
                target = input("Enter the target (IP, CIDR or hostname), e.g. 192.168.1.0/24: ").strip()
                cmd = ["nmap", "-sn", target]
                save = ask_save_filename()
                proc = run_and_print(cmd, save_file=save)
                if proc and proc.stdout:
                    hosts = extract_live_hosts_from_nmap_sn(proc.stdout)
                    print("Live hosts found:", ", ".join(hosts) if hosts else "<none>")

            elif choice == "2":
                target = input("Enter the target IP/host: ").strip()
                cmd = ["nmap", "-O", target]
                save = ask_save_filename()
                run_and_print(cmd, save_file=save)

            elif choice == "3":
                target = input("Enter the target IP/host: ").strip()
                cmd = ["nmap", "-p-", target]
                save = ask_save_filename()
                proc = run_and_print(cmd, save_file=save)
                if proc and proc.stdout:
                    open_ports = extract_open_ports_simple(proc.stdout)
                    if open_ports:
                        print("Open ports (simple parse):")
                        for host, ports in open_ports.items():
                            print(f"  {host}: {', '.join(ports)}")
                    else:
                        print("No open ports found by simple parser or parser could not detect format.")

            elif choice == "4":
                target = input("Enter the target IP/host: ").strip()
                if os.name != "nt" and not is_root_unix():
                    print("Warning: -sS (SYN scan) usually requires root privileges on Unix.")
                    yn = input("Continue anyway (you may get permission errors)? [y/N]: ").strip().lower()
                    if yn != "y":
                        print("Aborting SYN scan.")
                        continue
                cmd = ["nmap", "-sS", target]
                save = ask_save_filename()
                run_and_print(cmd, save_file=save)

            elif choice == "5":
                target = input("Enter the target IP/host: ").strip()
                extra = input("Additional flags to combine with -Pn? (e.g. -p 22,80) or press Enter: ").strip()
                cmd = ["nmap", "-Pn"]
                if extra:
                    cmd.extend(shlex.split(extra))
                cmd.append(target)
                save = ask_save_filename()
                run_and_print(cmd, save_file=save)

            elif choice == "6":
                target = input("Enter the target IP/host (or range/CIDR): ").strip()
                flags = input("Enter the full nmap flags exactly as you would on the command line (e.g. -sS -Pn -p 1-1024): ").strip()
                cmd = ["nmap"]
                if flags:
                    cmd.extend(shlex.split(flags))
                cmd.append(target)
                save = ask_save_filename()
                proc = run_and_print(cmd, save_file=save)
                # try to show simple open ports if a port scan was included
                if proc and proc.stdout and ("-p" in (flags or "") or "-p-" in (flags or "")):
                    open_ports = extract_open_ports_simple(proc.stdout)
                    if open_ports:
                        print("Open ports (simple parse):")
                        for host, ports in open_ports.items():
                            print(f"  {host}: {', '.join(ports)}")

            elif choice == "7":
                print("Exiting. Goodbye.")
                break

            else:
                print("Invalid choice. Please choose 1-7.")

    except KeyboardInterrupt:
        print("\nUser interrupted. Exiting.")
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
