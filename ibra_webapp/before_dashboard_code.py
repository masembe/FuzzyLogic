#!/usr/bin/env python

# this is a refactored version of the code
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl  # I am using this lib to easily create membership functions

# Step 1: Create Antecedents/Consequents, plus variables to hold membership functions
age = ctrl.Antecedent(np.arange(0, 10, 1),
                      'age')  # -> this is our first antecedent, we repeat the logic, change the ranges
distance = ctrl.Antecedent(np.arange(0, 10, 1), 'distance')
energy_rating = ctrl.Antecedent(np.arange(0, 100, 1), 'energy_rating')
population = ctrl.Antecedent(np.arange(0, 10, 1), 'population')
# then the consequence, ranges really depend on your params
price_increase = ctrl.Consequent(np.arange(0, 60, 1), 'price_increase')


# age.automf(3) # This create 3 classes ie: low, medium, high


def set_obj(obj, key1, value_1, key2, value_2, key3, value_3):
    obj[key1] = fuzz.trimf(obj.universe, value_1)
    if len(value_2) > 1:
        obj[key2] = fuzz.trimf(obj.universe, value_2)
    if obj.label == 'energy_rating':
        obj[key3] = fuzz.trimf(obj.universe, value_3)
    else:
        obj[key3] = fuzz.trapmf(obj.universe, value_3)


set_obj(age, 'new', [0, 0, 3.333333], 'n', [], 'old', [3.333, 8, 10, 10])
# distance.automf(3) # same thing
set_obj(distance, 'near', [0, 0, 4], 'medium', [0, 4, 9], 'far', [5.667, 8.667, 10, 10])

# 2nd way: Vanilla manual way, lets say for price increase
set_obj(price_increase, 'low', [0, 0, 20], 'medium', [10, 25, 40], 'high', [30, 50, 60, 60])

# 
set_obj(population, 'low', [0, 1, 1], 'm', [], 'high', [1, 5, 10, 10])

# energy_rating.automf(3)
set_obj(energy_rating, 'bad', [1, 1, 40], 'medium', [35, 55, 80], 'good', [70, 100, 100])

# In[20]:


# universe is explicitly stating that this is a global variable, specifically that they are "arrays"
# Method 2 can be used when you want to explictly name your ranges..usually in the consequent; ie, price increase
# You can use it if you wanna be an extremist programmer


# In[21]:


# proof that they all work, lemme visualize: distance is poor, avg, good
# distance['average'].view()
# distance.view()
# age.view()
# population.view()
# energy_rating.view()


# Lets create the fuzzy rules
# If the distance is near OR the Age is new, then the Price_increase will be high
rule1 = ctrl.Rule(distance['near'] | age['new'], price_increase['high'])
# If the distance is far  then Price_increase will be low
rule2 = ctrl.Rule(distance['far'], price_increase['low'])
# If (distance is medium)Then (price increase is medium)
rule3 = ctrl.Rule(distance['medium'], price_increase['medium'])
# If (distance is far)or (age is old)or (population is low) or (energy is bad) Then (price increase is low)
rule4 = ctrl.Rule(distance['far'] | age['old'] | population['low'] | energy_rating['bad'], price_increase['low'])
# unlike previously, this bad boy can take multiple params 
# If (distance is near)or (age is new)or (population is high) or (energy is good) Then (price increase is high)
rule5 = ctrl.Rule(distance['near'] | age['new'] | population['high'] | energy_rating['good'], price_increase['high'])
# If (distance is medium)  or (energy is medium) Then (price increase is medium)
rule6 = ctrl.Rule(distance['medium'] | energy_rating['medium'], price_increase['medium'])

# In[ ]:
# In[24]:
# The aggregation of the rules with the membership functions and rule base.

price_increase_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
price_increase_ = ctrl.ControlSystemSimulation(price_increase_ctrl)


# This is where the input variables of the system are placed.
def compute_price_increase(distance, age, population, energy_rating):
    """

    :param energy_rating:  A number showing the energy rating of the property
    :param population:   A number that shows population of the area in millions
    :param age:   A number describing the age of property in years
    :type distance: A number that shows distance of property from city centre.
    """

    price_increase_.input['distance'] = distance
    price_increase_.input['age'] = age
    price_increase_.input['population'] = population
    price_increase_.input['energy_rating'] = energy_rating

    # computation occurs here with defuzzification method by default being centroid.
    price_increase_.compute()
    return price_increase_.output['price_increase']


# This prints out the numerical output
# print(compute_price_increase(8, 2, 0, 0))

# This displays the shape for purposes of debugging.
price_increase.view(sim=price_increase_)
