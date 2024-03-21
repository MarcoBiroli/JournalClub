import submitit
import time

def parralel_helloworld(pid):
    print(f'Hello world! I am process {pid}')
    time.sleep(10)
    return pid+1

# executor is the submission interface. Logs are dumped in
# the specified folder.
executor = submitit.AutoExecutor(folder = 'log_test')

# set relevant SLURM parameters.
executor.update_parameters(
        timeout_min = 60,
        slurm_partition="q-1sem",
        tasks_per_node=1,
        slurm_mem=1000,
)

# submit 3 copies of the parralel_helloworld function to the cluster
jobs = [executor.submit(parralel_helloworld, pid) for pid in range(3)]

# wait for all the jobs to finish
[job.wait() for job in jobs]

print('Jobs completed.\n\n')

for pid, job in enumerate(jobs):
    result = job.result()
    output = job.stdout()
    errors = job.stderr()

    print(f'Job {pid} terminated')
    print('---'*3 + 'stdout' + '---'*3)
    print(output)
    print('---'*3 + 'stderr' + '---'*3)
    print(errors)
    print('---'*3 + 'return' + '---'*3)
    print(result)
    print('\n')

