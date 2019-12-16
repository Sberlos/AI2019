
def compute_lenght(solution, dist_matrix):
    total_length = 0
    starting_node = solution[0]
    from_node = starting_node
    #print("from_node: {}".format(from_node))
    #print("solution: {}".format(solution))
    #print("len solution: {}".format(len(solution)))
    for node in solution[1:]:
        total_length += dist_matrix[from_node, node]
        from_node = node
    #print("fine compute")
    return total_length

