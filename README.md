# 💰 What-if Pricing Scenario Simulation
### Modeling and Simulation | BSCS 601

A business simulation tool that models how different selling prices affect a
small retail store's revenue, profit, and profit margin. Built with 3 versions
for different interfaces.

## 📁 Project Structure
pricing-simulation/
├── v1/
│   └── simulation.py        ← Rich terminal UI with colored tables and charts
├── v2/
│   └── simulation.py        ← Tkinter GUI window with interactive charts
├── v3/
│   └── index.html           ← Browser-based app (no installation needed)
├── requirements.txt         ← Python libraries needed
└── README.md                ← You are here

## ⚙️ Requirements

- Python 3.8 or higher
- pip (comes with Python)
- A modern web browser (for Version 3)

> ⚠️ Note: Version 2 (Tkinter GUI) has a known rendering issue on Mac M1.
> It works perfectly on Windows. Version 1 and Version 3 work on both.

## 🛠️ Setup Instructions

### 🍎 Mac

**1. Open Terminal**
Press CMD + Space, type Terminal, hit Enter.

**2. Clone the project**
```bash
git clone https://github.com/YOUR_USERNAME/pricing-simulation.git
cd pricing-simulation
```

**3. Install libraries**
```bash
pip3 install -r requirements.txt
```

**4. Run the versions**
```bash
# Version 1 - Rich Terminal
python3 v1/simulation.py

# Version 2 - GUI (may not display correctly on Mac M1)
python3 v2/simulation.py

# Version 3 - Browser (just open the file)
open v3/index.html
```

### 🪟 Windows

**1. Install Python**
Go to https://python.org, download Python 3.
During installation, check ✅ "Add Python to PATH"

**2. Open Command Prompt**
Press Windows + R, type cmd, hit Enter.

**3. Clone the project**
```bash
git clone https://github.com/IzanagiIzumi/pricing-simulation.git
cd pricing-simulation
```

**4. Install libraries**
```bash
pip install -r requirements.txt
```

**5. Run the versions**
```bash
# Version 1 - Rich Terminal
python v1/simulation.py

# Version 2 - GUI Window (works best on Windows)
python v2/simulation.py

# Version 3 - Browser (just open the file)
start v3/index.html
```

## 🖥️ Version Descriptions

### Version 1 — Rich Terminal UI
- Runs in the terminal/command prompt
- Colorful tables and styled output using the Rich library
- Saves a chart image as simulation_results.png
- Works on both Mac and Windows

### Version 2 — Tkinter GUI Window
- Opens a desktop window with input fields
- Interactive table and embedded charts
- Best experienced on Windows
- Known rendering issue on Mac M1

### Version 3 — Browser App
- Opens directly in any web browser
- No Python needed — just open index.html
- Most visually polished version
- Works on all platforms


## 📊 How to Use the Simulation

1. Enter your **cost per unit** (how much it costs you to buy one item)
2. Enter the **number of units sold**
3. Enter your **fixed costs** (rent, electricity, salaries, etc.)
4. Enter **selling prices** for each scenario you want to test
5. Click or press **Run Simulation**
6. View the results table and charts showing profit, loss, and margins
