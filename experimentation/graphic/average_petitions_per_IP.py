import matplotlib.pyplot as plt
import numpy as np
from experimentation.graphic.utils import load_data_list

data_file = "C:\\Users\\Dani\\repos-git\\classrank\\local_code\\ips_avg_petitions.tsv"



list_results = load_data_list(data_file)
list_results.reverse()



# x_axis = np.array([ data_line[1] for data_line in list_results])
# y_axis = np.array(range(len(list_results)))

x_axis = np.array(range(len(list_results)))
y_axis = np.array([ data_line[1] for data_line in list_results])

# x_axis = np.array([1,2,3])
# y_axis = np.array([4,5,6])


print(x_axis)

plt.plot(x_axis, y_axis)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
plt.show()
plt.savefig("avg_petitions_per_ipP")
