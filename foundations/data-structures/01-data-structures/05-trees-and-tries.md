# Trees and Tries

A tree models a hierarchy. The root has no parent, a leaf has no children, and
the height of a tree is the longest root-to-leaf path. Traversals visit each
node once: preorder visits node-left-right, inorder visits left-node-right, and
postorder visits left-right-node.

## Binary Search Trees

A binary search tree (BST) maintains an ordering invariant: keys in the left
subtree precede the node key, and keys in the right subtree follow it. Inorder
traversal yields sorted keys.

Search, insertion, deletion, predecessor, and successor take `O(h)` for tree
height `h`. A plain BST may become a chain, so its worst case is `O(n)`.
AVL and red-black trees maintain logarithmic height and provide `O(log n)`
operations.

Use a BST for ordered keys and range queries. Use a heap when you only need
the current extreme; see [Heaps and Priority Queues](04-heaps-and-priority-queues.md).

## Tries

A trie stores strings by sharing prefix paths. Each edge represents a symbol,
and a terminal marker records that a complete key ends at a node. A terminal
node can have children: both `car` and `cart` may be present.

Insertion, exact search, and prefix search take `O(L)`, where `L` is the
key length. Tries work well for autocomplete and prefix matching, trading
memory for predictable prefix operations.
