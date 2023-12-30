'''
unit test for the hall blast loading defs
'''

import unittest
import BlastLoading as bl
import Graph_parameters as graph

class test_BlastLoading(unittest.TestCase):

    def test_compute_scaled_distance(self):
        z = bl.compute_scaled_distance(6000,155)
        self.assertEqual(round(z,2),8.53)

    def test_compute_Pra_blast_parameter(self):
        Pra =bl.compute_Pra_blast_parameter(2.7,12.8)
        self.assertEqual(round(Pra,2), 34.56)

    def test_compute_R_blast_parameter(self):
        R = bl.compute_R_blast_parameter(12.0, 30.0)
        self.assertEqual(round(R,2), 0.8)

    def test_compute_clearing_time_tc(self):
        tc = bl.compute_clearing_time_tc(12.0, 0.8, 1.325)
        self.assertEqual(round(tc,2), 20.13)

    def test_compute_tof(self):
        tof = bl.compute_tof(163.5, 12.8)
        self.assertEqual(round(tof, 2), 25.55)

class test_First_Graph_parameters(unittest.TestCase):

    def test_compute_blast_wave_graph_parameters_Pso(self):
        f = graph.BlastGraphBuilder.Build_Pso_BlastGraph()
        Pso = f.Get_y_coordinate(8.53)
        self.assertEqual(Pso.round(2), 7.78)

    def test_compute_blast_wave_graph_parameters_tA(self):
        f = graph.BlastGraphBuilder.Build_tA_BlastGraph()
        ta = f.Get_y_coordinate(8.53)
        self.assertEqual(ta.round(2), 3.34)

    def test_compute_blast_wave_graph_parameters_Lw(self):
        f = graph.BlastGraphBuilder.Build_Lw_BlastGraph()
        Lw = f.Get_y_coordinate(8.53)
        self.assertEqual(Lw.round(2), 2.08)

    def test_compute_blast_wave_parameter_Cra(self):
        f = graph.BlastGraphBuilder.Build_Cra_BlastGraph()
        Cra = f.Get_y_coordinate(12.8)
        self.assertEqual(Cra.round(2), 2.71)

    def test_compute_blast_wave_graph_parameters_to(self):
        f = graph.BlastGraphBuilder.Build_to_BlastGraph()
        to = f.Get_y_coordinate(8.53)
        self.assertEqual(to.round(2), 2.33)
    
    def test_compute_blast_wave_parameter_Cr(self):
        f = graph.BlastGraphBuilder.Build_Cr_BlastGraph()
        Cr = f.Get_y_coordinate(12.8)
        self.assertEqual(Cr.round(2), 1.32)

    def test_compute_blast_wave_parameter_qo(self):
        f = graph.BlastGraphBuilder.Build_qo_BlastGraph()
        qo = f.Get_y_coordinate(12.8)
        self.assertEqual(qo.round(2), 3.82)



