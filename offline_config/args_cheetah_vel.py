import argparse
import torch
from utils.cli import boolean_argument


def get_args(rest_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default='reach-v2')
    parser.add_argument('--seed', type=int, default=73)# reach-v2

    parser.add_argument('--belief-rewards', default=False, help='use R+=E[R]')
    parser.add_argument('--num-belief-samples', default=20)
    parser.add_argument('--num-train-tasks', default=40)
    parser.add_argument('--num-eval-tasks', default=10)
    parser.add_argument('--hindsight-relabelling', default=False)

    parser.add_argument('--num-trajs-per-task', type=int, default=None,
                        help='how many trajs per task to use. If None - use all')
    parser.add_argument('--meta-batch', type=int, default=16,
                        help='number of tasks to average the gradient across')

    parser.add_argument('--num-iters', type=int, default=1000, help='number meta-training iterates')
    parser.add_argument('--rl-updates-per-iter', type=int, default=1000, help='number of RL steps per iteration')
    parser.add_argument('--batch-size', type=int, default=256, help='number of transitions in RL batch (per task)')

    parser.add_argument('--dqn-layers', nargs='+', default=[256, 256])
    parser.add_argument('--policy-layers', nargs='+', default=[256, 256])

    parser.add_argument('--actor-lr', type=float, default=0.0003, help='learning rate for actor (default: 3e-4)')
    parser.add_argument('--critic-lr', type=float, default=0.0003, help='learning rate for critic (default: 3e-4)')
    parser.add_argument('--clip-grad-value', type=float, default=None, help='clip gradients')

    parser.add_argument('--entropy-alpha', type=float, default=0.2, help='Entropy coefficient')
    parser.add_argument('--automatic-entropy-tuning', default=False)
    parser.add_argument('--alpha-lr', type=float, default=None,
                        help='learning rate for entropy coeff, if automatic tuning is True (default: 3e-4)')
    parser.add_argument('--gamma', type=float, default=0.99, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--soft-target-tau', type=float, default=0.005,
                        help='soft target network update (default: 5e-3)')
    parser.add_argument('--eval-deterministic', default=True)

    parser.add_argument('--transform-data-bamdp', default=False,
                        help='If true - perform state relabelling to bamdp, else - use existing data')

    # logging, saving, evaluation
    parser.add_argument('--log-interval', type=int, default=10,
                        help='log interval, one log per n iterations (default: 10)')
    parser.add_argument('--save-interval', type=int, default=100,
                        help='save models interval, every # iterations (default: 100)')

    parser.add_argument('--log-tensorboard', default=True, help='whether to use tb logger')
    parser.add_argument('--use-gpu', default=True, help='whether to use gpu')

    parser.add_argument('--results-log-dir', default=None, help='directory to save agent logs (default: ./logs)')

    parser.add_argument('--output-file-prefix', default='offline')
    # parser.add_argument('--output-file-prefix', default='offline_with_rr')

    parser.add_argument('--relabelled-data-dir', default='data_bamdp')
    # parser.add_argument('--relabelled-data-dir', default='data_bamdp_with_rr')

    parser.add_argument('--data-dir', default='data')
    parser.add_argument('--main-data-dir', default='./batch_data')

    parser.add_argument('--vae-dir', default='./trained_vae')

    parser.add_argument('--vae-model-name', default='relabel__08_10_20_32_40')
    # parser.add_argument('--vae-model-name', default='relabel__10_08_01_45_08')

    args = parser.parse_args(rest_args)

    return args
