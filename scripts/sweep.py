#!/usr/bin/env python

from puq import UniformParameter, InteractiveHost, Smolyak, TestProgram, Sweep

PUQ_dir = '/home/n22/IN718/PUQ_test/'
case_folder = '5_spot'
def run():
    # setup
    cpus = 24
    cpus_per_node = 48

    # declare your parameters
    parameters = [
        UniformParameter('x', 'on time [s]', min=0.1e-3, max=2e-3)
        ]
        #UniformParameter('y', 'power [W]', min=300, max=1200),
        #UniformParameter('z', 'wait_time [s]', min=0.1e-3, max=15e-3)
        #]
    
    # create an host (interactive or PBS)
    host = InteractiveHost(cpus=cpus, cpus_per_node=cpus_per_node)
    
    # choose a UQ method
    algo = Smolyak(parameters, level=1)
    
    prog = TestProgram(exe=PUQ_dir+'scripts/wrap.py --np='+str(cpus)+' --on_time=$x',# --power=$y --wait_time=$z',
            desc='Trial test for parallel runs',
            newdir=True,
            infiles =[PUQ_dir+case_folder+'/block.exo',PUQ_dir+case_folder+'/test.inp',PUQ_dir+'scripts/xyzdtp_gen.out'])

    return Sweep(algo, host, prog)

# run with
# > puq -v start -f <untitled>.hdf5 sweep.py
