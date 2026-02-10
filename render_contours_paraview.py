#!/usr/bin/env pvpython

import os
from pathlib import Path

from paraview.simple import (  # type: ignore
    GetActiveViewOrCreate,
    OpenFOAMReader,
    Show,
    ColorBy,
    RescaleTransferFunctionToDataRange,
    GetColorTransferFunction,
    SaveScreenshot,
    ResetCamera,
)

CASE_DIR = Path(__file__).resolve().parent.parent
FOAM_FILE = CASE_DIR / "cavity160.foam"
OUTDIR = CASE_DIR / "postProcessingScripts" / "output_paraview"


def main():
    if not FOAM_FILE.exists():
        raise FileNotFoundError(
            f"Missing {FOAM_FILE}. Create it with: touch cavity160.foam"
        )

    OUTDIR.mkdir(parents=True, exist_ok=True)

    reader = OpenFOAMReader(FileName=str(FOAM_FILE))
    # Read internal field + U
    reader.MeshRegions = ["internalMesh"]
    reader.CellArrays = ["U", "p"]

    view = GetActiveViewOrCreate("RenderView")
    view.ViewSize = [1600, 1200]

    display = Show(reader, view)
    display.Representation = "Surface"

    # Make sure we see the 2D domain nicely
    ResetCamera(view)

    # u component (Ux)
    ColorBy(display, ("CELLS", "U", "X"))
    RescaleTransferFunctionToDataRange(True, False)
    GetColorTransferFunction("U").RescaleTransferFunctionToDataRange(True)
    SaveScreenshot(str(OUTDIR / "u_contour_paraview.png"), view)

    # v component (Uy)
    ColorBy(display, ("CELLS", "U", "Y"))
    RescaleTransferFunctionToDataRange(True, False)
    GetColorTransferFunction("U").RescaleTransferFunctionToDataRange(True)
    SaveScreenshot(str(OUTDIR / "v_contour_paraview.png"), view)

    print("Wrote:")
    print(" -", OUTDIR / "u_contour_paraview.png")
    print(" -", OUTDIR / "v_contour_paraview.png")


if __name__ == "__main__":
    main()
