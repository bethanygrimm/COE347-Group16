To run the meshing script, move defineBlockMeshDict.py into the system folder and run <code>python3 defineBlockMeshDict.py</code>, and blockMeshDict should automatically show up in the system folder. Lines 4-22 can be varied if we want to change mesh dimensions, grading, and resolution. I will add a schematic in a bit (lmk if there are any errors)

also for every mesh you use can you put the parameters (of the Python script) in the Git please and thank you :3

**TO-DO:**
Part 6:
Re=20 (Andrew)
- Three contour plots
- Plot of the streamlines
Re=110 (Bethany)
- Three contour plots
- Plot of the time history of u, v, and p

Part 7:
Re=20 (Andrew)
- Just free-response
Re=110 (Bethany)
- Just free-response

Part 8: (Precious, Bethany)
- Five meshes (original, refinement 1, refinement 2, ref 2 with smaller timestep, ref 2 with even smaller timestep) (we can split these up, these take forever) (I (Bethany) can do the Paraview stuff as long as it's all on git yay)
- Attach details of each mesh
- Find St = f/(U/D) for each one
- Free-response

Part 9: (Khoi, Andrew)
- Four meshes
- idk man have fun

Part 10:
Extra credit (Precious)

Writeup (Andrew, Bethany)

Attach all files and team report

**also change the segment starting with "#SBATCH -p development" in openfoam.v7.parallel.slurm to the following (this is so you don't lose your progress)**
#SBATCH -p small          # Queue (partition) name
#SBATCH -N 1               # Total # of nodes
#SBATCH -n 2               # Total # of mpi tasks
#SBATCH -t 05:00:00        # Run time (hh:mm:ss)
