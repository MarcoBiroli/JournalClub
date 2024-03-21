import bz2
import pickle
import numpy as np

job_name = "my_cool_job"

# Resume after quitting
with bz2.open(job_name + ".job.pkl.bz2", "rb") as f:
    jobs = pickle.load(f)
    
print('Reloaded jobs.')

print('Waiting for job completion ...')

for job in jobs:
    print(job)

# wait for all jobs to finish
[job.wait() for job in jobs]

print('Recovered all jobs.')

res_list = []

# Examine job outputs for failures etc
fail_ids = [job.job_id for job in jobs if job.state not in  ('DONE', 'COMPLETED') and job.stderr().strip() != '']
res_list.extend([job.results() for job in jobs if job.job_id not in fail_ids ])
failures = [job for job in jobs if job.job_id in fail_ids]

if failures:
    print("failures")
    print("===")
    for job in failures:
        print(job.state, job.stderr())

# Save results to disk
with bz2.open(job_name + ".result.pkl.bz2", "wb") as f:
    pickle.dump(res_list, f)
    
total_matches = 0
grand_total = 0
for res in res_list:
    for matches, total in res:
        total_matches += matches
        grand_total += total

print('\n')
print('---'*5)
print('\n')

print(f'Sampled Pi = {total_matches/grand_total*4}, using {grand_total:e} samples.')
print(f'Known Pi = {np.pi}')
    
print('\n')
    
    
 
