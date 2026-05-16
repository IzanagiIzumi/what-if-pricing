import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

BG       = "#1e1e2e"
SURFACE  = "#2a2a3e"
ACCENT   = "#7c3aed"
GREEN    = "#22c55e"
RED      = "#ef4444"
YELLOW   = "#facc15"
WHITE    = "#f1f5f9"
GRAY     = "#94a3b8"

class PricingSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What-if Pricing Scenario Simulation")
        self.configure(bg=BG)
        self.geometry("950x700")
        self.resizable(True, True)
        self.price_entries = []
        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="💰 What-if Pricing Scenario Simulation",
                 font=("Helvetica", 18, "bold"), bg=ACCENT, fg=WHITE).pack()
        tk.Label(header, text="Small Retail Store  •  IT2032 Modeling and Simulation  •  BSCS 601",
                 font=("Helvetica", 10), bg=ACCENT, fg="#d8b4fe").pack()

        # Scrollable main area
        canvas_frame = tk.Frame(self, bg=BG)
        canvas_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.scroll_canvas = tk.Canvas(canvas_frame, bg=BG,
                                       yscrollcommand=scrollbar.set,
                                       highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.scroll_canvas.yview)
        self.main = tk.Frame(self.scroll_canvas, bg=BG)
        self.scroll_canvas.create_window((0, 0), window=self.main, anchor="nw")
        self.main.bind("<Configure>", lambda e: self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all")))

        # Input card
        card = tk.Frame(self.main, bg=SURFACE, bd=0, relief="flat", padx=24, pady=20)
        card.pack(fill="x", padx=24, pady=(20, 10))
        tk.Label(card, text="📦 Product Details", font=("Helvetica", 13, "bold"),
                 bg=SURFACE, fg=YELLOW).grid(row=0, column=0, columnspan=2,
                                              sticky="w", pady=(0, 12))

        fields = [
            ("Cost per Unit (PHP):",     "cost"),
            ("Number of Units Sold:",    "units"),
            ("Fixed Costs/Expenses (PHP):", "fixed"),
        ]
        self.inputs = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(card, text=label, font=("Helvetica", 11),
                     bg=SURFACE, fg=WHITE).grid(row=i+1, column=0, sticky="w", pady=6)
            entry = tk.Entry(card, font=("Helvetica", 11), bg="#3b3b52",
                             fg=WHITE, insertbackground=WHITE,
                             relief="flat", width=20, bd=6)
            entry.grid(row=i+1, column=1, sticky="w", padx=(16, 0), pady=6)
            self.inputs[key] = entry

        # Scenarios card
        sc_card = tk.Frame(self.main, bg=SURFACE, padx=24, pady=20)
        sc_card.pack(fill="x", padx=24, pady=(0, 10))
        tk.Label(sc_card, text="💰 Pricing Scenarios",
                 font=("Helvetica", 13, "bold"), bg=SURFACE, fg=YELLOW).pack(anchor="w")

        ctrl = tk.Frame(sc_card, bg=SURFACE)
        ctrl.pack(anchor="w", pady=(8, 0))
        tk.Label(ctrl, text="Number of scenarios:", font=("Helvetica", 11),
                 bg=SURFACE, fg=WHITE).pack(side="left")
        self.num_var = tk.IntVar(value=3)
        spin = tk.Spinbox(ctrl, from_=1, to=10, textvariable=self.num_var,
                          width=5, font=("Helvetica", 11),
                          bg="#3b3b52", fg=WHITE, buttonbackground=ACCENT,
                          relief="flat")
        spin.pack(side="left", padx=8)
        tk.Button(ctrl, text="Set Scenarios", font=("Helvetica", 10, "bold"),
                  bg=ACCENT, fg=WHITE, relief="flat", cursor="hand2",
                  padx=10, pady=4,
                  command=self.build_price_entries).pack(side="left", padx=4)

        self.price_frame = tk.Frame(sc_card, bg=SURFACE)
        self.price_frame.pack(fill="x", pady=(12, 0))
        self.build_price_entries()

        # Simulate button
        tk.Button(self.main, text="▶  RUN SIMULATION",
                  font=("Helvetica", 13, "bold"),
                  bg=GREEN, fg="#052e16", relief="flat",
                  cursor="hand2", padx=20, pady=12,
                  command=self.simulate).pack(pady=(8, 4))

        # Results area
        self.results_frame = tk.Frame(self.main, bg=BG)
        self.results_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def build_price_entries(self):
        for w in self.price_frame.winfo_children():
            w.destroy()
        self.price_entries = []
        n = self.num_var.get()
        for i in range(n):
            row = tk.Frame(self.price_frame, bg=SURFACE)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=f"Scenario {i+1} Price (PHP):",
                     font=("Helvetica", 11), bg=SURFACE, fg=WHITE).pack(side="left")
            e = tk.Entry(row, font=("Helvetica", 11), bg="#3b3b52",
                         fg=WHITE, insertbackground=WHITE,
                         relief="flat", width=16, bd=6)
            e.pack(side="left", padx=(12, 0))
            self.price_entries.append(e)

    def simulate(self):
        try:
            cost       = float(self.inputs["cost"].get())
            units      = int(self.inputs["units"].get())
            fixed      = float(self.inputs["fixed"].get())
            prices     = [float(e.get()) for e in self.price_entries]
        except ValueError:
            messagebox.showerror("Input Error", "Please fill in all fields with valid numbers.")
            return

        if any(v <= 0 for v in [cost, units, fixed] + prices):
            messagebox.showerror("Input Error", "All values must be greater than 0.")
            return

        total_cost     = (cost * units) + fixed
        revenues       = [p * units for p in prices]
        profits        = [rev - total_cost for rev in revenues]
        margins        = [(prof/rev*100) if rev else 0
                          for prof, rev in zip(profits, revenues)]

        # Clear previous results
        for w in self.results_frame.winfo_children():
            w.destroy()

        # Results table
        tk.Label(self.results_frame, text="📊 Simulation Results",
                 font=("Helvetica", 13, "bold"), bg=BG, fg=YELLOW).pack(anchor="w", pady=(12, 6))

        cols = ("Scenario", "Price (PHP)", "Revenue (PHP)", "Profit/Loss (PHP)", "Margin (%)", "Status")
        tree = ttk.Treeview(self.results_frame, columns=cols, show="headings", height=len(prices))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=SURFACE, foreground=WHITE,
                         fieldbackground=SURFACE, rowheight=30,
                         font=("Helvetica", 10))
        style.configure("Treeview.Heading", background=ACCENT, foreground=WHITE,
                         font=("Helvetica", 10, "bold"))

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=140)

        best_idx  = profits.index(max(profits))
        worst_idx = profits.index(min(profits))

        for i, (price, rev, prof, margin) in enumerate(zip(prices, revenues, profits, margins)):
            status = "✅ PROFIT" if prof > 0 else ("⚠️ BREAK EVEN" if prof == 0 else "❌ LOSS")
            tag    = "profit" if prof > 0 else ("even" if prof == 0 else "loss")
            tree.insert("", "end", values=(
                f"{'★ ' if i == best_idx else ''}S{i+1}",
                f"{price:,.2f}", f"{rev:,.2f}", f"{prof:,.2f}",
                f"{margin:.1f}%", status
            ), tags=(tag,))

        tree.tag_configure("profit", foreground="#86efac")
        tree.tag_configure("loss",   foreground="#fca5a5")
        tree.tag_configure("even",   foreground=YELLOW)
        tree.pack(fill="x")

        # Insight panel
        ins = tk.Frame(self.results_frame, bg=SURFACE, padx=16, pady=12)
        ins.pack(fill="x", pady=(10, 0))
        tk.Label(ins, text="🎯 Insights", font=("Helvetica", 12, "bold"),
                 bg=SURFACE, fg=YELLOW).pack(anchor="w")
        tk.Label(ins,
                 text=f"🏆 Best:  Scenario {best_idx+1} @ PHP {prices[best_idx]:,.2f}  →  PHP {profits[best_idx]:,.2f} profit",
                 font=("Helvetica", 11), bg=SURFACE, fg="#86efac").pack(anchor="w", pady=2)
        tk.Label(ins,
                 text=f"⚠️  Worst: Scenario {worst_idx+1} @ PHP {prices[worst_idx]:,.2f}  →  PHP {profits[worst_idx]:,.2f}",
                 font=("Helvetica", 11), bg=SURFACE, fg="#fca5a5").pack(anchor="w", pady=2)

        # Charts
        labels      = [f"S{i+1}\nPHP{p:,.0f}" for i, p in enumerate(prices)]
        x           = np.arange(len(prices))
        width       = 0.3
        total_costs = [total_cost] * len(prices)

        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        fig.patch.set_facecolor(BG)

        for ax in axes:
            ax.set_facecolor(SURFACE)
            ax.tick_params(colors=WHITE, labelsize=8)
            ax.xaxis.label.set_color(WHITE)
            ax.yaxis.label.set_color(WHITE)
            ax.title.set_color(WHITE)
            for spine in ax.spines.values():
                spine.set_edgecolor("#555555")

        axes[0].bar(x - width/2, revenues,    width, label='Revenue',    color='#4fc3f7', alpha=0.9)
        axes[0].bar(x + width/2, total_costs, width, label='Total Cost', color='#ef5350', alpha=0.9)
        axes[0].set_title('Revenue vs Total Cost', fontsize=10)
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(labels, color=WHITE, fontsize=8)
        axes[0].legend(facecolor=SURFACE, labelcolor=WHITE, fontsize=8)
        axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v/1000:.0f}k'))

        bar_colors = ['#22c55e' if p > 0 else '#ef4444' for p in profits]
        axes[1].bar(labels, profits, color=bar_colors, alpha=0.9)
        axes[1].axhline(0, color=WHITE, linewidth=0.8, linestyle='--')
        axes[1].set_title('Profit / Loss', fontsize=10)
        axes[1].tick_params(axis='x', colors=WHITE, labelsize=8)
        axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v/1000:.0f}k'))

        axes[2].plot(labels, margins, marker='o', color='#ffb74d', linewidth=2.5, markersize=7)
        axes[2].fill_between(range(len(labels)), margins, alpha=0.15, color='#ffb74d')
        axes[2].axhline(0, color=WHITE, linewidth=0.8, linestyle='--')
        axes[2].set_title('Profit Margin %', fontsize=10)
        axes[2].tick_params(axis='x', colors=WHITE, labelsize=8)
        axes[2].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1f}%'))

        plt.tight_layout()

        chart_frame = tk.Frame(self.results_frame, bg=BG)
        chart_frame.pack(fill="both", expand=True, pady=(12, 0))
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

if __name__ == "__main__":
    app = PricingSimulator()
    app.mainloop()