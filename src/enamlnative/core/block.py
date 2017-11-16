"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Apr 15, 2017

@author: jrm
"""
from atom.api import ForwardInstance, Enum
from enaml.core.declarative import Declarative, d_


class Block(Declarative):
    """ An object which dynamically insert's its children into another block's 
    parent object.

    The 'Block' object is used to cleanly and easily insert it's children
    into the children of another object. The 'Object' instance assigned to the
    'block' property of the 'Block' will be parented with the parent of
    the 'Block'. Creating a 'Block' with no parent is a programming
    error.

    """

    #: The Block to which this blocks children should be inserted into
    block = d_(ForwardInstance(lambda: Block))

    #: If replace, replace all parent's children (except the block of course)
    mode = d_(Enum('replace', 'append'))

    def initialize(self):
        """ A reimplemented initializer.

        This method will add the include objects to the parent of the
        include and ensure that they are initialized.

        """
        super(Block, self).initialize()

        block = self.block

        if block: #: This block is setting the content of another block
            #: Remove the existing blocks children
            if self.mode == 'replace':
                #: Clear the blocks children
                for c in block.children:
                    c.destroy()
            #: Add this blocks children to the other block
            block.insert_children(None, self.children)

        else: #: This block is inserting it's children into it's parent
            self.parent.insert_children(self, self.children)

    def _observe_block(self, change):
        """ A change handler for the 'objects' list of the Include.

        If the object is initialized objects which are removed will be
        unparented and objects which are added will be reparented. Old
        objects will be destroyed if the 'destroy_old' flag is True.

        """
        if self.is_initialized:
            if change['type'] == 'update':
                old_block = change['oldvalue']
                old_parent = old_block.parent
                for c in self.children:
                    old_parent.child_removed(c)
                new_block = change['value']
                new_block.parent.insert_children(new_block, self.children)

    def _observe__children(self, change):
        if not self.is_initialized:
            return
        block = self.block
        if change['type'] == 'update':
            if block:
                if self.mode == 'replace':
                    block.children = change['value']
                else:
                    for c in change['oldvalue']:
                        block.children.remove(c)
                        c.destroy()
                    before = block.children[-1] if block.children else None
                    block.insert_children(before, change['value'])
            else:
                for c in change['oldvalue']:
                    if c not in change['value']:
                        c.destroy()
                self.parent.insert_children(self, change['value'])
