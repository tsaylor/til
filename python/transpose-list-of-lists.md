# Transpose a list of lists

If you have a list of lists (or any sequences really), and want to 
join the lists together such that all the items in the same position
in the original lists are in a new list together, here's how to do it!

(It's hard to explain but the code snippet makes it clear. This is
kinda niche but it comes up from time to time.)

https://stackoverflow.com/questions/6473679/transpose-list-of-lists

```python
>>> somelist = [
...   ['a', 'b', 'c'],
...   [1, 2, 3]
... ]
...
>>> list(zip(*somelist))
[
  ['a', 1],
  ['b', 2],
  ['c', 3],
]
```
