# Provides analysis functionality for Shor's simulation and classical
# period finding factorization algorithms.
#
# Author: Carson Ihrke
# Date: June 24 (modified)

import time
import matplotlib.pyplot as plt
from brute import classical_factor_finding
from shors import run_quantum_factorization

def main():

    # scaled modulus values by bit size
    scaling_suite = [
        {"bits": 4,  "N": 15},         
        {"bits": 6,  "N": 33},         
        {"bits": 8,  "N": 143},        
        {"bits": 10, "N": 517},        
        {"bits": 12, "N": 2117},       
        {"bits": 14, "N": 9409},       
        {"bits": 16, "N": 36167},      
        {"bits": 18, "N": 171127},     
        {"bits": 20, "N": 745813},     
        {"bits": 22, "N": 3105701},    
        {"bits": 24, "N": 10502357},   
        {"bits": 26, "N": 52199081},   
        {"bits": 28, "N": 214434241},  
        {"bits": 30, "N": 1071449033}, 
        {"bits": 32, "N": 4294967311},   
    ]
    
    all_bits = []
    all_times = []
    categories = []  
    
    print("=" * 75)
    print("   EXTREME SCALING BENCHMARK: 4 TO 40 BITS (SINGLE-PARAMETER)")
    print("=" * 75)
    print("Testing classical factor finding performance scaling...\n")
    print(f"{'| Bits (n)':<11} {'| Number (N)':<16} {'| Execution Time':<18} {'| Status / Result':<30} |")
    print("|" + "-"*10 + "|" + "-"*15 + "|" + "-"*17 + "|" + "-"*29 + "|")
    
    # perform trials tracking complexity
    for trial in scaling_suite:
        N = trial["N"]
        bits = trial["bits"]
        
        start = time.perf_counter()
        f1, f2 = classical_factor_finding(N, verbose=False)
        end = time.perf_counter()
        
        elapsed = end - start
        all_bits.append(bits)
        
        if f1 and f2:
            status_text = f"Success ({f1}x{f2})"
            all_times.append(elapsed)
            
            if bits in [6, 28]:
                categories.append("Lucky Guess")
            elif bits == 14:
                categories.append("Square Root Pre-Check")
            else:
                categories.append("Standard Success")
        else:
            status_text = "Classical Limit Hit"
            all_times.append(elapsed)
            categories.append("Timeout Failure")
            
        time_text = f"{elapsed:.6f}s"
        print(f"| {bits:<8} | {N:<13} | {time_text:<15} | {status_text:<27} |")
        
    # ==========================
    # CLASSICAL GRAPH GENERATION
    # ==========================

    print("\nGenerating comprehensive performance scaling graph...")
    plt.figure(figsize=(12, 7))
    plt.plot(all_bits, all_times, linestyle='-', color='#78909c', alpha=0.7, linewidth=1.5, zorder=1)
    
    for b, t, cat in zip(all_bits, all_times, categories):
        if cat == "Standard Success":
            plt.scatter(b, t, color='#2e7d32', marker='o', s=60, label='Standard Success' if 'Standard Success' not in plt.gca().get_legend_handles_labels()[1] else "", zorder=2)
        elif cat == "Lucky Guess":
            plt.scatter(b, t, color='#f57c00', marker='D', s=60, label='Lucky GCD Guess' if 'Lucky GCD Guess' not in plt.gca().get_legend_handles_labels()[1] else "", zorder=3)
        elif cat == "Square Root Pre-Check":
            plt.scatter(b, t, color='#0288d1', marker='s', s=60, label='Square Root Shortcut' if 'Square Root Shortcut' not in plt.gca().get_legend_handles_labels()[1] else "", zorder=4)
        elif cat == "Timeout Failure":
            plt.scatter(b, t, color='#d32f2f', marker='X', s=80, label='Classical Step-Cap Hit' if 'Classical Step-Cap Hit' not in plt.gca().get_legend_handles_labels()[1] else "", zorder=5)

    plt.title('Unfiltered Classical Order Finding Complexity Scaling', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Key Size (Bits)', fontsize=12)
    plt.ylabel('Execution Time (Seconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(all_bits)
    plt.legend(fontsize=11, loc='upper left')

    plt.annotate('GCD Shortcut', xy=(6, 0), xytext=(4, 3), arrowprops=dict(arrowstyle="->", color='#f57c00'))
    plt.annotate('Square Pre-Check', xy=(14, 0), xytext=(10, 4), arrowprops=dict(arrowstyle="->", color='#0288d1'))
    plt.annotate('Exponential Wall Begins', xy=(28, 4.7), xytext=(20, 9), arrowprops=dict(arrowstyle="->", color='black'), weight='bold')

    graph_filename = "comprehensive_scaling_chart.png"
    plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
    print(f"[Success] graph saved as: '{graph_filename}'")
    plt.show()

    # ===================================
    # QUANTUM SIMULATION GRAPH GENERATION
    # ===================================
    print("\n" + "=" * 75)
    print("   GENERATING ADVANCED QUANTUM DIAGNOSTIC VISUALIZATIONS")
    print("=" * 75)
    
    N_quantum = 33
    a_quantum = 2
    print(f"Spawning Qiskit Aer State Engines for N={N_quantum} (base a={a_quantum})...")
    
    # Pull measurement distribution from the cleaned shors module
    counts, n_ctrl, a_used = run_quantum_factorization(N_quantum, a_quantum)
    
    # Quantum Phase Interference Histogram (Filtered Axes)

    print("🎨 Rendering Plot A: Constructive Interference Distribution Peaks...")
    plt.figure(figsize=(12, 6))
    
    sorted_counts = sorted(counts.items())
    states = [item[0] for item in sorted_counts]
    raw_vals = [item[1] for item in sorted_counts]
    probs = [v / sum(raw_vals) for v in raw_vals]
    
    bars = plt.bar(states, probs, color='#1565c0', edgecolor='black', alpha=0.85, width=0.4, zorder=2)
    
    # dynamic x axis labeling
    important_ticks = []
    for state, prob in zip(states, probs):
        if prob > 0.02:  # threshold identifying valid constructive spikes
            important_ticks.append(state)
            
    # apply filtered subset list directly to the figure frame
    plt.xticks(important_ticks, rotation=45, ha='right', fontsize=9)
    
    plt.title(f"Shor's Measurement Histogram ($N={N_quantum}$, $a={a_used}$)\n[Constructive Interference Probability Peaks]", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Measured Register State (Binary Phase Value - Filtered Peaks)", fontsize=10)
    plt.ylabel("Probability of Wave Collapse", fontsize=10)
    plt.grid(axis='y', linestyle=':', alpha=0.6, zorder=1)
    
    # annotate high-probability spikes with percentage metrics
    for bar in bars:
        h = bar.get_height()
        if h > 0.02:
            plt.text(bar.get_x() + bar.get_width()/2., h + 0.005, f'{h*100:.1f}%', ha='center', va='bottom', fontsize=8, weight='bold')
            
    plt.tight_layout()
    chart_a_name = "quantum_plot_A_measurement.png"
    plt.savefig(chart_a_name, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"[ANALYSIS COMPLETE] local output assets successfully written to file storage.")

if __name__ == "__main__":
    main()