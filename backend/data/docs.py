SAMPLE_DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Introduction to Neural Networks",
        "content": """
        A neural network is a series of algorithms that attempt to recognize underlying relationships
        in a set of data through a process that mimics the way the human brain operates. Neural networks
        consist of layers of nodes (neurons). Each node connects to others and has an associated weight
        and threshold. If the output of any individual node is above the threshold, that node is activated
        and sends data to the next layer. Otherwise, no data is passed to the next layer.

        The three main types of layers are: input layer (receives raw data), hidden layers (perform
        computations), and output layer (produces the final result). Deep learning refers to neural
        networks with many hidden layers.

        Activation functions like ReLU, Sigmoid, and Tanh introduce non-linearity, allowing networks
        to learn complex patterns. Backpropagation is the algorithm used to train neural networks by
        computing gradients and updating weights using gradient descent.
        """
    },
    {
        "id": "doc2",
        "title": "Machine Learning Fundamentals",
        "content": """
        Machine learning is a subset of artificial intelligence that provides systems the ability to
        automatically learn and improve from experience without being explicitly programmed. It focuses
        on developing computer programs that can access data and use it to learn for themselves.

        There are three main types of machine learning: supervised learning (labeled data, e.g.,
        classification and regression), unsupervised learning (unlabeled data, e.g., clustering and
        dimensionality reduction), and reinforcement learning (agent learns through rewards and penalties).

        Key concepts include: overfitting (model too complex, memorizes training data), underfitting
        (model too simple), bias-variance tradeoff, cross-validation, regularization (L1/L2), and
        hyperparameter tuning. Common algorithms include linear regression, decision trees, random forests,
        SVM, k-means, and gradient boosting.
        """
    },
    {
        "id": "doc3",
        "title": "Python Programming Basics",
        "content": """
        Python is a high-level, interpreted, general-purpose programming language. Its design philosophy
        emphasizes code readability with the use of significant indentation. Python is dynamically typed
        and garbage-collected.

        Key Python concepts: variables and data types (int, float, str, list, dict, tuple, set),
        control flow (if/elif/else, for loops, while loops), functions (def keyword, *args, **kwargs,
        lambda), classes and OOP (inheritance, encapsulation, polymorphism), and modules/packages.

        Python's popular libraries include NumPy (numerical computing), Pandas (data manipulation),
        Matplotlib (visualization), Scikit-learn (machine learning), TensorFlow and PyTorch (deep learning),
        FastAPI and Flask (web frameworks). List comprehensions, generators, decorators, and context
        managers are powerful Pythonic constructs.
        """
    },
    {
        "id": "doc4",
        "title": "Data Structures and Algorithms",
        "content": """
        Data structures are ways of organizing and storing data to enable efficient access and modification.
        Common data structures include: arrays (O(1) access), linked lists (O(n) access, O(1) insert at head),
        stacks (LIFO - Last In First Out), queues (FIFO - First In First Out), hash tables (O(1) average
        lookup), trees (hierarchical data), and graphs (networks of nodes and edges).

        Big O notation describes algorithm efficiency. O(1) is constant, O(log n) is logarithmic (binary search),
        O(n) is linear, O(n log n) is linearithmic (merge sort), O(n^2) is quadratic (bubble sort),
        O(2^n) is exponential.

        Key algorithms: sorting (bubble, merge, quick, heap sort), searching (linear, binary),
        graph traversal (BFS using queue, DFS using stack/recursion), dynamic programming (memoization,
        tabulation), and greedy algorithms.
        """
    },
    {
        "id": "doc5",
        "title": "Natural Language Processing",
        "content": """
        Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret,
        and manipulate human language. NLP combines computational linguistics with statistical, machine
        learning, and deep learning models.

        Key NLP tasks include: tokenization (splitting text into words/subwords), part-of-speech tagging,
        named entity recognition (NER), sentiment analysis, machine translation, text summarization,
        and question answering.

        Word embeddings like Word2Vec, GloVe, and FastText represent words as dense vectors capturing
        semantic meaning. Transformer architecture revolutionized NLP with self-attention mechanisms.
        Models like BERT (bidirectional encoder) and GPT (generative decoder) are pre-trained on massive
        corpora and fine-tuned for specific tasks.

        Retrieval-Augmented Generation (RAG) combines retrieval systems with generative models to
        produce factually grounded responses by fetching relevant documents before generation.
        """
    },
    {
        "id": "doc6",
        "title": "Database Systems",
        "content": """
        A database is an organized collection of structured information or data, typically stored
        electronically in a computer system. Relational databases (RDBMS) store data in tables with
        rows and columns, using SQL (Structured Query Language) for querying.

        Key SQL concepts: SELECT (retrieve), INSERT (add), UPDATE (modify), DELETE (remove), JOINs
        (INNER, LEFT, RIGHT, FULL OUTER), GROUP BY, HAVING, ORDER BY, subqueries, and indexes
        (speed up reads, slow down writes).

        ACID properties ensure reliable transactions: Atomicity (all or nothing), Consistency (valid state),
        Isolation (concurrent transactions do not interfere), Durability (committed data persists).

        NoSQL databases (MongoDB, Redis, Cassandra) trade ACID for scalability. Types include document
        stores, key-value stores, column-family stores, and graph databases. The CAP theorem states
        distributed systems can only guarantee two of: Consistency, Availability, Partition tolerance.
        """
    },
    {
        "id": "doc7",
        "title": "Computer Networks",
        "content": """
        Computer networking is the practice of connecting computers and other devices to share resources
        and communicate. The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session,
        Presentation, Application.

        TCP/IP is the foundational protocol suite. TCP (Transmission Control Protocol) provides reliable,
        ordered delivery with handshaking. UDP (User Datagram Protocol) is faster but unreliable, used
        for streaming and gaming. IP addresses identify devices; IPv4 uses 32-bit addresses, IPv6 uses 128-bit.

        HTTP/HTTPS is the application-layer protocol for the web. REST APIs use HTTP methods: GET (retrieve),
        POST (create), PUT/PATCH (update), DELETE (remove). DNS translates domain names to IP addresses.
        Firewalls, VPNs, load balancers, and CDNs are common networking components in production systems.
        """
    },
    {
        "id": "doc8",
        "title": "Operating Systems",
        "content": """
        An operating system (OS) is system software that manages hardware and software resources,
        providing services for computer programs. Key OS components: kernel (core, manages hardware),
        process management, memory management, file system, and I/O management.

        Process vs Thread: A process is an independent program with its own memory space. Threads share
        memory within a process and are lighter weight. Concurrency issues like race conditions, deadlocks,
        and starvation are managed with synchronization primitives: mutexes, semaphores, and monitors.

        Memory management techniques: paging (fixed-size blocks), segmentation (variable-size), virtual
        memory (disk as RAM extension), and caching (L1/L2/L3 CPU caches, TLB). Scheduling algorithms
        (FCFS, Round Robin, Priority) determine which process runs when.
        """
    },
]
