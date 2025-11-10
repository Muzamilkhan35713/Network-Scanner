
# 🛡️ Simple Nmap Wrapper — Python CLI Tool

This is a Python-based command-line interface (CLI) that wraps around the powerful `nmap` network scanner. It simplifies common scanning tasks and adds basic parsing and output-saving features, making it easier for beginners and professionals to run scans and interpret results.

---

## 🔍 Features

- Ping sweep to find live hosts (`nmap -sn`)
- OS detection (`nmap -O`)
- Full TCP port scan (`nmap -p-`)
- SYN scan (`nmap -sS`, requires root on Unix)
- Skip host discovery (`nmap -Pn`)
- Custom flag input for advanced scans
- Option to save raw output to a file
- Simple parsing of live hosts and open ports

---

## ⚙️ Requirements

- Python 3.x
- `nmap` must be installed and available in your system's PATH

---

## 🚀 How to Run (Python Version)

```bash
python3 nmap_wrapper.py
```

Choose an option from the menu and follow the prompts.

> ⚠️ Use responsibly: Only scan machines you own or have permission to test.

---

## 📦 Windows Executable (.exe)

If you don’t have Python installed, you can download and run the `.exe` version:

### 🔗 [Download the `.exe` from the Releases section](https://github.com/your-username/your-repo-name/releases)

- No need to install Python
- Just double-click to run
- Works on Windows

> If the `.exe` is blocked by GitHub, it will be available as a `.zip` file in the Releases tab.

---

## 🧰 How to Build `.exe` Yourself

```bash
pip install pyinstaller
pyinstaller --onefile nmap_wrapper.py
```

The `.exe` will be in the `dist/` folder.

---

## 📄 License

This project is open-source and available under the MIT License.

```

---

### ✅ How to Add the `.exe` for Download

1. Go to your GitHub repo.
2. Click **"Releases"** → **"Draft a new release"**.
3. Add a version tag like `v1.0`.
4. Upload your `.exe` file (or zip it first if GitHub blocks `.exe`).
5. Add a short description and click **"Publish release"**.

Your `.exe` will now be downloadable from the **Releases** section.

---

Let me know if you want help writing a changelog or adding screenshots to your README!
