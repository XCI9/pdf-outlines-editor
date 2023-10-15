# Rotate all pages in a file by 180 degrees
from pikepdf import Pdf, make_page_destination, Outline, OutlineItem, Name
from typing import Optional


class PdfOutlineParser:
    pdf: Pdf
    outline: Outline
    parent_lookup: dict[OutlineItem, Optional[OutlineItem]] = {}

    def __init__(self):
        pass

    def open(self, filename: str):
        self.pdf = Pdf.open(filename)
        self.outline = self.pdf.open_outline()

    def get_children(self, parent: Optional[OutlineItem] = None):
        if parent is None:
            return self.outline.root
        else:
            return parent.children

    def add_child_offset(self, title: str, target: int,
                         parent: Optional[OutlineItem], sibling: Optional[OutlineItem],
                         offset: int = 0):
        """Add new outline item under specify parent, 
        position at index offset relative to specify sibling.

        Argument
        -----
        title : title of new outline item
        target : the target page of new outline item
        parent : the parent to place new outline
        sibling : the sibling as reference to place new outline,
            if None, it will append at the end of list
        offset : the distance to place new outline refer to sibling,
            ex. 0 (default) -> insert before, 1 -> insert after

        """
        children = self.get_children(parent)

        new_child = OutlineItem(title, target, 'FitB')
        if sibling is None:
            children.append(new_child)
        else:
            children.insert(children.index(sibling)+offset, new_child)
        self.parent_lookup[new_child] = parent
        return new_child

    def removeChild(self, child: OutlineItem):
        parent = self.parent_lookup[child]
        self.get_children(parent).remove(child)
        del self.parent_lookup[child]

    def moveUp(self, node: OutlineItem):
        parent = self.parent_lookup[node]

        children = self.get_children(parent)
        index = children.index(node)

        # already at up
        if index == 0:
            return

        # swap with prev item
        children[index - 1], children[index] = children[index], children[index - 1]

    def moveDown(self, node: OutlineItem):
        parent = self.parent_lookup[node]

        children = self.get_children(parent)
        index = children.index(node)

        # already at down
        if index == len(children) - 1:
            return

        # swap with next item
        children[index + 1], children[index] = children[index], children[index + 1]

    def moveIn(self, node: OutlineItem):
        parent = self.parent_lookup[node]
        children = self.get_children(parent)

        index = children.index(node)
        if index == 0:
            return
        del children[index]
        children[index-1].children.append(node)

        # new parent is prev sibling
        self.parent_lookup[node] = children[index-1]

    def moveOut(self, node: OutlineItem):
        parent = self.parent_lookup[node]
        if parent is None:
            raise TimeoutError("Already at root!")
        grandparent = self.parent_lookup[parent]

        # remove from old parent
        parent.children.remove(node)

        # grandparent is new parent
        children = self.get_children(grandparent)
        children.insert(children.index(parent) + 1, node)

        self.parent_lookup[node] = grandparent

    def move(self, new_parent: Optional[OutlineItem], prev_node: OutlineItem, node: OutlineItem):
        parent = self.parent_lookup[node]
        self.get_children(parent).remove(node)

        children = self.get_children(new_parent)

        children.insert(children.index(prev_node) + 1, node)
        self.parent_lookup[node] = new_parent

    def clear(self):
        self.outline.root.clear()
        self.parent_lookup.clear()

    def edit_node_name(self, node: OutlineItem, name: str):
        node.title = name

    def edit_node_target_page(self, node: OutlineItem, page: int):
        destination = make_page_destination(self.pdf, page)
        node.destination = destination

    def save(self, filename: str, page_mode: str):
        match page_mode:
            case 'UseNone':
                self.pdf.Root["/PageMode"] = Name.UseNone
            case 'UseOutlines':
                self.pdf.Root["/PageMode"] = Name.UseOutlines
            case 'UseThumbs':
                self.pdf.Root["/PageMode"] = Name.UseThumbs
            case 'FullScreen':
                self.pdf.Root["/PageMode"] = Name.FullScreen
            case 'UseOC':
                self.pdf.Root["/PageMode"] = Name.UseOC
            case 'UseAttachments':
                self.pdf.Root["/PageMode"] = Name.UseAttachments
        self.outline._save()
        self.pdf.save(filename)
