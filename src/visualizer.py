def to_plantuml(graph, root):
    lines = ["@startuml", f"title {root} dependencies"]
    for name in graph:
        for dep in graph[name]:
            lines.append(f"[{name}] --> [{dep}]")
    lines.append("@enduml")
    return "\n".join(lines)

def print_ascii_tree(graph, name, prefix="", visited=None):
    if visited is None:
        visited = set()
    print(prefix + name)
    if name in visited:
        print(prefix + "  (цикл)")
        return
    visited.add(name)
    for dep in sorted(graph.get(name, set())):
        print_ascii_tree(graph, dep, prefix + "  ", visited)

def save_plantuml(graph, root, filename="graph.puml"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(to_plantuml(graph, root))
    return filename