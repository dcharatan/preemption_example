# Slurm Preemption Example

This repository demonstrates a minimal preemption-compatible Slurm job setup.

## Instructions

* You can run "training" directly in the terminal via `python3 train.py` and interrupt it using CTRL+C.
* You can run "training" on Slurm using via `python3 submit_job.py`. The job is configured to run out of time and automatically requeue. In the logs, you will see that the job ran out of time and requeued.

## Preemption Compatibility Checklist

To make your job preemption-compatible, make sure you do the following:

- Add `--requeue` to your job script. This will automatically requeue your job on preemption (i.e., if a higher-priority job takes its place).
- Add `trap 'scontrol requeue $SLURM_JOB_ID' SIGTERM` to your job script. This will automatically requeue your job on timeout.
- Add `#SBATCH --signal=SIGTERM@30` to your job script. This will make Slurm send a signal to your Python script (to allow it to save a checkpoint before preemption/timeout). Then, in your Python script, listen for `SIGTERM` using `signal.signal` and save a checkpoint on `SIGTERM`. Also, make sure your Python script automatically detects and loads checkpoints.
- Use `#SBATCH --open-mode=append` to prevent requeued jobs from overwriting previous logs.

## Example Logs

If your job gets preempted, you will see something like this:

```
2025-04-16 17:06:44 [INFO] Entering step 4.
2025-04-16 17:06:45 [INFO] Entering step 5.
2025-04-16 17:06:46 [INFO] Entering step 6.
slurmstepd: error: *** JOB 953585 ON sitzmann-h200-1 CANCELLED AT 2025-04-16T17:06:46 DUE TO PREEMPTION ***
2025-04-16 17:06:46 [INFO] Job was interrupted. Attempting to exit gracefully.
2025-04-16 17:06:46 [INFO] Attempting to save checkpoint at step 6.
2025-04-16 17:06:46 [INFO] Saved checkpoint at step 6.
Job is pending execution for job 953585
cpu-bind=MASK - sitzmann-h200-1, task  0  0 [2138290]: mask 0xc00000000000000000000000000000008000000000000001 set
2025-04-16 17:09:16 [INFO] Training on sitzmann-h200-1.csail.mit.edu
2025-04-16 17:09:16 [INFO] Attempting to load checkpoint.
2025-04-16 17:09:16 [INFO] Loaded checkpoint at step 6.
2025-04-16 17:09:16 [INFO] Entering step 6.
2025-04-16 17:09:17 [INFO] Entering step 7.
2025-04-16 17:09:18 [INFO] Entering step 8.
```

If your job times out, you will see something like this:

```
2025-04-16 17:24:29 [INFO] Entering step 75.
2025-04-16 17:24:30 [INFO] Entering step 76.
2025-04-16 17:24:31 [INFO] Entering step 77.
slurmstepd: error: *** JOB 953596 ON improbablex001 CANCELLED AT 2025-04-16T17:24:32 DUE TO TIME LIMIT ***
2025-04-16 17:24:32 [INFO] Job was interrupted. Attempting to exit gracefully.
2025-04-16 17:24:32 [INFO] Attempting to save checkpoint at step 77.
2025-04-16 17:24:32 [INFO] Saved checkpoint at step 77.
cpu-bind=MASK - improbablex001, task  0  0 [1617279]: mask 0xc000000000000000c000000000000000 set
2025-04-16 17:26:52 [INFO] Training on improbablex001.csail.mit.edu
2025-04-16 17:26:52 [INFO] Attempting to load checkpoint.
2025-04-16 17:26:52 [INFO] Loaded checkpoint at step 77.
2025-04-16 17:26:52 [INFO] Entering step 77.
2025-04-16 17:26:53 [INFO] Entering step 78.
2025-04-16 17:26:54 [INFO] Entering step 79.
```
