#---------------------------------------------------------------------------------------------------#
# File name: helpers_general.py                                                                     #
# Autor: Chrissi2802                                                                                #
# Created on: 19.12.2022                                                                            #
#---------------------------------------------------------------------------------------------------#
# This file provides auxiliary classes and functions.
# Exact description in the functions.


from datetime import datetime


class Program_runtime():
    """Class for calculating the programme runtime and outputting it to the console.
    """

    def __init__(self):
        """Initialisation of the class (constructor). Automatically saves the start time.
        """

        self.begin()

    def begin(self):
        """This method saves the start time.
        """

        self.__start = datetime.now()   # start time

    def finish(self, print = True):
        """This method saves the end time and calculates the runtime.
        
        Args:
            print (boolean, default True): If True, the start time, end time and the runtime are output to the console.

        Returns:
            self.__runtime (integer): Runtime
        """

        self.__end = datetime.now() # end time
        self.__runtime = self.__end - self.__start  # runtime

        if (print == True):
            self.show()

        return self.__runtime

    def show(self):
        """This method outputs start time, end time and the runtime on the console.
        """

        print()
        print("Start:", self.__start.strftime("%Y-%m-%d %H:%M:%S"))
        print("End:  ", self.__end.strftime("%Y-%m-%d %H:%M:%S"))
        print("Program runtime:", str(self.__runtime).split(".")[0])    # Cut off milliseconds
        print()


if (__name__ == "__main__"):
    
    # calculating the programme runtime
    Pr = Program_runtime()
    # Code here
    Pr.finish(print = True)

    