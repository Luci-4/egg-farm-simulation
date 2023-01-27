from pandas import read_csv, DataFrame
from scipy.stats import shapiro, wilcoxon
data = read_csv('output.csv')
bruteforce_egg_numbers = DataFrame(data, columns=["bruteforce egg number"])
expected_egg_numbers = DataFrame(data, columns=["expected value egg number"])
print(bruteforce_egg_numbers)
print(expected_egg_numbers)
bruteforce_shapiro_result = shapiro(bruteforce_egg_numbers)
expected_shapiro_result = shapiro(expected_egg_numbers)
print(bruteforce_shapiro_result.pvalue > 0.05)
print(expected_shapiro_result.pvalue > 0.05)
wilcoxon_results = wilcoxon(bruteforce_egg_numbers.values.ravel(), expected_egg_numbers.values.ravel(), alternative="less")
# wilcoxon_results = wilcoxon(bruteforce_egg_numbers.values.ravel(), expected_egg_numbers.values.ravel(), alternative="less")
# expected is better
print(wilcoxon_results)
