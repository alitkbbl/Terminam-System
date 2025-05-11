

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
    """Search among the children of a folder to find a node with a specific name"""
    current = parent.child
    while current:
        if current.name == name:
            return current
        current = current.next
    return None
