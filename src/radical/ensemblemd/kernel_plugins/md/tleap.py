#!/usr/bin/env python

"""A kernel that creates a new ASCII file with a given size and name.
"""

__author__    = "Vivek <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2014, http://radical.rutgers.edu"
__license__   = "MIT"

from copy import deepcopy

from radical.ensemblemd.exceptions import ArgumentError
from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------
#
_KERNEL_INFO = {

    "name":         "md.tleap",
    "description":  "Creates a new file of given size and fills it with random ASCII characters.",
    "arguments":   {
                    "--numofsims=":
                        {
                            "mandatory": True,
                            "description": "No. of frontpoints = No. of simulation CUs"
                        },
                    "--cycle=":
                        {
                            "mandatory": True,
                            "description": "Output filename for postexec"
                        }
                    },
    "machine_configs": 
    {
        "*": {
            "environment"   : {"FOO": "bar"},
            "pre_exec"      : [],
            "executable"    : "python",
            "uses_mpi"      : False
        },

        "xsede.stampede":
        {
            "environment" : {},
            "pre_exec" : [  "module load intel/13.0.2.146",
                            "module load python/2.7.9",
                            "module load mpi4py",
                            "module load netcdf/4.3.2",
                            "module load hdf5/1.8.13",
                            "module load amber",
                            "export PYTHONPATH=/work/02998/ardi/coco-0.19_installation/lib/python2.7/site-packages:$PYTHONPATH",
                            "export PATH=/work/02998/ardi/coco-0.19_installation/bin:$PATH"],
            "executable" : ["python"],
            "uses_mpi"   : False
        },

        "epsrc.archer":
        {
            "environment" : {},
            "pre_exec" : ["module load python-compute/2.7.6",
                      "module load pc-numpy/1.8.0-libsci",
                      "module load pc-scipy/0.13.3-libsci",
                      "module load pc-coco/0.18",
                      "module load pc-netcdf4-python/1.1.0",
                      "module load amber"],
            "executable" : ["python"],
            "uses_mpi"   : False
        },

        "lsu.supermic":
        {
            "environment" : {},
            "pre_exec" : [". /home/vivek91/modules/amber14/amber.sh",
                        "export PATH=/home/vivek91/.local/bin:/home/vivek91/modules/amber14/bin:/home/vivek91/modules/amber14/dat/leap/cmd:$PATH",
                        "export PYTHONPATH=/home/vivek91/.local/lib/python2.7/site-packages:$PYTHONPATH",
                        "module load hdf5/1.8.12/INTEL-140-MVAPICH2-2.0",
                        "module load netcdf/4.2.1.1/INTEL-140-MVAPICH2-2.0",
                        "module load fftw/3.3.3/INTEL-140-MVAPICH2-2.0",
                        "module load python/2.7.7-anaconda"],
            "executable" : ["python"],
            "uses_mpi"   : False
        },
        "xsede.comet":
        {
                "environment" : {},
                "pre_exec"    : ["module load hdf5/1.8.14",
                        "module load netcdf/4.3.2",
                        "module load fftw/3.3.4",
                        "module load python",
                        "module load scipy",
                        "module load mpi4py",
                        "module load amber",
                        "export PYTHONPATH=$PYTHONPATH:/home/vivek91/.local/lib/python2.7/site-packages"],
                "executable"  : ["python"],
                "uses_mpi"    : False
        },
    }
}


# ------------------------------------------------------------------------------
#
class Kernel(KernelBase):

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        """Le constructor.
        """
        super(Kernel, self).__init__(_KERNEL_INFO)

    # --------------------------------------------------------------------------
    #
    @staticmethod
    def get_name():
        return _KERNEL_INFO["name"]

    # --------------------------------------------------------------------------
    #
    def _bind_to_resource(self, resource_key):

        """(PRIVATE) Implements parent class method. 
        """
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            if "*" in _KERNEL_INFO["machine_configs"]:
                # Fall-back to generic resource key
                resource_key = "*"
            else:
                raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        executable = cfg["executable"]
        arguments = ['postexec.py','{0}'.format(self.get_arg("--numofsims=")),'{0}'.format(self.get_arg("--cycle="))]
       
        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"] 
        self._post_exec   = None
