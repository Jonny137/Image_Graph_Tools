import Graph_Extractor
import numpy as np
from scipy import polyval
from matplotlib import pyplot as plt


if __name__ == '__main__':
    # preparing x and y list and starting graph data extract module
    x_data = []
    y_data = []

    for value in Graph_Extractor.point_data:
        x_data.append(value[0])
        y_data.append(value[1])

    # getting x and y vectors in form of numpy array
    x = np.array(x_data)
    y = np. array(y_data)

    # calculate polynomial approx function parameters
    z = np.polyfit(x, y, 2)
    y_pred = np.poly1d(z)

    # Checking the fit by calculating MSE
    MSE = np.sqrt(np.sum((y_pred-y)**2)/10)
    # print(MSE)

    # now using the previous model generate y values based on x values outside of the range of the original data
    x_out = np.linspace(x[0]-20, x[-1]+100, 150)
    y_pred = polyval(z, x_out)

    # now plot the original data and corresponding fit through them
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x, y, 'g.', x_out, y_pred, 'b-')
    plt.grid()
    plt.show()
else:
    print("Script is not being called directly!")
