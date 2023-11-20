import matplotlib.pyplot as plt
def plot_SA(x,y):      
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel('temprature')
    plt.ylabel('obective function value')
    plt.title('Simulated annealing')
    plt.gca().invert_xaxis()
    # Show the plot (or you can save it to a file with plt.savefig)
    plt.show()