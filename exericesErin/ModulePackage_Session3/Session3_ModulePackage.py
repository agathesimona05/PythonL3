#Inputs
x = 10
y = 11

# 1. Play with module
# Import functions from calculator.py module
import calculator
print(calculator.addition(x, y))

# Import calculator package with an alias
import calculator as calc
print(calc.division(x, y))

# Import specific functions from calculator
from calculator import multiplication
print(multiplication(x, y))

# Import all functions from calculator
from calculator import *
print(soustraction(x, y))

# 2. Play with module inside a package
# Import nested module using an alias
from Utils import calculator as calc_nested
print(calc_nested.power(y, x))

# Import specific functions from calculator
from Utils.calculator import power
print(power(x, y))

# Import all functions from calculator
from Utils.calculator import *
print(round(10.256, 2))

# 3. Play with module inside a nested package
# Same logics can be reused
from Utils.SimpleOperation import calculator as nested_package_calc
print(nested_package_calc.rounding(10.256, 2))


