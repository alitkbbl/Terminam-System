# Terminal System

A Python-based simulation of a virtual terminal and file system.  
This project mimics basic UNIX-like commands such as `mkdir`, `touch`, `cd`, `ls`, `rm`, and file manipulation commands — all in memory.

## 📦 Features

- Create and manage directories and files
- Navigate directories using relative and absolute paths
- Simulate `cp`, `mv`, `rm`, and `rename`
- Modify `.txt` file contents:
  - Overwrite (`nwfiletxt`)
  - Append (`appendtxt`)
  - Edit/delete specific lines (`editline`, `deline`)
- Display file contents (`cat`)
- Custom prompt shows current directory path
- Recursive copy and delete operations
- All operations are virtual (no real disk I/O)

## 🚀 Getting Started

### Prerequisites

- Python 3.13

### Running the Program

```bash
python terminal_system.py


#### 🧪 Example Usage
(mkdir test)
(cd test)
(touch notes.txt)
(nwfiletxt notes.txt)
# Type content, end with /end/
(appendtxt notes.txt)
(cat notes.txt)


