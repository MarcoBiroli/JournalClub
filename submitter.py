import bz2
import pickle
import submitit
import time
import numpy as np

print('hello')

job_name = "my_cool_job"
NSAMPLES = 100000000

def montecarlo_sampling(seed):
    '''
    Samples 100 million points in the 2D square [-1, 1] x [-1, 1] with the given seed. And
    computes the number of points which fall within the centered circle of radius 1.

    Arguments:
        - seed (int)    : the seed with which to initialize the random number generator.

    Returns:
        - counter (int) : the number of samples which fell within the centered circle of
                          radius 1.
        - nsamples (int): the number of points which have been sampled.
    '''
    np.random.seed(seed)
    samples = (np.random.rand(NSAMPLES, 2) - 0.5)*2
    return ((samples[:, 0]**2 + samples[:, 1]**2) < 1).sum(), NSAMPLES

# executor is the submission interface (logs are dumped in the folder)
executor = submitit.AutoExecutor(folder="log_test")
# set timeout in min, and partition for running the job
executor.update_parameters(
    timeout_min=60,
    slurm_partition="q-1sem", #misc slurm args
    tasks_per_node=1,  # number of cores
    slurm_mem=1000,  # memory 
)

#submit 100 jobs:
jobs = [executor.submit(montecarlo_sampling, num) for num in range(100)]

# but actually maybe we want to come back to those jobs later, so let’s save them to disk
with bz2.open(job_name + ".job.pkl.bz2", "wb") as f:
    pickle.dump(jobs, f)


