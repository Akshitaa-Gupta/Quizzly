import re
import random
from difflib import SequenceMatcher

STANDARD_QUESTIONS = [
    # ==================== EASY QUESTIONS (1 - 25) ====================
    {
        "id": 1,
        "question": "In a singly linked list, what is the time complexity to insert a new node at the very beginning (head) of the list?",
        "options": {
            "A": "O(1)",
            "B": "O(n)",
            "C": "O(log n)",
            "D": "O(n^2)"
        },
        "correct_answer": "A",
        "difficulty": "Easy",
        "concept": "Singly Linked List Insertion",
        "explanation": "Inserting at the head only requires updating the new node's next pointer and pointing the head to the new node, which takes constant time O(1)."
    },
    {
        "id": 2,
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
        "explanation": "A Stack is a LIFO (Last-In, First-Out) data structure where elements are pushed and popped from the same end (the top)."
    },
    {
        "id": 3,
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
        "explanation": "A standard Queue follows the FIFO principle where elements are inserted at the rear and removed from the front."
    },
    {
        "id": 4,
        "question": "What is the time complexity to access an element at a given index in a standard contiguous memory array?",
        "options": {
            "A": "O(1)",
            "B": "O(n)",
            "C": "O(log n)",
            "D": "O(n log n)"
        },
        "correct_answer": "A",
        "difficulty": "Easy",
        "concept": "Array Random Access",
        "explanation": "Arrays support direct memory offset calculation: Address = Base_Address + index * element_size, allowing instant O(1) random access."
    },
    {
        "id": 5,
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
        "explanation": "A leaf node (or terminal node) is any node in a tree hierarchy that has an out-degree of 0, meaning it has no children."
    },
    {
        "id": 6,
        "question": "What is the best-case time complexity of Linear Search in an array of size n?",
        "options": {
            "A": "O(n)",
            "B": "O(1)",
            "C": "O(log n)",
            "D": "O(n^2)"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Linear Search Complexity",
        "explanation": "In the best case, the target element is located at the first index inspected, requiring only one comparison: O(1)."
    },
    {
        "id": 7,
        "question": "What is a mandatory prerequisite before Binary Search can be performed on an array?",
        "options": {
            "A": "The array must contain only positive numbers",
            "B": "The array elements must be sorted in order",
            "C": "The array size must be a power of two",
            "D": "The array must not contain duplicate values"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Binary Search Prerequisites",
        "explanation": "Binary Search repeatedly eliminates half of the remaining search space based on order comparisons, requiring elements to be sorted."
    },
    {
        "id": 8,
        "question": "In asymptotic analysis, what does Big-O notation (O) primarily describe for an algorithm?",
        "options": {
            "A": "Exact execution time in milliseconds",
            "B": "Lower bound of growth rate",
            "C": "Asymptotic upper bound of growth rate",
            "D": "Average hardware instruction count"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Asymptotic Notation",
        "explanation": "Big-O notation formally defines the asymptotic upper bound, representing the worst-case growth rate of time or memory as input size grows."
    },
    {
        "id": 9,
        "question": "Which component of an operating system runs with highest CPU privilege and directly manages core hardware resources?",
        "options": {
            "A": "Shell",
            "B": "Kernel",
            "C": "Compiler",
            "D": "Device Manager GUI"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Operating System Kernel",
        "explanation": "The kernel is the foundational core of the OS that executes in privileged kernel mode and directly arbitrates CPU, memory, and devices."
    },
    {
        "id": 10,
        "question": "Which of the following computer memory technologies retains its stored data even after electric power is turned off?",
        "options": {
            "A": "SRAM",
            "B": "DRAM",
            "C": "ROM",
            "D": "CPU Registers"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Non-Volatile Memory",
        "explanation": "ROM (Read-Only Memory) is non-volatile and permanently preserves essential firmware instructions (such as boot firmware) without continuous power."
    },
    {
        "id": 11,
        "question": "What data structure does the operating system maintain to store all control information and register state for an active process?",
        "options": {
            "A": "File Allocation Table (FAT)",
            "B": "Process Control Block (PCB)",
            "C": "Translation Lookaside Buffer (TLB)",
            "D": "Segment Map Table (SMT)"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Process Control Block",
        "explanation": "The Process Control Block (PCB) contains the process ID, state, program counter, CPU registers, memory limits, and open file lists."
    },
    {
        "id": 12,
        "question": "In operating system theory, what is the standard definition of a 'process'?",
        "options": {
            "A": "A source code file saved on a hard drive",
            "B": "A program loaded into memory and currently in execution",
            "C": "A hardware interrupt request from a device",
            "D": "A database query waiting for execution"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Process Definition",
        "explanation": "A program is passive code stored on disk, whereas a process is an active program instance currently in execution with dedicated memory space."
    },
    {
        "id": 13,
        "question": "In relational database design, what uniquely identifies each individual record in a database table?",
        "options": {
            "A": "Foreign Key",
            "B": "Candidate Attribute",
            "C": "Primary Key",
            "D": "Composite Index"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Primary Key in DBMS",
        "explanation": "A primary key is an attribute (or minimal set of attributes) chosen to uniquely identify each tuple in a relation, with values guaranteed to be unique and non-null."
    },
    {
        "id": 14,
        "question": "Which SQL statement is used to retrieve and query data from one or more database tables?",
        "options": {
            "A": "GET",
            "B": "SELECT",
            "C": "EXTRACT",
            "D": "RETRIEVE"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "SQL Query Basics",
        "explanation": "The SELECT statement is the standard SQL command used to query and return rows from relational tables."
    },
    {
        "id": 15,
        "question": "Which of the following is categorized as a Data Definition Language (DDL) command in SQL?",
        "options": {
            "A": "INSERT",
            "B": "UPDATE",
            "C": "CREATE",
            "D": "DELETE"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "DDL vs DML",
        "explanation": "DDL commands define and manage schema structures (e.g., CREATE, ALTER, DROP), while INSERT, UPDATE, and DELETE manipulate data (DML)."
    },
    {
        "id": 16,
        "question": "What is the primary function of a Foreign Key in a relational database?",
        "options": {
            "A": "To accelerate data insertion speed",
            "B": "To enforce referential integrity between two related tables",
            "C": "To encrypt sensitive table columns",
            "D": "To prevent duplicate column names"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Referential Integrity",
        "explanation": "A foreign key creates a link between records in two tables by ensuring that values in the child table match existing primary keys in the parent table."
    },
    {
        "id": 17,
        "question": "How many distinct layers are defined in the standard ISO/OSI networking reference model?",
        "options": {
            "A": "4",
            "B": "5",
            "C": "7",
            "D": "9"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "OSI Reference Model",
        "explanation": "The OSI model specifies 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application."
    },
    {
        "id": 18,
        "question": "What is the standard, default port assigned for unencrypted HTTP web server traffic?",
        "options": {
            "A": "21",
            "B": "25",
            "C": "80",
            "D": "443"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Standard Network Ports",
        "explanation": "Port 80 is the standard port reserved for unencrypted HTTP traffic, while HTTPS uses port 443."
    },
    {
        "id": 19,
        "question": "Which Internet protocol maps human-readable domain names (such as cse.college.edu) to IP addresses?",
        "options": {
            "A": "DHCP",
            "B": "DNS",
            "C": "FTP",
            "D": "SMTP"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Domain Name System",
        "explanation": "DNS (Domain Name System) functions as the directory of the Internet, translating user-friendly domain names into routable numerical IP addresses."
    },
    {
        "id": 20,
        "question": "At which layer of the OSI model does an IP router primarily make its packet forwarding decisions?",
        "options": {
            "A": "Physical Layer (Layer 1)",
            "B": "Data Link Layer (Layer 2)",
            "C": "Network Layer (Layer 3)",
            "D": "Transport Layer (Layer 4)"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Network Layer Routing",
        "explanation": "Routers operate at the Network Layer (Layer 3) to route packets across subnets based on logical destination IP addresses."
    },
    {
        "id": 21,
        "question": "Which Object-Oriented Programming (OOP) principle binds data and code together while restricting direct external access?",
        "options": {
            "A": "Inheritance",
            "B": "Encapsulation",
            "C": "Polymorphism",
            "D": "Composition"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Encapsulation in OOP",
        "explanation": "Encapsulation hides the internal implementation details of an object and exposes only controlled public interfaces (getters/setters)."
    },
    {
        "id": 22,
        "question": "What is the OOP mechanism where a subclass provides its own specific implementation of an inherited method?",
        "options": {
            "A": "Method Overloading",
            "B": "Method Overriding",
            "C": "Dynamic Casting",
            "D": "Static Linking"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "Method Overriding",
        "explanation": "Method overriding allows a derived class to supply a specialized version of a method already defined in its parent base class."
    },
    {
        "id": 23,
        "question": "What are the three essential cyclic stages executed by a CPU for every machine instruction?",
        "options": {
            "A": "Compile, Link, Run",
            "B": "Fetch, Decode, Execute",
            "C": "Input, Process, Output",
            "D": "Read, Verify, Commit"
        },
        "correct_answer": "B",
        "difficulty": "Easy",
        "concept": "CPU Instruction Cycle",
        "explanation": "The instruction execution cycle comprises: Fetching the instruction from memory, Decoding the opcode, and Executing the specified operation."
    },
    {
        "id": 24,
        "question": "Which CPU register stores the memory address of the next instruction waiting to be fetched and executed?",
        "options": {
            "A": "Instruction Register (IR)",
            "B": "Accumulator (ACC)",
            "C": "Program Counter (PC)",
            "D": "Memory Data Register (MDR)"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Program Counter Register",
        "explanation": "The Program Counter (PC) register continuously holds the memory address of the next instruction in sequence to be fetched."
    },
    {
        "id": 25,
        "question": "What is the worst-case time complexity of finding the maximum element in an unsorted array of n numbers?",
        "options": {
            "A": "O(1)",
            "B": "O(log n)",
            "C": "O(n)",
            "D": "O(n log n)"
        },
        "correct_answer": "C",
        "difficulty": "Easy",
        "concept": "Linear Array Search",
        "explanation": "Because the array is unordered, every single element must be inspected at least once, yielding a time complexity of O(n)."
    },

    # ==================== MEDIUM QUESTIONS (26 - 50) ====================
    {
        "id": 26,
        "question": "Which traversal algorithm applied to a Binary Search Tree (BST) visits nodes in ascending sorted order?",
        "options": {
            "A": "Pre-order traversal",
            "B": "In-order traversal",
            "C": "Post-order traversal",
            "D": "Level-order traversal"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "BST In-Order Traversal",
        "explanation": "Because a BST maintains left < root < right, an in-order traversal (visiting Left, then Root, then Right) produces strictly sorted keys."
    },
    {
        "id": 27,
        "question": "Which data structure is most appropriate for checking balanced parentheses and brackets in an expression?",
        "options": {
            "A": "Queue",
            "B": "Stack",
            "C": "Heap",
            "D": "Hash Map"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Parentheses Matching via Stack",
        "explanation": "A stack allows matching the most recently opened symbol with incoming closing symbols using its Last-In, First-Out property."
    },
    {
        "id": 28,
        "question": "In an AVL tree, what is the valid balance factor (height of left subtree minus height of right subtree) allowed for any node?",
        "options": {
            "A": "Strictly 0",
            "B": "-1, 0, or +1",
            "C": "Between -2 and +2",
            "D": "Any positive integer"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "AVL Tree Balance Factor",
        "explanation": "An AVL tree is strictly height-balanced: for every node, the height difference between left and right subtrees must not exceed 1 (i.e., -1, 0, or +1)."
    },
    {
        "id": 29,
        "question": "In hash tables using open addressing, how does Linear Probing resolve a collision at index k?",
        "options": {
            "A": "By attaching a singly linked list at slot k",
            "B": "By checking consecutive slots (k + 1, k + 2, ...) sequentially modulo table capacity",
            "C": "By immediately rehashing with a secondary hash function",
            "D": "By doubling table size on every collision"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Hash Table Linear Probing",
        "explanation": "Linear probing sequentially searches the next slots in the array (k+1, k+2, ...) until an empty bucket is discovered."
    },
    {
        "id": 30,
        "question": "What is the time complexity to extract (delete) the minimum element from a Binary Min-Heap containing n elements?",
        "options": {
            "A": "O(1)",
            "B": "O(log n)",
            "C": "O(n)",
            "D": "O(n log n)"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Heap Extract-Min Complexity",
        "explanation": "Extracting the root takes O(1), and restoring the min-heap property by sifting down the replacement leaf takes time proportional to tree height: O(log n)."
    },
    {
        "id": 31,
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
        "explanation": "Merge sort always divides input in half (log n recursive levels) and performs O(n) merging work across each level, guaranteeing O(n log n) in all cases."
    },
    {
        "id": 32,
        "question": "Under what condition does standard QuickSort degrade to its worst-case time complexity of O(n^2)?",
        "options": {
            "A": "When all elements in the array are randomized",
            "B": "When the chosen pivot repeatedly splits the array into maximally unbalanced partitions (e.g. 0 and n-1)",
            "C": "When the array size is an exact power of 2",
            "D": "When recursion depth is limited by stack size"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "QuickSort Degeneracy",
        "explanation": "If the pivot is consistently the smallest or largest element (such as picking the first element of an already sorted array), partitions are unbalanced, taking O(n^2)."
    },
    {
        "id": 33,
        "question": "Which algorithmic design paradigm does Dijkstra's single-source shortest path algorithm employ?",
        "options": {
            "A": "Divide and Conquer",
            "B": "Greedy Strategy",
            "C": "Dynamic Programming",
            "D": "Branch and Bound"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Dijkstra Algorithm Paradigm",
        "explanation": "Dijkstra's algorithm follows a greedy approach by always expanding the unvisited vertex with the smallest tentative distance."
    },
    {
        "id": 34,
        "question": "What is the recurrence relation describing the running time of standard Binary Search on an array of size n?",
        "options": {
            "A": "T(n) = 2T(n/2) + O(n)",
            "B": "T(n) = T(n/2) + O(1)",
            "C": "T(n) = T(n-1) + O(1)",
            "D": "T(n) = 2T(n/2) + O(1)"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Binary Search Recurrence",
        "explanation": "Binary Search compares middle element in O(1) time and recurses on only one half of the array, giving T(n) = T(n/2) + O(1), which solves to O(log n)."
    },
    {
        "id": 35,
        "question": "Which sorting algorithm is guaranteed to be both stable and achieve O(n log n) worst-case time complexity?",
        "options": {
            "A": "QuickSort",
            "B": "HeapSort",
            "C": "Merge Sort",
            "D": "Selection Sort"
        },
        "correct_answer": "C",
        "difficulty": "Medium",
        "concept": "Sorting Stability and Complexity",
        "explanation": "Merge Sort maintains the original relative order of equal keys (stability) and runs in O(n log n) time across worst, average, and best cases."
    },
    {
        "id": 36,
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
        "explanation": "The four required conditions are Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. Preemption breaks deadlock."
    },
    {
        "id": 37,
        "question": "What event triggers a page fault in a virtual memory management system?",
        "options": {
            "A": "Division by zero during execution",
            "B": "An access attempt to a virtual page whose valid bit in the page table is 0 (not loaded in RAM)",
            "C": "A cache tag mismatch in L1 cache",
            "D": "Disk storage capacity being fully exhausted"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Virtual Memory Page Fault",
        "explanation": "A page fault is an interrupt generated by the MMU when a program references a virtual memory page that is not currently present in physical RAM."
    },
    {
        "id": 38,
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
        "explanation": "If the time quantum exceeds the longest CPU burst of any process in the ready queue, each process runs to completion, acting identically to FCFS."
    },
    {
        "id": 39,
        "question": "A counting semaphore initialized with a value of 1 is functionally identical to which synchronization primitive?",
        "options": {
            "A": "Spinlock array",
            "B": "Binary Semaphore (Mutex Lock)",
            "C": "Monitor condition variable",
            "D": "Barrier synchronization"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Binary Semaphore Equivalence",
        "explanation": "A semaphore initialized with count 1 permits only one thread into the critical section at any given time, functioning as a binary mutex lock."
    },
    {
        "id": 40,
        "question": "What operating system phenomenon occurs when processes spend more time swapping pages to disk than executing useful CPU instructions?",
        "options": {
            "A": "Starvation",
            "B": "Thrashing",
            "C": "Belady's Anomaly",
            "D": "Aging"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Virtual Memory Thrashing",
        "explanation": "Thrashing occurs when the total working sets of active processes exceed available physical memory, forcing continuous page eviction and disk I/O."
    },
    {
        "id": 41,
        "question": "In the ACID model of database transactions, what does 'Atomicity' guarantee?",
        "options": {
            "A": "Data written to disk is never duplicated",
            "B": "All operations within a transaction complete successfully, or all are completely aborted (all-or-nothing)",
            "C": "Multiple concurrent transactions execute without reading each other's uncommitted data",
            "D": "Database integrity constraints persist across system power failures"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "ACID Atomicity",
        "explanation": "Atomicity ensures that a transaction is treated as a single indivisible unit: either all updates are committed, or the transaction is rolled back."
    },
    {
        "id": 42,
        "question": "A relational database table is in Second Normal Form (2NF) if it is in 1NF and contains no:",
        "options": {
            "A": "Transitive functional dependencies",
            "B": "Partial functional dependencies of non-prime attributes on any candidate key",
            "C": "Multi-valued dependencies",
            "D": "Foreign key constraints"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Database Normalization 2NF",
        "explanation": "2NF requires that all non-prime attributes are fully functionally dependent on the entire candidate key, eliminating partial key dependencies."
    },
    {
        "id": 43,
        "question": "Which SQL JOIN type returns all records from the left table and matched rows from the right table, padding missing right attributes with NULL?",
        "options": {
            "A": "INNER JOIN",
            "B": "CROSS JOIN",
            "C": "LEFT OUTER JOIN",
            "D": "FULL OUTER JOIN"
        },
        "correct_answer": "C",
        "difficulty": "Medium",
        "concept": "SQL Left Outer Join",
        "explanation": "A LEFT OUTER JOIN preserves all rows from the left relation, filling non-matching fields from the right table with NULL values."
    },
    {
        "id": 44,
        "question": "In SQL, which clause must be used to filter groups produced by a GROUP BY query based on aggregate calculations?",
        "options": {
            "A": "WHERE",
            "B": "HAVING",
            "C": "FILTER",
            "D": "ORDER BY"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "SQL HAVING vs WHERE",
        "explanation": "The WHERE clause filters individual rows prior to grouping; the HAVING clause filters summary groups after aggregation has been performed."
    },
    {
        "id": 45,
        "question": "What distinguishes a Clustered Index from a Secondary (Unclustered) Index in relational databases?",
        "options": {
            "A": "Clustered indexes can be created on multiple tables simultaneously",
            "B": "A clustered index defines the actual physical storage order of rows in the table",
            "C": "Clustered indexes do not support B-Tree indexing structures",
            "D": "A table can contain up to 16 clustered indexes"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Clustered Index Design",
        "explanation": "A table can have only one clustered index because its leaf pages dictate the physical on-disk arrangement of the actual data records."
    },
    {
        "id": 46,
        "question": "What is the exact sequence of segment flags exchanged during a standard TCP connection establishment handshake?",
        "options": {
            "A": "SYN -> ACK -> SYN-ACK",
            "B": "SYN -> SYN-ACK -> ACK",
            "C": "ACK -> SYN -> ACK",
            "D": "FIN -> ACK -> FIN-ACK"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "TCP Three-Way Handshake",
        "explanation": "The client initiates with a SYN segment, the server acknowledges and requests synchronization with SYN-ACK, and the client completes with an ACK."
    },
    {
        "id": 47,
        "question": "Why is TCP described as a reliable transport protocol whereas UDP is considered unreliable?",
        "options": {
            "A": "TCP is executed by hardware routers while UDP runs on end hosts",
            "B": "TCP implements acknowledgments, sequence numbers, and retransmissions, whereas UDP does not",
            "C": "TCP automatically encrypts packet payloads with TLS",
            "D": "UDP packets cannot be routed over wide area networks"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "TCP vs UDP Reliability",
        "explanation": "TCP tracks delivery with sequence numbers, positive ACKs, checksums, and timeout retransmissions, whereas UDP sends packets without delivery guarantees."
    },
    {
        "id": 48,
        "question": "How many usable host IP addresses are available in a standard IPv4 subnet configured with a /24 mask (255.255.255.0)?",
        "options": {
            "A": "256",
            "B": "254",
            "C": "255",
            "D": "128"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Subnetting Usable Host Calculation",
        "explanation": "With 8 host bits, there are 2^8 = 256 addresses total. Reserving the network identifier (.0) and the broadcast address (.255) leaves 254 usable host addresses."
    },
    {
        "id": 49,
        "question": "Which protocol resolves a known IPv4 address into its corresponding physical Data Link layer MAC address on an Ethernet network?",
        "options": {
            "A": "DNS",
            "B": "DHCP",
            "C": "ARP (Address Resolution Protocol)",
            "D": "RARP"
        },
        "correct_answer": "C",
        "difficulty": "Medium",
        "concept": "Address Resolution Protocol",
        "explanation": "ARP broadcasts a query on the local subnet to discover which physical MAC address corresponds to a destination IPv4 address."
    },
    {
        "id": 50,
        "question": "What is the primary computer architecture reason for incorporating Cache Memory into the memory hierarchy?",
        "options": {
            "A": "To increase permanent storage capacity for application files",
            "B": "To bridge the significant speed and latency gap between fast CPU registers and slower main memory (DRAM)",
            "C": "To provide error-correcting storage for CPU microcode",
            "D": "To enable multi-threading on single-core processors"
        },
        "correct_answer": "B",
        "difficulty": "Medium",
        "concept": "Cache Memory Architecture",
        "explanation": "Fast SRAM caches exploit spatial and temporal locality to provide near-instant data access, preventing high latency delays from main memory DRAM."
    },

    # ==================== HARD QUESTIONS (51 - 75) ====================
    {
        "id": 51,
        "question": "In Red-Black Trees, which structural property guarantees that no path from root to leaf is more than twice as long as any other path?",
        "options": {
            "A": "Every non-leaf node must have exactly two non-null children",
            "B": "Every path from any node to its descendant null leaves contains the exact same number of black nodes (black height)",
            "C": "All red nodes must reside exclusively in the right subtree",
            "D": "Tree height is dynamically recomputed after every search operation"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Red-Black Tree Properties",
        "explanation": "The rule that no two red nodes can appear consecutively, combined with uniform black height along all paths, bounds maximum height to <= 2 * log2(n + 1)."
    },
    {
        "id": 52,
        "question": "Which specialized tree data structure achieves O(L) retrieval and prefix matching for strings of length L independent of dictionary size N?",
        "options": {
            "A": "Splay Tree",
            "B": "Trie (Prefix Tree)",
            "C": "B+ Tree",
            "D": "Treap"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Trie Data Structure",
        "explanation": "A Trie organizes characters along directed paths where each step corresponds to an alphabet symbol, allowing prefix searches in O(L) time regardless of N."
    },
    {
        "id": 53,
        "question": "When a dynamic array (e.g. C++ std::vector or Python list) doubles its internal buffer capacity on reaching full capacity, what is the amortized cost per insertion?",
        "options": {
            "A": "O(n)",
            "B": "O(log n)",
            "C": "O(1) amortized",
            "D": "O(n log n)"
        },
        "correct_answer": "C",
        "difficulty": "Hard",
        "concept": "Dynamic Array Amortized Analysis",
        "explanation": "Geometric capacity doubling spreads the expensive O(n) reallocation and copying cost across n previous insertions, yielding an amortized O(1) time per append."
    },
    {
        "id": 54,
        "question": "Which dynamic programming algorithm computes the shortest path between all pairs of vertices in a weighted graph in O(V^3) time?",
        "options": {
            "A": "Dijkstra's Algorithm",
            "B": "Prim's Algorithm",
            "C": "Floyd-Warshall Algorithm",
            "D": "Kruskal's Algorithm"
        },
        "correct_answer": "C",
        "difficulty": "Hard",
        "concept": "Floyd-Warshall Algorithm",
        "explanation": "Floyd-Warshall employs dynamic programming with 3 nested loops over intermediate vertices k: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) in O(V^3)."
    },
    {
        "id": 55,
        "question": "Which single-source shortest path algorithm correctly accommodates negative edge weights and detects reachable negative weight cycles?",
        "options": {
            "A": "Dijkstra's Algorithm",
            "B": "Bellman-Ford Algorithm",
            "C": "Breadth-First Search (BFS)",
            "D": "A* Search Algorithm"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Bellman-Ford Algorithm",
        "explanation": "Bellman-Ford relaxes all edges |V|-1 times. An additional relaxation check that succeeds in reducing a distance proves the presence of a negative cycle."
    },
    {
        "id": 56,
        "question": "What is the time complexity of building a Binary Heap from an arbitrary unsorted array of n elements using the bottom-up Heapify approach?",
        "options": {
            "A": "O(n log n)",
            "B": "O(n)",
            "C": "O(n^2)",
            "D": "O(log n)"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Heapify Build Time Complexity",
        "explanation": "Bottom-up heap construction runs in linear O(n) time because the vast majority of nodes reside at lower levels and require few sift-down operations."
    },
    {
        "id": 57,
        "question": "In algorithm design, what two fundamental properties must an optimization problem possess to be solvable via Dynamic Programming?",
        "options": {
            "A": "Greedy choice property and divide-and-conquer symmetry",
            "B": "Optimal substructure and overlapping subproblems",
            "C": "Independent subproblems and polynomial verification",
            "D": "Asymptotic linearity and monotonic recurrence"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Dynamic Programming Foundations",
        "explanation": "DP applies when an optimal problem solution contains optimal solutions to subproblems (optimal substructure) and those subproblems recur repeatedly."
    },
    {
        "id": 58,
        "question": "What does Kahn's algorithm compute on a Directed Acyclic Graph (DAG) by iteratively queueing vertices with in-degree 0?",
        "options": {
            "A": "Minimum Spanning Tree",
            "B": "Topological Sort",
            "C": "Strongly Connected Components",
            "D": "Maximum Network Flow"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Kahn's Topological Sort",
        "explanation": "Kahn's algorithm repeatedly extracts zero-in-degree nodes, decrements successor in-degrees, and appends nodes to generate a topological dependency order."
    },
    {
        "id": 59,
        "question": "Which deadlock avoidance algorithm evaluates pending resource requests against declared maximum needs to ensure the system remains in a safe state?",
        "options": {
            "A": "Round-Robin Algorithm",
            "B": "Banker's Algorithm",
            "C": "Peterson's Algorithm",
            "D": "SSTF Disk Scheduling"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Banker's Deadlock Avoidance",
        "explanation": "Dijkstra's Banker's Algorithm simulates resource allocation to confirm that at least one execution sequence exists where all processes can finish safely."
    },
    {
        "id": 60,
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
        "explanation": "Belady's Anomaly is the counter-intuitive phenomenon where increasing physical page frames increases total page faults under First-In-First-Out (FIFO) replacement."
    },
    {
        "id": 61,
        "question": "What is the primary architectural function of the Translation Lookaside Buffer (TLB) in CPU memory management units?",
        "options": {
            "A": "To store dirty bits for disk block caching",
            "B": "To act as a high-speed hardware cache for recent virtual-to-physical address translations",
            "C": "To buffer interrupt requests from high-priority peripherals",
            "D": "To synchronize cache coherence across multi-core processors"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Translation Lookaside Buffer (TLB)",
        "explanation": "The TLB caches recent virtual page number to physical frame mappings, avoiding multi-level page table lookups in RAM on TLB hits."
    },
    {
        "id": 62,
        "question": "In the classic Readers-Writers synchronization problem, what adverse condition occurs if writers are given strict non-preemptive priority over readers?",
        "options": {
            "A": "Deadlock",
            "B": "Reader Starvation",
            "C": "Writer Starvation",
            "D": "Race condition on shared buffer"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Readers-Writers Starvation",
        "explanation": "When writers have strict priority, continuous arrival of writer requests prevents any waiting reader from acquiring the lock, causing reader starvation."
    },
    {
        "id": 63,
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
        "explanation": "An inverted page table has exactly one entry per physical frame of RAM rather than per virtual page, drastically reducing page table memory footprint."
    },
    {
        "id": 64,
        "question": "In database transaction concurrency control, what theoretical guarantee does Strict Two-Phase Locking (Strict 2PL) provide?",
        "options": {
            "A": "Freedom from deadlocks",
            "B": "Conflict Serializability and freedom from cascading aborts",
            "C": "Zero locking overhead",
            "D": "Guaranteed lock-free linearizability"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Strict Two-Phase Locking (2PL)",
        "explanation": "Strict 2PL holds all exclusive locks until the transaction commits or aborts, guaranteeing conflict serializable schedules and preventing cascading aborts."
    },
    {
        "id": 65,
        "question": "Why do commercial database management engines use B+ Trees instead of standard B Trees for index structures?",
        "options": {
            "A": "B+ Trees consume significantly less disk space for interior nodes",
            "B": "Leaf nodes store all actual record pointers and are doubly linked sequentially for efficient range scans",
            "C": "B+ Trees eliminate the need for rebalancing operations",
            "D": "B+ Trees support O(1) worst-case searches"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "B+ Tree Indexing Advantages",
        "explanation": "In a B+ Tree, interior nodes only store routing keys, allowing higher fanout, and leaves are linked in a sequence list, enabling fast range queries and sequential scans."
    },
    {
        "id": 66,
        "question": "A relational database schema is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency X -> Y:",
        "options": {
            "A": "Y is a prime attribute",
            "B": "X is a Superkey of the relation",
            "C": "X is a subset of Y",
            "D": "Y is functionally dependent on all candidate keys"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Boyce-Codd Normal Form (BCNF)",
        "explanation": "BCNF is stricter than 3NF: it requires the determinant X to be a superkey for every non-trivial functional dependency X -> Y (no exceptions for prime attributes)."
    },
    {
        "id": 67,
        "question": "What does the Write-Ahead Logging (WAL) protocol strictly enforce in database recovery algorithms (e.g. ARIES)?",
        "options": {
            "A": "Transactions must commit before log records are generated",
            "B": "The log record describing a change must be flushed to non-volatile storage before the corresponding dirty data page is written to disk",
            "C": "Database tables must be replicated across three servers before accepting writes",
            "D": "Undo operations are executed before Redo operations during crash recovery"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Write-Ahead Logging (WAL)",
        "explanation": "WAL mandates that log records containing before/after images must be written to disk before modified data pages reach disk, ensuring atomicity and durability."
    },
    {
        "id": 68,
        "question": "Under ANSI SQL transaction isolation levels, which phenomenon can occur in 'Repeatable Read' that is prevented in 'Serializable'?",
        "options": {
            "A": "Dirty Reads",
            "B": "Non-repeatable (Fuzzy) Reads",
            "C": "Phantom Reads",
            "D": "Lost Updates"
        },
        "correct_answer": "C",
        "difficulty": "Hard",
        "concept": "SQL Transaction Isolation Levels",
        "explanation": "Repeatable Read prevents dirty reads and non-repeatable reads by locking read rows, but phantom reads (new rows inserted by concurrent transactions matching a range query) can still occur."
    },
    {
        "id": 69,
        "question": "In TCP congestion control, what condition triggers the Fast Retransmit mechanism?",
        "options": {
            "A": "Expiration of the Retransmission Timeout (RTO) timer",
            "B": "Receipt of three duplicate ACKs (4 identical ACKs total) for the same sequence number",
            "C": "Drop in Round Trip Time (RTT) below threshold",
            "D": "Explicit Congestion Notification (ECN) echo bit set in window header"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "TCP Fast Retransmit Mechanism",
        "explanation": "Receipt of 3 duplicate ACKs indicates to sender that a specific segment was lost while subsequent segments arrived, prompting immediate retransmission without waiting for RTO."
    },
    {
        "id": 70,
        "question": "Which routing protocol uses a Path Vector algorithm to exchange Reachability and Autonomous System (AS) path attributes across the global Internet?",
        "options": {
            "A": "OSPF (Open Shortest Path First)",
            "B": "RIP (Routing Information Protocol)",
            "C": "BGP (Border Gateway Protocol)",
            "D": "IS-IS"
        },
        "correct_answer": "C",
        "difficulty": "Hard",
        "concept": "Border Gateway Protocol (BGP)",
        "explanation": "BGP is the exterior gateway protocol of the Internet, using path vectors (AS_PATH attribute) to advertise routes and prevent routing loops between autonomous systems."
    },
    {
        "id": 71,
        "question": "In Distance Vector routing protocols (like RIP), what classic problem causes routing loops where nodes continually increment hop counts to an unreachable destination?",
        "options": {
            "A": "Count-to-Infinity problem",
            "B": "Broadcast storm",
            "C": "Split horizon failure",
            "D": "Slow convergence anomaly"
        },
        "correct_answer": "A",
        "difficulty": "Hard",
        "concept": "Count-to-Infinity in Distance Vector",
        "explanation": "Count-to-Infinity occurs when two or more routers exchange outdated routing information about a failed link, incrementing hop counts until reaching infinity (e.g. 16 in RIP)."
    },
    {
        "id": 72,
        "question": "If a network engineer needs to carve a Class C network (192.168.1.0/24) into at least 6 usable subnets, each supporting at least 25 hosts, what subnet mask is required?",
        "options": {
            "A": "255.255.255.192 (/26)",
            "B": "255.255.255.224 (/27)",
            "C": "255.255.255.240 (/28)",
            "D": "255.255.255.248 (/29)"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Subnetting Calculation",
        "explanation": "Borrowing 3 bits gives 2^3 = 8 subnets (>= 6) with 5 host bits remaining (2^5 - 2 = 30 usable hosts >= 25). Subnet mask is /27, which equals 255.255.255.224."
    },
    {
        "id": 73,
        "question": "In pipelined CPU architectures, what type of hazard occurs when an instruction requires the result of a preceding instruction that has not yet completed execution?",
        "options": {
            "A": "Structural Hazard",
            "B": "Data Hazard (Read-After-Write / RAW)",
            "C": "Control Hazard",
            "D": "Branch Delay Hazard"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Pipeline Data Hazard",
        "explanation": "A RAW (Read-After-Write) data hazard occurs when an instruction depends on the output of an uncommitted previous instruction, requiring operand forwarding or pipeline stalls."
    },
    {
        "id": 74,
        "question": "In CPU cache design, why is an N-way Set Associative cache preferred over a Direct-Mapped cache?",
        "options": {
            "A": "It completely eliminates the need for replacement algorithms like LRU",
            "B": "It significantly reduces conflict misses by providing N locations in a set where a memory block can reside",
            "C": "It operates with zero tag comparison hardware overhead",
            "D": "It decreases hit time to less than a single clock cycle"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Set Associative Cache Design",
        "explanation": "Direct-mapped caches suffer from conflict misses when multiple active addresses map to the exact same cache line. Set associativity provides N lines per set to eliminate ping-pong thrashing."
    },
    {
        "id": 75,
        "question": "What microarchitectural structure is maintained by modern CPUs to cache target addresses of recently taken branches for immediate next-PC lookup?",
        "options": {
            "A": "Translation Lookaside Buffer (TLB)",
            "B": "Branch Target Buffer (BTB)",
            "C": "Return Address Stack (RAS)",
            "D": "Store Buffer"
        },
        "correct_answer": "B",
        "difficulty": "Hard",
        "concept": "Branch Target Buffer (BTB)",
        "explanation": "The Branch Target Buffer (BTB) caches the predicted target instruction address for taken branches, allowing the fetch unit to retrieve target instructions in the very next cycle without stalling."
    }
]


def get_standard_questions():
    """Returns a fresh deep-copy of standard question bank."""
    return [dict(q) for q in STANDARD_QUESTIONS]


def filter_questions_by_difficulty(questions, difficulty):
    """Filters questions by a specified difficulty ('Easy', 'Medium', 'Hard')."""
    return [q for q in questions if q.get("difficulty") == difficulty]


def build_mixed_quiz(question_pool, target_count):
    """
    Constructs a balanced quiz of length `target_count` containing roughly equal parts
    of Easy, Medium, and Hard questions from `question_pool`, without repetition.
    """
    easy_pool = [q for q in question_pool if q.get("difficulty") == "Easy"]
    med_pool = [q for q in question_pool if q.get("difficulty") == "Medium"]
    hard_pool = [q for q in question_pool if q.get("difficulty") == "Hard"]

    # Target division
    easy_count = target_count // 3
    med_count = target_count // 3
    hard_count = target_count - (easy_count + med_count)

    selected = []
    # If any pool doesn't have enough, borrow from others
    e_take = min(easy_count, len(easy_pool))
    m_take = min(med_count, len(med_pool))
    h_take = min(hard_count, len(hard_pool))

    selected.extend(random.sample(easy_pool, e_take) if e_take > 0 else [])
    selected.extend(random.sample(med_pool, m_take) if m_take > 0 else [])
    selected.extend(random.sample(hard_pool, h_take) if h_take > 0 else [])

    # If still need more to meet target_count
    if len(selected) < target_count:
        used_ids = {q["id"] for q in selected}
        remaining_pool = [q for q in question_pool if q["id"] not in used_ids]
        needed = target_count - len(selected)
        if remaining_pool and needed > 0:
            selected.extend(random.sample(remaining_pool, min(needed, len(remaining_pool))))

    # Shuffle selected questions so difficulty levels are distributed naturally
    random.shuffle(selected)
    return selected


class ConceptQuestionGenerator:
    """Processes PDF text into clean, direct concept-based MCQs with strict similarity validation."""

    def __init__(self):
        self.definition_patterns = [
            r'([A-Z][a-zA-Z0-9\s]{2,32})\s+(?:is|are)\s+defined\s+as\s+([^.]+?\.)',
            r'([A-Z][a-zA-Z0-9\s]{2,32})\s+(?:refers\s+to|means)\s+([^.]+?\.)',
            r'([A-Z][a-zA-Z0-9\s]{2,32})\s+(?:is|are)\s+(?:a|an|the|those)\s+([^.]+?\.)',
            r'(?:^|\.\s+)([A-Z][a-zA-Z0-9\s\/\-]{2,32})\s*:\s*([A-Z][^.\n]{15,180}\.)',
            r'(?:^|\.\s+)([A-Z][a-zA-Z0-9\s\/\-]{2,32})\s*[-–—]\s*([A-Z][^.\n]{15,180}\.)'
        ]

    def clean_text(self, text: str) -> str:
        """Strips PDF page headers, unit titles, line wraps, and metadata noise."""
        text = re.sub(r'Technical\s+Communication\s+UNIT-\d+.*?(?=[A-Z])', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Fundamentals\s+of\s+Communication.*?(?=[A-Z])', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Page\s+\d+(\s+of\s+\d+)?', '', text, flags=re.IGNORECASE)
        # Rejoin hyphenated words split across line breaks
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        # Unwrap single-newline breaks into single spaces
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        # Collapse multi-spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_sentences(self, text: str) -> list:
        """Splits text into clean sentences while filtering out headers and fragments."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        clean_sentences = []
        for s in sentences:
            s = s.strip()
            if len(s.split()) >= 6 and not s.endswith(':') and re.search(r'[a-zA-Z]', s):
                clean_sentences.append(s)
        return clean_sentences

    def _format_concept_name(self, concept: str) -> str:
        concept = concept.strip()
        concept = re.sub(r'^(?:1\)|2\)|3\)|4\)|5\)|6\)|7\)|8\)||\d+\.|\d+\))\s*', '', concept).strip()
        concept = re.sub(r'^(?:Types?\s+of\s+|Roles?\s+of\s+|Definition\s*:\s*)', '', concept, flags=re.IGNORECASE).strip()
        if concept.lower() == "cs of communication":
            return "the 7 Cs of Communication"
        if not concept.lower().startswith(('the ', 'a ', 'an ')):
            return concept
        return concept

    def _is_too_similar(self, str1: str, str2: str, threshold: float = 0.50) -> bool:
        """Checks if two option strings overlap significantly in meaning or structure."""
        s1, s2 = str1.lower(), str2.lower()
        if s1 in s2 or s2 in s1:
            return True
        ratio = SequenceMatcher(None, s1, s2).ratio()
        return ratio >= threshold

    def _classify_difficulty(self, concept: str, definition: str) -> str:
        """Categorizes question difficulty based on definition length and complexity."""
        length = len(definition)
        if length < 65:
            return "Easy"
        elif length < 125:
            return "Medium"
        else:
            return "Hard"

    def generate_questions(self, raw_text: str, target_count: int = None) -> list:
        cleaned_text = self.clean_text(raw_text)
        sentences = self.extract_sentences(cleaned_text)

        questions = []
        seen_concepts = set()
        bad_starts = ('for ', 'in ', 'if ', 'when ', 'why ', 'what ', 'page ', 'unit ', 'because ', 'to ', 'and ', 'but ', 'or ', 'it ', 'example', 'make ', 'ensure ', 'check ', 'consider ', 'set ', 'keep ')

        for sentence in sentences:
            if target_count is not None and len(questions) >= target_count:
                break

            match = None
            for pattern in self.definition_patterns:
                match = re.search(pattern, sentence)
                if match:
                    break

            if match:
                raw_concept = match.group(1).strip()
                raw_concept = re.sub(r'^(?:1\)|2\)|3\)|4\)|5\)|6\)|7\)|8\)||\d+\.|\d+\))\s*', '', raw_concept).strip()
                raw_concept = re.sub(r'^(?:Types?\s+of\s+|Roles?\s+of\s+|Definition\s*:\s*)', '', raw_concept, flags=re.IGNORECASE).strip()
                definition = match.group(2).strip()

                lower_c = raw_concept.lower()
                if any(lower_c.startswith(b) for b in bad_starts):
                    continue
                if len(raw_concept) < 3 or len(raw_concept) > 35:
                    continue
                if len(definition) < 15 or len(definition) > 220:
                    continue
                if lower_c in seen_concepts:
                    continue

                formatted_concept = self._format_concept_name(raw_concept)
                question_stem = f"According to the study material, what is {formatted_concept}?"
                correct_answer = definition[0].upper() + definition[1:]

                distractors = self._generate_distractors(raw_concept, correct_answer, sentences)
                if len(distractors) < 3:
                    continue

                all_options = [correct_answer] + distractors[:3]
                random.shuffle(all_options)

                diff = self._classify_difficulty(formatted_concept, definition)

                candidate_q = {
                    "id": f"PDF-{len(questions) + 1}",
                    "question": question_stem,
                    "options": {
                        "A": all_options[0],
                        "B": all_options[1],
                        "C": all_options[2],
                        "D": all_options[3]
                    },
                    "correct_answer": self._get_option_key(all_options, correct_answer),
                    "difficulty": diff,
                    "concept": formatted_concept,
                    "explanation": f"According to the document: {correct_answer}"
                }

                if self._validate_question(candidate_q):
                    questions.append(candidate_q)
                    seen_concepts.add(lower_c)

        return questions

    def _generate_distractors(self, concept: str, correct_def: str, all_sentences: list) -> list:
        distractors = []
        pool = [s for s in all_sentences if concept.lower() not in s.lower()]
        random.shuffle(pool)

        for sentence in pool:
            if len(distractors) >= 3:
                break
            if self._is_too_similar(sentence, correct_def):
                continue
            if any(self._is_too_similar(sentence, d) for d in distractors):
                continue
            words = sentence.split()
            if 6 <= len(words) <= 20:
                distractors.append(sentence)

        dynamic_fallbacks = [
            "A structural barrier in organizational communication hierarchy.",
            "The medium selected to convey a message across digital channels.",
            "The cognitive process of decoding symbols into meaningful thoughts.",
            "A method used exclusively for formal written documentations.",
            "The immediate environmental noise affecting signal clarity.",
            "An interactive feedback mechanism between participants in communication.",
            "The structured protocol used to exchange verified messages securely."
        ]
        random.shuffle(dynamic_fallbacks)

        for fallback in dynamic_fallbacks:
            if len(distractors) >= 3:
                break
            if not self._is_too_similar(fallback, correct_def) and not any(self._is_too_similar(fallback, d) for d in distractors):
                distractors.append(fallback)

        return distractors

    def _get_option_key(self, options_list: list, target_text: str) -> str:
        keys = ["A", "B", "C", "D"]
        for idx, option in enumerate(options_list):
            if option == target_text:
                return keys[idx]
        return "A"

    def _validate_question(self, q: dict) -> bool:
        opts = list(q["options"].values())
        if len(opts) != 4:
            return False
        for i in range(len(opts)):
            for j in range(i + 1, len(opts)):
                if self._is_too_similar(opts[i], opts[j], threshold=0.45):
                    return False
        if not q["question"].endswith("?"):
            return False
        return True
