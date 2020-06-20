import matplotlib.pyplot as plt
import numpy as np
import random

#TODO 1: Add kwarg parameter to format so the class will never need to change, just adjust kwarg values!!



class barPlot:
    """
    Class for easier bar plot generation.
    """
    def __init__(self, *args, **kwargs):
        # Set default Params
        self.params = {"qty": 1,
                       "barWidth": 0.2,
                       "barperVal": 1,
                       "suptitle": "Bar Plot"
                       }

        # Readjust params from input
        for key, val in kwargs.items():
            self.params[key] = val

        # Setup figure
        self.figure = plt.figure()
        self.figure.suptitle(self.params['suptitle'])

        # Setup subplots
        self.vals = []  # List for values to plot
        self.ax = []    # List for subplot axes
        for i in range(self.params["qty"]):
            # Get dimensions of figure
            dims = sub_dim(self.params["qty"], i+1)
            # Append subplot to axes list, ax
            self.ax.append(self.figure.add_subplot(dims[0], dims[1], dims[2]))
            # Setup Vals list for each subplot
            self.vals.append([])

    def add_val(self, val, ax_num):
        '''
        Add new value to subplot number indicated in input. 
        
        Parameters
        -------------
        val  :  list or dict (must call plot with plot_order parameter if dict)
            List of values to plot in bar plot

        ax_num  :  int
            Subplot axis number to plot these values
        '''
        self.vals[ax_num] = val

    def set_bar_locations(self):
    
        """ 
        Gets list of positions for bar locations. Initializes barPlot.r {list} variable
        """    
        self.r = []                                                                 # Set number of bars to plot
        
        for i in range(self.params['barperVal']):
            if i != 0:
                self.r.append([x + self.params['barWidth'] for x in self.r[i-1]])   # Setting every other bar
            else:
                self.r.append(np.arange(len(self.vals[0])))                         # Set first set of bars

    def plot(self, plot_order=[False], orientation="Horizontal", **kwargs):
        """
        Description
        ----------
        Plot self.vals data into a bar plot.
        
        Parameters
        ----------

        plot_order  :  list
            If type of vals is dict, indicate the key order to plot these values.

        orientation  :  string
            Indicate the type of bar plot ("Horizontal" or "Vertical")
        """
        # Run set_bar_locations()
        self.set_bar_locations() 

        # Get color from input kwarg       
        if 'colors' in kwargs.keys():
            colors = kwargs['colors']
        else:
            colors = []
            for i in range(len(self.r)):
                colors.append(random_color())

        
        # Add all plots to self.p list
        self.p = []

        # Loop through each subplot
        for ax_num in range(len(self.ax)):
            self.p.append([])
            # Loop through each value to plot
            if plot_order[0] == False:
                for j in range(len(self.vals[ax_num])):
                    if orientation == "Horizontal":
                        self.p[ax_num].append(self.ax[ax_num].barh(self.r[j], self.vals[ax_num][j], height=self.params['barWidth']-0.05, color=colors[j], edgecolor='k'))
                    elif orientation == "Vertical":
                        self.p[ax_num].append(self.ax[ax_num].bar(self.r[j], self.vals[ax_num][j], width=self.params['barWidth']-0.05, color=colors[j], edgecolor='k'))

            else:
                for j, key in enumerate(plot_order):
                    if orientation == "Horizontal":                    
                        self.p[ax_num].append(self.ax[ax_num].barh(self.r[j], self.vals[ax_num][key], height=self.params['barWidth']-0.05, color=colors[j], edgecolor='k'))
                    elif orientation == "Vertical":
                        self.p[ax_num].append(self.ax[ax_num].bar(self.r[j], self.vals[ax_num][key], width=self.params['barWidth']-0.05, color=colors[j], edgecolor='k'))


    def format(self, xlabels, sub_titles, legend_labels, orientation="Horizontal"):
        """
        Description
        ----------
        Function used to format the plots. Edit this function to change the specific formatting.
        
        Parameters
        ----------
        xlabels  :  list
            Labels for the x axis

        sub_titles  :  list
            Subplot tites

        legend_labels  :  list
            Labels to use for the legend

        orientation  :  str
            Bar plot orientation
        """
        ticks = 0
        for r in self.r:
            print(ticks)
            ticks += np.asarray(np.float64(r))
        ticks /= len(self.r)
        
        for enum in range(len(self.ax)):
            if orientation == "Horizontal":
                self.ax[enum].set_yticks(ticks)
                self.ax[enum].set_yticklabels(xlabels, fontsize=20)
                self.ax[enum].legend(self.p[enum], legend_labels, loc='upper left',fontsize=20)
                self.ax[enum].xaxis.grid(linestyle=':', color='k', linewidth=2)
                self.ax[enum].set_xlabel('Cost ($/mile)')
                self.ax[enum].set_title(sub_titles[enum])

            elif orientation == "Vertical":
                self.ax[enum].set_xticks(ticks)
                self.ax[enum].set_xticklabels(xlabels, fontsize=20)
                self.ax[enum].legend(self.p[enum], legend_labels, loc='upper left',fontsize=20)
                self.ax[enum].yaxis.grid(linestyle=':', color='k', linewidth=2)
                self.ax[enum].set_ylabel('Cost ($/mile)')
                self.ax[enum].set_title(sub_titles[enum])

    def show(self):
        """
        plt.show()
        """
        plt.show()


# Helper functions
def sub_dim(num, index, col_size=3, return_type=tuple):
    '''
    Automatically get subplot grid size.

    Parameters
    ----------
    num  :  int
        # of subplots
    
    index  :  int
        Index of specific subplot
    
    col_size  :  int
        Max column size
    
    return_type  :  tuple or int 
    '''
    if num<col_size: col_size=num           # Set column to num if num<column_size
    row_size=num//col_size                  
    if num>row_size*col_size: row_size+=1   # If num bigger than grid, add one row
    if return_type is tuple:
        return row_size, col_size, index
    else:
        vals = "{}{}{}".format(row_size, col_size, index)
        return int(vals)

def random_color():
    """
    Get random color tuple for matplotlib

    rtype  :  tuple (0-1, 0-1, 0-1)
    """
    return random.random(), random.random(), random.random()

