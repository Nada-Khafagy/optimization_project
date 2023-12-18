import matplotlib.pyplot as plt
def plot_SA(x,y):      
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel(r'temprature', fontsize=14)
    plt.ylabel(r'obective function value', fontsize=14)
    plt.title(r'Simulated annealing', fontsize=16)
    plt.gca().invert_xaxis()
    # Show the plot (or you can save it to a file with plt.savefig)
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

def plot_GA(x,y):      
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel(r'generation number', fontsize=14)
    plt.ylabel(r'Best individual in this generation', fontsize=14)
    plt.title(r'Genetic Algorithm', fontsize=16)
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

def plot_DPSO(x,y):      
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel(r'iteration number', fontsize=14)
    plt.ylabel(r'Best individual in this iteration', fontsize=14)
    plt.title(r'Discrete Particle swarm Algorithm', fontsize=16)
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

def plot_BFFA(x,y):      
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel(r'generation number', fontsize=14)
    plt.ylabel(r'Best individual in this generation', fontsize=14)
    plt.title(r'Binary Fire FLy Algorithm', fontsize=16)
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()