from radical.ensemblemd import Kernel
from radical.ensemblemd import Pipeline
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment

class MyApp(Pipeline):

      def __init__(self, steps,instances):
             Pipeline.__init__(self, steps,instances)

      def step_1(self, instance):
            k = Kernel(name="misc.hello")
            k.upload_input_data = ['./input_file.txt > temp.txt']
            k.arguments = ["--file=temp.txt"]
            k.download_output_data = ['./temp.txt > output_file.txt']
            return k

if __name__ == "__main__":

       cluster = SingleClusterEnvironment(
                   resource="localhost",
                   cores=1,
                   walltime=15,
                   username=None,
                   allocation=None,
                   database_name="mongod:mymongodburl"
             )

       os.system('Welcome! > input_file.txt')

       cluster.allocate()

       app = MyApp(steps=1,instances=1)

       cluster.run(app)

       cluster.deallocate()

       except EnsemblemdError, er:

             print "Ensemble MD Toolkit Error: {0}".format(str(er))
             raise # Just raise the execption again to get the backtrace