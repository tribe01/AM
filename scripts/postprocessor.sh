#!/bin/bash/
# Make sure to recompile phi.cc if number of temporal output files is changed
ls | grep -v *.h5 | grep -v *.log | grep -v *.out | xargs rm
wait
echo "GMV parsing started on: $(date)"
nohup /home/n22/truchas-gmv-parser.py *.h5 >& gmv_creator.plog &
wait
echo "GMV parsing ended on: $(date)"
echo "OKC generation started on: $(date)"
nohup /home/n22/softwares/visit/visit2_7_3.linux-x86_64/bin/visit -cli -nowin -s /home/n22/IN718/PUQ_test/scripts/okc_gen.py >& okc_gen.plog &
wait
echo "OKC generation ended on: $(date)"
echo "PHI calculation started on: $(date)"
nohup /home/n22/IN718/PUQ_test/scripts/PHI.out >& PHI_creator.plog &
wait
echo "Post processing of simulation data completed succesfully on: $(date)"
echo "Check PHI.txt to get the volume fraction of equiaxed grains formed"
exit
