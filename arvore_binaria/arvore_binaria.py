import numpy as np
from typing import Union, List, Tuple

class ArvoreBinaria:
    def __init__(self, 
                 valor: float, 
                 esquerda: 'ArvoreBinaria', 
                 direita: 'ArvoreBinaria', 
                 n_elementos: int):
        """Inicializa uma Árvore Binária.

        Args:
            valor (float): Valor do nó raiz da árvore.
            esquerda (ArvoreBinaria): Árvore a partir do filho à esquerda da raiz.
            direita (ArvoreBinaria): Árvore a partir do filho à direita da raiz.
            n_elementos (int): Número de elementos em toda a árvore. Qualquer 
                sub-árvore terá o mesmo número de elementos que a árvore principal.
        """
        self.valor = valor
        self.direita = direita
        self.esquerda = esquerda
        self.n_elementos = n_elementos
        
    def _max_heap(self, 
                  i: int, 
                  arr: List[float] = []) -> List[float]:
        """Transforma um nó e seus filhos em um heap máximo.

        Args:
            i (int): Índice do nó pai.
            arr (List[float], optional): Array onde o nó se encontra. Defaults to [].

        Returns:
            List[float]: Array que inclui o heap máximo.
        """
        
        #Se não houver um array, pega a própria árvore.
        if arr == []:
            arr = self.to_array()
        
        #Encontra o pai e os filhos
        #Tenta encontrar um valor para os filhos. Se não encontrar, o valor é 
        #   menos infinito para desconsiderar nas comparações.
        parent = arr[i]
        
        try:
            left = arr[(2*i)+1]
        except:
            left = float("-inf")
            
        try:
            right = arr[(2*i)+2]
        except:
            right = float("-inf")
        
        #Verifica se algum filho é maior que o pai.
        if left > parent or right > parent:
            #Troca o pai com o filho, que tenta "descer" ainda mais na árvore.
            if left > right:
                arr[(2*i)+1], arr[i] = arr[i], arr[(2*i)+1]
                return self._max_heap((2*i)+1, arr)
            else:
                arr[(2*i)+2], arr[i] = arr[i], arr[(2*i)+2]
                return self._max_heap((2*i)+2, arr)

        return arr

    def _root_left_right(self, 
                         arr: List[float], 
                         index_arr: List[int] = []
                         ) -> Tuple[int, List[int], List[int]]:
        """Encontra a raíz, a árvore à esquerda e a árvore à direita de uma 
            árvore binária.

        Args:
            arr (List[float]): Árvore em forma de array.
            index_arr (List[int], optional): Array com os índices de uma 
                árvore no arr. Defaults to [].

        Returns:
            Tuple[int, int, int]: Retorna a raíz, a árvore à esquerda e a 
                árvore à direita da árvore cujos índices estão em index_arr.
        """
        #Se index_arr não for passado, pega os índices de arr.
        if index_arr == []:
            index_arr = [x for x in range(len(arr))]
            
        root = index_arr[0]
        
        #Se a árvore tiver elementos além da raiz,
        if len(index_arr) > 1:
            #Cria a sub-árvore da esquerda com seu primeiro elemento.
            left = [index_arr[1]]
            
            #Se tiver elementos além da raiz e do primeiro da parte esquerda,
            if len(index_arr) > 2:
                #Cria a sub-árvore da direita com seu primeiro elemento.
                right = [index_arr[2]]
            else:
                #A sub-árvore da direita não tem elementos.
                right = []
        else:
            #As sub-árvores da direita e esquerda não têm elementos.
            left = []
            right = []

        for i in index_arr:
            if i != root:
                #Pega os filhos do elemento de índice i.
                children = [None, None]
                try:
                    children[0] = arr[(2*i)+1]
                    children[0] = (2*i)+1
                except:
                    children[0] = None
                    
                try:
                    children[1] = arr[(2*i)+2]
                    children[1] = (2*i)+2
                except:
                    children[1] = None
                
                #Se o elemento de índice i está à esquerda,
                if i in left:
                    #Adiciona seus filhos na esquerda.
                    left += [children[0], children[1]]
                else:
                    #Senão, adiciona na parte direita.
                    right += [children[0], children[1]]
        
        #Retira os filhos das folhas das sub-árvores (None)
        left = [n for n in left if n != None]
        right = [n for n in right if n != None]
        
        return (root, left, right)

    def _array2tree(self, 
                    arr: List[float], 
                    index_arr: List[int] = []
                    ) -> 'ArvoreBinaria':
        """Transforma um array em um objeto ArvoreBinária.

        Args:
            arr (List[float]): Array com todos os elementos da árvore.
            index_arr (List[int], optional): Índices dos elementos que 
                formarão a árvore. Defaults to [].

        Returns:
            ArvoreBinaria: Árvore a partir dos índices e elementos dados.
        """
        root, left, right = self._root_left_right(arr, index_arr)
        
        #Se não for uma lista vazia, transforma em uma árvore.
        if left != []:
            left = array2tree(arr, left)
        if right != []:
            right = array2tree(arr, right)

        tree = ArvoreBinaria(arr[root], left, right, len(arr))
        
        return tree
    
    def heapfy(self) -> None:
        """Transforma a árvore binária em um heap máximo.
        """
        arr = self.to_array()
        
        #Aplica _max_heap para cada índice da metade pra baixo.
        for i in range(int(np.floor((len(arr)-1)/2)), -1, -1):
            arr = self._max_heap(i, arr)

        #Transforma o novo array (heap) em uma árvore.
        new_tree = self._array2tree(arr)
        
        #Transfere os valores da nova árvore para ela mesma
        self.valor = new_tree.valor
        self.esquerda = new_tree.esquerda
        self.direita = new_tree.direita
        
    def to_array(self, 
                 tree_arr: List[Union[str, float]] = [], 
                 i: int = 0) -> List[float]:
        """Transforma a árvore em um array.

        Args:
            tree_arr (List[Union[str, float]], optional): Árvore em formato de array. Defaults to [].
            i (int, optional): Índice do nó a ser adicionado. Defaults to 0.

        Returns:
            List[float]: Array que representa a árvore.
        """
        
        #Se for vazio, coloca a mesma quantidade de elementos que a árvore.
        if tree_arr == []:
            tree_arr = ["-"]*self.n_elementos
        
        #Adiciona o valor na posição correta do array.
        tree_arr[i] = self.valor
        
        #Se houver um objeto, chama o método to_array dele.
        if self.esquerda != []:
            self.esquerda.to_array(tree_arr, (2*i)+1)
        if self.direita != []:
            self.direita.to_array(tree_arr, (2*i)+2)
        
        #Para evitar IndexError, o array é criado com o n_elementos. Como as
        #   sub-árvores são menores, retira os espaços vazios.
        tree_arr = [n for n in tree_arr if n != "-"]

        return tree_arr

    def print_tree(self):
        """Imprime a árvore visualmente.
        """
        
        #Pega o array e a altura da árvore.
        arr = self.to_array()
        #Altura: Piso do log do número de elementos da árvore na base 2, mais um.
        height = int(np.floor(np.log2(self.n_elementos)) + 1)
        elements_per_level = 1
        
        #Para cada level,
        for i in range(height):
            values = ""
            
            #Escreve os valores do level com um espaço entre eles.
            for j in range(elements_per_level):
                if arr != []:
                    values += f"{' '*height}{arr.pop(0)}"
                    
            #Imprime o level.
            print(" "*2*height, values)
            
            #Muda a altura e a quantidade de elementos para impressão.
            height -= 1
            elements_per_level *= 2
        

def children(arr: List[float],
             i: int
             ) -> Tuple[Union[int, None], Union[int, None]]:
    """Retorna os filhos de um nó.

    Args:
        arr (List[float]): Array com todos os nós.
        i (int): Índice do nó.

    Returns:
        Tuple[Union[int, None], Union[int, None]]: Índices dos filhos do nó de índice i.
    """
    try:
        left = arr[(2*i)+1]
        left = (2*i)+1
    except:
        left = None
        
    try:
        right = arr[(2*i)+2]
        right = (2*i)+2
    except:
        right = None

    return (left, right)

def root_left_right(arr: List[float], 
                    index_arr: List[int] = []
                    ) -> Tuple[int, List[int], List[int]]:
    """Encontra a raíz, a árvore à esquerda e a árvore à direita de uma 
            árvore binária.

        Args:
            arr (List[float]): Árvore em forma de array.
            index_arr (List[int], optional): Array com os índices de uma 
                árvore no arr. Defaults to [].

        Returns:
            Tuple[int, int, int]: Retorna a raíz, a árvore à esquerda e a 
                árvore à direita da árvore cujos índices estão em index_arr.
    """
    
    #Se index_arr não for passado, pega os índices de arr.
    if index_arr == []:
        index_arr = [x for x in range(len(arr))]
        
    root = index_arr[0]
    
    #Se a árvore tiver elementos além da raiz,
    if len(index_arr) > 1:
        #Cria a sub-árvore da esquerda com seu primeiro elemento.
        left = [index_arr[1]]
        
        #Se tiver elementos além da raiz e do primeiro da parte esquerda,
        if len(index_arr) > 2:
            #Cria a sub-árvore da direita com seu primeiro elemento.
            right = [index_arr[2]]
        else:
            #A sub-árvore da direita não tem elementos.
            right = []
    else:
        #As sub-árvores da direita e esquerda não têm elementos.
        left = []
        right = []

    for i in index_arr:
        if i != root:
            #Pega os filhos do elemento de índice i.
            child = children(arr, i)
            
            #Se o elemento de índice i está à esquerda,
            if i in left:
                #Adiciona seus filhos na esquerda.
                left += [child[0], child[1]]
            else:
                #Senão, adiciona na parte direita.
                right += [child[0], child[1]]
    
    #Retira os filhos das folhas das sub-árvores (None)
    left = [n for n in left if n != None]
    right = [n for n in right if n != None] 
    
    return (root, left, right)

def array2tree(arr: List[float], 
               index_arr: List[int] = []
               ) -> 'ArvoreBinaria':
    """Transforma um array em um objeto ArvoreBinária.

    Args:
        arr (List[float]): Array com todos os elementos da árvore.
        index_arr (List[int], optional): Índices dos elementos que 
            formarão a árvore. Defaults to [].

    Returns:
        ArvoreBinaria: Árvore a partir dos índices e elementos dados.
    """
    root, left, right = root_left_right(arr, index_arr)
    
    #Se não for uma lista vazia, transforma em uma árvore.
    if left != []:
        left = array2tree(arr, left)
    if right != []:
        right = array2tree(arr, right)
    
    n_elementos = len(arr)
    
    tree = ArvoreBinaria(arr[root], left, right, n_elementos)
    
    return tree
