"""
Member 3: DFA Output & Visualization
Display DFA states, transition table, initial/accepting states, and Graphviz diagram.

Integration: call show_dfa_output(root_or_parent, dfa) after subset_construction(...)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import tempfile
from pathlib import Path

from graphviz import Digraph
from PIL import Image, ImageTk


def build_dfa_graph(dfa):
    """Create a Graphviz Digraph for the DFA."""
    graph = Digraph("DFA", format="png")
    graph.attr(rankdir="LR", bgcolor="white")
    graph.attr("node", shape="circle", style="filled", fillcolor="white")
    graph.attr("edge", fontsize="12")

    # Use safe internal IDs while showing readable subset names.
    node_ids = {state: f"state_{i}" for i, state in enumerate(dfa.states)}
    graph.node("start", label="", shape="none", width="0", height="0")

    for state in dfa.states:
        label = dfa.state_name(state)
        if state in dfa.accepting_states:
            graph.node(node_ids[state], label=label, shape="doublecircle",
                       fillcolor="lightgoldenrod1")
        else:
            graph.node(node_ids[state], label=label)

    graph.edge("start", node_ids[dfa.initial_state])

    # Group labels for transitions with the same source and target.
    grouped = {}
    for (source, symbol), target in dfa.transitions.items():
        key = (source, target)
        grouped.setdefault(key, []).append(symbol)
    for (source, target), symbols in grouped.items():
        graph.edge(node_ids[source], node_ids[target],
                   label=", ".join(sorted(symbols)))

    return graph


def show_dfa_output(parent, dfa):
    """Open a window showing the DFA state summary, transition table and graph."""
    window = tk.Toplevel(parent)
    window.title("DFA Output & Visualization")
    window.geometry("1000x750")

    top = ttk.Frame(window, padding=10)
    top.pack(fill="x")
    ttk.Label(top, text="DFA Output", font=("Arial", 16, "bold")).pack(anchor="w")

    states_text = ", ".join(dfa.state_name(s) for s in dfa.states)
    accepting_text = ", ".join(
        dfa.state_name(s) for s in dfa.states if s in dfa.accepting_states
    ) or "None"

    ttk.Label(top, text=f"States: {states_text}", wraplength=950).pack(anchor="w", pady=3)
    ttk.Label(top, text=f"Initial state: {dfa.state_name(dfa.initial_state)}").pack(anchor="w")
    ttk.Label(top, text=f"Accepting states: {accepting_text}", wraplength=950).pack(anchor="w", pady=3)

    table_frame = ttk.LabelFrame(window, text="DFA Transition Table", padding=8)
    table_frame.pack(fill="x", padx=10, pady=5)

    rows = dfa.transition_table()
    columns = [f"col{i}" for i in range(len(rows[0]))]
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=min(len(rows), 10))
    tree.pack(side="left", fill="x", expand=True)
    for i, column in enumerate(columns):
        tree.heading(column, text=rows[0][i])
        tree.column(column, width=160, anchor="center")
    for row in rows[1:]:
        tree.insert("", "end", values=row)
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    graph_frame = ttk.LabelFrame(window, text="DFA Graph (Graphviz)", padding=8)
    graph_frame.pack(fill="both", expand=True, padx=10, pady=5)

    try:
        graph = build_dfa_graph(dfa)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = graph.render(filename="dfa_graph", directory=temp_dir,
                                      cleanup=True, view=False)
            image = Image.open(output_path).convert("RGB")
            # Scale large diagrams to fit the available window while preserving ratio.
            image.thumbnail((900, 430))
            photo = ImageTk.PhotoImage(image)
            image_label = ttk.Label(graph_frame, image=photo)
            image_label.image = photo  # Keep a reference to prevent image disappearance.
            image_label.pack(pady=5)

        def save_graph():
            try:
                graph.render(filename="dfa_graph", directory=".", format="png", cleanup=True)
                graph.save(filename="dfa_graph.gv")
                messagebox.showinfo("Saved", "Saved dfa_graph.png and dfa_graph.gv in the project folder.")
            except Exception as exc:
                messagebox.showerror("Save error", str(exc))

        ttk.Button(graph_frame, text="Save graph (PNG + DOT)", command=save_graph).pack(pady=5)
    except Exception as exc:
        ttk.Label(graph_frame, text=f"Could not render graph: {exc}").pack(anchor="w")

    return window