import math

#define variables
scaling = 1.0 #meters
c = 1.0 #airfoil chord length, keep this constant at 1.0
alpha = 30 #airofil angle in degrees, keep this constant at 30
#remember the numpy and math modules work in radians

lf = 2.0 #domain length in front of airfoil, lf > rl
lb = 7.0 #domain length behind airfoil, lb > rl
h = 3.5 #domain height, h > rh
rl = 1 #boundary in front of and behind airfoil
rh = 1 #boundary above and below airfoil
t = 0.1 #width in z-direction

lfCells = 10 #number of cells in region in front of airfoil
lfGrading = 1 #grading of cells in region in front of airfoil
lbCells = 30 #number of cells in region behind airfoil
lbGrading = 4 #grading of cells in region behind airfoil
hCells = 15 #number of cells in regions above and below airfoil
hGrading = 4 #grading of cells in regions above and below airfoil
rlCells = 10 #number of cells in boundary in front of and behind airfoil (RADIALLY OUTWARD)
rlGrading = 1 #grading of cells in boundary in front of and behind airfoil (RADIALLY OUTWARD)
rhCells = 10 #number of cells in boundary above and below airfoil (RADIALLY OUTWARD)
rhGrading = 1 #grading of cells in boundary above and below airfoil (RADIALLY OUTWARD)
bfCells = 15 #number of cells in boundary in front of and behind airfoil (ALONG AIRFOIL)
bfGrading = 1 #grading of cells in boundary in front of and behind airfoil (ALONG AIRFOIL)
bbCells = 15 #number of cells in boundary above and below airfoil (ALONG AIRFOIL)
bbGrading = 1 #grading of cells in boundary above and below airfoil (ALONG AIRFOIL)
tCells = 1 #keep this at 1
tGrading = 1 #keep this at 1

#start with vertices
#return 40 vertices, in the prescribed order
def defineVertices(c, alpha, lf, lb, h, rl, rh, t):
    vertices = []
    cl = 0.5*c
    ch = math.tan(alpha*math.pi/180.0) * cl
    vertices.append((-1*lf, h, 0))
    vertices.append((-1*(cl+rl), h, 0))
    vertices.append((0, h, 0))
    vertices.append(((cl+rl), h, 0))
    vertices.append((lb, h, 0))
    vertices.append((lb, 0, 0))
    vertices.append((lb, -1*h, 0))
    vertices.append(((cl+rl), -1*h, 0))
    vertices.append((0, -1*h, 0))
    vertices.append((-1*(cl+rl), -1*h, 0))
    vertices.append((-1*lf, -1*h, 0))
    vertices.append((-1*lf, 0, 0))
    vertices.append((-1*(cl+rl), 0, 0))
    vertices.append((0, ch+rh, 0))
    vertices.append(((cl+rl), 0, 0))
    vertices.append((0, -1*(ch+rh), 0))
    vertices.append((-1*(cl), 0, 0))
    vertices.append((0, ch, 0))
    vertices.append(((cl), 0, 0))
    vertices.append((0, -1*(ch), 0))
    vc = vertices.copy()
    for i in vc:
        j = (i[0], i[1], t)
        vertices.append(j)
    return vertices
vertices = (defineVertices(c, alpha, lf, lb, h, rl, rh, t))

#12 blocks
#I'm hardcoding everything sorry </3
def defineBlocks():
    blockVs = []
    blockVs.append((31,20,21,32,11,0,1,12))
    blockVs.append((32,21,22,33,12,1,2,13))
    blockVs.append((33,22,23,34,13,2,3,14))
    blockVs.append((34,23,24,25,14,3,4,5))
    blockVs.append((25,26,27,34,5,6,7,14))
    blockVs.append((34,27,28,35,14,7,8,15))
    blockVs.append((35,28,29,32,15,8,9,12))
    blockVs.append((32,29,30,31,12,9,10,11))
    blockVs.append((32,33,37,36,12,13,17,16))
    blockVs.append((37,33,34,38,17,13,14,18))
    blockVs.append((34,35,39,38,14,15,19,18))
    blockVs.append((39,35,32,36,19,15,12,16))

    blockCs = []
    blockCs.append((hCells, lfCells, tCells))
    blockCs.append((hCells, bfCells, tCells))
    blockCs.append((hCells, bbCells, tCells))
    blockCs.append((hCells, lbCells, tCells))
    blockCs.append(blockCs[3])
    blockCs.append(blockCs[1])
    blockCs.append(blockCs[2])
    blockCs.append(blockCs[0])
    blockCs.append((bfCells, rlCells, tCells))
    blockCs.append((rhCells, bbCells, tCells))
    blockCs.append(blockCs[8])
    blockCs.append(blockCs[9])

    blockGs = []
    blockGs.append((hGrading, 1/lfGrading, tGrading))
    blockGs.append((hGrading, 1/bfGrading, tGrading))
    blockGs.append((hGrading, bbGrading, tGrading))
    blockGs.append((hGrading, lbGrading, tGrading))
    blockGs.append((hGrading, 1/lbGrading, tGrading))
    blockGs.append((hGrading, 1/bbGrading, tGrading))
    blockGs.append((hGrading, bfGrading, tGrading))
    blockGs.append((hGrading, lfGrading, tGrading))
    blockGs.append((1/bfGrading, 1/rlGrading, tGrading))
    blockGs.append((rhGrading, bbGrading, tGrading))
    blockGs.append((1/bbGrading, 1/rlGrading, tGrading))
    blockGs.append((rhGrading, bfGrading, tGrading))

    return(blockVs, blockCs, blockGs)
blocks = defineBlocks()

#all edges are straight lines and do not need to be prescribed

#boundaries are defined by faces, which are in turn defined by vertices
def defineBoundaries():
    boundaries = []

    #inlet
    bInlet = []
    bInlet.append((0,20,31,11))
    bInlet.append((11,31,30,10))
    boundaries.append(("inlet","patch", bInlet))

    #outlet
    bOutlet = []
    bOutlet.append((4,24,25,5))
    bOutlet.append((5,25,26,6))
    boundaries.append(("outlet","patch", bOutlet))

    #top
    bTop = []
    sample = (0,1,21,20)
    for i in range(4):
        bTop.append((sample[0]+i, sample[1]+i, sample[2]+i, sample[3]+i))
    boundaries.append(("top","patch", bTop))

    #bottom
    bBottom = []
    sample = (6,7,27,26)
    for i in range(4):
        bBottom.append((sample[0]+i, sample[1]+i, sample[2]+i, sample[3]+i))
    boundaries.append(("bottom","patch", bBottom))

    #airfoil
    bAir = []
    sample = (16,17,37,36)
    for i in range(3):
        bAir.append((sample[0]+i, sample[1]+i, sample[2]+i, sample[3]+i))
    bAir.append((19,16,36,39))
    boundaries.append(("airfoil","wall", bAir))

    return(boundaries)
boundaries = defineBoundaries()

#now for formatting
with open("./blockMeshDict", "w") as text_file:
    text_file.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters " + str(scaling) + ";\n\n")
    text_file.write("vertices\n(\n")
    for i in range(len(vertices)):
        k = vertices[i]
        text_file.write("\t(" + str(k[0]) + " " + str(k[1]) + " " + str(k[2]) + ") // " + str(i) + "\n")
    text_file.write(");\n\n")
    text_file.write("blocks\n(\n")
    for i in range(len(blocks[0])):
        text_file.write("\t// block" + str(i) + "\n")
        text_file.write("\thex (")
        for j in blocks[0][i]:
            text_file.write(str(j) + " ")
        text_file.write(") (" + str(blocks[1][i][0]) + " " + str(blocks[1][i][1]) + " " + str(blocks[1][i][2]) + ") ")
        text_file.write("simpleGrading (" + str(blocks[2][i][0]) + " " + str(blocks[2][i][1]) + " " + str(blocks[2][i][2]) + ")\n")
    text_file.write(");\n\nedges\n(\n);\n\n")
    text_file.write("boundary\n(")
    for i in range(len(boundaries)):
        k = boundaries[i]
        text_file.write("\n\n\t" + k[0] + "\n\t{\n\t\ttype " + k[1] + ";\n\t\tfaces\n\t\t(\n")
        for j in k[2]:
            text_file.write("\t\t\t(" + str(j[0]) + " " + str(j[1]) + " " + str(j[2]) + " " + str(j[3]) + ")\n")
        text_file.write("\t\t);\n\t}")
    text_file.write("\n\n);")
