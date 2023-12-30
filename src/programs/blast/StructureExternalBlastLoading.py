import BlastPhases as bp

class LoadingTimeHistories():

    def __init__(self, charge_weight, distance, str_width, str_length, str_height):
        self.mass_weight = 1.2* charge_weight
        self.distance = distance
        self.str_width = str_width
        self.str_length = str_length
        self.str_height = str_height

        self.timehistories = bp.BlastPhaseTimeHistories()

    def compute_front_timehistory(self):
        return self.timehistories.front_wall_phase_graph(self.mass_weight, self.distance, self.str_height, self.str_width)

    def compute_side_timehistory(self):
        return self.timehistories.side_wall_phase_graph(self.mass_weight, self.distance + self.str_length / 2, self.str_length / 2)

    def compute_roof_timehistory(self):
        return self.timehistories.side_wall_phase_graph(self.mass_weight, self.distance, self.str_length)

    def compute_rear_timehistory(self):
        return self.timehistories.side_wall_phase_graph(self.mass_weight, self.distance + self.str_length, self.str_height)

