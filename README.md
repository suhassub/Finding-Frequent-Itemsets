# Finding-Frequent-Itemsets
Implements algorithms like PCY, Multihash and Toivonen to find the frequent itemsets of all sizes from a given set of transactions


1)PCY
-----

Input Parameters:
------------------
1. Input.txt: This is the input file containing all transactions. Each line corresponds to a transaction.
Each transaction has items that are comma separated. Use input.txt to test this algorithm.
2. Support: Integer that defines the minimum count to qualify as a frequent itemset.
3. Bucket size: This is the size of the hash table.

Output:
--------
The output needs to contain the frequent itemsets of all sizes sorted lexicographically. It should also
contain the hash buckets with their count of candidates. If the result just contains itemsets of size1 just
print them and return. If it contains itemsets of size >= 2 print the bucket counts of the hash as well. For
example consider the output below.
[‘a’, ‘b’, ‘d’]
{0:0, 1:2, 3:5}
[[‘a’, ‘b’]]
Here [‘a’, ‘b’, ‘d’] represents itemsets of size 1 and {0:0, 1:2, 3:5} represents the hash counts before
calculating frequent itemsets of size 2. [[‘a’, ‘b’]] represents itemsets of size 2. Print all bucket counts
only for ith frequent itemset where i >= 2. The counts in the buckets can vary depending on the hashing
function used. So do not try to match this with the output files provided.

Execution:
---------

 python suhas_subramanya_pcy.py input.txt 4 20
 
 Where support = 4 and buckets = 20


2) Multi­Hash Algorithm
   ---------------------

Output Sample:
--------------
[‘a’, ‘b’, ‘c’]
{0:0, 1:2, 3:5}
{0:1, 1:4, 3:2}
[[‘a’, ‘b’]]


Execution
----------
python suhas_subramanya_multihash.py input.txt 4 5


3) Toivonen Algorithm
----------------------

For this algorithm you need to use a
sample size of less than 60% of your entire dataset. Uses an appropriate sampling method to get the
random sample set. Also performs a simple Apriori algorithm with the random sample set. Checks for
negative borders and runs the algorithm again with a different sample set if required till there are no
negative borders that have frequency > support.

Output:
-------
Line 1 <number of iterations performed>
Line 2 <fraction of transactions used>
Line 3 onwards <frequent itemsets lexicographically sorted>

Execution
----------
python suhas_subramanya_toivonen.py input1.txt 20

Where support=20
