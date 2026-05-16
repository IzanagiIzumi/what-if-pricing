import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

BG      = "#1e1e2e"
SURFACE = "#2a2a3e"
ACCENT  = "#7c3aed"
GREEN   = "#22c55e"
RED     = "#ef4444"
YELLOW  = "#facc15"
WHITE   = "#f1f5f9"
GRAY    = "#94a3b8"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What-if Pricing Scenario Simulation")
        self.geometry("900x720")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.price_entries = []
        self._build()

    def _lbl(self, p, text, size=11, bold=False, fg=None):
        return tk.Label(p, text=text, bg=p["bg"], fg=fg or WHITE,
                        font=("Helvetica", size, "bold" if bold else "normal"))

    def _entry(self, p, w=20):
        return tk.Entry(p, font=("Helvetica", 11), bg="#3b3b52",
                        fg=WHITE, insertbackground=WHITE, relief="flat", width=w, bd=6)

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=ACCENT, pady=14)
        hdr.pack(fill="x")
        self._lbl(hdr, "💰 What-if Pricing Scenario Simulation",
                  size=16, bold=True).pack()
        self._lbl(hdr, "Small Retail Store  •  IT2032  •  BSCS 601",
                  size=10, fg="#d8b4fe").pack(pady=(3,0))

        # Main scroll area
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True)
        sb = tk.Scrollbar(wrap)
        sb.pack(side="right", fill="y")
        self.cv = tk.Canvas(wrap, bg=BG, highlightthickness=0,
                            yscrollcommand=sb.set)
        self.cv.pack(side="left", fill="both", expand=True)
        sb.config(command=self.cv.yview)
        self.fr = tk.Frame(self.cv, bg=BG)
        self._win = self.cv.create_window((0,0), window=self.fr, anchor="nw")
        self.fr.bind("<Configure>",
                     lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cv.bind("<Configure>",
                     lambda e: self.cv.itemconfig(self._win, width=e.width))
        self.cv.bind_all("<MouseWheel>",
                         lambda e: self.cv.yview_scroll(-1*(e.delta//120), "units"))

        self._build_inputs()
        self._build_scenarios()

        tk.Button(self.fr, text="▶  RUN SIMULATION",
                  font=("Helvetica", 13, "bold"),
                  bg=GREEN, fg="#052e16", relief="flat",
                  cursor="hand2", padx=20, pady=12,
                  command=self._simulate).pack(pady=12)

        self.res = tk.Frame(self.fr, bg=BG)
        self.res.pack(fill="both", expand=True, padx=24, pady=(0,32))

    def _card(self, text):
        outer = tk.Frame(self.fr, bg=SURFACE, padx=22, pady=18)
        outer.pack(fill="x", padx=24, pady=(0,10))
        self._lbl(outer, text, size=13, bold=True, fg=YELLOW).pack(anchor="w", pady=(0,12))
        return outer

    def _build_inputs(self):
        c = self._card("📦  Product Details")
        self.inputs = {}
        for lbl, key in [("Cost per Unit (PHP):", "cost"),
                          ("Number of Units Sold:", "units"),
                          ("Fixed Costs / Expenses (PHP):", "fixed")]:
            row = tk.Frame(c, bg=SURFACE)
            row.pack(anchor="w", pady=5)
            self._lbl(row, lbl, fg=GRAY).pack(side="left")
            e = self._entry(row)
            e.pack(side="left", padx=(14,0))
            self.inputs[key] = e

    def _build_scenarios(self):
        self._sc = self._card("💰  Pricing Scenarios")
        ctrl = tk.Frame(self._sc, bg=SURFACE)
        ctrl.pack(anchor="w", pady=(0,10))
        self._lbl(ctrl, "Number of scenarios:", fg=GRAY).pack(side="left")
        self.nvar = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=1, to=10, textvariable=self.nvar,
                   width=5, font=("Helvetica",11),
                   bg="#3b3b52", fg=WHITE, relief="flat").pack(side="left", padx=8)
        tk.Button(ctrl, text="Set Scenarios",
                  font=("Helvetica",10,"bold"),
                  bg=ACCENT, fg=WHITE, relief="flat",
                  cursor="hand2", padx=10, pady=4,
                  command=self._set_prices).pack(side="left")
        self._pf = tk.Frame(self._sc, bg=SURFACE)
        self._pf.pack(fill="x")
        self._set_prices()

    def _set_prices(self):
        for w in self._pf.winfo_children():
            w.destroy()
        self.price_entries = []
        for i in range(self.nvar.get()):
            r, c = divmod(i, 3)
            cell = tk.Frame(self._pf, bg=SURFACE)
            cell.grid(row=r, column=c, padx=10, pady=6, sticky="w")
            self._lbl(cell, f"Scenario {i+1} (PHP):", size=10, fg=GRAY).pack(anchor="w")
            e = self._entry(cell, w=16)
            e.pack(anchor="w", pady=(2,0))
            self.price_entries.append(e)

    def _simulate(self):
        try:
            cost   = float(self.inputs["cost"].get())
            units  = int(self.inputs["units"].get())
            fixed  = float(self.inputs["fixed"].get())
            prices = [float(e.get()) for e in self.price_entries]
        except ValueError:
            messagebox.showerror("Input Error", "Please fill all fields with valid numbers.")
            return
        if any(v <= 0 for v in [cost, units, fixed] + prices):
            messagebox.showerror("Input Error", "All values must be greater than 0.")
            return

        tc      = (cost * units) + fixed
        revs    = [p * units for p in prices]
        profs   = [r - tc for r in revs]
        margins = [(p/r*100) if r else 0 for p,r in zip(profs,revs)]
        bi      = profs.index(max(profs))
        wi      = profs.index(min(profs))

        for w in self.res.winfo_children():
            w.destroy()

        # Summary
        sb = tk.Frame(self.res, bg=SURFACE, padx=20, pady=14)
        sb.pack(fill="x", pady=(12,8))
        self._lbl(sb, "📋  Summary", size=12, bold=True, fg=YELLOW).pack(anchor="w", pady=(0,8))
        row = tk.Frame(sb, bg=SURFACE)
        row.pack(fill="x")
        for i,(lbl,val,clr) in enumerate([
            ("Total Cost",  f"PHP {tc:,.2f}",        RED),
            ("Best Profit", f"PHP {profs[bi]:,.2f}",  GREEN),
            ("Best Margin", f"{margins[bi]:.1f}%",    YELLOW)]):
            box = tk.Frame(row, bg="#3b3b52", padx=18, pady=12)
            box.grid(row=0, column=i, padx=8, sticky="ew")
            row.columnconfigure(i, weight=1)
            self._lbl(box, lbl, size=9, fg=GRAY).pack()
            self._lbl(box, val, size=14, bold=True, fg=clr).pack(pady=(4,0))

        # Table
        tf = tk.Frame(self.res, bg=SURFACE, padx=20, pady=14)
        tf.pack(fill="x", pady=(0,8))
        self._lbl(tf, "📊  Results Table", size=12, bold=True, fg=YELLOW).pack(anchor="w", pady=(0,8))
        st = ttk.Style()
        st.theme_use("clam")
        st.configure("T.Treeview", background=SURFACE, foreground=WHITE,
                     fieldbackground=SURFACE, rowheight=30, font=("Helvetica",10))
        st.configure("T.Treeview.Heading", background=ACCENT, foreground=WHITE,
                     font=("Helvetica",10,"bold"))
        cols = ("Scenario","Price","Revenue","Profit/Loss","Margin","Status")
        tv   = ttk.Treeview(tf, columns=cols, show="headings",
                             height=len(prices), style="T.Treeview")
        for col,w in zip(cols,[100,120,130,140,90,120]):
            tv.heading(col, text=col)
            tv.column(col, anchor="center", width=w)
        tv.tag_configure("profit", foreground="#86efac")
        tv.tag_configure("loss",   foreground="#fca5a5")
        tv.tag_configure("even",   foreground=YELLOW)
        for i,(p,r,pr,m) in enumerate(zip(prices,revs,profs,margins)):
            tag = "profit" if pr>0 else ("even" if pr==0 else "loss")
            tv.insert("","end",
                      values=(f"{'★ ' if i==bi else ''}S{i+1}",
                              f"{p:,.2f}", f"{r:,.2f}", f"{pr:,.2f}",
                              f"{m:.1f}%",
                              "✅ PROFIT" if pr>0 else ("⚠️ BREAK EVEN" if pr==0 else "❌ LOSS")),
                      tags=(tag,))
        tv.pack(fill="x")

        # Insights
        ins = tk.Frame(self.res, bg=SURFACE, padx=20, pady=14)
        ins.pack(fill="x", pady=(0,8))
        self._lbl(ins, "🎯  Insights", size=12, bold=True, fg=YELLOW).pack(anchor="w", pady=(0,6))
        self._lbl(ins, f"🏆 Best:  S{bi+1} @ PHP {prices[bi]:,.2f}  →  PHP {profs[bi]:,.2f} profit",
                  fg="#86efac").pack(anchor="w", pady=2)
        self._lbl(ins, f"⚠️  Worst: S{wi+1} @ PHP {prices[wi]:,.2f}  →  PHP {profs[wi]:,.2f}",
                  fg="#fca5a5").pack(anchor="w", pady=2)

        # Charts
        cc = tk.Frame(self.res, bg=SURFACE, padx=20, pady=14)
        cc.pack(fill="both", expand=True, pady=(0,24))
        self._lbl(cc, "📈  Charts", size=12, bold=True, fg=YELLOW).pack(anchor="w", pady=(0,8))

        xl  = [f"S{i+1}\nPHP{p:,.0f}" for i,p in enumerate(prices)]
        x   = np.arange(len(prices))
        w   = 0.3
        tcs = [tc]*len(prices)

        fig, axes = plt.subplots(1, 3, figsize=(13,4))
        fig.patch.set_facecolor(BG)
        for ax in axes:
            ax.set_facecolor(SURFACE)
            ax.tick_params(colors=WHITE, labelsize=8)
            ax.xaxis.label.set_color(WHITE)
            ax.yaxis.label.set_color(WHITE)
            ax.title.set_color(WHITE)
            for sp in ax.spines.values():
                sp.set_edgecolor("#555")

        axes[0].bar(x-w/2, revs, w, label="Revenue",    color="#4fc3f7", alpha=0.9)
        axes[0].bar(x+w/2, tcs,  w, label="Total Cost", color="#ef5350", alpha=0.9)
        axes[0].set_title("Revenue vs Total Cost", fontsize=10)
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(xl, color=WHITE, fontsize=8)
        axes[0].legend(facecolor=SURFACE, labelcolor=WHITE, fontsize=8)
        axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"PHP {v:,.0f}"))

        axes[1].bar(xl, profs, color=["#22c55e" if p>0 else "#ef4444" for p in profs], alpha=0.9)
        axes[1].axhline(0, color=WHITE, linewidth=0.8, linestyle="--")
        axes[1].set_title("Profit / Loss", fontsize=10)
        axes[1].tick_params(axis="x", colors=WHITE, labelsize=8)
        axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"PHP {v:,.0f}"))

        axes[2].plot(xl, margins, marker="o", color="#ffb74d", linewidth=2.5, markersize=7)
        axes[2].fill_between(range(len(xl)), margins, alpha=0.15, color="#ffb74d")
        axes[2].axhline(0, color=WHITE, linewidth=0.8, linestyle="--")
        axes[2].set_title("Profit Margin %", fontsize=10)
        axes[2].tick_params(axis="x", colors=WHITE, labelsize=8)
        axes[2].yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:.1f}%"))

        plt.tight_layout()
        cv2 = FigureCanvasTkAgg(fig, master=cc)
        cv2.draw()
        cv2.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

        self.update_idletasks()
        self.cv.yview_moveto(0.35)

if __name__ == "__main__":
    App().mainloop()
