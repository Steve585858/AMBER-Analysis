#!/bin/bash
#man qsub to know more


part="loop_temperature"   

if [[ ${part} == 'loop_temperature' ]]; then
    ## declare an array variable
    array1 = (5 6 7)
    array2 = (320 325 330)
    for index in "${!array1[*]}"
    do  
        output5=`qsub ${array1[$index]}5_${array2[$index]}K_300B.sh`
        echo $output5
        JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
        echo $JOB_ID5

        output6=`qsub -W depend=afterany:$JOB_ID5 ${array1[$index]}6_${array2[$index]}K_300B.sh`
        echo $output6
        JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
        echo $JOB_ID6
    done
fi

if [[ ${part} == 'loop_pressure' ]]; then
    ## declare an array variable
    declare -a shIDs_box=("010B" "025B" "050B" "075B" "100B" "125B" "150B" "175B" "200B" "225B" "250B" "275B" "300B")
    declare -a shIDs=()
    for shID in "${shIDs[@]}"
    do  
        #command5="ls -al 05_300K_${shID}.sh"
        #echo ${command5}

        output5=`qsub 05_300K_${shID}.sh`
        echo $output5
        JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
        echo $JOB_ID5

        output6=`qsub -W depend=afterany:$JOB_ID5 06_300K_${shID}.sh`
        echo $output6
        JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
        echo $JOB_ID6
    done
fi

if [[ ${part} == 'part25_305K_300B' ]]; then
    output5=`qsub 25_305K_300B.sh`
    echo $output5
    JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID5

    output6=`qsub -W depend=afterany:$JOB_ID5 26_305K_300B.sh`
    echo $output6
    JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID6
fi

if [[ ${part} == 'part35_310K_300B' ]]; then
    output5=`qsub 35_310K_300B.sh`
    echo $output5
    JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID5

    output6=`qsub -W depend=afterany:$JOB_ID5 36_310K_300B.sh`
    echo $output6
    JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID6
fi

if [[ ${part} == 'part45_315K_300B' ]]; then
    output5=`qsub 45_315K_300B.sh`
    echo $output5
    JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID5

    output6=`qsub -W depend=afterany:$JOB_ID5 46_315K_300B.sh`
    echo $output6
    JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID6
fi

if [[ ${part} == '305K_300B_Heat' ]]; then
    output2=$(qsub 23_305K_300B.sh)
    echo $output2
    JOB_ID2=`echo $output2 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID2

    output3=$(qsub -W depend=afterany:$JOB_ID2 33_310K_300B.sh)
    echo $output3
    JOB_ID3=`echo $output3 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID3
    
    output4=$(qsub -W depend=afterany:$JOB_ID3 43_315K_300B.sh)
    echo $output4
    JOB_ID4=`echo $output4 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID4
fi


if [[ ${part} == '330K_300B_Heat' ]]; then
    output2=$(qsub 53_320K_300B.sh)
    echo $output2
    JOB_ID2=`echo $output2 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID2

    output3=$(qsub -W depend=afterany:$JOB_ID2 63_325K_300B.sh)
    echo $output3
    JOB_ID3=`echo $output3 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID3
    
    output4=$(qsub -W depend=afterany:$JOB_ID3 73_330K_300B.sh)
    echo $output4
    JOB_ID4=`echo $output4 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID4
fi

if [[ ${part} == 'part1' ]]; then
    #output1=$(qsub 01_Min.sh)
    #echo $output1
    #JOB_ID1=`echo $output1 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    #echo $JOB_ID1

    output2=$(qsub 02_Heat.sh)
    #output2=$(qsub -W depend=afterany:$JOB_ID1 02_Heat.sh)
    echo $output2
    JOB_ID2=`echo $output2 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID2

    output3=$(qsub -W depend=afterany:$JOB_ID2 03_Heat.sh)
    echo $output3
    JOB_ID3=`echo $output3 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID3
fi

if [[ ${part} == 'part2' ]]; then
    #output4=$(qsub -W depend=afterany:$JOB_ID3 04_Pressure_10.sh)
    output4=$(qsub 04_300K_010B.sh)
    echo $output4
    JOB_ID4=`echo $output4 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID4
fi

if [[ ${part} == 'part3' ]]; then
    #output5=$(qsub -W depend=afterany:$JOB_ID4 05_300K_010B.sh)
    output5=$(qsub 05_300K_010B.sh)
    echo $output5
    JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID5

    output6=$(qsub -W depend=afterany:$JOB_ID5 06_300K_010B.sh)
    echo $output6
    JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID6
fi

if [[ ${part} == 'part315K_300B' ]]; then
    output13=$(qsub 13_315K_300B.sh)
    echo $output13
    JOB_ID13=`echo $output13 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID13

    output15=$(qsub -W depend=afterany:$JOB_ID13 15_315K_300B.sh)
    echo $output15
    JOB_ID15=`echo $output15 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID15

    output16=$(qsub -W depend=afterany:$JOB_ID15 16_315K_300B.sh)
    echo $output16
    JOB_ID16=`echo $output16 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID16
fi

if [[ ${part} == 'part4' ]]; then
    #output2=$(qsub 02_Heat.sh)
    #output2=$(qsub -W depend=afterany:$JOB_ID1 02_Heat.sh)
    #echo $output2
    #JOB_ID2=`echo $output2 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    #echo $JOB_ID2

    #output3=$(qsub 03_Heat.sh)
    #output3=$(qsub -W depend=afterany:$JOB_ID2 03_Heat.sh)
    #echo $output3
    #JOB_ID3=`echo $output3 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    #echo $JOB_ID3

    #output4=$(qsub 04_300K_Pressure.sh)
    #output4=$(qsub -W depend=afterany:$JOB_ID3 04_300K_Pressure.sh)
    #echo $output4
    #JOB_ID4=`echo $output4 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    #echo $JOB_ID4

    output4=$(qsub 04_300K_Pressure.sh)
    #output4=$(qsub -W depend=afterany:$JOB_ID3 04_300K_Pressure.sh)
    echo $output4
    JOB_ID4=`echo $output4 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID4

    #output5=$(qsub 05_300K_300B.sh)
    output5=$(qsub -W depend=afterany:$JOB_ID4 05_300K_300B.sh)
    echo $output5
    JOB_ID5=`echo $output5 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID5

    output6=$(qsub -W depend=afterany:$JOB_ID5 06_300K_300B.sh)
    echo $output6
    JOB_ID6=`echo $output6 | awk 'match($0,/[0-9]+/){print substr($0, RSTART, RLENGTH)}'`
    echo $JOB_ID6
fi

