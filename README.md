# final_project
Fractional Cascading on Binary Tree
https://www.youtube.com/watch?v=qDiORH5IoKo

File 1: fractional_cascading.py
This is the file that implements a basic fractional cascading. 
Run this program by typing in command line the following:
* python -u fractional_cascading.py
And it will show you the current 2d arrays and fractionally cascaded structure, then prompt you to enter a value you want to search in the 2d arrays
Printed results are in the PDF name "Fractional Cascading Basic"

File 2: binary_tree_FC.py
This is the file that implements fractional cascading on binary tree data structure. 
Run this program by typing in command line the following:
* python -u fractional_cascading.py 
Each node will be named by its index in preorder traversal just for viewing's sake


Question from the Professor:
1. What if the value is actually in the array? 
Right now, I don’t keep track of that, but it would be quite simple for me to change the answer from an index to a data pair of (boolean, index). Where I would get the boolean by just comparing the current original item (whether it’s from the pass item or from the pointer of the passed item) value and the target.

2. Search locally
For both programs, I have checked locally using the same idea below
Binary tree:
if pass_index != -2 and node.val[curr_index-1].val >= target:
                curr_index -= 1
2d array:
if fc_data[k][curr_index-1].val >= target:
                        curr_index -= 1
                        curr_element = fc_data[k][curr_index]

3. Does your code handle duplicate values?
Yes, it does. 

4. Does your code have flexibility to sample every k-th item instead of every other item?
Right now, no. I would have to hard code to change the promotion section and the local search section. 
Right now it checks n%2 != 0 to only promoted odd index item, I would have to change it to something else depends on the k-th item. Like every 5 item, I would do n%5 != 0.
And also change search locally accordingly. Both changes shouldn’t be too hard, I just have to take in one extra argument for both building the FC and searching the FC. 


