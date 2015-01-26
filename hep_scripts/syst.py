
def show(matrix):
    # Print out matrix
    for row in matrix:
        formatted_row = []
        for element in row:
            formatted_row.append(str(element*1000000)[:4])
        print formatted_row 
    print " "

def mult(matrix1,matrix2):
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
    else:
        # Multiply if correct dimensions
        new_matrix = zero(len(matrix1),len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
        return new_matrix

def add(matrix1,matrix2):
    # Matrix multiplication
    if (len(matrix1[0]) != len(matrix2[0])) or (len(matrix1)!= len(matrix2)) :
        # Check matrix dimensions
        print 'Matrices must equal dimensions!'
    else:
        new_matrix = zero(len(matrix1),len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                new_matrix[i][j] = matrix1[i][j]+matrix2[i][j]
        return new_matrix

def cor_matrix(m) : 
    new_matrix = [[1. for row in range(m)] for col in range(m)]
    return new_matrix

def uncor_matrix(m) : 
    new_matrix = [[0. for row in range(m)] for col in range(m)]
    for i in range(m):
        new_matrix[i][i] = 1.
    return new_matrix

def zero(m,n):
    # Create zero matrix
    new_matrix = [[0. for row in range(n)] for col in range(m)]
    return new_matrix


bins = 11

corM = uncor_matrix(bins)
show(corM)


syst_list = []
cor_list = []

ewk_syst = [0.0002,0.0003,0.0005,0.0002,0.0001,0.0001,0.0001,0.0002,0.0001,0.0002,0.0001]
syst_list.append(ewk_syst)
cor_list.append(1)
qcd_syst = [0.0010,0.0019,0.0022,0.0018,0.0005,0.0015,0.0014,0.0025,0.0013,0.0006,0.0016]
syst_list.append(qcd_syst)
cor_list.append(0)
pdf_syst = [0.0015,0.0016,0.0013,0.0015,0.0016,0.0017,0.0016,0.0017,0.0015,0.0015,0.0023]
syst_list.append(pdf_syst)
cor_list.append(1)
rec_syst = [0.0002,0.0004,0.0006,0.0008,0.0009,0.0008,0.0015,0.0007,0.0003,0.0011,0.0009]
syst_list.append(rec_syst)
cor_list.append(1)

M = zero(bins,bins) 

for cor, syst in  zip( cor_list,syst_list):
  M_new = zero(bins,bins) 
  if cor:
    cor_M = cor_matrix(bins)
  else:
    cor_M = uncor_matrix(bins)
  for i in range(bins):
    for j in range(bins):
      M_new[i][j]=cor_M[i][j]*syst[i]*syst[j]
    
  show(M_new)
  M = add(M,M_new)

show(M)



