# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 09:15:12 2022

@author: Pr.TAC_MACHINO
"""
from random import*
f = lambda x : 3*x**2 - 3*x + 8 

n = 0
p = 1
m = 100000000
for i in range(m) :
    x = randint(0,10)
    y = randint(0,280)
    if y>0 and y<f(x) :
        n = n + 1
p = 2800*n/m
print(p)     