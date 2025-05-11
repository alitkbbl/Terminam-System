
class FileSystemNode:
    def __init__(self, name, is_file, parent=None):
        """
            :param name: Name of the file or directory
            :param is_file: True for a file, False for a directory
            :param parent: Parent node (used for the 'cd ..' command)
        """
        self.name = name
        self.is_file = is_file
        self.parent = parent
        self.child = None
        self.next = None

        self.content = [] if is_file else None

    def add_child(self, child):
        child.next = self.child
        self.child = child


def find_child(parent, name):
    current = parent.child
    while current:
        if current.name == name:
            return current
        current = current.next
    return None



class FileSystem:
    def __init__(self):
        self.root = FileSystemNode("root", is_file=False, parent=None)
        self.current = self.root

    def get_node_by_path(self, path):
        """
        Returns the target node using the given path.
        Supports both absolute paths (starting with '/') and relative paths.
        """
        if path.startswith('/'):
            node = self.root
            if path == '/':
                return node
            parts = path.strip('/').split('/')
        else:
            node = self.current
            parts = path.split('/')
        for part in parts:
            if part == "" or part == ".":
                continue
            elif part == "..":
                if node.parent:
                    node = node.parent
            else:
                nxt = find_child(node, part)
                if nxt is None:
                    return None
                node = nxt
        return node

    def ls_command(self, args):
        node = self.current
        children = []
        child = node.child
        while child:
            if child.is_file:
                children.append(child.name)
            else:
                children.append(child.name + "/")
            child = child.next
        if children:
            print("\t".join(children))
        else:
            print("Empty directory.")

    def mkdir_command(self, args):
        """
        The mkdir command:
        Usage format:
            mkdir <folder_name>             -> Creates a folder in the current directory
            mkdir <path> <folder_name>      -> Creates a folder at a specified path
        """
        if len(args) == 2:
            folder_name = args[1]
            target = self.current
        elif len(args) == 3:
            target = self.get_node_by_path(args[1])
            folder_name = args[2]
            if target is None or target.is_file:
                print("Path not found or not a directory.")
                return
        else:
            print("Usage: mkdir [<path>] <folder_name>")
            return

        if find_child(target, folder_name):
            print("A node with that name already exists.")
            return

        new_dir = FileSystemNode(folder_name, is_file=False, parent=target)
        target.add_child(new_dir)

    def touch_command(self, args):
        """
        The touch command:
        Usage format:
            touch <file_name>.txt              -> Creates a file in the current directory
            touch <path> <file_name>.txt       -> Creates a file at the specified path
        """
        if len(args) == 2:
            file_name = args[1]
            target = self.current
        elif len(args) == 3:
            target = self.get_node_by_path(args[1])
            file_name = args[2]
            if target is None or target.is_file:
                print("Path not found or not a directory.")
                return
        else:
            print("Usage: touch [<path>] <file_name>")
            return

        if not file_name.endswith(".txt"):
            print("File name must end with .txt")
            return

        if find_child(target, file_name):
            print("A node with that name already exists.")
            return

        new_file = FileSystemNode(file_name, is_file=True, parent=target)
        target.add_child(new_file)
        print(f"File '{file_name}' created.")

    def cd_command(self, args):
        if len(args) != 2:
            print("Usage: cd <path>")
            return
        new_dir = self.get_node_by_path(args[1])
        if new_dir is None or new_dir.is_file:
            print("Path not found or not a directory.")
            return
        self.current = new_dir

    def remove_subtree(self, node):
        """
        Deletes a node and all its subnodes recursively.
        (Note: In Python, memory management is handled by the garbage collector.)
        """
        child = node.child
        while child:
            next_child = child.next
            self.remove_subtree(child)
            child = next_child

    def rm_command(self, args):
        if len(args) != 2:
            print("Usage: rm <path>")
            return
        target = self.get_node_by_path(args[1])
        if target is None:
            print("Path not found.")
            return
        if target.parent is None:
            print("Cannot remove root directory.")
            return

        parent = target.parent
        if parent.child == target:
            parent.child = target.next
        else:
            curr = parent.child
            while curr and curr.next != target:
                curr = curr.next
            if curr:
                curr.next = target.next
        self.remove_subtree(target)

    def rename_command(self, args):
        if len(args) != 3:
            print("Usage: rename <path> <new_name>")
            return
        target = self.get_node_by_path(args[1])
        if target is None:
            print("Path not found.")
            return
        if target.parent is None:
            print("Cannot rename root directory.")
            return

        new_name = args[2]
        if find_child(target.parent, new_name):
            print("A node with that name already exists.")
            return

        target.name = new_name

    def deep_copy(self, node, new_parent):
        """
        Performs a deep copy of a node for the 'cp' command, including all its child nodes.

        Args:
            node (Node): The node to be copied.

        Returns:
            Node: A new node object that is a deep copy of the original, including all descendants.
        """
        copy_node = FileSystemNode(node.name, node.is_file, parent=new_parent)
        if node.is_file:
            copy_node.content = node.content[:]
        child = node.child
        while child:
            child_copy = self.deep_copy(child, copy_node)
            copy_node.add_child(child_copy)
            child = child.next
        return copy_node

    def cp_command(self, args):
        """
        The cp command: Copies a file or folder.
        Usage format:
            cp <source_path> <destination_path>
        """
        if len(args) != 3:
            print("Usage: cp <source_path> <destination_path>")
            return
        src = self.get_node_by_path(args[1])
        if src is None:
            print("Source path not found.")
            return
        dst = self.get_node_by_path(args[2])
        if dst is not None:
            if dst.is_file:
                print("Destination is a file.")
                return
            if find_child(dst, src.name):
                print("Destination already has a node with the same name.")
                return
            copy_node = self.deep_copy(src, dst)
            dst.add_child(copy_node)
        else:
            if "/" in args[2]:
                parts = args[2].rsplit('/', 1)
                parent_path = parts[0] if parts[0] != "" else "/"
                new_name = parts[1]
            else:
                parent_path = "."
                new_name = args[2]
            parent_dst = self.get_node_by_path(parent_path)
            if parent_dst is None or parent_dst.is_file:
                print("Destination parent path is not valid.")
                return
            if find_child(parent_dst, new_name):
                print("A node with that name already exists in the destination.")
                return
            copy_node = self.deep_copy(src, parent_dst)
            copy_node.name = new_name
            parent_dst.add_child(copy_node)

    def mv_command(self, args):
        """
        The mv command: Moves or renames a file/folder.
        Usage format:
        mv <source_path> <destination_path>
        """
        if len(args) != 3:
            print("Usage: mv <source_path> <destination_path>")
            return
        src = self.get_node_by_path(args[1])
        if src is None:
            print("Source path not found.")
            return
        if src.parent is None:
            print("Cannot move root directory.")
            return
        dst = self.get_node_by_path(args[2])
        if dst is not None:
            if dst.is_file:
                print("Destination is a file.")
                return
            if find_child(dst, src.name):
                print("Destination already has a node with the same name.")
                return
            parent = src.parent
            if parent.child == src:
                parent.child = src.next
            else:
                curr = parent.child
                while curr and curr.next != src:
                    curr = curr.next
                if curr:
                    curr.next = src.next
            src.parent = dst
            src.next = dst.child
            dst.child = src
        else:
            if "/" in args[2]:
                parts = args[2].rsplit('/', 1)
                parent_path = parts[0] if parts[0] else "/"
                new_name = parts[1]
            else:
                parent_path = "."
                new_name = args[2]
            parent_dst = self.get_node_by_path(parent_path)
            if parent_dst is None or parent_dst.is_file:
                print("Destination parent path is not valid.")
                return
            if find_child(parent_dst, new_name):
                print("A node with that name already exists in the destination.")
                return
            parent = src.parent
            if parent.child == src:
                parent.child = src.next
            else:
                curr = parent.child
                while curr and curr.next != src:
                    curr = curr.next
                if curr:
                    curr.next = src.next
            src.parent = parent_dst
            src.name = new_name
            src.next = parent_dst.child
            parent_dst.child = src

    def nwfiletxt_command(self, args):
        """
        The nwfiletxt command: Overwrites the content of a text file.
        Usage format:
        nwfiletxt <path>
        """
        if len(args) != 2:
            print("Usage: nwfiletxt <path>")
            return
        node = self.get_node_by_path(args[1])
        if node is None or not node.is_file:
            print("File not found or not a file.")
            return
        print("Enter new content for the file. Type '/end/' to finish.")
        new_lines = []
        while True:
            line = input()
            if line.strip() == "/end/":
                break
            new_lines.append(line)
        node.content = new_lines

    def appendtxt_command(self, args):
        """
        The appendtxt command: Appends text to the end of a file.
        Usage format:
            appendtxt <path>
        """
        if len(args) != 2:
            print("Usage: appendtxt <path>")
            return
        node = self.get_node_by_path(args[1])
        if node is None or not node.is_file:
            print("File not found or not a file.")
            return
        print("Enter text to append. Type '/end/' to finish.")
        while True:
            line = input()
            if line.strip() == "/end/":
                break
            node.content.append(line)

    def editline_command(self, args):
        """
        The editline command: Edits a specific line in a file.
        Usage format:
            editline <path> <line_number> <new_text>
        """
        if len(args) < 4:
            print("Usage: editline <path> <line_number> <new_text>")
            return
        node = self.get_node_by_path(args[1])
        if node is None or not node.is_file:
            print("File not found or not a file.")
            return
        try:
            line_number = int(args[2])
        except ValueError:
            print("Line number must be an integer.")
            return
        if line_number < 1 or line_number > len(node.content):
            print("Invalid line number.")
            return
        new_text = " ".join(args[3:])
        node.content[line_number - 1] = new_text

    def deline_command(self, args):
        """
        The deline command: Deletes a specific line from a file's contents.
        Usage format:
            deline <path> <line_number>
        """
        if len(args) != 3:
            print("Usage: deline <path> <line_number>")
            return
        node = self.get_node_by_path(args[1])
        if node is None or not node.is_file:
            print("File not found or not a file.")
            return
        try:
            line_number = int(args[2])
        except ValueError:
            print("Line number must be an integer.")
            return
        if line_number < 1 or line_number > len(node.content):
            print("Invalid line number.")
            return
        del node.content[line_number - 1]

    def cat_command(self, args):
        """
        The cat command: Displays the contents of a text file.
        Usage format:
            cat <path>
        """
        if len(args) != 2:
            print("Usage: cat <path>")
            return
        node = self.get_node_by_path(args[1])
        if node is None or not node.is_file:
            print("File not found or not a file.")
            return
        for line in node.content:
            print(line)

    def print_help(self):
        help_text = """
Available commands:
    ls                               : List contents of current directory
    mkdir [<path>] <folder_name>       : Create a directory
    touch [<path>] <file_name>.txt     : Create a text file
    cd <path>                        : Change directory
    rm <path>                        : Remove file or directory recursively
    rename <path> <new_name>           : Rename a file or directory
    cp <source_path> <destination_path> : Copy file or directory
    mv <source_path> <destination_path> : Move or rename file or directory
    nwfiletxt <path>                 : Overwrite file content
    appendtxt <path>                 : Append text to file
    editline <path> <line_number> <new_text> : Edit a specific line in a text file
    deline <path> <line_number>       : Delete a specific line from a text file
    cat <path>                       : Display contents of a text file
    help                             : Show this help message
    exit                             : Exit the program
"""
        print(help_text)


    def process_command(self, command_line):
        if not command_line.strip():
            return
        args = command_line.split()
        cmd = args[0]
        if cmd == "ls":
            self.ls_command(args)
        elif cmd == "mkdir":
            self.mkdir_command(args)
        elif cmd == "touch":
            self.touch_command(args)
        elif cmd == "cd":
            self.cd_command(args)
        elif cmd == "rm":
            self.rm_command(args)
        elif cmd == "rename":
            self.rename_command(args)
        elif cmd == "cp":
            self.cp_command(args)
        elif cmd == "mv":
            self.mv_command(args)
        elif cmd == "nwfiletxt":
            self.nwfiletxt_command(args)
        elif cmd == "appendtxt":
            self.appendtxt_command(args)
        elif cmd == "editline":
            self.editline_command(args)
        elif cmd == "deline":
            self.deline_command(args)
        elif cmd == "cat":
            self.cat_command(args)
        elif cmd == "help":
            self.print_help()
        else:
            print("Unknown command:", cmd)


    def get_full_path(self, node):
        """Organizes the absolute path from the root to the current directory for display in the prompt."""
        parts = []
        while node:
            parts.insert(0, node.name)
            node = node.parent
        return "/" + "/".join(parts[1:]) if len(parts) > 1 else "/"


    def run(self):
        """
        Starts the main loop for the virtual file system simulation.
        Displays a prompt with the current path and waits for user commands.
        Type 'exit' to quit.
        """
        print("Virtual File System Simulation. Type 'help' for commands.")
        while True:
            prompt_path = self.get_full_path(self.current)
            command_line = input(f"({prompt_path}) $ ")
            if command_line.strip() == "exit":
                break
            self.process_command(command_line)


