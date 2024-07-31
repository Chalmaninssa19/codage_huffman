from collections import defaultdict, Counter
import os
import json
import math
#from graphviz import Digraph
#from IPython.display import Image

#La classe noeud
class Node :
    def __init__(self,symbol,value) :
        self.symbol = symbol
        self.value = value
        self.right_son = None
        self.left_son = None
        self.huff = ''
        
#Creer la foret
def create_forest(symbols, probabs):
    nodes = []
    for i in range(len(symbols)) :
        nodes.append(Node(symbols[i], probabs[i]))
    return nodes

#Afficher la foret
def print_forest(forest) :
    for i in range(len(forest)) :
        print(forest[i].symbol + " : " + str(forest[i].value))

#Afficher un noeud
def print_node(node) :
    if node.left_son and node.right_son:
        print(node.symbol + " : " + str(node.value) + " ; gauche = " + node.left_son.symbol + ", droite = "+node.right_son.symbol)
    else :
        print(node.symbol + " : " + str(node.value) + " ; gauche = none, droite = none")

#Algorithme de tri par selection
def triSelection(tab) :
    for i in range(len(tab)) :
        for j in range(i+1, len(tab)) :
            if (tab[j].value < tab[i].value) :
                p = tab[i]
                tab[i] = tab[j]
                tab[j] = p
    return  tab

#Avoir le noeud ayant la valeur minimum du probabilite
def get_min_forest(forest) :
    min_value = forest[0]
    for i in range(len(forest)) :
        if min_value.value > forest[i].value :
            min_value = forest[i]

    return min_value

#Avoir les deux noeuds minimum d'une foret
def get_two_node_min(forest) :
    list = []
    i = 2
    while i > 0 :
        min = forest[0]
        list.append(min)
        forest.pop(0)
        i = i - 1
    return list

#Somme de valeur probabiltes d'une foret
def sum(forest) :
    sum = 0
    for i in range(len(forest)) :
        sum = sum + forest[i].value

    return sum
    
#Ajouter dans la liste la somme des deux minimum
def add_sum_in_list(forest, two_node_min) :
    new_symbol = two_node_min[0].symbol + "" + two_node_min[1].symbol
    new_value = sum(two_node_min)
    new_node = Node(new_symbol, new_value)
    two_node_min[0].huff = 1
    two_node_min[1].huff = 0
    new_node.left_son = two_node_min[0]
    new_node.right_son = two_node_min[1]
    forest.append(new_node)

#Avoir les noeuds feuilles
def get_forest_node(text) :
    freq_dict = Counter(text)
    forest = [Node(symbol, value) for symbol, value in freq_dict.items()]
    return forest
    
#Creer l'arbre de huffman
def build_huffman_tree(text) : 
    forest = get_forest_node(text)
    forest_sorted = triSelection(forest)
    while(len(forest_sorted) > 1) :
        two_node_min = get_two_node_min(forest_sorted)
        add_sum_in_list(forest_sorted, two_node_min)
        forest_sorted = forest_sorted = triSelection(forest_sorted)
    return forest_sorted[0]
    
#Creer le codage de huffman pour chaque caractere
def build_huffman_codes(node, code="", huffman_codes={}):
    if node:
        if not node.left_son and not node.right_son:
            huffman_codes[node.symbol] = code
        build_huffman_codes(node.left_son, code + "1", huffman_codes)
        build_huffman_codes(node.right_son, code + "0", huffman_codes)
    return huffman_codes

#Encode le text par le dictionnaire d'encodage
def encode(text, huffman_codes_dict):
    encoded_text = "".join(huffman_codes_dict[char] for char in text)
    return encoded_text

#Dictionnaire d'encodage
def get_huffman_dictionnaries(text) :
    if not text:
        return "", None

    huffman_tree = build_huffman_tree(text)
    huffman_codes = build_huffman_codes(huffman_tree)
    return huffman_codes

#Sauvegarder le dictionnaire dans un fichier
def save_dictionnary(dictionnary, path) :
    json_data = json.dumps(dictionnary)
        
    with open(path, "w") as fichier:
        fichier.write(json_data)

#Avoir le dictionnaire depuis un fichier
def get_dictionnary(path) :   
    with open(path, "r") as fichier:
        json_data = fichier.read()
            
    my_dict = json.loads(json_data)

    return my_dict

#Renverser le dictionnaire
def reverse_dictionnary(dict) :
    dictionnary_renverse = {value: cle for cle, value in dict.items()}

    return dictionnary_renverse


#Encoder le text par le codage de huffman
def huffman_encoding(text):
    if not text:
        return "", None

    huffman_tree = build_huffman_tree(text)
    huffman_codes = build_huffman_codes(huffman_tree)
    dict = get_huffman_dictionnaries(text)   
    
    #min = min_change(dict, text, 'o')
    #print('Minimum de changement = ' + str(min))
    forest = get_forest_node(text)
    long = calcul_longueur_moyenne(dict, forest, len(text))
    entropie = calcul_entropie(forest, len(text))
    entrop = entropie / math.log2(2)
    entrop1 = entrop +1
    print("Entropie = "+str(entropie))
    print("Longueur moyenne = "+str(long))
    print(str(entrop) + " <= " + str(long) + " < " + str(entrop1))
    save_dictionnary(huffman_codes, 'huffman_dictionnary.json')
    encoded_text = encode(text, huffman_codes)

    return encoded_text, huffman_tree

#Complete la chaine de caractere de sequence de bit encoder 
#en un multiple de 8
def pad_encoded_text(encoded_text) :
    #Nombre de bit a ajouter
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding) :
        encoded_text += "0"
        
    #Formater extra_padding en une chaine caracatere binaire de 8 bits
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text

#Convertit la sequence de bit encoder et rembourrer
#en un tableau d'octets
def get_byte_array(padded_encoded_text) :
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))

    return b

#Compresion du fichier par methode de huffman
def compress(path) :
    filename, file_extension = os.path.splitext(path)
    output_path = filename + ".bin"

    with open(path, 'r') as file, open(output_path, 'wb') as output :
        text = file.read()
        text = text.rstrip()

        encoded_text, huffman_tree = huffman_encoding(text)

        #Afficher l'image de l'arbre binaire
        #dot = draw_tree(huffman_tree)
        #dot.render('tree', format='png', view=True)

        padded_encoded_text = pad_encoded_text(encoded_text)
        b = get_byte_array(padded_encoded_text)
        output.write(bytes(b))

    print("Compressed")
    return output_path

#Supprimer les bits rebourrers
def remove_padding(bit_string) :
    padded_info = bit_string[:8]
    extra_padding = int(padded_info, 2)

    bit_string = bit_string[8:]
    encoded_text = bit_string[:-1*extra_padding]

    return encoded_text

#Decoder le texte encoder en servant du dictionnaire
def decode_text(encoded_text, path_dictionnary) :
    current_code = ""
    decoded_text = ""
    dictionnary = get_dictionnary(path_dictionnary)
    dict_reverse = reverse_dictionnary(dictionnary)
    
    for bit in encoded_text:
        current_code += bit
        if(current_code in dict_reverse) :
            character = dict_reverse[current_code]
            decoded_text += character
            current_code = ""

    return decoded_text
    
#Decodage de huffman
def huffman_decoding(encoded_text, path_dictionnary):
    if not encoded_text :
        return ""

    decoded_text = decode_text(encoded_text, path_dictionnary)

    return decoded_text
    
#Decompression d'un fichier compresser
def decompress(input_path, path_dictionnary) :
    filename, file_extension = os.path.splitext(input_path)
    output_path = filename + "_decompressed" + ".txt"

    with open(input_path, 'rb') as file, open(output_path, 'w') as output :
        bit_string = ""
        byte = file.read(1)
        while(len(byte) > 0) :
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
            
        encoded_text = remove_padding(bit_string)
        decoded_text = huffman_decoding(encoded_text, path_dictionnary)
        output.write(decoded_text)
        
    print("Decompressed")
    return output_path

#Afficher l'arbre binaire
def print_tree(node) :
    if node.left_son and node.right_son:
        print_node(node)
        print_tree(node.left_son)
        print_tree(node.right_son)
    print_node(node)

#Calculer l'entropie de la source d'information
def calcul_entropie(forest, size) : 
    entropie = 0
    for i in range(len(forest)) :
        prob = float(forest[i].value / size)
        value = prob * math.log2(prob)
        entropie = entropie + value
    return -entropie

#Longueur moyenne du codage optimal
def calcul_longueur_moyenne(dictionnary, forest, size) :
    sum = 0
    for i in range(len(forest)) :
        for key in dictionnary :
            if forest[i].symbol == key :
                code_size = len(dictionnary[key])
                prob = float(forest[i].value / size)
                longueur = code_size * prob
                sum = sum + longueur
    return sum

#Taux de changement du codage si on ajoute une lettre au texte
def min_change(dictionnary, text, letter) :
    min = 0
    value_before = dictionnary[letter]
    value_after = dictionnary[letter]
    while value_before == value_after:
        text = text + '' + letter
        dict2 = get_huffman_dictionnaries(text)
        value_after = dict2[letter]
        min = min + 1

    return min


#Dessiner un arbre binaire
#def draw_tree(root):
    #dot = Digraph()
    #if not root:
        #return dot
    #stack = [(root, None)]
    #while stack:
        #node, parent = stack.pop()
        #dot.node(node.symbol)
        #if parent:
            #dot.edge(parent.symbol, node.symbol)
        #if node.right_son:
            #stack.append((node.right_son, node))
        #if node.left_son:
            #stack.append((node.left_son, node))

    #return dot