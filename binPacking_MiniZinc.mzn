%
% 1D Bin Packing Optimization. 
%
% For use with http://www.minizinc.org
% http://www.minizinc.org/downloads/doc-latest/minizinc-tute.pdf
%

int: binCapacity = 3;
int: numItems = 5;
array[1..numItems] of int: sizes = [1,1,1,1,2];


int: maxBins = numItems;
array[1..maxBins] of var 0..1: binUsed;
array[1..numItems, 1..maxBins] of var 0..1: itemInBin;

constraint forall(j in 1..numItems) (sum(i in 1..maxBins) (itemInBin[j,i]) == 1);
constraint forall(i in 1..maxBins) (   sum(j in 1..numItems) (  itemInBin[j,i] * sizes[j]  ) <= binCapacity*binUsed[i]    );

solve minimize sum(binUsed)