import csv
import os
import sys


# =========================
# Basic Data Structures
# =========================

class Stack:
    def __init__(self):
        self._a = []

    def push(self, x):
        self._a.append(x)

    def pop(self):
        if self.is_empty():
            return None
        return self._a.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._a[-1]

    def is_empty(self):
        return len(self._a) == 0


class Queue:
    """
    Simple queue using list + head index (no pop(0)).
    """
    def __init__(self):
        self._a = []
        self._head = 0

    def enqueue(self, x):
        self._a.append(x)

    def dequeue(self):
        if self.is_empty():
            return None
        x = self._a[self._head]
        self._head += 1

        # occasional cleanup to avoid memory growth
        if self._head > 50 and self._head * 2 > len(self._a):
            self._a = self._a[self._head:]
            self._head = 0

        return x

    def is_empty(self):
        return self._head >= len(self._a)

    def view(self):
        return self._a[self._head:]


# =========================
# Searching
# =========================

def binary_search(A, x, lo, hi):
    """
    Returns index of x in sorted list A, otherwise -1.
    """
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if A[mid] == x:
        return mid
    if A[mid] > x:
        return binary_search(A, x, lo, mid - 1)
    return binary_search(A, x, mid + 1, hi)


# =========================
# Sorting (Merge Sort + Heap Sort)
# =========================

def merge_sort_inplace(A, lo, hi, show_steps=False):
    if lo >= hi:
        return

    mid = (lo + hi) // 2
    merge_sort_inplace(A, lo, mid, show_steps)
    merge_sort_inplace(A, mid + 1, hi, show_steps)

    i, j = lo, mid + 1
    merged = []

    while i <= mid and j <= hi:
        if A[i] <= A[j]:
            merged.append(A[i]); i += 1
        else:
            merged.append(A[j]); j += 1

    while i <= mid:
        merged.append(A[i]); i += 1
    while j <= hi:
        merged.append(A[j]); j += 1

    A[lo:hi + 1] = merged

    if show_steps:
        print("Step:", A)


class MaxHeap:
    def __init__(self):
        self.a = []
        self.heapSize = 0

    def build(self, A):
        self.a = A[:]
        self.heapSize = len(self.a)
        for i in range(self.heapSize // 2 - 1, -1, -1):
            self._heapify_down(i)

    def _heapify_down(self, i):
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            largest = i

            if left < self.heapSize and self.a[left] > self.a[largest]:
                largest = left
            if right < self.heapSize and self.a[right] > self.a[largest]:
                largest = right

            if largest == i:
                break
            self.a[i], self.a[largest] = self.a[largest], self.a[i]
            i = largest

    def _heapify_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.a[p] >= self.a[i]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def insert(self, x):
        x = int(x)
        self.a.append(x)
        self.heapSize += 1
        self._heapify_up(self.heapSize - 1)

    def delete_value(self, x):
        idx = -1
        for i in range(self.heapSize):
            if self.a[i] == x:
                idx = i
                break
        if idx == -1:
            return False

        # replace with last
        self.a[idx] = self.a[-1]
        self.a.pop()
        self.heapSize -= 1

        if idx < self.heapSize:
            # fix both directions
            self._heapify_down(idx)
            self._heapify_up(idx)
        return True

    def get_max(self):
        if self.heapSize == 0:
            return None
        return self.a[0]


def heap_sort(A, show_steps=False):
    h = MaxHeap()
    h.build(A)

    for i in range(len(A) - 1, 0, -1):
        h.a[0], h.a[i] = h.a[i], h.a[0]
        h.heapSize -= 1
        h._heapify_down(0)
        if show_steps:
            print("Step:", h.a)

    return h.a


# =========================
# Expression Processing (Infix -> Postfix/Prefix)
# =========================

def brackets_ok(tokens):
    st = Stack()
    for t in tokens:
        if t == "(":
            st.push(t)
        elif t == ")":
            if st.is_empty():
                return False
            st.pop()
    return st.is_empty()


def tokenize(expr):
    tokens = []
    i = 0
    allowed = set("0123456789+-*/() ")
    for ch in expr:
        if ch not in allowed:
            return None  # invalid character

    while i < len(expr):
        ch = expr[i]
        if ch == " ":
            i += 1
            continue
        if ch.isdigit():
            num = ""
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append(num)
            continue
        if ch in ["+", "-", "*", "/", "(", ")"]:
            tokens.append(ch)
            i += 1
            continue
    return tokens


def infix_to_postfix(tokens, show_steps=False):
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    st = Stack()
    out = []

    for t in tokens:
        if t.isdigit():
            out.append(t)
            if show_steps:
                print("OUT:", out, "| STACK:", st._a)
        elif t == "(":
            st.push(t)
            if show_steps:
                print("OUT:", out, "| STACK:", st._a)
        elif t == ")":
            while (not st.is_empty()) and st.peek() != "(":
                out.append(st.pop())
                if show_steps:
                    print("OUT:", out, "| STACK:", st._a)
            if st.is_empty():
                return None
            st.pop()  # pop '('
            if show_steps:
                print("OUT:", out, "| STACK:", st._a)
        else:
            while (not st.is_empty()) and (st.peek() in prec) and prec[st.peek()] >= prec[t]:
                out.append(st.pop())
                if show_steps:
                    print("OUT:", out, "| STACK:", st._a)
            st.push(t)
            if show_steps:
                print("OUT:", out, "| STACK:", st._a)

    while not st.is_empty():
        top = st.pop()
        if top == "(":
            return None
        out.append(top)
        if show_steps:
            print("OUT:", out, "| STACK:", st._a)

    return out


def swap_parentheses(tokens):
    out = []
    for t in tokens:
        if t == "(":
            out.append(")")
        elif t == ")":
            out.append("(")
        else:
            out.append(t)
    return out


def infix_to_prefix(tokens, show_steps=False):
    rev = tokens[::-1]
    rev = swap_parentheses(rev)
    postfix = infix_to_postfix(rev, show_steps=show_steps)
    if postfix is None:
        return None
    return postfix[::-1]


# =========================
# Graph BFS (Adjacency Matrix)
# =========================

def bfs_levels(adj, names, start_idx):
    n = len(adj)
    visited = [False] * n
    level = [-1] * n

    q = Queue()
    visited[start_idx] = True
    level[start_idx] = 0
    q.enqueue(start_idx)

    print(f"Start: {names[start_idx]}")
    print("Queue:", [names[i] for i in q.view()])
    print()

    while not q.is_empty():
        u = q.dequeue()
        print(f"Dequeue: {names[u]} (level {level[u]})")

        for v in range(n):
            if adj[u][v] == 1 and not visited[v]:
                visited[v] = True
                level[v] = level[u] + 1
                q.enqueue(v)

        print("Queue:", [names[i] for i in q.view()])
        print()

    return level


# =========================
# Currency CSV
# =========================

def check_currency(code, csv_path="currency_list.csv"):
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("code") == code:
                    return True, row.get("name")
    except FileNotFoundError:
        return False, None
    return False, None


# =========================
# Main Menu
# =========================

def read_int(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Warning: please enter a valid integer.")


def main():
    menu = {
        1: "Binary Search (price lookup)",
        2: "Sorting Algorithms (Merge / Heap)",
        3: "Financial formula processor (Infix->Postfix/Prefix)",
        4: "Purchasing priority management (Max-Heap)",
        5: "Currency communication network analysis (BFS)",
        6: "Shopping cart with Undo (Stack)",
        7: "Exit"
    }

    while True:
        print("\n" + "=" * 60)
        print("Final Project - Data Structures & Algorithms")
        print("=" * 60)

        for k in menu:
            print(f"{k}. {menu[k]}")

        choice = input("Enter the number: ").strip()

        if choice == "7":
            sys.exit(0)

        # 1) Binary Search
        if choice == "1":
            prices_raw = input("Enter the price list (space-separated integers): ").split()
            try:
                prices = list(map(int, prices_raw))
            except ValueError:
                print("Warning: price list must contain only integers.")
                continue

            target = read_int("Enter the price you want: ")

            # sort (manual) then binary search, per project requirement
            if len(prices) > 1:
                merge_sort_inplace(prices, 0, len(prices) - 1, show_steps=False)

            idx = binary_search(prices, target, 0, len(prices) - 1)
            print("Sorted list:", prices)
            print("Result:", idx if idx != -1 else "Not found")

        # 2) Sorting
        elif choice == "2":
            raw = input("Enter the transaction amounts (space-separated integers): ").split()
            try:
                A = list(map(int, raw))
            except ValueError:
                print("Warning: input must contain only integers.")
                continue

            print("Choose sorting algorithm:")
            print("1. Merge Sort")
            print("2. Heap Sort")
            alg = input("Enter 1 or 2: ").strip()

            if alg == "1":
                if len(A) > 1:
                    merge_sort_inplace(A, 0, len(A) - 1, show_steps=True)
                print("Sorted:", A)
            elif alg == "2":
                sorted_A = heap_sort(A, show_steps=True)
                print("Sorted:", sorted_A)
            else:
                print("Invalid choice.")

        # 3) Formula Processor
        elif choice == "3":
            raw = input('Enter fully-parenthesized expression like "(1*(2+3))": ')
            tokens = tokenize(raw)
            if not tokens or not brackets_ok(tokens):
                print("Invalid expression.")
                continue

            print("1. Postfix")
            print("2. Prefix")
            c = input("Choose 1 or 2: ").strip()

            if c == "1":
                out = infix_to_postfix(tokens, show_steps=True)
                print("Postfix:", " ".join(out) if out else "Invalid")
            elif c == "2":
                out = infix_to_prefix(tokens, show_steps=True)
                print("Prefix:", " ".join(out) if out else "Invalid")
            else:
                print("Invalid choice.")

        # 4) Purchasing priority management
        elif choice == "4":
            raw = input("Enter suggested purchase prices (space-separated integers): ").split()
            try:
                offers = list(map(int, raw))
            except ValueError:
                print("Warning: input must contain only integers.")
                continue

            h = MaxHeap()
            h.build(offers)

            while True:
                best = h.get_max()
                if best is None:
                    print("No offers left.")
                    break

                print(f"Best offer: {best}")
                ans = input("Sell this offer? (yes/no): ").strip().lower()
                if ans == "yes":
                    h.delete_value(best)
                    print("Sold.\n")
                elif ans == "no":
                    break
                else:
                    print("Invalid input. Please enter yes or no.")

        # 5) BFS analysis
        elif choice == "5":
            names = input("Enter currency names (space-separated): ").split()
            if not names:
                print("Invalid input.")
                continue

            n = len(names)
            print("Enter adjacency matrix rows (0/1), each row space-separated:")
            adj = []
            ok = True
            for i in range(n):
                row_raw = input().split()
                try:
                    row = list(map(int, row_raw))
                except ValueError:
                    ok = False
                    break
                if len(row) != n or any(x not in (0, 1) for x in row) or row[i] != 0:
                    ok = False
                    break
                adj.append(row)

            if not ok:
                print("Invalid adjacency matrix. Must be n×n with 0/1 and diagonal = 0.")
                continue

            for i, nm in enumerate(names, start=1):
                print(f"{i}. {nm}")
            start = read_int(f"Choose start (1..{n}): ")
            if not (1 <= start <= n):
                print("Invalid choice.")
                continue

            levels = bfs_levels(adj, names, start - 1)
            print("Levels:", levels)

        # 6) Shopping cart with undo
        elif choice == "6":
            cart = []
            history = Stack()  # stores actions: ("add"/"delete", code, name)

            while True:
                print("\n1. Add currency")
                print("2. Delete currency")
                print("3. Undo")
                print("4. Return to main menu")

                c = input("Enter choice: ").strip()

                if c == "4":
                    break

                if c == "1":
                    code = input("Enter currency code to add: ").strip().upper()
                    ok, name = check_currency(code)
                    if not ok:
                        print("Currency not found in CSV.")
                        continue
                    cart.append(code)
                    history.push(("add", code, name))
                    print("Cart:", cart)

                elif c == "2":
                    if not cart:
                        print("Cart is empty.")
                        continue
                    for i, code in enumerate(cart, start=1):
                        print(f"{i}. {code}")
                    idx = read_int("Choose item number to delete: ") - 1
                    if not (0 <= idx < len(cart)):
                        print("Invalid index.")
                        continue
                    code = cart.pop(idx)
                    ok, name = check_currency(code)
                    history.push(("delete", code, name))
                    print("Cart:", cart)

                elif c == "3":
                    last = history.pop()
                    if last is None:
                        print("Nothing to undo.")
                        continue
                    action, code, name = last
                    if action == "add":
                        # undo add => remove one occurrence
                        if code in cart:
                            cart.remove(code)
                        print(f"Undo: removed {code} ({name})")
                    else:
                        # undo delete => add back
                        cart.append(code)
                        print(f"Undo: restored {code} ({name})")
                    print("Cart:", cart)

                else:
                    print("Invalid choice.")

        else:
            print("Invalid menu option. Please try again.")


if __name__ == "__main__":
    main()
