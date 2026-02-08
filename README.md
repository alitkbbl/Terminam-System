# Virtual File System Simulation

A Python-based command-line interface (CLI) that simulates a functioning file system entirely in memory (RAM). This project mimics the behavior of a real operating system's file manager, allowing users to navigate directories, manipulate files, and even edit text content without touching the actual hard drive.

## 📖 About The Project

This simulation is an excellent educational tool for understanding Operating System concepts, specifically how file systems are structured hierarchically. Instead of relying on the host OS's `os` or `shutil` libraries, this project implements the logic for path resolution, tree traversal, and data storage from scratch using fundamental computer science algorithms.

## 🧠 Data Structures

A key feature of this project is its implementation of data structures. Instead of using Python's built-in recursive dictionaries or lists to represent folders, the system utilizes a **Linked-List based General Tree**.

### 1. The File System Tree (Left-Child, Right-Sibling Representation)
The core structure relies on the `FileSystemNode` class. To handle a directory containing an arbitrary number of files efficiently, the **"First Child - Next Sibling"** representation is used.

- **`self.child`**: Points only to the *first* file or sub-directory inside the current folder.
- **`self.next`**: Points to the *next* file or folder in the same directory (its sibling).
- **`self.parent`**: A pointer back to the containing directory (enabling `cd ..`).

**Visual Representation:**
If `/home` contains `user` and `docs`, and `user` contains `data.txt`:
```text
[root]
  |
  ↓ child
[home] ---------------------> next: None
  |
  ↓ child
[user] -> next -> [docs] -> next: None
  |
  ↓ child
[data.txt]
```
**Why this structure?**
This approach transforms a General Tree (N-ary tree) into a Binary Tree structure, making memory usage efficient and traversal algorithms (like deep copying or recursive deletion) standardized.

### 2. File Content Storage
For nodes where `is_file=True`, the content is stored in a list:
- **`self.content`**: A `List[str]`.
- Each element in the list represents a single line of text.
- **Complexity:** This allows for $O(1)$ access time when editing or deleting specific lines (e.g., the `editline` or `deline` commands) given an index.

---

## 🚀 Features

- **Path Navigation:** Full support for absolute paths (`/home/user`) and relative paths (`..`, `.`).
- **CRUD Operations:** Create (`mkdir`, `touch`), Read (`ls`, `cat`), Update (`rename`, `mv`), and Delete (`rm`) nodes.
- **Deep Copying:** The `cp` command implements a custom deep copy algorithm to duplicate entire directory trees recursively.
- **In-Memory Text Editor:**
  - Write new files.
  - Append text to existing files.
  - Edit specific lines by line number.
  - Delete specific lines.


## 🛠️ Installation & Usage

No external libraries are required. You only need Python 3 installed.

1. **Download** the `FileSystemNode.py` file.
2. **Run** the script via terminal:

bash
python FileSystemNode.py

3. You will see the prompt: `(/) $`. You are now inside the virtual root directory.

---

## ⌨️ Command Reference

### File & Directory Management
| Command | Usage | Description |
| :--- | :--- | :--- |
| **ls** | `ls` | List contents of the current directory. |
| **mkdir** | `mkdir <name>` | Create a new directory. |
| **touch** | `touch <name>.txt` | Create a new text file (must end in .txt). |
| **rm** | `rm <path>` | Recursively remove a file or directory. |
| **cp** | `cp <src> <dst>` | Copy a file or directory recursively. |
| **mv** | `mv <src> <dst>` | Move or rename a file/directory. |
| **rename** | `rename <path> <new>` | Rename a specific node. |

### Navigation
| Command | Usage | Description |
| :--- | :--- | :--- |
| **cd** | `cd <path>` | Change directory (supports `..` and `/`). |
| **exit** | `exit` | Terminate the simulation. |

### Content Editing
| Command | Usage | Description |
| :--- | :--- | :--- |
| **cat** | `cat <file>` | Print file content to the screen. |
| **nwfiletxt** | `nwfiletxt <file>` | Overwrite file content (type `/end/` to save). |
| **appendtxt** | `appendtxt <file>` | Append text to the end of a file. |
| **editline** | `editline <file> <n> <txt>` | Replace line number `<n>` with `<txt>`. |
| **deline** | `deline <file> <n>` | Delete line number `<n>`. |

---
## 🤝 Conclusion

The Virtual File System Simulation project serves as a comprehensive and effective demonstration of foundational computer science principles. By implementing core file system logic—from hierarchical path resolution to O(1)O(1) line editing—entirely from scratch using the Left-Child, Right-Sibling tree structure, this repository offers deep insight into operating system design and in-memory data management. It is a testament to the power of building robust, complex systems without external dependencies, making it an ideal resource for anyone looking to master low-level file system mechanics.
