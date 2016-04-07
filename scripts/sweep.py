#!/usr/bin/env python

from puq import UniformParameter, InteractiveHost, Smolyak, TestProgram, Sweep

PUQ_dir = '/home/n22/IN718/PUQ_test/'
def run():
    # declare your parameters
    parameters = [
        UniformParameter('x', 'on time [s]', min=0.1e-3, max=2e-3)
        ]
        #UniformParameter('y', 'power [W]', min=300, max=1200),
        #UniformParameter('z', 'wait_time [s]', min=0.1e-3, max=15e-3)
        #]
    
    # create an host (interactive or PBS)
    host = InteractiveHost(cpus=32, cpus_per_node=32)
    
    # choose a UQ method
    algo = Smolyak(parameters, level=1)
    
    prog = TestProgram(exe=PUQ_dir+'scripts/wrap.py --on_time=$x',# --power=$y --wait_time=$z',
            desc='Trial test with two parameters',
            newdir=False)
            #infiles =[PUQ_dir+'test/block.exo',PUQ_dir+'test/test.inp',PUQ_dir+'test/xyzdtp.dat'])

    return Sweep(algo, host, prog)

# run with
# > puq -v start -f <untitled>.hdf5 sweep.py
