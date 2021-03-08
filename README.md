# World-GDP-Analysis-with-MLE-of-pareto-distribution

Data was retrieved from the World Bank. 

link: https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CN&country=#


To conduct the maximum likelihood estimate, I'm gonna make an assumption that this data follows a pareto distribution. A pareto distribution is a common distribution amongst many fields, but is especially prominent wealth economics. The pareto principal, which is the underlying idea of this distribution, is that 80% of an outcome is caused by 20% of the causes. This idea can be illustrated with gdp, as in 80% of gdp is caused by 20% of the population. I will be looking specifically at GDP for all countries for 2019.  I will illustrate the distribution as well as a lorenz curve (gdp version) using matplot. 


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
arr.sort()
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



