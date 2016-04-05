#!/usr/bin/env python

from puq import UniformParameter, InteractiveHost, Smolyak, TestProgram, Sweep

def run():
    # declare your parameters
    parameters = [
        UniformParameter('z', 'wait time [s]', min=0.1e-3, max=10e-3),
    ]
    #    UniformParameter('power', 'your description here', min=0.1e-3, max=3e-3),
    #    UniformParameter('wiat-time', 'your description here', min=0.1e-3, max=3e-3)
    #]
    
    # create an host (interactive or PBS)
    host = InteractiveHost(cpus=12, cpus_per_node=48)
    
    # choose a UQ method
    algo = Smolyak(parameters, level=1)
    
    prog = TestProgram(exe='./wrap.py --wait_time=$z',
            desc='something something',
            newdir=False)

    return Sweep(algo, host, prog)

# run with
# > puq -v start -f <untitled>.hdf5 sweep.py
