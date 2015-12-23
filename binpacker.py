#
# Bin packing as a LP problem:
# http://www.or.deis.unibo.it/kp/Chapter8.pdf
#
# Requisite Wiki Article:
# https://en.wikipedia.org/wiki/Bin_packing_problem
#
# PuLP Library:
# https://pythonhosted.org/PuLP/index.html
#

from pulp import *
import time

#
# A list of item tuples (name, weight) -- name is meaningless except to humans.
# Weight and Size are used interchangeably here and elsewhere.
#
items = [("a", 5),
         ("b", 6),
         ("c", 7),
         ("d", 32),
         ("e", 2),
         ("f", 32),
         ("g", 5),
         ("h", 7),
         ("i", 9),
         ("k", 12),
         ("l", 11),
         ("m", 1),
         ("n", 2)]

itemCount = len(items)

# Max number of bins allowed.
maxBins = 32

# Bin Size
binCapacity = 32



# Indicator variable assigned 1 when the bin is used.
y = pulp.LpVariable.dicts('BinUsed', range(maxBins),
                            lowBound = 0,
                            upBound = 1,
                            cat = pulp.LpInteger)

# An indicator variable that is assigned 1 when item is placed into binNum
possible_ItemInBin = [(itemTuple[0], binNum) for itemTuple in items
                                            for binNum in range(maxBins)]
x = pulp.LpVariable.dicts('itemInBin', possible_ItemInBin,
                            lowBound = 0,
                            upBound = 1,
                            cat = pulp.LpInteger)

# Initialize the problem
prob = LpProblem("Bin Packing Problem", LpMinimize)

# Add the objective function.
prob += lpSum([y[i] for i in range(maxBins)]), "Objective: Minimize Bins Used"

#
# This is the constraints section.
#

# First constraint: For every item, the sum of bins in which it appears must be 1
for j in items:
    prob += lpSum([x[(j[0], i)] for i in range(maxBins)]) == 1, ("An item can be in only 1 bin -- " + str(j[0]))

# Second constraint: For every bin, the number of items in the bin cannot exceed the bin capacity
for i in range(maxBins):
    prob += lpSum([items[j][1] * x[(items[j][0], i)] for j in range(itemCount)]) <= binCapacity*y[i], ("The sum of item sizes must be smaller than the bin -- " + str(i))

# Write the model to disk
prob.writeLP("BinPack.lp")

# Solve the optimization.
start_time = time.time()
prob.solve()
print("Solved in %s seconds." % (time.time() - start_time))


# Bins used
print("Bins used: " + str(sum(([y[i].value() for i in range(maxBins)]))))

# The rest of this is some unpleasent massaging to get pretty results.
bins = {}
for itemBinPair in x.keys():
    if(x[itemBinPair].value() == 1):
        itemNum = itemBinPair[0]
        binNum = itemBinPair[1]
        if binNum in bins:
            bins[binNum].append(itemNum)
        else:
            bins[binNum] = [itemNum]

for b in bins.keys():
    print(str(b) + ": " + str(bins[b]))
