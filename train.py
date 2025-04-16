import sys
from pathlib import Path
import time
import logging
import platform
import signal


def load_checkpoint(path: Path) -> int:
    """Load the current step from a checkpoint."""
    logging.info("Attempting to load checkpoint.")
    with path.open("r") as f:
        step = int(f.read())
    logging.info(f"Loaded checkpoint at step {step}.")
    return step


def save_checkpoint(path: Path, step: int) -> None:
    """Save the current step to a checkpoint."""
    logging.info(f"Attempting to save checkpoint at step {step}.")
    with path.open("w") as f:
        f.write(str(step))
    logging.info(f"Saved checkpoint at step {step}.")


if __name__ == "__main__":
    # Read the workspace from the arguments.
    # You could also read it from environment variables, use Hydra, etc.
    workspace = Path(sys.argv[1])
    workspace.mkdir(exist_ok=True, parents=True)

    # Set up logging.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info(f"Training on {platform.node()}")

    # Attempt to resume from a checkpoint.
    checkpoint_path = workspace / "checkpoint.txt"
    try:
        step = load_checkpoint(checkpoint_path)
    except FileNotFoundError:
        # If no checkpoint exists, start from the beginning.
        step = 0

    # Set up a signal handler to listen for preemption.
    # Slurm will send SIGTERM to the process before killing it.
    # If you want to handle CTRL+C as well, listen for SIGINT.
    def handle_interrupt(*_):
        # Save progress to a checkpoint, then exit the process.
        logging.info("Job was interrupted. Attempting to exit gracefully.")
        save_checkpoint(checkpoint_path, step)
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_interrupt)
    signal.signal(signal.SIGINT, handle_interrupt)

    # Simulate a training loop.
    while step < 120:
        logging.info(f"Entering step {step}.")
        time.sleep(1)
        step += 1

    logging.info("Training complete.")
