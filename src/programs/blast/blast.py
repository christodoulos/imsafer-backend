#!/usr/bin/python3
import sys
import StructureExternalBlastLoading as blast
import matplotlib.pyplot as plt

def save_timehistory(fname, x, y):
    with open(fname, 'w') as f:
        f.write("x,y\n")
        for v in zip(x,y):
            f.write("{},{}\n".format(v[0],v[1]))

charge_weight = float(sys.argv[1])
distance = float(sys.argv[2])
str_width = float(sys.argv[3])
str_length = float(sys.argv[4])
str_height = float(sys.argv[5])

#timehistories = blast.LoadingTimeHistories(charge_weight=5000, distance=155, str_width=30, str_length=30, str_height=12)

timehistories = blast.LoadingTimeHistories(charge_weight=charge_weight, distance=distance, str_width=str_width, str_length=str_length, str_height=str_height)

(x,y) = timehistories.compute_front_timehistory()

plt.plot(x,y, label="front")
save_timehistory("./front.csv", x,y)

(x,y) = timehistories.compute_rear_timehistory()

plt.plot(x,y, label="rear")
save_timehistory("./rear.csv", x,y)

(x,y) = timehistories.compute_roof_timehistory()

plt.plot(x,y, label="roof")
save_timehistory("./roof.csv", x,y)

(x,y) = timehistories.compute_side_timehistory()

plt.plot(x,y, label="side")
save_timehistory("./side.csv", x,y)

plt.grid(True)
plt.ylabel("Pressure (psi)")
plt.xlabel("Time (msec)")
plt.legend()
plt.savefig("./plot.png")
