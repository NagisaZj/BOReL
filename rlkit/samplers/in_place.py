import numpy as np

from rlkit.samplers.util import rollout, offline_sample, offline_rollout, offline_rollout_online
from rlkit.torch.sac.policies import MakeDeterministic


class InPlacePathSampler(object):
    """
    A sampler that does not serialization for sampling. Instead, it just uses
    the current policy and environment as-is.

    WARNING: This will affect the environment! So
    ```
    sampler = InPlacePathSampler(env, ...)
    sampler.obtain_samples  # this has side-effects: env will change!
    ```
    """
    def __init__(self, env, policy, max_path_length):
        self.env = env
        self.policy = policy

        self.max_path_length = max_path_length

    def start_worker(self):
        pass

    def shutdown_worker(self):
        pass

    def obtain_samples(self, deterministic=False, max_samples=np.inf, max_trajs=np.inf, accum_context=True,
                       is_select=False, resample=1, r_thres=0., is_onlineadapt_max=False, is_sparse_reward=False):
        """
        Obtains samples in the environment until either we reach either max_samples transitions or
        num_traj trajectories.
        The resample argument specifies how often (in trajectories) the agent will resample it's context.
        """
        assert max_samples < np.inf or max_trajs < np.inf, "either max_samples or max_trajs must be finite"
        policy = MakeDeterministic(self.policy) if deterministic else self.policy
        paths = []
        n_steps_total = 0
        n_trajs = 0
        while n_steps_total < max_samples and n_trajs < max_trajs:
            path = rollout(
                self.env, policy, max_path_length=self.max_path_length, accum_context=accum_context,
                is_select=is_select, r_thres=r_thres, is_onlineadapt_max=is_onlineadapt_max,
                is_sparse_reward=is_sparse_reward)
            # save the latent context that generated this trajectory
            path['context'] = policy.z.detach().cpu().numpy()
            paths.append(path)
            n_steps_total += len(path['observations'])
            n_trajs += 1
            # don't we also want the option to resample z ever transition?
            if n_trajs % resample == 0:
                policy.sample_z()
        return paths, n_steps_total

class OfflineInPlacePathSampler(InPlacePathSampler):
    def __init__(self, env, policy, max_path_length):
        super().__init__(env, policy, max_path_length)

    def obtain_samples(self, buffer, deterministic=False, max_samples=np.inf, max_trajs=np.inf, accum_context=True, resample=1,
                       rollout=False):
        """
        Obtains samples from saved trajectories until either we reach either max_samples transitions or
        num_traj trajectories.
        The resample argument specifies how often (in trajectories) the agent will resample it's context.
        """
        assert max_samples < np.inf or max_trajs < np.inf, "either max_samples or max_trajs must be finite"
        policy = MakeDeterministic(self.policy) if deterministic else self.policy
        paths = []
        n_steps_total = 0
        n_trajs = 0
        while n_steps_total < max_samples and n_trajs < max_trajs:
            if rollout:
                path = offline_rollout(self.env, policy, buffer, max_path_length=self.max_path_length, accum_context=accum_context)
            else:
                path = offline_sample(self.env, policy, buffer, max_path_length=self.max_path_length, accum_context=accum_context)
            # save the latent context that generated this trajectory
            path['context'] = policy.z.detach().cpu().numpy()
            paths.append(path)
            n_steps_total += len(path['observations'])
            n_trajs += 1
            # don't we also want the option to resample z ever transition?
            if n_trajs % resample == 0:
                policy.sample_z()
        return paths, n_steps_total

    def obtain_samples_online(self, buffer, deterministic=False, max_samples=np.inf, max_trajs=np.inf, accum_context=True, resample=1,
                       rollout=False):
        """
        Obtains samples from saved trajectories until either we reach either max_samples transitions or
        num_traj trajectories.
        The resample argument specifies how often (in trajectories) the agent will resample it's context.
        """
        assert max_samples < np.inf or max_trajs < np.inf, "either max_samples or max_trajs must be finite"
        policy = MakeDeterministic(self.policy) if deterministic else self.policy
        paths = []
        n_steps_total = 0
        n_trajs = 0
        while n_steps_total < max_samples and n_trajs < max_trajs:
            if rollout:
                path = offline_rollout_online(self.env, policy, buffer, max_path_length=self.max_path_length, accum_context=accum_context)
            else:
                path = offline_sample(self.env, policy, buffer, max_path_length=self.max_path_length, accum_context=accum_context)
            # save the latent context that generated this trajectory
            path['context'] = policy.z.detach().cpu().numpy()
            paths.append(path)
            n_steps_total += len(path['observations'])
            n_trajs += 1
            # don't we also want the option to resample z ever transition?
            if n_trajs % resample == 0:
                policy.sample_z()
        return paths, n_steps_total