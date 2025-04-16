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
