# --- Smith and Waterman alignment script

from pickle import FALSE, TRUE
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
        New matrix completed from the Smith and Waterman algorithm 
    """
    # Creation of the transformed matrix

    row_seq = len(seq2) + 1
    col_seq = len(seq1) + 1
    transformed_matrix= np.zeros((row_seq, col_seq),dtype = int)
 
    for i in range(1,row_seq):
        
            for j in range(1,col_seq):
                
                left = transformed_matrix[i][j-1] 
                diagonal = transformed_matrix[i-1][j-1] + dot_matrix[i-1][j-1] 
                top = transformed_matrix[i-1][j]
                
                if top < 0:
                    
                    top = 0
                    
                if diagonal < 0:
                    
                    diagonal = 0
                    
                if left < 0:
                    
                    left = 0 
                    
                transformed_matrix[i,j] = max(diagonal, top, left)
    
    return(np.matrix(transformed_matrix)) 
   

def smith_waterman(seq1,seq2, transformed_matrix):
    """Smith and Waterman local alignment.

    Finds the optimal path starting from the maximum value of the transformed 
    matrix and going up to the first 0 met. Creating chain of string with gap when insertion
    or deletion occurs (top / left).


    /!\ The program choose the optimal as the first meet !
    
    
    Parameters
    ----------
    seq1: list
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
   
    # find the maximal score and the index in the transformed matrix 
    
    index_max = np.where(transformed_matrix == np.amax(transformed_matrix))
   
    idx_row = index_max[0] # tuple of max value indexes in row
    idx_col = index_max[1] # tuple of max value indexes in col   
    
    # Performs as many alignments as there are max 
    align_list = []
    for i, j in zip(idx_row, idx_col): 
        #From the right bottom to the left top
        aligned_sequence1 = ""
        aligned_sequence2 = ""
        
        check_zero = FALSE
        
        while i > 0 and j > 0:
            
            score_diagonal = transformed_matrix[i-1,j-1]
            score_left = transformed_matrix[i,j-1]
            score_top = transformed_matrix[i-1,j]
            max_value = max(score_diagonal, score_left, score_top)        

            # Calcule the score value
                
            if max_value == score_diagonal :

                aligned_sequence2 += seq2[i-1]
                aligned_sequence1 += seq1[j-1]
                i -= 1
                j -= 1
                
            elif max_value == score_top:

                aligned_sequence2 += seq2[i-1]
                aligned_sequence1 += '-'
                i -= 1
                        
            elif max_value == score_left :
                
                aligned_sequence2 += '-'
                aligned_sequence1 += seq1[j-1]
                j -= 1
                
            if max_value == 0:
                check_zero = TRUE
                break
                
        # finish when index in j or i = 0
        
        if not check_zero:
        
            while j > 0:
                
                aligned_sequence1 += seq1[j-1]
                aligned_sequence2 += '-'
                j -= 1
                
            while i > 0:
                
                aligned_sequence1 += '-'
                aligned_sequence2 += seq2[i-1]
                i -= 1
            
        aligned_sequence1 = aligned_sequence1[::-1]
        aligned_sequence2 = aligned_sequence2[::-1]

        align_list.append([aligned_sequence1, aligned_sequence2])
       
    return(align_list)


def transformation_SW_gp(dot_matrix, seq1, seq2):
    """Creation of the transformed matrix from the dot product matrix and 
    fasta sequences.

    The transformed matrix is created by following the Smith and Waterman algorithm 
    with the dot product matrix as the score matrix and a affine gap penalty set to:
    -1 for gap opening and 0 for gap extension

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
        New matrix completed from the Smith and Waterman algorithm 
    """
    # Creation of the transformed matrix

    row_seq = len(seq2) + 1
    col_seq = len(seq1) + 1
    transformed_matrix= np.zeros((row_seq, col_seq),dtype = int)
  
    # Create a penalty matrix of 1 (no penalty) and gap penalty
    
    penalty_matrix = np.ones((row_seq, col_seq),dtype = int)
    open_gap = -1
    extension_gap = 0
  
    for i in range(0,row_seq):
        
            for j in range(0,col_seq):
                 # First cell
                
                if i == 0 and j == 0:
                    transformed_matrix[i][j] = 0
                
                # First row
                
                elif i == 0:
                     
                    if penalty_matrix[i, j-1] == 1 : # no penalty
                        
                        transformed_matrix[i][j] = transformed_matrix[i][j-1] 
                 
                    else:
                        
                        transformed_matrix[i][j] = transformed_matrix[i][j-1] + penalty_matrix[i, j-1] # penalty
                    
                    if transformed_matrix[i][j] < 0:
                        transformed_matrix[i][j] = 0
                        
                    # Update penalty matrix
                     
                    if penalty_matrix[i, j-1] == 1: 
                        penalty_matrix[i,j] = open_gap
                    
                    else:
                        penalty_matrix[i,j] = extension_gap
                    
                    
                # First column
                
                elif j == 0:
                   
                    if penalty_matrix[i-1, j] == 1:
                        transformed_matrix[i][j] = transformed_matrix[i-1][j]
                    else:
                        transformed_matrix[i][j] = transformed_matrix[i-1][j] + penalty_matrix[i-1, j]
                    
                    if transformed_matrix[i][j] < 0:
                        transformed_matrix[i][j] = 0
                        
                     # Update penalty matrix
                     
                    if penalty_matrix[i-1, j] == 1:
                        penalty_matrix[i,j] = open_gap
                    
                    else:
                        penalty_matrix[i,j] = extension_gap
                        
            
                # Rest of the matrix
                            
                else:
                    
                 # ------- Score arround i,j    
                 
                    # if there isn't penalty in left cell : take left score
                    if penalty_matrix[i, j-1] == 1 :
                            
                        left= transformed_matrix[i][j-1] 
                        
                    else: # else score + penalty
                        left = transformed_matrix[i][j-1] +  penalty_matrix[i, j-1]    
                    
                    if left < 0:
                        left = 0      
                    # if there isn't penalty in top : take top score
                    if penalty_matrix [i-1][ j] == 1 :
                        
                        top = transformed_matrix[i-1][j] 
                        
                    else: 
                        # penalty
                        top =transformed_matrix[i-1][j] + penalty_matrix [i-1][ j]
                    
                    if top < 0:
                        top = 0  
                            
                       # no penalty
                    diagonal = transformed_matrix[i-1][j-1] + dot_matrix[i-1][j-1]
                    
                    if diagonal < 0:
                        diagonal = 0  
                    
            # ------- Check if it's gap opening or gap extension          
                   
                    # if left is max and if it's 1 in penalty matrix : gap opening 
                    max_val = max(top, left, diagonal)
                    
                    if max_val == left:
                        transformed_matrix[i,j] = left    
                                            
                        if penalty_matrix[i, j-1] == 1:
                            penalty_matrix[i,j] = open_gap
                        
                        else: # else it's a gap extension
                            penalty_matrix[i,j] = extension_gap
                        
                    
                    elif max_val == top: # if top is max and if it's 1 in penalty matrix : gap opening 
                        transformed_matrix[i,j] = top
                        
                        if penalty_matrix[i-1, j] == 1:
                            penalty_matrix[i,j] = open_gap
                        
                        else:  # else it's a gap extension
                            penalty_matrix[i,j] = extension_gap
                    
                    else:
                        transformed_matrix[i][j] = diagonal
                        penalty_matrix[i,j] = 1  
  
    return(np.matrix(transformed_matrix))