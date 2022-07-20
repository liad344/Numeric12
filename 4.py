from operator import le
import pkgutil
from re import A
from turtle import color
import matplotlib.pyplot as plt
import math

fix_point_iterations = [] 
fix_point_iterations_errors = []

atkin_iterations = [] 
atkin_errors = []

stephans_iterations = []
stephans_errors = []

def rel_error(xk_1, xk):
    return abs(xk_1-xk)


def caclculate_atkin(xn,xn1,xn2):
    return xn - ((xn1-xn)**2)/(xn2-2*xn1+xn)


def fixed_point(g,xk,epsilon):
    global fix_point_iterations 
    global fix_point_iterations_errors

    while True:  
        xk_1 = g(xk)
        print(xk_1)
   
        fix_point_iterations.append(xk)
        fix_point_iterations_errors.append(rel_error(xk_1,xk))

        if rel_error(xk_1,xk) < epsilon:
            return
        xk = xk_1

#atkin uses already calculated values: 
def fixed_point_atkin(iterations,epsilon):
    global atkin_iterations
    global atkin_errors
    
    first = caclculate_atkin(iterations[0],iterations[1],iterations[2])
    atkin_iterations.append(first)
    for i in range(2, len(iterations)-2) : 
        atkin = caclculate_atkin(iterations[i],iterations[i+1],iterations[i+2])
        atkin_errors.append(rel_error(atkin,first))
        if rel_error(first,atkin) < epsilon:
            return   
       
        atkin_iterations.append(atkin)    
        first = atkin
   
    atkin_errors.append(0)
    return
    


def fixed_point_stephan(g,x0,epsilon):
    global stephans_iterations
    global stephans_errors 

    while True :
        x1 = g(x0); x2 = g(x1)
        if rel_error(x1,x0) < epsilon :
            return
        
        stephans_errors.append(rel_error(x1,x0))
        x0 = caclculate_atkin(x0,x1,x2)
        stephans_iterations.append(x0)

def main(x0, g):
    fixed_point(g, x0, epsilon=1*10**-30)
    fixed_point_stephan(g,x0, epsilon=1*10**-20)
    fixed_point_atkin(fix_point_iterations,epsilon=1*10**-20)
    
    print("len of fixed point" , len(fix_point_iterations))
    print("len of atkin " , len(atkin_iterations))
    print("len of stephan " , len(stephans_iterations))

    fixed  = plt.scatter(fix_point_iterations, fix_point_iterations_errors,  color=("red"))
    atkin = plt.scatter(atkin_iterations, atkin_errors, color=("green"))
    steph = plt.scatter(stephans_iterations, stephans_errors,  color=("blue"), )

    plt.xlabel("iterations"); plt.ylabel("rel error")
    plt.show()



x0 = 1

# cos(x^2)-1 ~ -1/2x^4+1/24x^8 more numariclly stable
g = lambda x: eval("-0.5*(x**4)+(1/24)*x**8")

main(x0,g)