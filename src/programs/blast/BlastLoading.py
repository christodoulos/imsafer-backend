'''
contains all blast loading computations
'''

def compute_scaled_distance(mass_weight, blast_distance):
    '''
    Compute scaled distance Z 
    intput:
    - mass weight (W) 
    - blast distance (R)
    output:
    - scaled distance (Z)
    '''

    return blast_distance / mass_weight**(1/3)

def compute_Pra_blast_parameter(Cra, Pso):
    '''
    Compute Pra 
    input:
    - Cra 
    - Pso (psi)
    output:
    - Pra (psi)
    '''

    return Cra * Pso

def compute_clearing_time_tc_2(front_wall_height, front_wall_width, Cr):

    R = compute_R_blast_parameter(front_wall_height, front_wall_width)
    S = compute_S_blast_parameter(front_wall_height, front_wall_width)

    return compute_clearing_time_tc(S,R,Cr)

def compute_S_blast_parameter(front_wall_height, front_wall_width):
    '''
    compute s blast parameter 
    input:
    - front wall height 
    - front wall width
    output:
    - s parameter
    '''

    return min(front_wall_height, 1/2 * front_wall_width)

def compute_G_blast_parameter(front_wall_height, front_wall_width):
    '''
    compute g blast parameter 
    input:
    - front wall height 
    - front wall width
    output:
    - g parameter
    '''

    return max(front_wall_height, 1/2 * front_wall_width)

def compute_R_blast_parameter(front_wall_height, front_wall_width):
    '''
    compute R blast parameter 
    input:
    - front wall height 
    - front wall width
    output:
    - R parameter
    '''

    S = compute_S_blast_parameter(front_wall_height, front_wall_width)
    G = compute_G_blast_parameter(front_wall_height,front_wall_width)

    return S/G

def compute_clearing_time_tc(S, R, Cr):
    '''
    compute clearing time tc 
    input:
    - parameter S
    - parameter R
    - sound velocity Cr (ft/ms)
    output:
    - tc (ms)
    '''

    return 4*S/((1+R)*Cr)

def compute_tof(Is, Pso):
    '''
    compute tof
    input:
    - Is (psi - ms)
    - Pso (psi)
    output:
    - tof (ms)
    '''

    return 2*Is/Pso

def compute_w_clear(number, mass_weight):
    return number * mass_weight**(1/3)

def compute_w_clear_reverse(number, mass_weight):
    return number / mass_weight**(1/3)
 
def compute_blast_wave_parameter_trf(Ira, Pra):
    '''
    compute trf (ms)
    input:
    - Ira (psi-ms)
    - Pra (psi)
    output:
    - tfr (ms)
    '''

    return 2*Ira/Pra

def compute_CD_coefficient(Pso):
    '''
    for now this coefficient is equal to 1.0 
    but it can be more...!
    '''

    return 1.0

