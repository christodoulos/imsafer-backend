import StructureExternalBlastLoading as blast
import matplotlib.pyplot as plt

timehistories = blast.LoadingTimeHistories(charge_weight=5000, distance=155, str_width=30, str_length=30, str_height=12)

(x,y) = timehistories.compute_front_timehistory()

plt.plot(x,y, label="front")

(x,y) = timehistories.compute_rear_timehistory()

plt.plot(x,y, label="rear")

(x,y) = timehistories.compute_roof_timehistory()

plt.plot(x,y, label="foof")

(x,y) = timehistories.compute_side_timehistory()

plt.plot(x,y, label="side")

plt.grid(True)
plt.ylabel("Pressure (psi)")
plt.xlabel("Time (msec)")
plt.legend()
plt.show()