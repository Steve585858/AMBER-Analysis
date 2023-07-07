#!/bin/bash
#PBS -V                 ## Export all environmental variables
#PBS -N 01_Min          ## Set job name
#PBS -o 01_Min.job.log  ## Write standard output file name
#PBS -j oe              ## Merges standard output and error into standard output file
#PBS -k n               ## Do not retain standard output and error files on execution node
#PBS -r n               ## Job is not restartable
#PBS -m abe             ## Send user e-mail on job abort, begin, termination.

#PBS -q route                      ## Use CPUs to run the job
#PBS -l nodes=1:ppn=20,mem=20GB    ## Use 1 node, with 20 processors per node and 20GB memory

module purge
module load amber/19-serial

SECONDS=0
echo "Started job on `date` "

cd ${PBS_O_WORKDIR}
echo Working directory is $PBS_O_WORKDIR
echo Running on host `hostname`
echo Directory is `pwd`
echo This jobs runs on the following processors:
NODES=`cat $PBS_NODEFILE`
echo $NODES
# Compute the number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

prmtop="DPPC_512.prmtop"
coords="DPPC_512.inpcrd"
base="01_Min"
pmemd -O -i ${base}.in -o ${base}.out -p ${prmtop} -c ${coords} -r ${base}.rst

echo "Finished job on `date` "
diff=$SECONDS
echo "Elapsed: $(($diff / 3600)) hours, $((($diff / 60) % 60)) minutes and $(($diff % 60)) seconds"


