"""
Subject Question Bank for Quizzly
Contains 105 verified, academic multiple-choice questions across 5 core B.Tech CSE subjects:
1. Python Programming (20 questions)
2. Data Structures (25 questions)
3. Computer Organization and Architecture (20 questions)
4. Discrete Structures and Theory of Logic (20 questions)
5. Mathematics (20 questions)
"""

ALL_SUBJECT_QUESTIONS = [
    # =========================================================================
    # 1. PYTHON PROGRAMMING (20 Questions: 7 Easy, 7 Medium, 6 Hard)
    # =========================================================================
    {
        "subject": "python",
        "question": "Which of the following built-in Python data types is immutable?",
        "options": {
            "A": "List",
            "B": "Dictionary",
            "C": "Tuple",
            "D": "Set"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Python Data Types",
        "explanation": "Tuples cannot be modified after creation, making them immutable, unlike lists, dictionaries, and sets."
    },
    {
        "subject": "python",
        "question": "What keyword is used to define a user-defined function in Python?",
        "options": {
            "A": "function",
            "B": "def",
            "C": "fun",
            "D": "lambda"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Function Definition",
        "explanation": "The 'def' keyword introduces a function definition in Python syntax."
    },
    {
        "subject": "python",
        "question": "What is the output of bool([]) in Python?",
        "options": {
            "A": "True",
            "B": "False",
            "C": "None",
            "D": "IndexError"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Truthy and Falsy Values",
        "explanation": "Empty collections (empty list, tuple, dict, set, string) evaluate to False in boolean contexts."
    },
    {
        "subject": "python",
        "question": "What is the result of 'python'[1:4] in Python string slicing?",
        "options": {
            "A": "pyt",
            "B": "ytho",
            "C": "yth",
            "D": "y"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "String Slicing",
        "explanation": "Slice [1:4] extracts characters from index 1 up to index 3 (exclusive of index 4): 'y', 't', 'h'."
    },
    {
        "subject": "python",
        "question": "Which operator is used to calculate floor division in Python?",
        "options": {
            "A": "/",
            "B": "//",
            "C": "%",
            "D": "**"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Arithmetic Operators",
        "explanation": "The '//' operator performs integer floor division, discarding any fractional remainder."
    },
    {
        "subject": "python",
        "question": "What data type must dictionary keys possess in standard Python?",
        "options": {
            "A": "Any data type without restriction",
            "B": "Only string data types",
            "C": "Hashable and immutable types",
            "D": "Strictly integer types"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Dictionary Keys",
        "explanation": "Dictionary keys must be hashable so Python can map them to hash table buckets; mutable types like lists cannot be keys."
    },
    {
        "subject": "python",
        "question": "Which built-in function returns the total number of items in a sequence or collection?",
        "options": {
            "A": "count()",
            "B": "size()",
            "C": "len()",
            "D": "length()"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Built-in Functions",
        "explanation": "The len() function returns the length (the number of items) of an object."
    },
    {
        "subject": "python",
        "question": "What distinguishes a generator expression from a list comprehension in Python?",
        "options": {
            "A": "Generators only work with floating-point numbers",
            "B": "Generators produce items lazily on demand using an iterator, saving memory",
            "C": "List comprehensions cannot be iterated using a for-loop",
            "D": "Generators execute much slower and store all elements in RAM"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Generators vs Comprehensions",
        "explanation": "Generators evaluate lazily and yield values one at a time via the iterator protocol without creating the full list in memory."
    },
    {
        "subject": "python",
        "question": "In Python function definitions, what does the *args syntax accomplish in the parameter list?",
        "options": {
            "A": "Forces arguments to be passed as keyword parameters",
            "B": "Collects arbitrary positional arguments into a tuple",
            "C": "Multiplies incoming argument values automatically",
            "D": "Unpacks dictionary key-value pairs into the scope"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Variable-length Arguments",
        "explanation": "*args collects excess positional arguments into a single tuple parameter."
    },
    {
        "subject": "python",
        "question": "What is the primary role of the Global Interpreter Lock (GIL) in CPython?",
        "options": {
            "A": "To accelerate GPU-based parallel tensor calculations",
            "B": "To ensure thread-safe memory management by allowing only one native thread to execute Python bytecode at a time",
            "C": "To compile Python source files directly into machine code",
            "D": "To prevent unauthorized network connections in standard sockets"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "CPython GIL Architecture",
        "explanation": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once."
    },
    {
        "subject": "python",
        "question": "What is the difference between copy.copy() and copy.deepcopy() in Python?",
        "options": {
            "A": "copy() works only on integers; deepcopy() works on strings",
            "B": "copy() creates a shallow copy sharing nested object references, while deepcopy() recursively clones nested objects",
            "C": "deepcopy() modifies original object IDs in place",
            "D": "copy() is faster because it saves data directly to secondary disk"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Shallow vs Deep Copy",
        "explanation": "A shallow copy constructs a new compound object and inserts references to existing items, whereas a deep copy duplicates child objects recursively."
    },
    {
        "subject": "python",
        "question": "In a Python try-except-finally block, when does the finally block execute?",
        "options": {
            "A": "Only when an unhandled exception is raised",
            "B": "Only when no exception occurs in the try block",
            "C": "Always, regardless of whether an exception occurred, was handled, or a return statement was hit",
            "D": "Exclusively when the program terminates abnormally"
        },
        "correct_answer": "C",
        "difficulty": "Medium",
        "concept": "Exception Handling Control Flow",
        "explanation": "The finally clause always executes before leaving the try statement, providing clean-up actions."
    },
    {
        "subject": "python",
        "question": "What is the purpose of the functools.wraps decorator when authoring custom decorators?",
        "options": {
            "A": "To convert the wrapped function into a static method",
            "B": "To preserve the original function's name, docstring, and metadata",
            "C": "To automatically serialize function arguments into JSON",
            "D": "To prevent recursion depth limit errors"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Decorator Metadata Preservation",
        "explanation": "functools.wraps copies the original function's __name__, __doc__, and other attributes to the wrapper function."
    },
    {
        "subject": "python",
        "question": "In Python class instantiation, which method is actually responsible for creating and returning the new instance before initialization?",
        "options": {
            "A": "__init__",
            "B": "__new__",
            "C": "__call__",
            "D": "__setup__"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Object Creation Lifecycle",
        "explanation": "__new__ is the static constructor that creates and returns the instance, while __init__ initializes that instance."
    },
    {
        "subject": "python",
        "question": "Which algorithm does Python employ to resolve method lookups in multiple inheritance hierarchies?",
        "options": {
            "A": "Dijkstra Shortest Path Search",
            "B": "C3 Linearization Algorithm",
            "C": "Depth-First Search with backtracking",
            "D": "A* Heuristic Tree Search"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Method Resolution Order (MRO)",
        "explanation": "Python 2.3+ uses the C3 Linearization algorithm to produce a monotonic Method Resolution Order (MRO) for multiple inheritance."
    },
    {
        "subject": "python",
        "question": "In Python descriptor protocol, what methods define a data descriptor?",
        "options": {
            "A": "__enter__ and __exit__",
            "B": "__get__ and either __set__ or __delete__",
            "C": "__iter__ and __next__",
            "D": "__repr__ and __str__"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Python Descriptors",
        "explanation": "A descriptor defining __set__() or __delete__() is a data descriptor, taking precedence over instance dictionary lookups."
    },
    {
        "subject": "python",
        "question": "How does CPython's garbage collector handle cyclical references between isolated objects?",
        "options": {
            "A": "Cyclical references are instantly collected via simple reference counting",
            "B": "A generational cyclic garbage collector identifies unreferenced cycles through periodic pointer traversal across 3 generations",
            "C": "CPython crashes when cyclical references occur",
            "D": "The OS kernel automatically reclaims cyclic memory on context switches"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Garbage Collection Architecture",
        "explanation": "While reference counting handles non-cyclic objects, a generational cyclic GC runs periodically to detect and isolate cyclic graphs."
    },
    {
        "subject": "python",
        "question": "In Python's asyncio cooperative multitasking framework, what yields control back to the event loop?",
        "options": {
            "A": "Calling time.sleep() directly",
            "B": "Awaiting a coroutine or future via the 'await' expression",
            "C": "Raising an unhandled KeyboardInterrupt",
            "D": "Spawning a native C thread"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Asyncio Event Loop Semantics",
        "explanation": "The 'await' keyword pauses the execution of the current coroutine and yields control back to the event loop until the awaited task completes."
    },
    {
        "subject": "python",
        "question": "What is the primary role of __slots__ in a Python class definition?",
        "options": {
            "A": "Enables multi-threading synchronization on instance methods",
            "B": "Replaces the dynamic instance __dict__ with a fixed array of attributes, drastically reducing memory overhead",
            "C": "Permits dynamic addition of undeclared attributes at runtime",
            "D": "Forces all attribute values to be strictly typed integers"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Memory Optimization via __slots__",
        "explanation": "__slots__ avoids creating the __dict__ per instance, optimizing memory for classes with millions of instances."
    },
    {
        "subject": "python",
        "question": "When defining a custom Context Manager with __enter__ and __exit__, how can __exit__ suppress an exception raised within the with-block?",
        "options": {
            "A": "By setting exc_type = None",
            "B": "By returning True from the __exit__ method",
            "C": "By raising a StopIteration exception",
            "D": "Exceptions in with-blocks can never be suppressed"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Context Manager Protocol",
        "explanation": "If __exit__ returns True, Python silences the exception and continues normal execution immediately after the with-statement."
    },

    # =========================================================================
    # 2. DATA STRUCTURES (25 Questions: 8 Easy, 9 Medium, 8 Hard)
    # =========================================================================
    {
        "subject": "data_structures",
        "question": "What is the time complexity to access an element at a given index in a contiguous memory array?",
        "options": {
            "A": "O(1)",
            "B": "O(n)",
            "C": "O(log n)",
            "D": "O(n^2)"
        },
        "correct_answer": "A",
        "difficulty": "Easy",
        "concept": "Array Random Access",
        "explanation": "Arrays support instant O(1) random access via arithmetic offset calculation: Base + index * element_size."
    },
    {
        "subject": "data_structures",
        "question": "Which data structure operates strictly according to the Last-In, First-Out (LIFO) principle?",
        "options": {
            "A": "Queue",
            "B": "Stack",
            "C": "Array",
            "D": "Binary Tree"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Stack Operations",
        "explanation": "A Stack is a LIFO structure where both insertion and removal occur at the top."
    },
    {
        "subject": "data_structures",
        "question": "Which data structure operates strictly according to the First-In, First-Out (FIFO) principle?",
        "options": {
            "A": "Priority Queue",
            "B": "Stack",
            "C": "Queue",
            "D": "Hash Table"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Queue Operations",
        "explanation": "A standard Queue follows the FIFO principle: items are inserted at the rear and removed from the front."
    },
    {
        "subject": "data_structures",
        "question": "In a singly linked list, what is the time complexity to insert a new node at the very beginning (head)?",
        "options": {
            "A": "O(1)",
            "B": "O(n)",
            "C": "O(log n)",
            "D": "O(n^2)"
        },
        "correct_answer": "A",
        "difficulty": "Easy",
        "concept": "Linked List Head Insertion",
        "explanation": "Inserting at the head requires updating the new node's next pointer and pointing head to it in constant time O(1)."
    },
    {
        "subject": "data_structures",
        "question": "In tree data structures, what is a node that does not have any children called?",
        "options": {
            "A": "Root node",
            "B": "Leaf node",
            "C": "Internal node",
            "D": "Ancestor node"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Tree Terminology",
        "explanation": "A leaf node is any terminal node with a degree of 0 (no child nodes)."
    },
    {
        "subject": "data_structures",
        "question": "What is the best-case time complexity of Linear Search in an array of size n?",
        "options": {
            "A": "O(n)",
            "B": "O(1)",
            "C": "O(log n)",
            "D": "O(n^2)"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Linear Search Best-Case",
        "explanation": "In the best case, the target element is at the first index inspected, taking O(1) time."
    },
    {
        "subject": "data_structures",
        "question": "What is a mandatory prerequisite before Binary Search can be executed on an array?",
        "options": {
            "A": "The array must contain only positive integers",
            "B": "The array elements must be sorted in order",
            "C": "The array size must be a power of two",
            "D": "The array cannot contain duplicate items"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Binary Search Precondition",
        "explanation": "Binary Search compares middle elements and discards half the space, requiring elements to be sorted."
    },
    {
        "subject": "data_structures",
        "question": "In asymptotic analysis, what does Big-O notation (O) primarily represent?",
        "options": {
            "A": "Exact execution time in milliseconds",
            "B": "Asymptotic upper bound of growth rate",
            "C": "Strict lower bound of time complexity",
            "D": "Average hardware instruction count"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Big-O Asymptotic Upper Bound",
        "explanation": "Big-O notation describes the upper bound on the asymptotic growth rate of an algorithm."
    },
    {
        "subject": "data_structures",
        "question": "Which tree traversal algorithm applied to a Binary Search Tree (BST) visits keys in ascending sorted order?",
        "options": {
            "A": "Pre-order traversal",
            "B": "In-order traversal",
            "C": "Post-order traversal",
            "D": "Level-order traversal"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "BST In-Order Traversal",
        "explanation": "In a BST, Left < Root < Right. In-order traversal (Left, Root, Right) processes nodes in sorted order."
    },
    {
        "subject": "data_structures",
        "question": "Which data structure is most appropriate for checking balanced parentheses in a mathematical expression?",
        "options": {
            "A": "Queue",
            "B": "Stack",
            "C": "Heap",
            "D": "Hash Map"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Bracket Matching via Stack",
        "explanation": "A stack naturally pairs the most recently opened bracket with the next closing bracket using LIFO order."
    },
    {
        "subject": "data_structures",
        "question": "In an AVL tree, what is the valid balance factor (height of left minus right subtree) allowed for every node?",
        "options": {
            "A": "Strictly 0",
            "B": "-1, 0, or +1",
            "C": "Between -2 and +2",
            "D": "Any positive integer"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "AVL Tree Balance Factor",
        "explanation": "An AVL tree is strictly height-balanced: height difference between left and right subtrees cannot exceed 1."
    },
    {
        "subject": "data_structures",
        "question": "In open addressing hash tables, how does Linear Probing resolve a collision at index k?",
        "options": {
            "A": "By attaching a singly linked list at bucket k",
            "B": "By sequentially probing slots (k + 1, k + 2, ...) modulo table capacity",
            "C": "By immediately doubling the table capacity",
            "D": "By computing a secondary cryptographic hash"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Linear Probing Collision Resolution",
        "explanation": "Linear probing inspects consecutive buckets sequentially until an unoccupied slot is located."
    },
    {
        "subject": "data_structures",
        "question": "What is the time complexity to extract (delete) the minimum element from a Binary Min-Heap of n elements?",
        "options": {
            "A": "O(1)",
            "B": "O(log n)",
            "C": "O(n)",
            "D": "O(n log n)"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Heap Extract-Min",
        "explanation": "Removing the root takes O(1), and restoring the heap property by sifting down takes tree height time: O(log n)."
    },
    {
        "subject": "data_structures",
        "question": "What is the worst-case time complexity of Merge Sort when sorting an array of size n?",
        "options": {
            "A": "O(n)",
            "B": "O(n log n)",
            "C": "O(n^2)",
            "D": "O(log n)"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Merge Sort Complexity",
        "explanation": "Merge sort divides in half log n times and merges with O(n) work per level, guaranteeing O(n log n) always."
    },
    {
        "subject": "data_structures",
        "question": "Under what condition does standard QuickSort degrade to its worst-case time complexity of O(n^2)?",
        "options": {
            "A": "When elements are randomized evenly",
            "B": "When the chosen pivot repeatedly partitions the array into maximally unbalanced sizes (0 and n-1)",
            "C": "When array size is a power of 2",
            "D": "When recursion is restricted to small sub-arrays"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "QuickSort Degeneracy",
        "explanation": "Unbalanced partitions (e.g., choosing the first element of an already sorted array as pivot) degrade QuickSort to O(n^2)."
    },
    {
        "subject": "data_structures",
        "question": "Which algorithmic design paradigm does Dijkstra's single-source shortest path algorithm employ?",
        "options": {
            "A": "Divide and Conquer",
            "B": "Greedy Strategy",
            "C": "Dynamic Programming",
            "D": "Branch and Bound"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Dijkstra Greedy Paradigm",
        "explanation": "Dijkstra's algorithm greedily extracts the unvisited vertex with the minimum tentative distance at each step."
    },
    {
        "subject": "data_structures",
        "question": "What is the recurrence relation describing standard Binary Search on an array of size n?",
        "options": {
            "A": "T(n) = 2T(n/2) + O(n)",
            "B": "T(n) = T(n/2) + O(1)",
            "C": "T(n) = T(n-1) + O(1)",
            "D": "T(n) = 2T(n/2) + O(1)"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Binary Search Recurrence",
        "explanation": "Binary Search compares middle element in O(1) and recurses on only one half of size n/2: T(n) = T(n/2) + O(1)."
    },
    {
        "subject": "data_structures",
        "question": "In Red-Black Trees, what property guarantees that the tree height remains bounded by 2 * log2(n + 1)?",
        "options": {
            "A": "Every non-leaf node must have exactly two non-null children",
            "B": "Every path from any node to its descendant null leaves contains the exact same number of black nodes",
            "C": "All red nodes must reside in the right subtree",
            "D": "The tree depth is recomputed after every search"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Red-Black Tree Black-Height",
        "explanation": "Uniform black height combined with the restriction against consecutive red nodes bounds maximum tree height to 2 * log2(n+1)."
    },
    {
        "subject": "data_structures",
        "question": "Which tree data structure achieves O(L) retrieval and prefix matching for strings of length L independent of total dictionary size N?",
        "options": {
            "A": "Splay Tree",
            "B": "Trie (Prefix Tree)",
            "C": "B+ Tree",
            "D": "Treap"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Trie Data Structure",
        "explanation": "A Trie navigates edge characters sequentially, matching prefixes in O(L) time regardless of total stored strings N."
    },
    {
        "subject": "data_structures",
        "question": "When a dynamic array doubles its buffer capacity upon becoming full, what is the amortized cost per insertion?",
        "options": {
            "A": "O(n)",
            "B": "O(log n)",
            "C": "O(1) amortized",
            "D": "O(n log n)"
        },
        "correct_answer": "C",
        "difficulty": "Hard",
        "concept": "Amortized Array Insertion",
        "explanation": "Geometric doubling amortizes the occasional O(n) reallocation cost over n preceding insertions, giving O(1) amortized time."
    },
    {
        "subject": "data_structures",
        "question": "Which algorithm computes the shortest path between all pairs of vertices in a weighted graph in O(V^3) time using dynamic programming?",
        "options": {
            "A": "Dijkstra's Algorithm",
            "B": "Prim's Algorithm",
            "C": "Floyd-Warshall Algorithm",
            "D": "Kruskal's Algorithm"
        },
        "correct_answer": "C",
        "difficulty": "Hard",
        "concept": "Floyd-Warshall Algorithm",
        "explanation": "Floyd-Warshall uses a 3-loop dynamic programming recurrence: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) in O(V^3)."
    },
    {
        "subject": "data_structures",
        "question": "Which single-source shortest path algorithm handles negative edge weights and detects reachable negative cycles?",
        "options": {
            "A": "Dijkstra's Algorithm",
            "B": "Bellman-Ford Algorithm",
            "C": "Breadth-First Search (BFS)",
            "D": "A* Search"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Bellman-Ford Algorithm",
        "explanation": "Bellman-Ford relaxes edges |V|-1 times; a further relaxation that reduces distance proves the presence of a negative cycle."
    },
    {
        "subject": "data_structures",
        "question": "What is the time complexity of building a Binary Heap from an arbitrary array of n elements using bottom-up heapify?",
        "options": {
            "A": "O(n log n)",
            "B": "O(n)",
            "C": "O(n^2)",
            "D": "O(log n)"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Bottom-Up Heapify Complexity",
        "explanation": "Bottom-up heap construction runs in linear O(n) time because the sum of heights across nodes converges mathematically to O(n)."
    },
    {
        "subject": "data_structures",
        "question": "In algorithm design, what two fundamental properties must a problem exhibit to be solvable via Dynamic Programming?",
        "options": {
            "A": "Greedy choice property and divide-and-conquer symmetry",
            "B": "Optimal substructure and overlapping subproblems",
            "C": "Independent subproblems and polynomial verification",
            "D": "Asymptotic linearity and monotonic recurrence"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Dynamic Programming Foundations",
        "explanation": "Dynamic Programming requires optimal substructure (optimal solution contains optimal sub-solutions) and overlapping subproblems."
    },
    {
        "subject": "data_structures",
        "question": "What does Kahn's algorithm compute on a Directed Acyclic Graph (DAG) by repeatedly queueing vertices with in-degree 0?",
        "options": {
            "A": "Minimum Spanning Tree",
            "B": "Topological Sort",
            "C": "Strongly Connected Components",
            "D": "Maximum Network Flow"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Kahn's Topological Sort",
        "explanation": "Kahn's algorithm removes in-degree 0 nodes iteratively to generate a valid topological dependency sequence in O(V + E)."
    },

    # =========================================================================
    # 3. COMPUTER ORGANIZATION AND ARCHITECTURE (20 Questions: 7 Easy, 7 Med, 6 Hard)
    # =========================================================================
    {
        "subject": "coa",
        "question": "Which component of an operating system runs with highest privilege and directly manages core CPU, memory, and devices?",
        "options": {
            "A": "Shell",
            "B": "Kernel",
            "C": "Compiler",
            "D": "Device Manager GUI"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "OS Kernel",
        "explanation": "The kernel is the foundational core of the OS that operates in privileged supervisor mode and arbitrates physical hardware."
    },
    {
        "subject": "coa",
        "question": "Which of the following computer memory technologies retains its stored data without electric power?",
        "options": {
            "A": "SRAM",
            "B": "DRAM",
            "C": "ROM",
            "D": "CPU Registers"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Non-Volatile Memory",
        "explanation": "ROM (Read-Only Memory) is non-volatile and permanently stores essential boot firmware without continuous electric power."
    },
    {
        "subject": "coa",
        "question": "What are the three fundamental cyclic phases executed by a CPU for every machine instruction?",
        "options": {
            "A": "Compile, Link, Run",
            "B": "Fetch, Decode, Execute",
            "C": "Input, Process, Output",
            "D": "Read, Verify, Commit"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Instruction Execution Cycle",
        "explanation": "The CPU instruction cycle fundamentally repeats: Fetching opcode from memory, Decoding instruction signals, and Executing the operation."
    },
    {
        "subject": "coa",
        "question": "Which CPU register specifically holds the memory address of the next instruction waiting to be fetched?",
        "options": {
            "A": "Instruction Register (IR)",
            "B": "Accumulator (ACC)",
            "C": "Program Counter (PC)",
            "D": "Memory Data Register (MDR)"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Program Counter Register",
        "explanation": "The Program Counter (PC) stores the memory location of the next sequential instruction to be fetched."
    },
    {
        "subject": "coa",
        "question": "What is the primary computer architecture reason for incorporating Cache Memory?",
        "options": {
            "A": "To increase permanent secondary storage capacity",
            "B": "To bridge the speed and latency gap between fast CPU registers and slower main memory (DRAM)",
            "C": "To provide error-correcting storage for CPU microcode",
            "D": "To enable multi-threading on single-core processors"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Cache Memory Purpose",
        "explanation": "SRAM caches exploit temporal and spatial locality to drastically reduce average memory access latency for CPU registers."
    },
    {
        "subject": "coa",
        "question": "Which CPU register holds the instruction that was most recently fetched from memory during decoding?",
        "options": {
            "A": "Memory Address Register (MAR)",
            "B": "Instruction Register (IR)",
            "C": "Program Counter (PC)",
            "D": "Stack Pointer (SP)"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Instruction Register",
        "explanation": "Once fetched from memory via the MDR, the machine instruction is placed in the Instruction Register (IR) for decoding."
    },
    {
        "subject": "coa",
        "question": "In computer arithmetic, what representation is universally used by modern digital systems to store signed integers?",
        "options": {
            "A": "Sign-Magnitude Representation",
            "B": "Two's Complement Representation",
            "C": "One's Complement Representation",
            "D": "Excess-128 Biased Format"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Signed Number Representation",
        "explanation": "Two's complement is standard because addition and subtraction circuitry are identical, and it eliminates duplicate representations of zero (+0 and -0)."
    },
    {
        "subject": "coa",
        "question": "In CPU addressing modes, what is the effective address of the operand in Immediate Addressing?",
        "options": {
            "A": "The address specified in the base register",
            "B": "There is no memory address; the operand itself is stored directly within the instruction",
            "C": "The memory location pointed to by the program counter",
            "D": "The top of the hardware stack"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Immediate Addressing Mode",
        "explanation": "In immediate addressing, the operand value is part of the instruction itself (e.g., ADD R1, #5), requiring no memory lookup."
    },
    {
        "subject": "coa",
        "question": "What algorithm is used in digital multipliers to efficiently multiply signed binary numbers in two's complement?",
        "options": {
            "A": "Dijkstra's Algorithm",
            "B": "Booth's Multiplication Algorithm",
            "C": "Huffman Coding Algorithm",
            "D": "Horner's Rule"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Booth's Algorithm",
        "explanation": "Booth's algorithm inspects pairs of adjacent bits to speed up multiplication of signed binary numbers by reducing addition steps."
    },
    {
        "subject": "coa",
        "question": "What is the primary difference between a hardwired control unit and a microprogrammed control unit?",
        "options": {
            "A": "Hardwired units use ROM microcode; microprogrammed units use fixed logic gates",
            "B": "Hardwired units use combinational logic gates for maximum speed; microprogrammed units execute microinstructions stored in control memory for flexibility",
            "C": "Microprogrammed units are faster than hardwired units",
            "D": "Hardwired units cannot be used in RISC architectures"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Hardwired vs Microprogrammed Control",
        "explanation": "Hardwired control relies on fixed logic gates and flip-flops for speed, while microprogrammed control interprets microcode from control memory."
    },
    {
        "subject": "coa",
        "question": "What event triggers a page fault in a computer system utilizing virtual memory with paging?",
        "options": {
            "A": "A division by zero arithmetic error",
            "B": "Access attempt to a virtual page whose valid/present bit in the page table is 0 (not loaded in physical RAM)",
            "C": "A tag mismatch in the L1 instruction cache",
            "D": "Physical hard drive capacity being exhausted"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Virtual Memory Page Fault",
        "explanation": "A page fault interrupt occurs when the MMU references a virtual page that is currently swapped out to secondary storage."
    },
    {
        "subject": "coa",
        "question": "In Round-Robin CPU scheduling, what happens if the time quantum is configured to be arbitrarily large?",
        "options": {
            "A": "The system experiences severe thrashing",
            "B": "It degenerates into First-Come, First-Served (FCFS) scheduling",
            "C": "Shortest Job First (SJF) behavior is emulated",
            "D": "Context switching frequency increases uncontrollably"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Round-Robin Scheduling Quantum",
        "explanation": "When the quantum exceeds any process CPU burst, each process runs to completion without preemption, matching FCFS."
    },
    {
        "subject": "coa",
        "question": "What phenomenon occurs when a computer spends more time swapping virtual pages to disk than executing useful CPU instructions?",
        "options": {
            "A": "Starvation",
            "B": "Thrashing",
            "C": "Belady's Anomaly",
            "D": "Aging"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Virtual Memory Thrashing",
        "explanation": "Thrashing arises when total active working sets exceed physical RAM, causing continuous page faults and disk I/O thrashing."
    },
    {
        "subject": "coa",
        "question": "Which of the following conditions is NOT one of Coffman's four mandatory conditions for a deadlock to occur?",
        "options": {
            "A": "Mutual Exclusion",
            "B": "Hold and Wait",
            "C": "No Preemption",
            "D": "Preemptive Scheduling"
        },
        "correct_answer": "D",
        "difficulty": "Medium",
        "concept": "Coffman Deadlock Conditions",
        "explanation": "The 4 conditions are Mutual Exclusion, Hold & Wait, No Preemption, and Circular Wait. Preemptive scheduling prevents deadlock."
    },
    {
        "subject": "coa",
        "question": "In pipelined CPU architectures, what type of hazard occurs when an instruction depends on the result of an earlier uncommitted instruction?",
        "options": {
            "A": "Structural Hazard",
            "B": "Data Hazard (Read-After-Write / RAW)",
            "C": "Control Hazard",
            "D": "Branch Delay Hazard"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Pipeline Data Hazards",
        "explanation": "RAW data hazards occur when an instruction reads an operand before a preceding instruction finishes writing it, resolved via forwarding or stalls."
    },
    {
        "subject": "coa",
        "question": "In CPU cache design, why is an N-way Set Associative cache preferred over a Direct-Mapped cache?",
        "options": {
            "A": "It completely eliminates the need for replacement algorithms",
            "B": "It significantly reduces conflict misses by providing N locations in a set where a memory block can reside",
            "C": "It operates with zero tag comparison hardware overhead",
            "D": "It decreases hit time to less than a single clock cycle"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Set-Associative Cache Design",
        "explanation": "Set associativity allows N cache lines per set, preventing ping-pong conflict thrashing seen in direct-mapped caches."
    },
    {
        "subject": "coa",
        "question": "What is the primary architectural function of the Translation Lookaside Buffer (TLB) in CPU memory management units?",
        "options": {
            "A": "To store dirty bits for disk block caching",
            "B": "To act as a high-speed hardware cache for recent virtual-to-physical address translations",
            "C": "To buffer interrupt requests from high-priority peripherals",
            "D": "To synchronize cache coherence across multi-core processors"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Translation Lookaside Buffer",
        "explanation": "The TLB caches recent virtual page number to physical frame mappings, avoiding multi-level page table lookups on TLB hits."
    },
    {
        "subject": "coa",
        "question": "In an Inverted Page Table architecture, how is the total number of entries in the table determined?",
        "options": {
            "A": "By the size of the virtual address space divided by page size",
            "B": "By the number of physical frames present in main memory (RAM)",
            "C": "By the total number of running processes multiplied by thread count",
            "D": "By the capacity of the swap partition on secondary storage"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Inverted Page Table Sizing",
        "explanation": "An inverted page table has exactly one entry per physical frame of RAM rather than per virtual page, drastically reducing table size."
    },
    {
        "subject": "coa",
        "question": "What microarchitectural structure is maintained by modern CPUs to cache target addresses of taken branches for immediate next-PC lookup?",
        "options": {
            "A": "Translation Lookaside Buffer (TLB)",
            "B": "Branch Target Buffer (BTB)",
            "C": "Return Address Stack (RAS)",
            "D": "Store Buffer"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Branch Target Buffer (BTB)",
        "explanation": "The BTB caches predicted branch target instruction addresses so the fetch unit can retrieve target instructions without pipeline bubbles."
    },
    {
        "subject": "coa",
        "question": "What is Belady's Anomaly observed in virtual memory page replacement algorithms?",
        "options": {
            "A": "Least Recently Used (LRU) evicts the most frequently referenced page",
            "B": "Allocating more physical page frames results in an increase in page faults under FIFO replacement",
            "C": "Clock algorithm performs worse than random replacement on thrashing workloads",
            "D": "Dirty pages cannot be written back to disk during heavy paging"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Belady's Anomaly in Paging",
        "explanation": "Belady's Anomaly describes the counter-intuitive situation where increasing physical memory frames yields more page faults under FIFO."
    },

    # =========================================================================
    # 4. DISCRETE STRUCTURES AND THEORY OF LOGIC (20 Questions: 7 Easy, 7 Med, 6 Hard)
    # =========================================================================
    {
        "subject": "dstl",
        "question": "In propositional logic, what is a compound proposition that is always true for every truth assignment called?",
        "options": {
            "A": "Contradiction",
            "B": "Tautology",
            "C": "Contingency",
            "D": "Fallacy"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Tautology Definition",
        "explanation": "A tautology is a compound propositional statement that evaluates to True under every possible truth assignment."
    },
    {
        "subject": "dstl",
        "question": "What is the truth value of the logical conjunction P ∧ Q when P is True and Q is False?",
        "options": {
            "A": "True",
            "B": "False",
            "C": "Undefined",
            "D": "Tautological"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Logical Conjunction",
        "explanation": "The conjunction P ∧ Q is True if and only if both P and Q are True. If Q is False, P ∧ Q is False."
    },
    {
        "subject": "dstl",
        "question": "What is the cardinality of the empty set (null set Ø)?",
        "options": {
            "A": "1",
            "B": "0",
            "C": "Undefined",
            "D": "Infinite"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Set Cardinality",
        "explanation": "The empty set contains no elements, so its cardinality |Ø| is exactly 0."
    },
    {
        "subject": "dstl",
        "question": "If a finite set S has n elements, what is the cardinality of its Power Set P(S)?",
        "options": {
            "A": "n^2",
            "B": "2^n",
            "C": "n!",
            "D": "2n"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Power Set Cardinality",
        "explanation": "Each element in S has two choices (included or excluded) in any subset, producing exactly 2^n total subsets."
    },
    {
        "subject": "dstl",
        "question": "Under what condition is a binary relation R on set A classified as symmetric for all a, b in A?",
        "options": {
            "A": "(a, a) ∈ R",
            "B": "(a, b) ∈ R implies (b, a) ∈ R",
            "C": "(a, b) ∈ R and (b, c) ∈ R implies (a, c) ∈ R",
            "D": "(a, b) ∈ R and (b, a) ∈ R implies a = b"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Symmetric Relations",
        "explanation": "A relation is symmetric if whenever an ordered pair (a, b) belongs to R, the reverse pair (b, a) also belongs to R."
    },
    {
        "subject": "dstl",
        "question": "What is a function f: A → B called if it is both one-to-one (injective) and onto (surjective)?",
        "options": {
            "A": "Homomorphism",
            "B": "Bijection (one-to-one correspondence)",
            "C": "Isomorphism only on groups",
            "D": "Endomorphism"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Bijective Functions",
        "explanation": "A bijection is both injective (each output has at most one pre-image) and surjective (every codomain element is mapped)."
    },
    {
        "subject": "dstl",
        "question": "If k + 1 or more objects are placed into k boxes, then at least one box contains two or more objects. What is this theorem known as?",
        "options": {
            "A": "Fermat's Little Theorem",
            "B": "Pigeonhole Principle",
            "C": "Binomial Theorem",
            "D": "Euclid's Division Lemma"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Pigeonhole Principle",
        "explanation": "The Pigeonhole Principle states that distributing more items than bins guarantees at least one bin holds multiple items."
    },
    {
        "subject": "dstl",
        "question": "To be classified as an Equivalence Relation, what three properties must a binary relation satisfy?",
        "options": {
            "A": "Reflexive, Antisymmetric, Transitive",
            "B": "Reflexive, Symmetric, Transitive",
            "C": "Irreflexive, Symmetric, Intransitive",
            "D": "Asymmetric, Transitive, Complete"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Equivalence Relations",
        "explanation": "An equivalence relation partitions a set into disjoint equivalence classes, requiring reflexivity, symmetry, and transitivity."
    },
    {
        "subject": "dstl",
        "question": "What three properties define a Partially Ordered Set (Poset)?",
        "options": {
            "A": "Reflexive, Symmetric, Transitive",
            "B": "Reflexive, Antisymmetric, Transitive",
            "C": "Irreflexive, Asymmetric, Transitive",
            "D": "Symmetric, Antisymmetric, Equipotent"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Partially Ordered Sets (Poset)",
        "explanation": "A partial order relation (Poset) must be reflexive, antisymmetric (aRb and bRa implies a=b), and transitive."
    },
    {
        "subject": "dstl",
        "question": "What visual graph diagram represents finite partially ordered sets without showing redundant reflexive loops or transitive edges?",
        "options": {
            "A": "Venn Diagram",
            "B": "Hasse Diagram",
            "C": "K-Map",
            "D": "Euler Diagram"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Hasse Diagrams",
        "explanation": "A Hasse diagram displays poset covers as upward directed edges, omitting self-loops (reflexivity) and transitive edges."
    },
    {
        "subject": "dstl",
        "question": "Which classical rule of logical inference states: 'If P is true, and P implies Q is true, then Q must be true'?",
        "options": {
            "A": "Modus Tollens",
            "B": "Modus Ponens",
            "C": "Hypothetical Syllogism",
            "D": "Disjunctive Syllogism"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Modus Ponens",
        "explanation": "Modus Ponens (the law of detachment) states: [P ∧ (P → Q)] → Q."
    },
    {
        "subject": "dstl",
        "question": "According to the Handshaking Lemma in graph theory, what is the sum of degrees of all vertices in an undirected graph G = (V, E)?",
        "options": {
            "A": "|E|",
            "B": "2 * |E|",
            "C": "|V| * |E|",
            "D": "|E| / 2"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Handshaking Lemma",
        "explanation": "Each edge connects two vertices and contributes exactly 2 to the sum of degrees: ∑ deg(v) = 2|E|."
    },
    {
        "subject": "dstl",
        "question": "In planar graph theory, what is Euler's Formula relating vertices (V), edges (E), and faces (F) for any connected planar graph?",
        "options": {
            "A": "V + E - F = 2",
            "B": "V - E + F = 2",
            "C": "V - E - F = 1",
            "D": "V + E + F = 0"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Euler Planar Formula",
        "explanation": "Euler's formula states that for any connected planar graph, V - E + F = 2."
    },
    {
        "subject": "dstl",
        "question": "What is a compound Boolean proposition expressed as a disjunction of elementary conjunctions (minterms) called?",
        "options": {
            "A": "Conjunctive Normal Form (CNF)",
            "B": "Disjunctive Normal Form (DNF)",
            "C": "Prenex Normal Form",
            "D": "Skolem Normal Form"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Disjunctive Normal Form",
        "explanation": "Disjunctive Normal Form (DNF) is an OR of AND terms (sum of products)."
    },
    {
        "subject": "dstl",
        "question": "In lattice theory, what formal mathematical condition must a poset (L, ≤) satisfy to be classified as a Lattice?",
        "options": {
            "A": "Every chain must have a prime number of elements",
            "B": "Every pair of elements must have a unique Least Upper Bound (join) and a unique Greatest Lower Bound (meet)",
            "C": "The poset must contain no cycles of length greater than 3",
            "D": "All elements must be comparable under the partial order"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Lattice Theory Definition",
        "explanation": "A lattice is a poset where every two-element subset {a, b} has a unique supremum (LUB: a ∨ b) and infimum (GLB: a ∧ b)."
    },
    {
        "subject": "dstl",
        "question": "What is the characteristic equation used to solve the linear homogeneous recurrence relation: a_n = 5*a_{n-1} - 6*a_{n-2}?",
        "options": {
            "A": "r^2 + 5r + 6 = 0",
            "B": "r^2 - 5r + 6 = 0",
            "C": "r^2 - 6r + 5 = 0",
            "D": "r^2 + 6r - 5 = 0"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Homogeneous Recurrence Relations",
        "explanation": "Substituting a_n = r^n gives r^2 - 5r + 6 = 0, with characteristic roots r = 2 and r = 3."
    },
    {
        "subject": "dstl",
        "question": "According to Kuratowski's Theorem, a graph is planar if and only if it does not contain a subgraph homeomorphic to which two graphs?",
        "options": {
            "A": "K3 and K3,3",
            "B": "K5 and K3,3",
            "C": "K4 and K2,3",
            "D": "K6 and K4,4"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Kuratowski Planarity Theorem",
        "explanation": "Kuratowski's theorem characterizes planar graphs: a graph is planar iff it contains no subdivision of K5 (complete graph on 5 vertices) or K3,3 (utility graph)."
    },
    {
        "subject": "dstl",
        "question": "In predicate logic, what is the valid logical equivalence for the negation of a universally quantified statement ¬∀x P(x)?",
        "options": {
            "A": "∀x ¬P(x)",
            "B": "∃x ¬P(x)",
            "C": "¬∃x P(x)",
            "D": "∃x P(x)"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "De Morgan's Laws for Quantifiers",
        "explanation": "Not all x satisfy P(x) is logically equivalent to saying there exists at least one x that does not satisfy P(x): ¬∀x P(x) ≡ ∃x ¬P(x)."
    },
    {
        "subject": "dstl",
        "question": "According to the Principle of Inclusion-Exclusion for three finite sets A, B, and C, what is |A ∪ B ∪ C|?",
        "options": {
            "A": "|A| + |B| + |C|",
            "B": "|A| + |B| + |C| - |A ∩ B| - |B ∩ C| - |A ∩ C| + |A ∩ B ∩ C|",
            "C": "|A| + |B| + |C| - |A ∩ B ∩ C|",
            "D": "|A| + |B| + |C| - |A ∩ B| - |B ∩ C| - |A ∩ C| - |A ∩ B ∩ C|"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Principle of Inclusion-Exclusion",
        "explanation": "To avoid over-counting, add singletons, subtract pairwise intersections, and add back the triple intersection."
    },
    {
        "subject": "dstl",
        "question": "In a Boolean Algebra (B, ∧, ∨, ¬, 0, 1), which property states that x ∨ (x ∧ y) = x?",
        "options": {
            "A": "Distributive Law",
            "B": "Absorption Law",
            "C": "De Morgan's Law",
            "D": "Idempotent Law"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Boolean Algebra Absorption Law",
        "explanation": "The absorption law states x ∨ (x ∧ y) = x and x ∧ (x ∨ y) = x."
    },

    # =========================================================================
    # 5. MATHEMATICS (20 Questions: 7 Easy, 7 Medium, 6 Hard)
    # =========================================================================
    {
        "subject": "mathematics",
        "question": "What is the rank of an m × n Zero Matrix (a matrix where all entries are 0)?",
        "options": {
            "A": "1",
            "B": "0",
            "C": "min(m, n)",
            "D": "Undefined"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Matrix Rank",
        "explanation": "The rank of a matrix is the maximum number of linearly independent row/column vectors. For a zero matrix, rank is 0."
    },
    {
        "subject": "mathematics",
        "question": "What is the first derivative of f(x) = sin(x) with respect to x?",
        "options": {
            "A": "-cos(x)",
            "B": "cos(x)",
            "C": "-sin(x)",
            "D": "tan(x)"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Differential Calculus",
        "explanation": "By standard calculus rules, d/dx [sin(x)] = cos(x)."
    },
    {
        "subject": "mathematics",
        "question": "What is the value of the standard limit: lim (x → 0) [sin(x) / x]?",
        "options": {
            "A": "0",
            "B": "1",
            "C": "Infinity",
            "D": "Does not exist"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Calculus Limits",
        "explanation": "Using L'Hôpital's rule or geometric trigonometric squeeze theorem, lim (x → 0) [sin(x) / x] = 1."
    },
    {
        "subject": "mathematics",
        "question": "What is the determinant of an n × n Identity Matrix I_n?",
        "options": {
            "A": "0",
            "B": "1",
            "C": "n",
            "D": "n!"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Identity Matrix Determinant",
        "explanation": "The determinant of an identity matrix is the product of its diagonal 1s, which equals 1."
    },
    {
        "subject": "mathematics",
        "question": "What is the probability of an impossible event in classical probability theory?",
        "options": {
            "A": "1",
            "B": "0",
            "C": "-1",
            "D": "0.5"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Probability Axioms",
        "explanation": "By Kolmogorov's probability axioms, P(Ø) = 0 for an event with zero favorable outcomes."
    },
    {
        "subject": "mathematics",
        "question": "A square matrix A is called Symmetric if which matrix relation holds?",
        "options": {
            "A": "A^T = -A",
            "B": "A^T = A",
            "C": "A * A^T = I",
            "D": "det(A) = 0"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Symmetric Matrices",
        "explanation": "A matrix is symmetric when it equals its transpose: A^T = A (a_ij = a_ji)."
    },
    {
        "subject": "mathematics",
        "question": "What is the indefinite integral ∫ e^(2x) dx?",
        "options": {
            "A": "2 * e^(2x) + C",
            "B": "(1/2) * e^(2x) + C",
            "C": "e^(2x) + C",
            "D": "(1/4) * e^(2x) + C"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Integral Calculus",
        "explanation": "Using substitution u = 2x, du = 2 dx gives (1/2) * e^(2x) + C."
    },
    {
        "subject": "mathematics",
        "question": "What are the eigenvalues of an upper or lower triangular matrix?",
        "options": {
            "A": "The sums of the row elements",
            "B": "The entries along the main diagonal",
            "C": "Strictly 0 and 1",
            "D": "The determinants of the 2x2 sub-matrices"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Triangular Matrix Eigenvalues",
        "explanation": "The characteristic polynomial det(A - λI) of a triangular matrix is the product of (a_ii - λ), so eigenvalues are its diagonal entries."
    },
    {
        "subject": "mathematics",
        "question": "Which fundamental theorem of linear algebra asserts that every square matrix satisfies its own characteristic polynomial equation?",
        "options": {
            "A": "Cramer's Rule",
            "B": "Cayley-Hamilton Theorem",
            "C": "Gauss-Jordan Elimination",
            "D": "Spectral Theorem"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Cayley-Hamilton Theorem",
        "explanation": "The Cayley-Hamilton theorem states that if p(λ) = det(A - λI) is the characteristic polynomial of A, then p(A) = 0."
    },
    {
        "subject": "mathematics",
        "question": "In probability theory, what does Bayes' Theorem state for conditional probability P(A|B)?",
        "options": {
            "A": "P(A|B) = P(A) * P(B)",
            "B": "P(A|B) = [P(B|A) * P(A)] / P(B)",
            "C": "P(A|B) = P(A ∩ B) * P(B)",
            "D": "P(A|B) = P(A) + P(B) - P(B|A)"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Bayes' Theorem",
        "explanation": "Bayes' Theorem updates the prior probability P(A) given evidence B: P(A|B) = [P(B|A) * P(A)] / P(B)."
    },
    {
        "subject": "mathematics",
        "question": "In a Poisson distribution with parameter λ, what is the mathematical relationship between the mean and the variance?",
        "options": {
            "A": "Variance = (Mean)^2",
            "B": "Mean = Variance = λ",
            "C": "Variance = λ * (1 - p)",
            "D": "Mean = 2 * Variance"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Poisson Distribution Properties",
        "explanation": "A distinguishing characteristic of the Poisson distribution is that both its expected value (mean) and variance equal λ."
    },
    {
        "subject": "mathematics",
        "question": "What condition must a real-valued function f(x) satisfy on [a, b] to guarantee the application of Rolle's Theorem?",
        "options": {
            "A": "f(a) = f(b), continuous on [a, b], and differentiable on (a, b)",
            "B": "f(x) must be strictly increasing on [a, b]",
            "C": "The second derivative f''(x) must be zero everywhere",
            "D": "f(x) must be a polynomial of degree at most 2"
        },
        "correct_answer": "A",
        "difficulty": "Medium",
        "concept": "Rolle's Theorem Conditions",
        "explanation": "Rolle's Theorem requires continuity on [a, b], differentiability on (a, b), and f(a) = f(b) to ensure ∃ c ∈ (a, b) where f'(c) = 0."
    },
    {
        "subject": "mathematics",
        "question": "Under what algebraic condition is a real square matrix Q defined as Orthogonal?",
        "options": {
            "A": "Q * Q^T = 0",
            "B": "Q^T * Q = I (so Q^(-1) = Q^T)",
            "C": "det(Q) = 0",
            "D": "Q^T = -Q"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Orthogonal Matrices",
        "explanation": "A matrix is orthogonal if its transpose equals its inverse: Q^T * Q = I, preserving vector lengths and inner products."
    },
    {
        "subject": "mathematics",
        "question": "What is the Taylor series expansion of e^x centered at x = 0 (Maclaurin series)?",
        "options": {
            "A": "∑ (x^n / n!) for n = 0 to ∞",
            "B": "∑ ((-1)^n * x^n / n) for n = 1 to ∞",
            "C": "∑ (x^(2n) / (2n)!) for n = 0 to ∞",
            "D": "∑ (x^n) for n = 0 to ∞"
        },
        "correct_answer": "A",
        "difficulty": "Medium",
        "concept": "Taylor and Maclaurin Series",
        "explanation": "e^x = 1 + x + x^2/2! + x^3/3! + ... = ∑ (x^n / n!)."
    },
    {
        "subject": "mathematics",
        "question": "According to the Rank-Nullity Theorem for a finite-dimensional linear transformation T: V -> W, what equation relates rank and nullity?",
        "options": {
            "A": "Rank(T) * Nullity(T) = dim(W)",
            "B": "Rank(T) + Nullity(T) = dim(V)",
            "C": "Rank(T) - Nullity(T) = dim(V)",
            "D": "Rank(T) + Nullity(T) = dim(W)"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Rank-Nullity Theorem",
        "explanation": "The fundamental theorem of linear transformations states dim(Image(T)) + dim(Kernel(T)) = dim(Domain(V))."
    },
    {
        "subject": "mathematics",
        "question": "Under what condition is an n × n matrix A guaranteed to be diagonalizable over the real numbers?",
        "options": {
            "A": "det(A) ≠ 0",
            "B": "A has n linearly independent eigenvectors",
            "C": "All entries in A are non-zero integers",
            "D": "A is skew-symmetric"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Matrix Diagonalization",
        "explanation": "A matrix A of size n × n is diagonalizable if and only if it possesses n linearly independent eigenvectors, forming P^-1 A P = D."
    },
    {
        "subject": "mathematics",
        "question": "At what points do the inflection points of the standard Normal Distribution probability density curve occur?",
        "options": {
            "A": "x = μ only",
            "B": "x = μ - σ and x = μ + σ",
            "C": "x = μ - 2σ and x = μ + 2σ",
            "D": "x = 0 and x = 1"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Normal Distribution Inflection Points",
        "explanation": "Setting the second derivative of the Gaussian PDF f''(x) = 0 yields the inflection points at exactly one standard deviation from the mean: μ ± σ."
    },
    {
        "subject": "mathematics",
        "question": "In multivariable calculus, what does the gradient vector ∇f of a scalar function f(x, y, z) represent at a point?",
        "options": {
            "A": "The tangent line where f equals zero",
            "B": "A vector pointing in the direction of maximum rate of increase of f, with magnitude equal to that rate",
            "C": "The total volume enclosed by the level surface",
            "D": "The curvature of the scalar field"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Gradient Vector Direction",
        "explanation": "The gradient ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z) points in the direction of steepest ascent, and ||∇f|| is the maximum directional derivative."
    },
    {
        "subject": "mathematics",
        "question": "What matrix composed of all first-order partial derivatives represents the best linear approximation of a vector-valued function f: R^n → R^m?",
        "options": {
            "A": "Hessian Matrix",
            "B": "Jacobian Matrix",
            "C": "Gram Matrix",
            "D": "Vandermonde Matrix"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Jacobian Matrix",
        "explanation": "The Jacobian matrix J contains the partial derivatives J_ij = ∂f_i / ∂x_j of a vector function."
    },
    {
        "subject": "mathematics",
        "question": "According to the Central Limit Theorem (CLT), what happens to the distribution of the normalized sum of n independent and identically distributed (i.i.d.) random variables with finite variance as n becomes large?",
        "options": {
            "A": "It degenerates into a uniform distribution",
            "B": "It converges in distribution to a standard Normal (Gaussian) distribution",
            "C": "It converges to a discrete Poisson distribution",
            "D": "It approaches an exponential decay curve"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Central Limit Theorem",
        "explanation": "The CLT guarantees that the standardized sum of i.i.d. random variables with finite variance approaches a standard normal distribution N(0, 1) as n → ∞."
    }
]
