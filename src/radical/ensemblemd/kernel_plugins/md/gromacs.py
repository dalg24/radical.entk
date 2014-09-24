#!/usr/bin/env python

"""A kernel that creates a new ASCII file with a given size and name.
"""

__author__    = "Ole Weider <ole.weidner@rutgers.edu>"
__copyright__ = "Copyright 2014, http://radical.rutgers.edu"
__license__   = "MIT"

from copy import deepcopy

from radical.ensemblemd.exceptions import ArgumentError
from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------
# 
_KERNEL_INFO = {
    "name":         "md.gromacs",
    "description":  "Creates a new file of given size and fills it with random ASCII characters.",
    "arguments":   {"--grompp=":
                        {
                            "mandatory": True,
                            "description": "Input parameter filename"
                        },
                    "--topol=":
                        {
                            "mandatory": True,
                            "description": "Input topology filename"
                        },
                    "--inputfile=":
                        {
                            "mandatory": True,
                            "description": "Input gro filename"
                        },
                    "--outputfile=":
                        {
                            "mandatory": True,
                            "description": "Output gro filename"
                        }
                    },
    "machine_configs": 
    {
        "*": {
            "environment"   : {"FOO": "bar"},
            "pre_exec"      : [],
            "executable"    : ".",
            "uses_mpi"      : False
        },

        "stampede.tacc.utexas.edu":
        {
            "environment" : {},
            "pre_exec" : ["module load TACC && module load gromacs"],
            "executable" : ["/bin/bash"]
        },

        "trestles.sdsc.xsede.org":
        {
            "environment" : {},
            "pre_exec" : ["(test -d $HOME/bin || mkdir $HOME/bin)","export PATH=$PATH:$HOME/bin","module load gromacs","ln -s /opt/gromacs/bin/grompp_mpi $HOME/bin/grompp && ln -s /opt/gromacs/bin/mdrun_mpi $HOME/bin/mdrun"],
            "executable" : ["/bin/bash"]
        },

        "archer.ac.uk":
        {
            "environment" : {},
            "pre_exec" : ["module load packages-archer","module load gromacs"],
            "executable" : ["/bin/bash"]
        }
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

        executable = "/bin/bash"
        arguments = ['-l', '-c', '{0} run.sh {1} {2} {3} {4}'.format(cfg["executable"],
                                                                     self.get_arg("--grompp="),
                                                                     self.get_arg("--inputfile="),
                                                                     self.get_arg("--topol="),
                                                                     self.get_arg("--outputfile="))]
       
        self._executable  = executable
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"] 
        self._post_exec   = None
