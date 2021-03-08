
from numpy import  sqrt, zeros, array
from math import log
from scipy.optimize import minimize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


y = pd.read_csv(r'C:\Users\danor\Desktop\worldgdps.csv')
dy = array(y['2019'])
arr = dy[~np.isnan(dy)]/1000000000000  #scaline data down per $ 1 trillion
#sort array from lowest o high
arr.sort()
print(y.nlargest(50, ['2019']))

def gini(arr):
    count = arr.size
    coefficient = 2 / count
    indexes = np.arange(1, count + 1)
    weighted_sum = (indexes * arr).sum()
    total = arr.sum()
    constant = (count + 1) / count
    return coefficient * weighted_sum / total - constant

def lorenz(arr):
    # this divides the prefix sum by the total sum
    # this ensures all the values are between 0 and 1.0
    scaled_prefix_sum = arr.cumsum() / arr.sum()
    # this prepends the 0 value (because 0% of all people have 0% of all wealth)
    return np.insert(scaled_prefix_sum, 0, 0)

# show the gini index!
print('gini coefficienet',gini(arr))
print('min', min(arr))
lorenz_curve = lorenz(arr)

# we need the X values to be between 0.0 to 1.0
plt.plot(np.linspace(0.0, 1.0, lorenz_curve.size), lorenz_curve)
# plot the straight line perfect equality curve
plt.plot([0,1], [0,1])
plt.xlabel('cum % of World GDP')
plt.ylabel('cum % of Population (Countries)')
plt.title('Lorenz Curve for World GDP 2019')
plt.show()
####
import scipy.stats


plt.hist(arr, 50, facecolor='green', alpha=0.5);
plt.xlabel('GDP (in $ trillions current)')
plt.ylabel('number of countries')
plt.title('Distribution of World GDP')
plt.show()


# log likelihood function of pareto distribution

def fun(a, data):
    xm = min(data)
    n = data.size
    print("a",a)
    print("xm",xm)
#    print n
    f = zeros(n)
    for i in range(n):
#       print f[i]
       f[i] = log(a)+a*log(xm)-(a+1)*log(data[i])
#       print f[i]
    fsum = sum(f)
#    print fsum 
    print("fsum",-fsum)
    return -fsum


guess = .10


theta_mle = minimize(fun,guess, args=arr, tol=.1,options={'maxiter':1000,'disp':True})

print(theta_mle)

# Compute Hessian for the variance of theta_mle
# H = - sum(data)/(theta^2)

estimate = theta_mle.x
print("parameter estimate", estimate)

H = - sum(arr)/(estimate**2)
var_theta = -1/H
print("variance", var_theta)
se_theta = sqrt(var_theta)
print("standard error", se_theta)

  

\


