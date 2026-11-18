import sys
import fire
from .RAGApplication import RAGApplication


if __name__ == "__main__":
    try:
        fire.Fire(RAGApplication)
    except ValueError as val_err:
        print(f"ERROR: {val_err}")
        sys.exit(1)
    except FileNotFoundError as found_err:
        print(f"ERROR: {found_err}")
        sys.exit(2)
