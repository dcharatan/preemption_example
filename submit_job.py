import os
from pathlib import Path
import shutil

BRANCH = "main"

if __name__ == "__main__":
    # In practice, you would pick a unique job directory.
    job_dir = Path("slurm_job_dir")
    if job_dir.exists():
        print("Deleting job directory for new demo.")
        shutil.rmtree(job_dir, ignore_errors=True)

    # I think it's a good idea to always run jobs from a particular commit to ensure
    # that they're reproducible.
    print(f"Cloning code from branch {BRANCH}.")
    code_dir = job_dir / "code"
    code_dir.mkdir(parents=True, exist_ok=True)
    os.system(
        "git clone --depth 1 --single-branch --no-tags "
        f"--branch {BRANCH} https://github.com/dcharatan/preemption_example.git "
        f"{code_dir}"
    )

    # Create the Slurm job file.
    workspace_dir = job_dir / "workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    slurm_file = f"""#!/bin/bash
#SBATCH -J preemption_example
#SBATCH -o {job_dir}/out.txt
#SBATCH -e {job_dir}/error.txt
#SBATCH --open-mode=append
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --partition=csail-shared
#SBATCH --qos=lab-free
#SBATCH --time=00:01:00
#SBATCH --signal=SIGTERM@30
#SBATCH --requeue

# Automatically requeue jobs on timeout.
trap 'scontrol requeue $SLURM_JOB_ID' SIGTERM

# Add code for loading environments, linking datasets, etc. here.

cd {code_dir}
python3 train.py {workspace_dir}
"""  # noqa: E501

    slurm_script_path = job_dir / "job.slurm"
    with slurm_script_path.open("w") as f:
        f.write(slurm_file)

    os.system(f"chmod +x {slurm_script_path}")
    os.system(f"sbatch {slurm_script_path}")
