# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Object to represent the information at a node in the DAGCircuit."""
from __future__ import annotations
from typing import Dict, Optional, List, Tuple

from qiskit.exceptions import QiskitError
from qiskit.circuit import Instruction, Qubit, Clbit, ClassicalRegister
from qiskit.circuit.bit import Bit


class DAGNode:
    """Object to represent the information at a node in the ``DAGCircuit``.

    It is used as the return value from ``*_nodes()`` functions and can
    be supplied to functions that take a node.
    """

    def __init__(self, data_dict: Dict, nid: int = -1):
        """Create a node"""
        self._node_id = nid
        self.data_dict = data_dict

    @property
    def type(self) -> Optional[str]:
        """Returns the type of the node, else None"""
        return self.data_dict.get('type')

    @property
    def op(self) -> Optional[Instruction]:
        """Returns the Instruction object corresponding to the op for the node, else None"""
        if 'type' not in self.data_dict or self.data_dict['type'] != 'op':
            raise QiskitError("The node %s is not an op node" % (str(self)))
        return self.data_dict.get('op')

    @property
    def name(self) -> Optional[str]:
        """Returns the name of the node, else None"""
        return self.data_dict.get('name')

    @name.setter
    def name(self, new_name: str):
        """Sets the name of the node to be the given ``new_name``"""
        self.data_dict['name'] = new_name

    @property
    def qargs(self) -> List[Qubit]:
        """
        Returns list of Qubit, else an empty list.
        """
        return self.data_dict.get('qargs', [])

    @qargs.setter
    def qargs(self, new_qargs: List[Qubit]):
        """Sets the qargs to be the given list of ``new_qargs``."""
        self.data_dict['qargs'] = new_qargs

    @property
    def cargs(self) -> List[Clbit]:
        """
        Returns list of Clbit, else an empty list.
        """
        return self.data_dict.get('cargs', [])

    @property
    def condition(self) -> Optional[Tuple[ClassicalRegister, int]]:
        """
        Returns a tuple conatining a ClassicalRegister and the
        value of the condition, else None.
        """
        return self.data_dict.get('condition')

    @property
    def wire(self) -> Optional[Bit]:
        """
        Returns the Bit object corresponding to this wire, else None.
        """
        if self.data_dict['type'] not in ['in', 'out']:
            raise QiskitError('The node %s is not an input/output node' % str(self))
        return self.data_dict.get('wire')

    def __lt__(self, other):
        return self._node_id < other._node_id

    def __gt__(self, other):
        return self._node_id > other._node_id

    def __hash__(self):
        """Needed for ancestors function, which returns a set.
        To be in a set requires the object to be hashable
        """
        return hash(id(self))

    def __str__(self):
        # TODO is this used anywhere other than in DAG drawing?
        # needs to be unique as it is what pydot uses to distinguish nodes
        return str(id(self))

    @staticmethod
    def semantic_eq(node1: DAGNode, node2: DAGNode) -> bool:
        """
        Check if nodes are considered equivalent. This method is checked
        as a ``node_match`` for `nx.is_isomorphic()`_ in the ``networkx`` library.

        Args:
            node1: A node to compare.
            node2: The other node to compare.

        Return:
            If ``node1`` == ``node2``

        .. _nx.is_isomorphic(): https://networkx.github.io/documentation/networkx-1.10/reference/\
                                generated/networkx.algorithms.isomorphism.is_isomorphic.html
        """
        # For barriers, qarg order is not significant so compare as sets
        if 'barrier' == node1.name == node2.name:
            return set(node1.qargs) == set(node2.qargs)
        return node1.data_dict == node2.data_dict
