# Offline Meta Reinforcment Learning - Identifiability Challenges and Effective Data Collection Strategies

### Requirements ### 
All requirements are specified in ``requirements.txt``. \
We also provide a yaml file: ``omrl.yml``. Run: ``conda env create -f omrl.yml`` and activate the env with ``conda activate omrl``.  
For the MuJoCo-based experiments (``Half-Cheetah-Vel`` and ``Ant-Semi-circle`` you will need a MuJoCo license).  

## Offline Setting ##
### Data collection ###
The main script for data collecion is ``train_single_agent.py``.  
Configuration files are in ``data_collection_config``. All training parameters can be set from within the files, or by passing command line arguments.  

Run:  
``python train_single_agent.py --env-type X --seed Y``  

where X is a domain (e.g., ``gridworld``, ``point_robot_sparse``, ``cheetah_vel``, ``ant_semicircle_sparse``, ``point_robot_wind``, ``escape_room``) and Y is some integer (e.g. ``73``).  
This will train a standard RL agent (implemented in ``learner.py``) to solve a single task. Different seeds correspond to different tasks (from the same task distribution).  




### VAE training ###
The main script for the VAE training is ``train_vae_offline.py``.  
Configuration files are in ``vae_config``. All training parameters can be set from within the files, or by passing command line arguments.  

Run (for example):  
``python train_vae_offline.py --env-type ant_semicircle_sparse`` 

``CUDA_VISIBLE_DEVICES=2 python train_vae_offline.py --env-type cheetah_vel --env-name sweep-v2``  


This will train the VAE (implemented in ``models\vae.py``).  

Reward Relabelling (RR) is used when the argument ``--hindsight-relabelling`` is set to ``True``. 



### Offline Meta-RL Training ###
The main script for the offline meta-RL training is ``train_agent_offline.py``.  
Configuration files are in ``offline_config``. All training parameters can be set from within the files, or by passing command line arguments.  

Run (for example):  



"Handle-Pull-V2"		"Handle-Pull-Side-V2"	"Pick-Out-Of-Hole-V2"		"Plate-Slide-Side-V2"		"Plate-Slide-V2"		"Reach-Wall-V2"  "Soccer-V2"  "Push-Wall-V2"  "Window-Close-V2"  	"Shelf-Place-V2"  "Sweep-V2" 

CUDA_VISIBLE_DEVICES=1 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name handle-pull-v2 --vae-model-name relabel__11_10_08_47_32

CUDA_VISIBLE_DEVICES=2 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name handle-pull-side-v2  --vae-model-name relabel__11_10_08_47_44

CUDA_VISIBLE_DEVICES=3 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name pick-out-of-hole-v2  --vae-model-name relabel__11_10_08_47_59

CUDA_VISIBLE_DEVICES=4 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name plate-slide-side-v2  --vae-model-name relabel__11_10_08_48_18

CUDA_VISIBLE_DEVICES=5 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name plate-slide-v2  --vae-model-name relabel__11_10_08_48_28

CUDA_VISIBLE_DEVICES=6 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name reach-wall-v2  --vae-model-name relabel__11_10_08_48_42

CUDA_VISIBLE_DEVICES=7 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name soccer-v2  --vae-model-name relabel__11_10_08_48_54

CUDA_VISIBLE_DEVICES=0 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name push-wall-v2  --vae-model-name relabel__11_10_08_49_10

CUDA_VISIBLE_DEVICES=1 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name window-close-v2  --vae-model-name relabel__11_10_08_49_49

CUDA_VISIBLE_DEVICES=2 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name shelf-place-v2  --vae-model-name relabel__11_10_08_50_04

CUDA_VISIBLE_DEVICES=3 python train_offline_agent.py --env-type cheetah_vel  --transform-data-bamdp True --env-name sweep-v2  --vae-model-name relabel__11_10_08_50_15





Note the ``--transform-data-bamdp`` argument. When training the meta-RL agent for the first time, this argument should be set to ``True`` in order to perform State Relabelling. 
That is, after loading the datasets and the trained vae, the datasets will be passed through the encoder to produce the approximate belief. This belief is then concatenated 
to the states in our data to form the hyper-states on which our meta-RL agent is trained. This new dataset (with hyper-states) is also saved locally. If this dataset is available
(e.g., after already running the script), you can change the argument to ``False`` in order to save time.  



## Online Setting ##
For the online training, run: ``python online_training.py --env-type X`` where X is a domain (see Data Collection part above).
Configuration files are in ``online_config``. All training parameters can be set from within the files, or by passing command line arguments.  


## Citation ##
```
@inproceedings{dorfman2021offline,
  title={Offline Meta Reinforcement Learning--Identifiability Challenges and Effective Data Collection Strategies},
  author={Dorfman, Ron and Shenfeld, Idan and Tamar, Aviv},
  booktitle={Thirty-Fifth Conference on Neural Information Processing Systems},
  year={2021}
}
```

## Communication ##
For any questions, please contact Ron Dorfman: ``rondorfman2@gmail.com``





