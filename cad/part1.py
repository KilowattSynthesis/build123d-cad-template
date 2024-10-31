import os
from pathlib import Path

import build123d as bd
from loguru import logger

if os.getenv("CI"):

    def show(*args: object) -> bd.Part:
        """Do nothing (dummy function) to skip showing the CAD model in CI."""
        logger.info(f"Skipping show({args}) in CI")
        return args[0]
else:
    import ocp_vscode

    def show(*args: object) -> bd.Part:
        """Show the CAD model in the CAD viewer."""
        ocp_vscode.show(*args)
        return args[0]


# region Constants
# ADD CONSTANTS HERE
# end region


def validate() -> None:
    """Raise if variables are not valid."""


def make_part1() -> bd.Part:
    """Create a CAD model of part1."""
    p = bd.Part()

    p += bd.Cylinder(radius=20, height=20)

    return p


if __name__ == "__main__":
    validate()

    parts = {
        "part1": show(make_part1()),
    }

    logger.info("Showing CAD model(s)")

    (export_folder := Path(__file__).parent.with_name("build")).mkdir(
        exist_ok=True
    )
    for name, part in parts.items():
        assert isinstance(part, bd.Part), f"{name} is not a Part"
        # assert part.is_manifold is True, f"{name} is not manifold"

        bd.export_stl(part, str(export_folder / f"{name}.stl"))
        bd.export_step(part, str(export_folder / f"{name}.step"))
