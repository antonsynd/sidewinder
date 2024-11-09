#!/usr/bin/env python3
import argparse
from io import StringIO
from pathlib import Path
from typing import MutableSequence, Optional

import antlr4.tree.Tree
from antlr4 import ParserRuleContext
from graphviz import Digraph
from PythonParser import PythonParser

from sidewinder.compiler_toolchain.antlr.ast_builder import AntlrASTBuilder, FileInputContext


def main() -> None:
    args = parse_args()

    input_path: Path = args.input
    input_buffer = StringIO(input_path.read_text())
    output_path: Path = args.output

    antlr_builder = AntlrASTBuilder()
    parser: PythonParser = antlr_builder._create_parser(input=input_buffer)
    parse_tree: FileInputContext = parser.file_input()

    pruned_tree: FileInputContext = prune_tree(node=parse_tree)
    dot: Digraph = antlr_tree_to_dot(tree=pruned_tree, parser=parser)
    dot.render(outfile=output_path, format="png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)

    return parser.parse_args()


def prune_tree(node: FileInputContext) -> FileInputContext:
    # Check if node text is empty; if so, ignore this node (prune it)
    if not node.getText().strip():
        return None

    if isinstance(node, antlr4.tree.Tree.TerminalNodeImpl):
        return node

    # Recursively prune each child node
    pruned_children: MutableSequence[FileInputContext] = []
    for child in node.getChildren():
        pruned_child = prune_tree(child)
        if pruned_child:  # Only keep non-pruned children
            pruned_children.append(pruned_child)

    # Update children list to only include pruned children
    node.children = pruned_children

    # If the node has exactly one child
    if node.getChildCount() == 1:
        # If its child is terminal, keep this node
        if isinstance(node.getChild(0), antlr4.tree.Tree.TerminalNodeImpl):
            return node
        else:
            # Otherwise get the child directly
            return node.getChild(0)

    return node


def print_class_hierarchy(obj):
    # Print __slots__ for each class in the hierarchy
    print("Slots in hierarchy:")
    for cls in obj.__class__.__mro__:
        if hasattr(cls, "__slots__"):
            slots = cls.__slots__
            # Slots may be defined as a single string or a tuple of strings
            if isinstance(slots, str):
                slots = (slots,)
            print(f"{cls}: {slots}")


def antlr_tree_to_dot(
    tree: FileInputContext,
    parser: PythonParser,
    dot: Optional[Digraph] = None,
):
    if not dot:
        dot = Digraph()

    label: str = tree.getText()
    if not label:
        label = "<empty>"

    simple_label: str = label.replace("\n", "\\n")

    if isinstance(tree, ParserRuleContext):
        rule_index: int = tree.getRuleIndex()
        rule_name: str = parser.ruleNames[rule_index] if rule_index >= 0 else "<unknown_rule>"
        label += f"\nRule: {rule_name}"

        simple_label += f" [Rule: {rule_name}]"

    print(f"Label: '{simple_label}'")
    print_class_hierarchy(tree)
    print()

    dot.node(name=str(id(tree)), label=label)

    if not isinstance(tree, antlr4.tree.Tree.TerminalNodeImpl):
        for child in tree.getChildren():
            dot.edge(tail_name=str(id(tree)), head_name=str(id(child)))
            antlr_tree_to_dot(tree=child, parser=parser, dot=dot)

    return dot


if __name__ == "__main__":
    main()
