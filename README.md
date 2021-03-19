# World-GDP-Analysis-with-MLE-of-pareto-distribution

Data was retrieved from the World Bank. 

link: https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CN&country=#
As previously explained in my 

To conduct the maximum likelihood estimate, I'm gonna make an assumption that this data follows a pareto distribution. A pareto distribution is a common distribution amongst many fields, but is especially prominent wealth economics. The pareto principal, which is the underlying idea of this distribution, is that 80% of an outcome is caused by 20% of the causes. This idea can be illustrated with gdp, as in 80% of gdp is caused by 20% of the population. The pdf of the pareto distribution, is characterized by two parameters: Xm and alpha. Xm is fixed and is simply the minimum value of the variable. We will be estimating alpha which like the gini coefficient, represents inequality with an alpha of 1.16 representing the 80-20 rule.I will find the estimate for alpha itself by numerically optimizing the log like function of the pareto dist. pdf using the scipy optimize package.

I will be looking specifically at GDP for all countries for 2019.  I will illustrate the distribution as well as a lorenz curve (gdp version) using matplot. While the lorenz curve is generally used to look at the cum. percen ratios of wealth to population as a measure of income inequality,  it can also be used to illustrate inequalities of other variables such as GDP.   


![image](https://user-images.githubusercontent.com/64437206/110268736-d3767380-7f87-11eb-9d58-8cf1cf170d6d.png)

PDF of Pareto Dist. provided by wiki:https://en.wikipedia.org/wiki/Pareto_distribution

# Let's begin
```
#Required Packages

from math import log
from scipy.optimize import minimize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

```
Importing, scaling, and removing Nas in data
```
y = pd.read_csv(r'C:\Users\danor\Desktop\worldgdps.csv')
dy = array(y['2019'])
arr = dy[~np.isnan(dy)]/1000000000000 #scaling down for easier intepretability (gdp in trillions) and removing NAs
```
Here is the distribution plot of the data. 
```
plt.hist(arr, 50, facecolor='green', alpha=0.5);
plt.xlabel('GDP (in $ trillions current)')
plt.ylabel('number of countries')
plt.title('Distribution of World GDP')
plt.show()

```
This distribution does lend evidence to the gdp inequality within the world, possibly suggesting a pareto distribution.

![image](https://user-images.githubusercontent.com/64437206/110266395-50531e80-7f83-11eb-995a-12de67b1066b.png)

From this plot it can be seen the outliers within the data which are China and United States
# Lorenz Curve

Lorenz curve is usually used to measure income iequality with the straight line being the equality line where everyone has equal income (or in this case equal gdp).  The further away the blue curve is from the equality line, the greater then inequality. 
```
arr.sort() #array must be sorted
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

# we need the X values to be between 0.0 to 1.0
plt.plot(np.linspace(0.0, 1.0, lorenz_curve.size), lorenz_curve)
# plot the straight line perfect equality curve
plt.plot([0,1], [0,1])
plt.xlabel('cum % of World GDP')
plt.ylabel('cum % of Population (Countries)')
plt.title('Lorenz Curve for World GDP 2019')
plt.show()

```

![image](https://user-images.githubusercontent.com/64437206/110269300-0705cd80-7f89-11eb-87c3-f396d23c9231.png)

This can be interpreted in the following ways:

1. 60% of the cum. population contributes ~0% of the world gdp.
2. 80% of the cum. population contributes ~5% of the world gdp.
3. 80% of the world gdp contributes 80% of the world gdp. 

Meaning that the majority of the people in the world do not contribute to the gdp statistic.
This huge gdp inequality can be explained by several factors including economic institutions, governments, natural resources, etc
Another big factor, as suggested by economist Hernando de Soto, is that a lot of underdeveloped countries have working markets, it's just that a lot of the data is not being tracked.

Gini coefficient of U.S
```
# show the gini index!
print('gini coefficienet',gini(arr))
print('min', min(arr))
lorenz_curve = lorenz(arr)
```
Gini coefficient is measureed from 0 to 1, 0 being the most equal society (equality line) and 1 being the most inequal (1 person produces it all). 
For the 2019, the gini coefficient for world gdp is .87 which is pretty high and further supports the pareto distribution being a good assumption. 

# Optimizing the log likelihood function of the Pareto Distribution

Here is the derivation of the log like function from wiki:

![image](https://user-images.githubusercontent.com/64437206/110269752-fe61c700-7f89-11eb-83f7-51045de3e689.png)

Here is my function for log likelihood function:
Make note for the xm parameter, that is always the min of the data so we're just computing one estimate alpha.

```

# log likelihood function of pareto distribution

def fun(a, data):
    xm = min(data)
    n = data.size
    print("a",a) #print statements to help with debugging
    print("xm",xm)
#    print n
    f = zeros(n)
    for i in range(n):
#       print f[i]
       f[i] = log(a)+a*log(xm)-(a+1)*log(data[i]) #log likelihood function
#       print f[i]
    fsum = sum(f)
#    print fsum 
    print("fsum",-fsum)
    return -fsum # return negative b/c there is only a min function (making it negative will maximize the function) hence maximum likelihood estimate
```
Optimizing as well as computing variance/std error using Hessian
```
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
```
![image](https://user-images.githubusercontent.com/64437206/110270356-3f0e1000-7f8b-11eb-8b4c-4485256d1a63.png)

Looks like my optimization was successful and found the maximum likelihood estimate for alpha in three iterations.



