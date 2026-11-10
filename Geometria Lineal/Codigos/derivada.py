import numpy as np
  
# defining polynomial function
var = np.poly1d([1, 2, 1])
print("Polynomial function, f(x):\n", var)
  
# calculating the derivative
derivative = var.deriv()
print("Derivative, f(x)'=", derivative)
  
# calculates the derivative of after 
# given value of x
print("When x=5  f(x)'=", derivative(5))