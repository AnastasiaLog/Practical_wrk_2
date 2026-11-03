def make_graph(root, packages):
    graph = {}

    def dfs(name):
        graph[name] = set()
        for dep in packages.get(name, set()):
            if dep not in graph:
                dfs(dep)
            graph[name].add(dep)

    dfs(root)
    return graph