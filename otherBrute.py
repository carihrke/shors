# Linear search for factors of some coprime N. Provides necessary methods as well as functionality
# for analysis.
#
# Authors: Carson Ihrke and Will Geiger
# Date: June 24 (modified)

import time
import math
import matplotlib.pyplot as plt

# linear search brute force
# @params: modulus (N)
def classical_factor_finding(N, verbose=False):
    """
    Sequentially tests odd integers starting from 3 up to the square root of N.
    """
    if N % 2 == 0:
        return 2, N // 2
        
    limit = math.isqrt(N) + 1
    for i in range(3, limit, 2):
        if N % i == 0:
            factor_1 = i
            factor_2 = N // i
            if verbose:
                print(f"   [Found] Factors identified: {factor_1} x {factor_2}")
            return factor_1, factor_2
            
    return None, None


def main():

    # scaled modulus values by bit size
    scaling_suite = [
        {"bits": 4,  "N": 15},         
        {"bits": 6,  "N": 35},         
        {"bits": 8,  "N": 143},        
        {"bits": 10, "N": 899},  
        {"bits": 12, "N": 2117},       
        {"bits": 14, "N": 11413},       
        {"bits": 16, "N": 52441},      
        {"bits": 18, "N": 243877},     
        {"bits": 20, "N": 1013141},     
        {"bits": 22, "N": 4149223},    
        {"bits": 24, "N": 16736171},   
        {"bits": 26, "N": 67011403},   
        {"bits": 28, "N": 268202507},  
        {"bits": 30, "N": 1073215271}, 
        {"bits": 32, "N": 4293918797},   
        {"bits": 34, "N": 17175628429},
        {"bits": 36, "N": 68713566403},
        {"bits": 38, "N": 274872251141}, 
        {"bits": 40, "N": 1099505862217},
        {"bits": 42, "N": 4398033364913}, 
        {"bits": 44, "N": 17592116124439},
        {"bits": 46, "N": 70368693845881}
    ]

    all_bits = []
    all_times = []
    
    print("=" * 75)
    print("   HARDENED SEMI-PRIME TRIAL DIVISION SCALING BENCHMARK")
    print("=" * 75)
    print("Testing true brute-force performance without low-effort shortcuts...\n")
    print(f"{'| Bits (n)':<11} {'| Number (N)':<16} {'| Execution Time':<18} {'| Structural Composition':<30} |")
    print("|" + "-"*10 + "|" + "-"*15 + "|" + "-"*17 + "|" + "-"*29 + "|")
    
    # perform trials tracking complexity
    for trial in scaling_suite:
        N = trial["N"]
        bits = trial["bits"]
        desc = trial["desc"]
        
        start = time.perf_counter()
        f1, f2 = classical_factor_finding(N, verbose=False)
        end = time.perf_counter()
        
        elapsed = end - start
        all_bits.append(bits)
        all_times.append(elapsed)
        
        time_text = f"{elapsed:.6f}s"
        print(f"| {bits:<8} | {N:<13} | {time_text:<15} | {desc:<27} |")
        
    # ================
    # GRAPH GENERATION
    # ================

    print("\nGenerating comprehensive linear trial-division scaling graph...")
    plt.figure(figsize=(12, 7))
    
    # Trace baseline performance trend line
    plt.plot(all_bits, all_times, linestyle='-', color='#c62828', alpha=0.8, linewidth=2.0, zorder=1)
    
    # Scatter data nodes directly on the curve showing the progression
    plt.scatter(all_bits, all_times, color='#b71c1c', marker='o', s=50, label='Semi-Prime Brute Force Search', zorder=2)

    plt.title('Hardened Classical Semi-Prime Factorization Complexity Scaling', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Key Size (Bits)', fontsize=12)
    plt.ylabel('Execution Time (Seconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(all_bits)
    plt.legend(fontsize=11, loc='upper left')

    # Visual annotations identifying the structural reality of the timeline curve
    plt.annotate('Polynomial Run Zone (Fast)', xy=(12, all_times[4]), xytext=(4, all_times[-1] * 0.2), 
                 arrowprops=dict(arrowstyle="->", color='black'))
    plt.annotate('The Exponential Computation Wall', xy=(all_bits[-1], all_times[-1]), 
                 xytext=(all_bits[-6], all_times[-1] * 0.8), 
                 arrowprops=dict(arrowstyle="->", color='black'), weight='bold')

    graph_filename = "comprehensive_scaling_chart.png"
    plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
    print(f"📈 Success! Hardened complexity graph saved as: '{graph_filename}'")
    plt.show()
    
    print(f"\n======= [BENCHMARK RUN COMPLETE] =======")

if __name__ == "__main__":
    main()