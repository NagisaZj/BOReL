#!/bin/bash
   # Script to reproduce results

 Foldername="0723_offline_meta_rl_aa"
 mkdir out_logs/${Foldername} &> /dev/null
 declare -a tasks=( "Push-V2"		"Reach-V2"		"Pick-Place-V2"		"Peg-Insert-Side-V2"		"Window-Open-V2"		"Drawer-Close-V2"		"Lever-Pull-V2"		"Handle-Pull-V2"		"Handle-Pull-Side-V2"	"Pick-Out-Of-Hole-V2"		"Plate-Slide-Side-V2"		"Plate-Slide-V2"		"Reach-Wall-V2"  "Soccer-V2"  "Push-Wall-V2"  "Window-Close-V2"  	"Shelf-Place-V2"  "Sweep-V2")

 n=1
 gpunum=8
 for task in "${tasks[@]}"
 do

 CUDA_VISIBLE_DEVICES=${n} nohup python train_vae_offline.py --env-type cheetah_vel >& out_logs/${task}.txt &
 n=$[($n+1) % ${gpunum}]
 done
# CUDA_VISIBLE_DEVICES=3 python policy_train.py ./configs/sparse-point-robot.json
# python policy_train.py ./configs/sparse-point-robot.json --is_uniform