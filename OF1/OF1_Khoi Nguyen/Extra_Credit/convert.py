#!/usr/bin/env python3
"""
batch_xy_to_csv.py

Convert OpenFOAM-style .xy files to .csv files.
- Reads all *.xy in an input directory (optionally recursive)
- Writes one CSV per input file to an output directory
- Uses header: x, y, z, U_x, U_y, U_z
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Optional


def parse_xy_file(path: Path, ncols: int = 6) -> List[List[float]]:
    """
    Parse a .xy file that may contain comment/header lines and data lines like:
        (x y z) (Ux Uy Uz)
    or plain numeric columns.
    Returns list of rows with at least ncols floats (first ncols kept).
    """
    rows: List[List[float]] = []

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            # Skip common comment styles
            if s.startswith(("#", "//", "%", ";")):
                continue

            # Remove delimiters often present in OpenFOAM sampling outputs
            s2 = (
                s.replace("(", " ")
                 .replace(")", " ")
                 .replace("[", " ")
                 .replace("]", " ")
                 .replace(",", " ")
            )

            parts = re.split(r"\s+", s2.strip())

            nums: List[float] = []
            for p in parts:
                try:
                    nums.append(float(p))
                except ValueError:
                    pass

            if len(nums) >= ncols:
                rows.append(nums[:ncols])

    return rows


def write_csv(rows: List[List[float]], out_path: Path, header: List[str]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(f"{v:.16g}" for v in r) + "\n")  # good numeric fidelity


def convert_directory(
    in_dir: Path,
    out_dir: Path,
    recursive: bool = False,
    ncols: int = 6,
    header: Optional[List[str]] = None,
) -> None:
    if header is None:
        header = ["x", "y", "z", "U_x", "U_y", "U_z"]

    if not in_dir.exists() or not in_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {in_dir}")

    pattern = "**/*.xy" if recursive else "*.xy"
    xy_files = sorted(in_dir.glob(pattern))

    if not xy_files:
        print(f"No .xy files found in: {in_dir} (recursive={recursive})")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    for xy_path in xy_files:
        rows = parse_xy_file(xy_path, ncols=ncols)

        if not rows:
            print(f"SKIP (no numeric rows): {xy_path}")
            skipped += 1
            continue

        # Preserve relative structure if recursive
        rel = xy_path.relative_to(in_dir)
        out_path = (out_dir / rel).with_suffix(".csv")

        write_csv(rows, out_path, header)
        print(f"OK   {xy_path}  ->  {out_path}  ({len(rows)} rows)")
        converted += 1

    print(f"\nDone. Converted: {converted}, Skipped: {skipped}")


def main():
    parser = argparse.ArgumentParser(description="Batch convert .xy files to .csv")
    parser.add_argument("--in_dir", required=True, help="Input directory containing .xy files")
    parser.add_argument("--out_dir", required=True, help="Output directory for .csv files")
    parser.add_argument("--recursive", action="store_true", help="Search input directory recursively")
    args = parser.parse_args()

    convert_directory(Path(args.in_dir), Path(args.out_dir), recursive=args.recursive)


if __name__ == "__main__":
    main()
