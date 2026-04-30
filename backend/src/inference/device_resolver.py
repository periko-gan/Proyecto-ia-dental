from __future__ import annotations


def resolve_device(preferred: str | None = None) -> str:
    if preferred:
        return preferred

    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass

    return "cpu"
