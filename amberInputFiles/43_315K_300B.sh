#!/bin/bash
#PBS -V                          ## Export all environmental variables
#PBS -N 43_315K_300B                  ## Set job name
#PBS -o logs/43_315K_300B.log     ## Write standard output file name
#PBS -e logs/43_315K_300B.error   ## Write standard output file name
#PBS -j oe                       ## Merges standard output and error into standard output file
#PBS -k n                        ## Do not retain standard output and error files on execution node
#PBS -r n                        ## Job is not restartable
#PBS -m abe                      ## Send user e-mail on job abort, begin, termination.
#PBS -q share.gpu                ## Use GPUs to run the job
#PBS -l nodes=1:ppn=10,mem=20gb,gpus=1

SECONDS=0
echo "Started job on `date` "

export "CUDA_VISIBLE_DEVICES=`/share/apps/CLUSTER/local/get_free_gpus`"
echo CUDA_VISIBLE_DEVICES = $CUDA_VISIBLE_DEVICES
if [[ ${CUDA_VISIBLE_DEVICES} == '0,1' ]]; then
   CoreMap="0:2"
fi
if [[ ${CUDA_VISIBLE_DEVICES} == '2,3' ]]; then
   CoreMap="1:3"
fi
export MV2_CPU_MAPPING=${CoreMap}
echo MV2_CPU_MAPPING = $MV2_CPU_MAPPING

module purge
module load amber/19-cuda_mvapich2

cd ${PBS_O_WORKDIR}
echo Working directory is $PBS_O_WORKDIR
echo Running on host `hostname`
echo Directory is `pwd`
echo This jobs runs on the following processors:
NODES=`cat $PBS_NODEFILE`
echo $NODES
## Compute the number of processors
NPROCS=`wc -l < $PBS_NODEFILE`
echo This job has allocated $NPROCS nodes

prmtop="DPPC_512.prmtop"
base="43_315K_300B"
##NAMES=("01" "02" "03"  "04"  "05"  "06"  "07"  "08"  "09"  "10")
NAMES=("01")
prevName="33_310K_300B_01"

for name in ${NAMES[@]}; do
   currName=${base}_${name}
   echo starting mpirun on $currName
   mpirun -np 2 pmemd.cuda.MPI -O \
      -i ${base}.in -o ${currName}.out -p $prmtop -c ${prevName}.rst \
      -ref ${prevName}.rst -r ${currName}.rst -x ${currName}.nc 
   prevName=${currName}
done

#echo set | qsub  ##forward the names and values of all shell variables

echo "Finished job on `date` "
diff=$SECONDS
echo "Elapsed: $(($diff / 3600)) hours, $((($diff / 60) % 60)) minutes and $(($diff % 60)) seconds"