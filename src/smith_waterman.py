# --- Smith and Waterman alignment script

import numpy as np # import the numpy module and rename it

def transformation_SW(dot_matrix, seq1, seq2):
    """Creation of the transformed matrix from the dot product matrix and 
    fasta sequences.

    The transformed matrix is created by following the Smith and Waterman algorithm 
    with the dot product matrix as the score matrix and a fixed gap penalty set to 0

    Parameters
    ----------
    dot_matrix : array
        An array where each value corresponds to the dot product obtained 
        from the embedding vectors of one position of protein 1 and another
        position of protein 2.
    seq2: list
        list with every amino acids of fasta_file2 separated by quotes
    seq2: list
        list with every amino acids of fasta_file2 separated by quotes
        
    Returns
    -------
    transformed_matrix : matrix
        New matrix completed from the Needleman and Wunsch algorithm 
    """
    # Creation of the transformed matrix
    # print(dot_matrix.shape)
    row_seq1 = len(seq1) + 1
    col_seq2 = len(seq2) + 1
    transformed_matrix= np.zeros((row_seq1, col_seq2),dtype = int)
    # print(row_seq1, col_seq2)
    # print(transformed_matrix.shape)
    # print(transformed_matrix)
    for i in range(1,row_seq1):
        
            for j in range(1,col_seq2):
                
                top = transformed_matrix[i][j-1] 
                diagonal = transformed_matrix[i-1][j-1] + dot_matrix[i-1][j-1] 
                bottom = transformed_matrix[i-1][j]
                
                if top < 0:
                    
                    top = 0
                    
                if diagonal < 0:
                    
                    diagonal = 0
                    
                if bottom < 0:
                    
                    bottom = 0 
                    
                transformed_matrix[i,j] = max(diagonal, top, bottom)
    
    return(np.matrix(transformed_matrix)) 
   

def smith_waterman(seq1,seq2, transformed_matrix):
    """Smith and Waterman local alignment.

    Finds the optimal path starting from the maximum value of the transformed 
    matrix and going up to the first 0 met. Creating chain of string with gap when insertion
    or deletion occurs (top / left).


    /!\ The program choose the optimal as the first meet !
    
    
    Parameters
    ----------
    seq2: list
        list with every amino acids of fasta_file2 separated by quotes
    seq2: list
        list with every amino acids of fasta_file2 separated by quotes
    transformed_matrix : matrix
        Transformed matrix completed from the Needleman and Wunsch algorithm 
          
    Returns
    -------
    aligned_sequence1: string
        Chain of string composed of amino acid and gap
    aligned_sequence2: string
        Chain of string composed of amino acid and gap
    """
    # Find optimal path
    
    aligned_sequence1 = ""
    aligned_sequence2 = ""
    
    # find the maximal score and the index in the transformed matrix 
    
    #index_max = np.where(transformed_matrix == np.amax(transformed_matrix))
    index_max = np.unravel_index(np.argmax(transformed_matrix, axis=None), transformed_matrix.shape) # Take the first max met
    print(index_max)
 
    i = int(index_max[0])
    j = int(index_max[1])
    
    
#From the right bottom to the left top

    while i > 0 and j > 0:
        
        score_diagonal = transformed_matrix[i-1,j-1]
        score_top = transformed_matrix[i,j-1]
        score_left = transformed_matrix[i-1,j]
        max_value = max(score_diagonal, score_left, score_top)        

        # Calcule the score value
            
        if max_value == score_diagonal :

            aligned_sequence2 += seq2[j-1]
            aligned_sequence1 += seq1[i-1]
            i -= 1
            j -= 1
        
        elif max_value == score_top :

            aligned_sequence2 += seq2[j-1]
            aligned_sequence1 += '-'
            j -= 1
                       
        elif max_value == score_left :
            
            aligned_sequence2 += '-'
            aligned_sequence1 += seq1[i-1]
            i -= 1
            
    # finish
    
    while j > 0:
        
        aligned_sequence2 += seq2[j-1]
        aligned_sequence1 += '-'
        j -= 1
        
    while i > 0:
        
        aligned_sequence2 += '-'
        aligned_sequence1 += seq1[i-1]
        i -= 1
    
    aligned_sequence1 = aligned_sequence1[::-1]
    aligned_sequence2 = aligned_sequence2[::-1]
    
    return(aligned_sequence1, aligned_sequence2)