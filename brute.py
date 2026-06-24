# Provides algorithm implementation for period finding factorization, the classical ideology
# behind Shor's algorithm.
#
# Author: Carson Ihrke
# Date: June 24 (modified)

from math import gcd, isqrt

# Factorization via period finding
# @params: modulus (N)
# @return: factors of N (p, q)
def classical_factor_finding(N, verbose=True):
    """
    Purely classical approach to factoring N by iterating through bases internally.
    Uses an adaptive 3,000,000 step-cap to successfully calculate larger periods
    without locking up the CPU on completely un-factorable bases.
    """
    if verbose:
        print(f"-> Starting classical factorization search for N={N}...")
    
    # Pre-Processing
    root = isqrt(N)
    if root * root == N:
        if verbose:
            print(f"   [Pre-Check] Success! Detected that N is a perfect square ({root}^2).")
        return root, root

    local_gcd = gcd
    max_bases_to_check = min(N, 30)
    
    for a in range(2, max_bases_to_check):
        
        # Check for a lucky guess via GCD
        common_divisor = local_gcd(a, N)
        if common_divisor != 1:
            if verbose:
                print(f"   [Base a={a}] Lucky guess! Instantly found common divisor via GCD.")
            return common_divisor, N // common_divisor
            
        # Period Finding Loop with Hash Map Optimization
        seen_remainders = {}
        current_value = a % N
        r = 1
        
        # BALANCED ADAPTIVE CAP: Enough to crack complex numbers, 
        # but low enough to reject failing bases in under 1 second.
        max_period_steps = 3000000
        reached_cap = False
        
        while current_value != 1:
            if current_value in seen_remainders:
                r = r - seen_remainders[current_value]
                break
                
            seen_remainders[current_value] = r
            current_value = (current_value * a) % N
            r += 1
            
            if r > max_period_steps:
                reached_cap = True
                break
                
        if reached_cap:
            continue 
                
        # Step 3: Classical Post-Processing Conditions
        if r % 2 != 0:
            continue
            
        x = pow(a, r // 2, N)
        if (x + 1) % N == 0:
            continue
            
        factor1 = local_gcd(x - 1, N)
        factor2 = local_gcd(x + 1, N)
        
        for factor in [factor1, factor2]:
            if 1 < factor < N:
                if verbose:
                    print(f"   [Base a={a}] Success! Period r={r} generated non-trivial factors.")
                return factor, N // factor
                
    return None, None

def main():
    N = 4294967311  # 32-bit test number
    print(f"--- Factoring N={N} using Single-Parameter Classical Order Finding ---")
    
    factor1, factor2 = classical_factor_finding(N, verbose=True)
    
    print("-" * 65)
    if factor1 and factor2:
        print(f"SUCCESS: Factors of {N} are {factor1} and {factor2}")
    else:
        print(f"FAILED: Could not factor N={N} within the balanced classical limit.")

if __name__ == "__main__":
    main()