'''
defs regarding blast phases
'''

import BlastLoading as bl
import Graph_parameters as graph
from scipy.interpolate import interp1d

class BlastPhaseTimeHistories():

    def __init__(self) -> None:
        pass

    def compute_Pso(self, scaled_distance):
        PsoGraph = graph.BlastGraphBuilder.Build_Pso_BlastGraph()
        return PsoGraph.Get_y_coordinate(scaled_distance)

    def compute_ta(self, scaled_distance, mass_weight):
        tawGraph = graph.BlastGraphBuilder.Build_tA_BlastGraph()
        taw = tawGraph.Get_y_coordinate(scaled_distance)
        return bl.compute_w_clear(taw, mass_weight)

    def compute_Lw(self, scaled_distance, mass_weight):
        lwwGraph = graph.BlastGraphBuilder.Build_Lw_BlastGraph()
        Lww = lwwGraph.Get_y_coordinate(scaled_distance)
        return bl.compute_w_clear(Lww, mass_weight)

    def compute_to(self, scaled_distance, mass_weight):
        towGraph = graph.BlastGraphBuilder.Build_to_BlastGraph()
        tow = towGraph.Get_y_coordinate(scaled_distance)
        return bl.compute_w_clear(tow, mass_weight)  

    def compute_is(self, scaled_distance, mass_weight):
        f = graph.BlastGraphBuilder.Build_is_BlastGraph()
        isw = f.Get_y_coordinate(scaled_distance)
        return bl.compute_w_clear(isw, mass_weight)

    def compute_Cra(self, Pso):
        f = graph.BlastGraphBuilder.Build_Cra_BlastGraph()
        return f.Get_y_coordinate(Pso)

    def compute_Cr(self, Pso):
        f = graph.BlastGraphBuilder.Build_Cr_BlastGraph()
        return f.Get_y_coordinate(Pso)

    def compute_ir(self, Pso, mass_weight):
        f = graph.BlastGraphBuilder.Build_ir_BlastGraph()
        irw = f.Get_y_coordinate(Pso)
        return bl.compute_w_clear(irw, mass_weight)

    def compute_qo(self, Pso):
        f = graph.BlastGraphBuilder.Build_qo_BlastGraph()
        return f.Get_y_coordinate(Pso)

    def compute_new_scaled_distance_from_Pra(self, Pra):
        f = graph.BlastGraphBuilder.Build_Pra_BlastGraph()
        return f.Get_x_coordinate(Pra)

    def compute_new_scaled_distance_from_ira(self, ira, mass_weight):
        f = graph.BlastGraphBuilder.Build_ir_BlastGraph()
        return f.Get_x_coordinate(bl.compute_w_clear_reverse(ira, mass_weight))

    def compute_Pr_negative(self, scaled_distance):
        f = graph.BlastGraphBuilder.Build_Pr_negative_Blast_Graph()
        return f.Get_y_coordinate(scaled_distance)

    def compute_ir_negative(self, scaled_distance, mass_weight):
        f = graph.BlastGraphBuilder.Build_ir_negative_Blast_Graph()
        ir_negative = f.Get_y_coordinate(scaled_distance)
        return bl.compute_w_clear(ir_negative, mass_weight)

    def compute_trf_negative(self, Pra_negative, ira_negative):
        return 2*ira_negative/Pra_negative

    def compute_td(self, Lw_L, Pso, mass_weight):
        f = graph.BlastMultiGraphBuilder.Build_td_graph()
        td_w = f.Get_y_coordinate(Lw_L, Pso)
        return bl.compute_w_clear(td_w, mass_weight)

    def compute_Ce_positive(self, Lw_L):
        f = graph.BlastGraphBuilder.Build_Ce_positive_Blast_Graph()
        return f.Get_y_coordinate(Lw_L)

    def compute_Ce_negative(self, Lw_L):
        f = graph.BlastGraphBuilder.Build_Ce_negative_Blast_Graph()
        return f.Get_y_coordinate(Lw_L)

    def compute_tof_positive(self, Lw_L, Pso, mass_weight):
        f = graph.BlastMultiGraphBuilder.Build_tof_graph()
        tof_w = f.Get_y_coordinate(Lw_L, Pso)
        return bl.compute_w_clear(tof_w, mass_weight)

    def compute_tof_negative(self, Lw_L, mass_weight):
        f = graph.BlastGraphBuilder.Build_tof_negative_Graph()
        tof_w_negative = f.Get_y_coordinate(Lw_L)
        return bl.compute_w_clear(tof_w_negative, mass_weight)

    def front_wall_phase_graph(self, mass_weight, distance, structure_height, structure_width):
        '''
        
        '''

        # Step 1 
        # compute the scaled distance
        scaled_distance = bl.compute_scaled_distance(mass_weight, distance)

        # Step 2
        # get graph values
        Pso = self.compute_Pso(scaled_distance)
        ta  = self.compute_ta(scaled_distance, mass_weight)
        Lw  = self.compute_Lw(scaled_distance, mass_weight)
        to  = self.compute_to(scaled_distance, mass_weight)
        Is  = self.compute_is(scaled_distance, mass_weight)
        Ir  = self.compute_ir(Pso, mass_weight)
        Cr  = self.compute_Cr(Pso)
        Cra = self.compute_Cra(Pso)
        qo  = self.compute_qo(Pso) 

        # Step 4
        # compute extra parameters

        Pra = bl.compute_Pra_blast_parameter(Cra, Pso)
        tc  = bl.compute_clearing_time_tc_2(structure_height, structure_width, Cr)
        tof = bl.compute_tof(Is, Pso)
        trf = bl.compute_blast_wave_parameter_trf(Ir, Pra)
        Cd  = bl.compute_CD_coefficient(Pso)

        pressure_eq = Pso + Cd * qo

        x_new = [0,tof]
        y_new = [pressure_eq, 0]
        P = interp1d(x_new, y_new)

        # Step 5
        # create possitive phase (x,y)

        x = [0, tc, tof, to]
        y = [Pra, P(tc).round(4), 0, 0]

        # Step 6
        # get negative phase new scaled distances
        
        z_Pra = self.compute_new_scaled_distance_from_Pra(Pra)
        z_ira = self.compute_new_scaled_distance_from_ira(Ir, mass_weight)

        # Step 7 
        # get negative phases graph values

        Pra_negative = self.compute_Pr_negative(z_Pra)
        ira_negative = self.compute_ir_negative(z_ira, mass_weight)

        trf_negatice = self.compute_trf_negative(Pra_negative, ira_negative)

        # Step 8
        # get final negative phase values

        x.append(to + 0.27 * trf_negatice)
        x.append(to + trf_negatice)

        y.append(-Pra_negative)
        y.append(0)

        return (x,y)

    def side_wall_phase_graph(self, mass_weight, distance, structure_length):
        '''
        
        '''

        scaled_distance = bl.compute_scaled_distance(mass_weight, distance)

        Pso = self.compute_Pso(scaled_distance)
        Lw = self.compute_Lw(scaled_distance, mass_weight)
        to  = self.compute_to(scaled_distance, mass_weight)

        Lw_L = Lw/structure_length

        Ce = self.compute_Ce_positive(Lw_L)
        td = self.compute_td(Lw_L, Pso, mass_weight)
        tof = self.compute_tof_positive(Lw_L, Pso, mass_weight)

        Pof = Ce * Pso
        qo = self.compute_qo(Pof)

        Cd = -0.4

        p = Ce * Pso + Cd * qo

        Ce_negative = self.compute_Ce_negative(Lw_L)
        tof_negative = self.compute_tof_negative(Lw_L, mass_weight)
        Pr_negative = Ce_negative * Pso

        x = [0, td, min(to, tof), max(to, tof), to+0.27*tof_negative, to+tof_negative]
        y = [0, p,  0,   0,  -Pr_negative, 0]

        return (x,y)

