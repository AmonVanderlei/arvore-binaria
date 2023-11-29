import arvore_binaria

#Função que ordena um array usando heaps.
def heap_sort(heap, heap_arr = [], last = 0):
    if heap_arr == []:
        heap_arr = heap.to_array()
    if last == 0:
        last = heap.n_elementos - 1
    
    heap_arr[0], heap_arr[last] = heap_arr[last], heap_arr[0]
    
    new_tree = arvore_binaria.array2tree(heap_arr[0:last])
    new_tree.heapfy()
    tree_arr = new_tree.to_array()
    
    for i, _ in enumerate(tree_arr):
        heap_arr[i] = tree_arr[i]
    
    if last == 1:
        return heap_arr
    
    return heap_sort(heap, heap_arr, last-1)

#Cria uma lista não ordenada.
arr = [3, 5, 2, 8, 7, 1, 6, 4]

#Transforma o array em uma árvore binária.
tree = arvore_binaria.array2tree(arr)

#Imprime a árvore inicial gerada.
tree.print_tree()

#Transforma a árvore em heap.
tree.heapfy()

#Imprime a árvore depois de convertida em heap.
tree.print_tree()

#Imprime a lista ordenada.
print(heap_sort(tree))