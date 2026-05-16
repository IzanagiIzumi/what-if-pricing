import matplotlib.pyplot as plt
import numpy as np

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Please enter a value greater than 0.")
            else:
                return value
        except ValueError:
            print("  Invalid input. Please enter a number.")

def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("  Please enter a value greater than 0.")
            else:
                return value
        except ValueError:
            print("  Invalid input. Please enter a whole number.")

def run_simulation():
    print("=" * 55)
    print("   WHAT-IF PRICING SCENARIO SIMULATION")
    print("   Small Retail Store - Business Simulation")
    print("=" * 55)

    print("\n📦 Enter your product details:\n")
    cost_per_unit = get_float_input("  Cost per unit (PHP): ")
    units_sold    = get_int_input("  Number of units sold: ")
    fixed_costs   = get_float_input("  Fixed costs/expenses (PHP): ")

    print("\n💰 Enter the selling prices you want to test:")
    print("  (You will enter prices one by one)")
    num_prices = get_int_input("\n  How many price scenarios do you want to test? ")

    prices = []
    for i in range(num_prices):
        price = get_float_input(f"  Scenario {i+1} - Selling price (PHP): ")
        prices.append(price)

    # --- Calculations ---
    total_costs    = [(cost_per_unit * units_sold) + fixed_costs] * len(prices)
    revenues       = [p * units_sold for p in prices]
    profits        = [rev - tc for rev, tc in zip(revenues, total_costs)]
    profit_margins = [(prof / rev) * 100 if rev != 0 else 0
                      for prof, rev in zip(profits, revenues)]

    # --- Results Table ---
    print("\n" + "=" * 55)
    print("   SIMULATION RESULTS")
    print("=" * 55)
    print(f"  Fixed Cost per Unit : PHP {cost_per_unit:,.2f}")
    print(f"  Units Sold          : {units_sold}")
    print(f"  Fixed Expenses      : PHP {fixed_costs:,.2f}")
    print(f"  Total Cost          : PHP {total_costs[0]:,.2f}")
    print("-" * 55)
    print(f"  {'Scenario':<12} {'Price':>10} {'Revenue':>12} {'Profit':>12} {'Margin':>8}")
    print("-" * 55)

    for i, (price, rev, prof, margin) in enumerate(
            zip(prices, revenues, profits, profit_margins)):
        status = "✅ PROFIT" if prof > 0 else ("⚠️  BREAK EVEN" if prof == 0 else "❌ LOSS")
        print(f"  Scenario {i+1:<3}  PHP {price:>8,.2f}  PHP {rev:>9,.2f}  PHP {prof:>9,.2f}  {margin:>6.1f}%  {status}")

    print("-" * 55)

    best_idx   = profits.index(max(profits))
    worst_idx  = profits.index(min(profits))
    print(f"\n  🏆 Best  Scenario : Scenario {best_idx+1} @ PHP {prices[best_idx]:,.2f} (PHP {profits[best_idx]:,.2f} profit)")
    print(f"  ⚠️  Worst Scenario : Scenario {worst_idx+1} @ PHP {prices[worst_idx]:,.2f} (PHP {profits[worst_idx]:,.2f})")
    print("=" * 55)

    # --- Charts ---
    labels = [f"S{i+1}\nPHP{p:,.0f}" for i, p in enumerate(prices)]
    x      = np.arange(len(prices))
    width  = 0.3

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle("What-if Pricing Scenario Simulation\nSmall Retail Store",
                 fontsize=14, fontweight='bold')

    # Chart 1: Revenue vs Total Cost
    ax1 = axes[0]
    ax1.bar(x - width/2, revenues,    width, label='Revenue',    color='steelblue')
    ax1.bar(x + width/2, total_costs, width, label='Total Cost', color='tomato')
    ax1.set_title('Revenue vs Total Cost')
    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('Amount (PHP)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()
    ax1.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda val, _: f'PHP {val:,.0f}'))

    # Chart 2: Profit per Scenario
    bar_colors = ['green' if p > 0 else 'red' for p in profits]
    ax2 = axes[1]
    ax2.bar(labels, profits, color=bar_colors)
    ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax2.set_title('Profit / Loss per Scenario')
    ax2.set_xlabel('Scenario')
    ax2.set_ylabel('Profit (PHP)')
    ax2.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda val, _: f'PHP {val:,.0f}'))

    # Chart 3: Profit Margin Line
    ax3 = axes[2]
    ax3.plot(labels, profit_margins, marker='o', color='darkorange', linewidth=2)
    ax3.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax3.set_title('Profit Margin per Scenario')
    ax3.set_xlabel('Scenario')
    ax3.set_ylabel('Margin (%)')
    ax3.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda val, _: f'{val:.1f}%'))

    plt.tight_layout()
    plt.savefig('simulation_results.png', dpi=150, bbox_inches='tight')
    print("\n  📊 Charts saved as simulation_results.png")
    plt.show()
    print("\n  ✅ Simulation complete!\n")

if __name__ == "__main__":
    run_simulation()