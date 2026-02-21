# Data Structures Final Project (Python)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Course](https://img.shields.io/badge/Course-Data%20Structures-orange)

This repository contains my **final project for the Data Structures course**.  
It is a menu-driven Python program demonstrating key data structures and algorithms through practical tasks.

---

## Topics Covered

### 1) Searching
- Binary Search (performed on a sorted list)

### 2) Sorting
- Merge Sort
- Heap Sort (using a custom Max Heap)
- Step-by-step output to show intermediate states

### 3) Stacks & Expression Processing
- Parentheses validation using a Stack
- Tokenization of arithmetic expressions
- Infix → Postfix conversion
- Infix → Prefix conversion
- Intermediate stack/output states are printed for learning purposes

### 4) Heaps
- Custom Max Heap implementation
- Purchasing priority management (selecting the best offer)

### 5) Graphs (BFS)
- BFS traversal on an adjacency matrix
- Currency communication network analysis
- Prints queue states during traversal

### 6) Undo System (Stack)
- Shopping cart management with Undo functionality

---

## Files

- `main.py` — main menu and implementations  
- `currency_list.csv` — currency codes dataset used in the project (columns: `code`, `name`)

---

## How to Run

Make sure you have Python 3 installed:

```bash
python main.py
```

The program will display a main menu where you can choose between different data structure and algorithm demonstrations.

---

# Program Flow & Sample Usage

When the program runs, a menu is displayed:

```
1. Binary Search
2. Sorting Algorithms
3. Financial Formula Processor
4. Purchasing Priority Management
5. Currency Communication Network Analysis
6. Shopping Cart with Undo
7. Exit
```

---

## 1️⃣ Binary Search (Price Lookup)

### Example Input

```
Price list:
[32000, 31000, 35000, 30000, 33000]

Target:
33000
```

### Output

```
Sorted list:
[30000, 31000, 32000, 33000, 35000]

Price 33000 found at index 3.
```

If the value does not exist:

```
Price 34000 not found in the list.
```

---

## 2️⃣ Sorting Algorithms

The user selects a sorting algorithm (Merge Sort or Heap Sort).

### Example Input

```
Transactions:
[500, 1200, 300, 900]
```

### Step-by-Step Output

```
Step 1:
[300, 1200, 500, 900]

Step 2:
[300, 500, 1200, 900]

Step 3:
[300, 500, 900, 1200]

Final Sorted List:
[300, 500, 900, 1200]
```

The intermediate steps are printed to demonstrate how the algorithm processes the data.

---

## 3️⃣ Financial Formula Processor

Converts fully-parenthesized infix expressions into Prefix and Postfix formats.

### Example Input

```
Infix:
((A+B)*(C-D))
```

### Output

```
Prefix:
* + A B - C D

Postfix:
A B + C D - *
```

Stack operations are printed during execution to show how the algorithm works internally.

---

## 4️⃣ Purchasing Priority Management (Max Heap)

### Example Input

```
Offers:
[42000, 41500, 43000, 41000]
```

### Output

```
Max-Heap:
[43000, 42000, 41500, 41000]

Best offer:
43000

After selling 43000:

New Heap:
[42000, 41000, 41500]
```

The heap is dynamically updated after each operation.

---

## 5️⃣ Currency Communication Network (BFS)

### Step 1 – Enter number of currencies

```
4
```

### Step 2 – Enter currency names

```
BTC ETH BNB ADA
```

### Step 3 – Enter adjacency matrix

```
0 1 1 0
0 0 0 1
0 0 0 0
0 0 0 0
```

This represents:

- BTC → ETH, BNB  
- ETH → ADA  

### Step 4 – Choose starting currency

```
BTC
```

### BFS Output

```
Level 0:
BTC
Queue: [BTC]

Level 1:
ETH BNB
Queue: [ETH, BNB]

Level 2:
ADA
Queue: [ADA]
```

The queue state is displayed at each level to visualize the BFS process.

---

## 6️⃣ Shopping Cart with Undo (Stack-Based)

Menu:

```
1. Add currency
2. Delete currency
3. Undo
4. Return to main menu
```

### Example Execution

```
Cart: []

Add BTC → [BTC]
Add ETH → [BTC, ETH]
Delete BTC → [ETH]

Undo → [BTC, ETH]
Undo → [BTC]
Undo → []
```

Multiple consecutive undo operations are supported using a stack structure.

---

## License

MIT
