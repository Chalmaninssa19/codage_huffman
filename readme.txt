Pour compresser un fichier 
---------------------------
-Ouvrir un terminal dans le repertoire codage_huffman
-executer la commande suivante : python compression.py "nom_fichier_a_compresser.txt"

Pour decompresser un fichier 
---------------------------
-Ouvrir un terminal dans le repertoire codage_huffman
-executer la commande suivante : python decompression.py "nom_fichier_a_decompresser.bin"

Phase de Compression Huffman
----------------------------
1.Chercher la probabilite de chaque lettre dans le texte
2.Creer un foret de noeud grace au probabilite et lettre 
3.Creer l'arbre de Huffman grace au noeud
4.Trouver le code de Huffman associe a chaque lettre en parcourant l'arbre depuis la racine sachant que la direction droite sera assigner a 0 et direction gauche 1, puis enregistrer le dictionnaire du codage dans un fichier json
5.Coder le texte via le dictionnaire 
6.Rebourrer le texte encoder qui est une chaine de succession de bit par 8 bits
7.Convertir le succession de bit encoder et rebourrer en un tableau d'Octet qui sera enregsitrer dans un fichier 


Phase de decompression de Huffman
---------------------------------
1.Lire le fichier compresser
2.Convertir le texte contenu en une chaine de succession binaire 
3.Supprimer le rebourrage pour trouver le texte encoder originaire
4.Decoder le texte originaire via le dictionnaire du codage enregistrer depuis un fichier

