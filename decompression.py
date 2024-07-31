#Decompression
import huffman
import sys


path_file_compressed = sys.argv[1] 
path_dictionnary = 'huffman_dictionnary.json'
decompressed = huffman.decompress(path_file_compressed, path_dictionnary)