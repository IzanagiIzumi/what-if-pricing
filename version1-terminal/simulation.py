import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box

console = Console()

def get_float(prompt):
    while True:
        try:
            val = float(Prompt.ask(f"  [cyan]{prompt}[/cyan]"))
            if val <= 0:
                console.print("  [red]Please enter a value greater than 0.[/red]")
            else:
                return val
        except ValueError:
            console.print("  [red]Invalid input. Please enter a number.[/red]")

def get_int(prompt):
    while True:
        try:
            val = int(Prompt.ask(f"  [cyan]{prompt}[/cyan]"))
            if val <= 0:
                console.print("  [red]Please enter a value greater than 0.[/red]")
            else:
                return val
        except ValueError:
            console.print("  [red]Invalid input. Please enter a whole number.[/red]")

def run():
    console.clear()
    console.print(Panel.fit(
        "[bold yellow]WHAT-IF PRICING SCENARIO SIMULATION[/bold yellow]\n"
        "[dim]Small Retail Store — Business Simulation[/dim]\n"
        "[dim]IT2032 Modeling and Simulation | BSCS 601[/dim]",
        border_style="bright_yellow", padding=(1, 4)
    ))

    console.print("\n[bold white]📦 Product Details[/bold white]\n")
    cost_per_unit = get_float("Cost per unit (PHP)")
    units_sold    = get_int("Number of units sold")
    fixed_costs   = get_float("Fixed costs/expenses (PHP)")

    console.print("\n[bold white]💰 Pricing Scenarios[/bold white]\n")
    num_prices = get_int("How many price scenarios do you want to test")

    prices = []
    for i in range(num_prices):
        price = get_float(f"Scenario {i+1} — Selling price (PHP)")
        prices.append(price)

    total_cost     = (cost_per_unit * units_sold) + fixed_costs
    revenues       = [p * units_sold for p in prices]
    profits        = [rev - total_cost for rev in revenues]
    profit_margins = [(prof / rev * 100) if rev != 0 else 0
                      for prof, rev in zip(profits, revenues)]

    # Summary panel
    console.print(f"\n")
    console.print(Panel(
        f"[white]Cost per Unit :[/white]  [green]PHP {cost_per_unit:,.2f}[/green]\n"
        f"[white]Units Sold    :[/white]  [green]{units_sold}[/green]\n"
        f"[white]Fixed Expenses:[/white]  [green]PHP {fixed_costs:,.2f}[/green]\n"
        f"[white]Total Cost    :[/white]  [bold red]PHP {total_cost:,.2f}[/bold red]",
        title="[bold]📋 Summary[/bold]", border_style="blue", padding=(0, 2)
    ))

    # Results table
    table = Table(
        title="\n📊 Simulation Results",
        box=box.ROUNDED,
        border_style="bright_blue",
        header_style="bold cyan",
        show_lines=True
    )
    table.add_column("Scenario",      justify="center", style="bold white")
    table.add_column("Selling Price", justify="right",  style="yellow")
    table.add_column("Revenue",       justify="right",  style="green")
    table.add_column("Profit / Loss", justify="right")
    table.add_column("Margin",        justify="right",  style="magenta")
    table.add_column("Status",        justify="center")

    best_idx  = profits.index(max(profits))
    worst_idx = profits.index(min(profits))

    for i, (price, rev, prof, margin) in enumerate(
            zip(prices, revenues, profits, profit_margins)):
        if prof > 0:
            prof_str  = f"[green]PHP {prof:,.2f}[/green]"
            status    = "✅ PROFIT"
        elif prof == 0:
            prof_str  = f"[yellow]PHP {prof:,.2f}[/yellow]"
            status    = "⚠️  BREAK EVEN"
        else:
            prof_str  = f"[red]PHP {prof:,.2f}[/red]"
            status    = "❌ LOSS"

        label = f"[bold yellow]★ S{i+1}[/bold yellow]" if i == best_idx else f"S{i+1}"
        table.add_row(
            label,
            f"PHP {price:,.2f}",
            f"PHP {rev:,.2f}",
            prof_str,
            f"{margin:.1f}%",
            status
        )

    console.print(table)

    console.print(Panel(
        f"[bold green]🏆 Best  Scenario:[/bold green]  Scenario {best_idx+1} "
        f"@ PHP {prices[best_idx]:,.2f}  →  PHP {profits[best_idx]:,.2f} profit\n"
        f"[bold red]⚠️  Worst Scenario:[/bold red]  Scenario {worst_idx+1} "
        f"@ PHP {prices[worst_idx]:,.2f}  →  PHP {profits[worst_idx]:,.2f}",
        title="[bold]🎯 Insights[/bold]", border_style="green", padding=(0, 2)
    ))

    # Charts
    labels      = [f"S{i+1}\nPHP{p:,.0f}" for i, p in enumerate(prices)]
    x           = np.arange(len(prices))
    width       = 0.3
    total_costs = [total_cost] * len(prices)

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.patch.set_facecolor('#1e1e2e')
    fig.suptitle("What-if Pricing Scenario Simulation — Small Retail Store",
                 fontsize=13, fontweight='bold', color='white')

    for ax in axes:
        ax.set_facecolor('#2a2a3e')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#555555')

    ax1 = axes[0]
    ax1.bar(x - width/2, revenues,    width, label='Revenue',    color='#4fc3f7', alpha=0.9)
    ax1.bar(x + width/2, total_costs, width, label='Total Cost', color='#ef5350', alpha=0.9)
    ax1.set_title('Revenue vs Total Cost')
    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Amount (PHP)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, color='white')
    ax1.legend(facecolor='#2a2a3e', labelcolor='white')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'PHP {v:,.0f}'))

    bar_colors = ['#66bb6a' if p > 0 else '#ef5350' for p in profits]
    ax2 = axes[1]
    ax2.bar(labels, profits, color=bar_colors, alpha=0.9)
    ax2.axhline(0, color='white', linewidth=0.8, linestyle='--')
    ax2.set_title('Profit / Loss per Scenario')
    ax2.set_xlabel('Scenario')
    ax2.set_ylabel('Profit (PHP)')
    ax2.tick_params(axis='x', colors='white')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'PHP {v:,.0f}'))

    ax3 = axes[2]
    ax3.plot(labels, profit_margins, marker='o', color='#ffb74d',
             linewidth=2.5, markersize=8)
    ax3.fill_between(range(len(labels)), profit_margins,
                     alpha=0.15, color='#ffb74d')
    ax3.axhline(0, color='white', linewidth=0.8, linestyle='--')
    ax3.set_title('Profit Margin per Scenario')
    ax3.set_xlabel('Scenario')
    ax3.set_ylabel('Margin (%)')
    ax3.tick_params(axis='x', colors='white')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1f}%'))

    plt.tight_layout()
    plt.savefig('version1-terminal/simulation_results.png', dpi=150, bbox_inches='tight',
                facecolor='#1e1e2e')
    console.print("\n  [green]📊 Charts saved as simulation_results.png[/green]")
    plt.show()
    console.print("\n  [bold green]✅ Simulation complete![/bold green]\n")

if __name__ == "__main__":
    run()