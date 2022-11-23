
"""
Shamir secret sharing uses the polynomial interpolation principle
I implemented in the following two phases :

Phase 1 : Generation of shares-
1.First decide the values for the number of shares (n), and threshold (t)
2.Next construct a random polynomial p(x),with degree t-1 by choossing random coefficients of the polynomial.
set the constant term inthe polynomial to be equal to the secret s
3.To generate n shares,randomly pick n points lying on the polynomial p(x)
4.Distribute the picked coordinates in the previous step among the shares.These acts as the shares in the system

Phase 2 : Reconstruction of secret-
1.Collect t or more shares
2.To use interpolation algorithm to reconstruct the polynomial,P'(x),from the shares.
3.Determine the value of the reconstructed polynomial for x=0.This value reveals the constant term of the polynomial
which happens to be the original secret.
Thus the secret is reconstructed
"""

import random
from math import ceil
from decimal import Decimal

field_size = 10**5

def reconstruct_secret(shares):
    """
    Combines individual shares (points on graph)
    using Lagranges interpolation.

    `shares` is a list of points (x,y) belonging to a
    polynomial with a constant of out key.

    """
    sums=0
    for j,share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i,share_i in enumerate(shares):
            xi,yi = share_i
            if i!=j:
                prod*= Decimal(Decimal(xi)/(xi-xj))
        prod *= yj
        sums+=Decimal(prod)
    return int(round(Decimal(sums),0))

def polynomial(x,coefficients):

    """
    This generates a single point on the graph of given polynomial in `x`.
    The polynomial is given by the list of coefficients.

    """
    point=0
    # Loop through reversed list, so that indices from enumerate match the
    # actual coefficient indices
    for i,j in enumerate(coefficients[::-1]):
        point+=x**i*j
    return point

def coeff(t,secret):
    """
    Randomly generate a list of coefficients for a polynomial with degree of t-1,
    whose constant is `secret`

    For example with a 3rd degree coefficient like this :
    3x^3 + 4x^2 + 18x + 554
    554 is the secret, and the polynomial degree+1 is how many points are needed to recover this secret.
    (in this case it's 4 points).
    """
    coeff=[random.randrange(0,field_size)for _ in range(t-1)]
    coeff.append(secret)
    return coeff

def generate_shares(n,m,secret):
    """
    Split given `secret` into n shares with minimum threshold of m shares to recover this secret,
    using SSS algorithm.
    """
    coefficients = coeff(m,secret)
    shares=[]
    for i in range(1,n+1):
        x=random.randrange(1,field_size)
        shares.append((x,polynomial(x,coefficients)))
    return  shares

if __name__ == '__main__':
    #(3,6) sharing scheme
    t,n=3,6
    secret = 123456789
    print(f'Original Secret: {secret}')

    #Phase 1 : Generation of shares
    shares = generate_shares(n, t, secret)
    print(f'Shares:{", ".join(str(share)for share in shares)}')

    #Phase 2 : Secret Reconstruction
    # Picking t shares randomly for reconstruction

    pool = random.sample(shares,t)
    print(f'Combining shares : {", ".join(str(share) for share in pool)}')
    print(f'Reconstructed secret: {reconstruct_secret(pool)}')







