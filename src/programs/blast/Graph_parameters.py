'''
contains computations for blast parameters in 
Fig. 2-15 (pdf p.166)
'''

import numpy as np
from scipy.interpolate import interp1d

class BlastGraph():
    '''
    simple blast graph
    '''

    def __init__(self, x, y):
        self.fx = interp1d(x, y, kind='slinear')
        self.fy = interp1d(y, x, kind='slinear')

    def Get_x_coordinate(self, y_coordinate):
        return self.fy(y_coordinate)

    def Get_y_coordinate(self, x_coordinate):
        return self.fx(x_coordinate)

class BlastLinearGraph():
    '''
    
    '''

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def Get_x_coordinate(self, y_coordinate):
        length = len(self.y)
        for i in range(length):
            if y_coordinate < self.y[i]:
                x_coord = [self.x[i-1], self.x[i]]
                y_coord = [self.y[i-1], self.y[i]]
                f = interp1d(y_coord, x_coord)
                return f(y_coordinate).round(4)
        return self.x[length - 1]

    def Get_y_coordinate(self, x_coordinate):
        length = len(self.x)
        for i in range(length):
            if x_coordinate < self.x[i]:
                x_coord = [self.x[i-1], self.x[i]]
                y_coord = [self.y[i-1], self.y[i]]
                f = interp1d(x_coord, y_coord)
                return f(x_coordinate).round(4)
        return self.y[length - 1]

class BlastGraphBuilder():

    def Build_Pso_BlastGraph():
        '''
        Pso graph using Fig. 2-15 (pdf p.166) from 
        (UFC) Structures to resist the effects of accidental explosions /n
        output: /n
        - Pso (psi)
        '''

        x = np.array([0.2,    0.3,    0.5,    0.7,    1.0,    2.0,   3.0,   4.0,  5.0,  6.0,  7.0,  8.0,  10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0])
        y = np.array([7000.0, 4500.0, 2500.0, 1800.0, 1000.0, 320.0, 150.0, 70.0, 41.0, 28.0, 20.0, 16.0, 9.5,  3.0,  1.8,  1.4,  0.8,  0.59,  0.4])

        return BlastLinearGraph(x,y)

    def Build_tA_BlastGraph():
        '''
        tA graph using Fig. 2-15 (pdf p.166) from 
        (UFC) Structures to resist the effects of accidental explosions /n
        output: /n
        - tA/W^(1/3) (ms/lb^(1/3))
        '''
        
        x = np.array([0.2,    0.3,    0.5,    0.7,    1.0,    2.0,   3.0,   4.0,  5.0,  6.0,  7.0,  8.0, 10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0])
        y = np.array([0.009,  0.015,  0.03,   0.045,  0.08,   0.25,  0.5,   0.85, 1.5,  1.8,  2.5,  3.0, 4.3,  14.0, 21.0, 30.0, 28.0, 55.0, 80.0])

        return BlastGraph(x,y)

    def Build_Lw_BlastGraph():
        '''
        Lw graph using Fig. 2-15 (pdf p.166) from 
        (UFC) Structures to resist the effects of accidental explosions 
        output:
        - Lw/W^(1/3) (ft/lb^1/3)
        '''
        
        x = np.array([0.5,  0.7,    1.0,    2.0,   3.0,   4.0,  5.0,  6.0,  7.0,  8.0, 10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0])
        y = np.array([0.5,  0.55,   0.54,   0.49,  0.6,   1.0,  1.5,  1.8,  1.9,  2.0, 2.3,  3.2,  3.9,  4.1,  4.5,  4.9,  4.95])

        return BlastGraph(x,y)

    def Build_to_BlastGraph():
        '''
        to graph using Fig. 2-15 (pdf p.166) from 
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - to/W(1/3) (ms/lb^1/3)
        '''

        x = np.array([0.5,  0.7,    1.0,    2.0,   3.0,   4.0,  5.0,  6.0,  7.0,  8.0, 10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0])
        y = np.array([0.19, 0.18,   0.19,   0.6,   1.8,   1.7,  1.6,  1.7,  2.0,  2.2, 2.7,  3.5,  3.9,  4.1,  4.5,  5.0,  5.5])

        return BlastGraph(x,y)

    def Build_is_BlastGraph():
        '''
        is graph using Fig. 2-15 (pdf p.166) from 
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - is/W^(1/3) (psi - ms/lb^1/3)
        '''

        x = np.array([0.2,   0.3,    0.5,  0.7,    1.0,    2.0,   3.0,   4.0,   5.0,  6.0,  7.0,  8.0,  10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0])
        y = np.array([260.0, 110.0,  42.0, 25.0,   20.0,   22.0,  25.0,  18.0,  15.0, 14.0, 11.0, 10.0, 8.0,  4.2,  2.9,  2.2,  1.8,  1.2,  0.8])

        return BlastGraph(x,y)

    def Build_Cra_BlastGraph():
        '''
        Cra graph for zero angle of incidence (a) using Fig. 2-193 (pdf p.344) from 
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - Cra 
        '''

        x = np.array([0.2,  0.5,   1.0,   2.0,   5.0,   10.0,  20.0,  30.0,  50.0,  70.0, 100.0, 150.0, 200.0, 300.0, 400.0, 500.0, 1000.0, 2000.0, 3000.0, 5000.0])
        y = np.array([2.0,  2.1,   2.2,   2.3,   2.4,   2.6,   3.0,   3.2,   4.0,   4.3,  5.0,   5.5,   6.0,   6.7,   7.0,   7.8,   8.3,    10.0,   10.9,   12.3])

        return BlastGraph(x,y)

    def Build_ir_BlastGraph():
        '''
        ir graph for zero angle of incidence (a) using Fig. 2-194 (pdf p.345-346) from 
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - Ir/W^(1/3) (psi-ms/lb^1/3)
        '''

        x = np.array([0.7, 1.0, 1.5, 2.0, 3.0, 5.0,  10.0,  20.0,  50.0,  100.0, 200.0, 400.0, 700.0, 1000.0, 1500.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0])
        y = np.array([2.2, 3.0, 4.1, 5.1, 7.0, 10.0, 15.0,  20.2,  35.0,  51.0,  79.0,  150.0, 195.0, 260.0,  410.0,  600.0,  1100.0, 1990.0, 3200.0, 5000.0, 8500.0])

        return BlastGraph(x,y)

    def Build_Cr_BlastGraph():
        '''
        Cr graph using Fig. 2-192 (pdf p.343) from 
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - Cr (ft/ms)
        '''

        x = np.array([0.0,  5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0])
        y = np.array([1.12, 1.2, 1.28, 1.36, 1.43, 1.48, 1.54, 1.59, 1.65, 1.71, 1.76, 1.81, 1.85, 1.88, 1.93, 1.97])

        return BlastGraph(x,y)

    def Build_qo_BlastGraph():
        '''
        qo graph using Fig. 2-3 (pdf p.155) from 
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - qo (psi)
        '''

        x = np.array([2.0, 3.0,  4.0,  5.0, 6.0,  7.0, 8.0, 10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0, 200.0, 300.0, 500.0])
        y = np.array([0.1, 0.22, 0.39, 0.6, 0.85, 1.2, 1.5, 2.2,  8.0,  18.0, 28.0, 40.0, 70.0, 120.0, 320.0, 600.0, 1200.0])

        return BlastGraph(x,y)

    def Build_Pra_BlastGraph():
        '''
        Pra graph using Fig. 2-15 (pdf p.166) from
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - Pra (psi)
        '''

        x = np.array([0.2,     0.3,     0.5,     0.7,     1.0,    2.0,    3.0,   4.0,   5.0,   6.0,  7.0,  8.0,  10.0, 20.0, 30.0, 40.0, 50.0, 70.0, 100.0])
        y = np.array([90000.0, 55000.0, 29000.0, 18000.0, 9000.0, 2200.0, 700.0, 300.0, 170.0, 90.0, 59.0, 40.0, 25.0, 6.5,  4.0,  2.5,  1.8,  1.1,  0.7])

        return BlastGraph(x,y)

    def Build_Pr_negative_Blast_Graph():
        '''
        get Pr negative graph using Fig. 2-16 (pdf p.167) from
        (UFC) Structures to resist the effects of accidental explosions
        output:
        - Pr negative (psi)
        '''

        x = np.array([0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 20.0, 30.0])
        y = np.array([15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 13,  8.0, 7.0, 5.0, 4.0, 3.5, 3.0, 2.5, 2.3,  1.5,  1.0])

        return BlastLinearGraph(x,y)

    def Build_ir_negative_Blast_Graph():
        '''
        
        '''

        x = np.array([0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0,  8.0,  9.0,  10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        y = np.array([70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 60.0, 40.0, 30.0, 25.0, 20.0, 18.0, 15.0, 13.0, 12.0, 10.0, 7.0,  5.0,  4.0,  3.0])

        return BlastLinearGraph(x,y)

    def Build_Ce_positive_Blast_Graph():
        '''
        (pdf p. 348)
        '''

        x = np.array([0.35, 0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0,  3.0,  4.0,  5.0,  6.0, 7.0])
        y = np.array([0.22, 0.24, 0.28, 0.33, 0.36, 0.39, 0.42, 0.46, 0.66, 0.77, 0.85, 0.88, 0.9, 0.9])

        return BlastLinearGraph(x,y)

    def Build_Ce_negative_Blast_Graph():
        '''
        (pdf p. 348)
        '''

        x = np.array([0.35, 0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0, 3.0, 4.0])
        y = np.array([0.15, 0.16, 0.18, 0.21, 0.22, 0.23, 0.24, 0.25, 0.27, 0.28, 0.3])

        return BlastLinearGraph(x,y)

    def Build_td_P_4_Blast_Graph():
        ''' (pdf p. 2-197)'''

        x = np.array([0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0])
        y = np.array([2.4,  2.5,  2.55, 2.5,  2.4,  2.4,  1.6])

        return BlastLinearGraph(x,y)

    def Build_td_P_8_Blast_Graph():
        ''' (pdf p. 2-197)'''

        x = np.array([0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0])
        y = np.array([1.75,  1.8, 1.83, 1.85, 1.88, 1.85, 1.3])

        return BlastLinearGraph(x,y)

    def Build_td_P_16_Blast_Graph():
        ''' (pdf p. 2-197)'''

        x = np.array([0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0])
        y = np.array([1.1,  1.2,  1.3,  1.35, 1.38, 1.3,  0.7])

        return BlastLinearGraph(x,y)

    def Build_td_P_32_Blast_Graph():
        ''' (pdf p. 2-197)'''

        x = np.array([0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  2.0])
        y = np.array([0.65, 0.68, 0.7,  0.71, 0.71, 0.7,  0.42])

        return BlastLinearGraph(x,y)

    def Build_tof_2_Blast_Graph():
        ''' pdf p.350 '''

        x = np.array([0.35, 0.4,  0.5,  0.6, 0.7, 0.8, 0.9, 1.0, 2.0])
        y = np.array([14.0, 13.0, 11.5, 9.2, 8.5, 7.8, 7.4, 6.9, 5.2])

        return BlastLinearGraph(x,y)

    def Build_tof_4_Blast_Graph():
        ''' pdf p.350 '''

        x = np.array([0.35, 0.4,  0.5,  0.6, 0.7, 0.8, 0.9, 1.0, 2.0])
        y = np.array([12.0, 10.0, 8.5,  7.5, 6.8, 6.3, 5.9, 5.5, 4.1])

        return BlastLinearGraph(x,y)

    def Build_tof_8_Blast_Graph():
        ''' pdf p.350 '''

        x = np.array([0.35, 0.4,  0.5,  0.6, 0.7, 0.8, 0.9, 1.0, 2.0])
        y = np.array([8.8,  8.0,  6.8,  5.9, 5.4, 4.8, 4.5, 4.4, 3.1])

        return BlastLinearGraph(x,y)

    def Build_tof_16_Blast_Graph():
        ''' pdf p.350 '''

        x = np.array([0.35, 0.4,  0.5,  0.6, 0.7, 0.8, 0.9, 1.0, 2.0])
        y = np.array([6.5,  5.9,  4.8,  4.1, 3.6, 3.4, 3.1, 2.9, 2.1])

        return BlastLinearGraph(x,y)

    def Build_tof_32_Blast_Graph():
        ''' pdf p.350 '''

        x = np.array([0.35, 0.4,  0.5,  0.6, 0.7, 0.8, 0.9, 1.0, 2.0])
        y = np.array([4.2,  3.9,  3.2,  2.8, 2.6, 2.4, 2.1, 2.0, 1.5])

        return BlastLinearGraph(x,y)

    def Build_tof_negative_Graph():
        '''
        pdf p.350
        '''

        x = np.array([0.35, 3.5])
        y = np.array([14.0, 10.0])

        return BlastLinearGraph(x,y)

class BlastMultiGraph():

    def __init__(self):
        self.graphs = []
        self.extra_values = []
        pass

    def add_Graph(self, graph, extra_value):
        self.graphs.append(graph)
        self.extra_values.append(extra_value)

    def Get_y_coordinate(self, x_coordinate, extra_value):

        length = len(self.extra_values)

        for i in range(length):
            if extra_value < self.extra_values[i]:

                x1 = self.extra_values[i-1]
                x2 = self.extra_values[i]
                x_temp = [x1, x2]

                y1 = self.graphs[i-1].Get_y_coordinate(x_coordinate)
                y2 = self.graphs[i].Get_y_coordinate(x_coordinate)
                y_temp = [y1, y2]

                f = interp1d(x_temp, y_temp)

                return f(extra_value).round(4)

    def Get_x_coordinate(self, y_coordinate, extra_value):

        length = len(self.extra_values)

        for i in range(length):
            if extra_value < self.extra_values[i]:

                x1 = self.extra_values[i-1]
                x2 = self.extra_values[i]
                x_temp = [x1, x2]

                y1 = self.graphs[i-1].Get_x_coordinate(y_coordinate)
                y2 = self.graphs[i].Get_x_coordinate(y_coordinate)
                y_temp = [y1, y2]

                f = interp1d(x_temp, y_temp)

                return f(extra_value).round(4)

class BlastMultiGraphBuilder():

    def Build_td_graph():
        '''
        '''
        
        td_multiGraph = BlastMultiGraph()
        td_multiGraph.add_Graph(BlastGraphBuilder.Build_td_P_4_Blast_Graph(), 4)
        td_multiGraph.add_Graph(BlastGraphBuilder.Build_td_P_8_Blast_Graph(), 8)
        td_multiGraph.add_Graph(BlastGraphBuilder.Build_td_P_16_Blast_Graph(), 16)
        td_multiGraph.add_Graph(BlastGraphBuilder.Build_td_P_32_Blast_Graph(), 32)

        return td_multiGraph

    def Build_tof_graph():
        '''
        '''

        tof_multiGraph = BlastMultiGraph()
        tof_multiGraph.add_Graph(BlastGraphBuilder.Build_tof_2_Blast_Graph(), 2)
        tof_multiGraph.add_Graph(BlastGraphBuilder.Build_tof_4_Blast_Graph(), 4)
        tof_multiGraph.add_Graph(BlastGraphBuilder.Build_tof_8_Blast_Graph(), 8)
        tof_multiGraph.add_Graph(BlastGraphBuilder.Build_tof_16_Blast_Graph(), 16)
        tof_multiGraph.add_Graph(BlastGraphBuilder.Build_tof_32_Blast_Graph(), 32)

        return tof_multiGraph




