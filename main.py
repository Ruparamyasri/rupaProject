import random
from math import ceil
from decimal import Decimal

field_size = 10**5

def reconstruct_secret(shares):
    sums=0
    for j,share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i,share_i in enumerate(shares):
            xi,_ = share_i
            if i!=j:
                prod*= Decimal(Decimal(xi)/(xi-xj))
        prod *= yj
        sums+=Decimal(prod)
    return int(round(Decimal(sums),0))

def polynom(x,coefficients):
    point=0
    for i,j in enumerate(coefficients[::-1]):
        point+=x**i*j
    return point

def coeff(t,secret):
    coeff=[random.randrange(0,field_size)for _ in range(t-1)]
    coeff.append(secret)
    return coeff

def generate(n,m,secret):
    coefficients = coeff(m,secret)
    shares=[]
    for i in range(1,n+1):
        x=random.randrange(1,field_size)
        shares.append((x,polynom(x,coefficients)))
    return  shares

if __name__ == '__main__':
    t,n=3,5
    secret = 1234
    shares = generate(n,t,secret)
    print(f'shares:{", ".join(str(share)for share in shares)}')

    pool = random.sample(shares,t)
    print(f'Reconstruct: {reconstruct_secret(pool)}')







