import math

#define variables
scaling = 1.0 #meters
d = 1.0 #diameter of cylinder
r = 1.0 #radius of outer circle
h = 3.5 #domain height
lf = 3.5 #domain length in front of cylinder
lb = 3.5 #domain length behind cylinder
w = 0.1 #width in z-direction
wCells = 1 #keep this at 1
wGrading = 1 #keep this at 1
circCells = 45 #cells along the circumference of the circle, each block being 1/8 of the full circle
circGrading = 1 #grading across the circumference of the circle, ideally keep this as 1 for symmetry
radialCells = 20 #number of cells radially outward
radialGrading = 2 #grading of cells radially outward
lfCells = 30 #number of cells in region in front of cylinder
lfGrading = 4 #grading of cells in region in front of cylinder
lbCells = 30 #number of cells in region behind cylinder
lbGrading = 4 #grading of cells in region behind cylinder
hCells = 15 #number of cells in regions above and below cylinder
hGrading = 4 #grading of cells in regions above and below cylinder

#start with vertices
#return 64 vertices, in the prescribed order
def defineVertices(d, r, h, lf, lb, w):
    vertices = []
    vertices.append((-1*lf, h, 0))
    vertices.append((-1/2*math.sqrt(2)*r, h, 0))
    vertices.append((0, h, 0))
    vertices.append((1/2*math.sqrt(2)*r, h, 0))
    vertices.append((lb, h, 0))
    vertices.append((lb, 1/2*math.sqrt(2)*r, 0))
    vertices.append((lb, 0, 0))
    vertices.append((lb, -1.2*math.sqrt(2)*r, 0))
    vertices.append((lb, -1*h, 0))
    vertices.append((1/2*math.sqrt(2)*r, -1*h, 0))
    vertices.append((0, -1*h, 0))
    vertices.append((-1/2*math.sqrt(2)*r, -1*h, 0))
    vertices.append((-1*lf, -1*h, 0))
    vertices.append((-1*lf, -1/2*math.sqrt(2)*r, 0))
    vertices.append((-1*lf, 0, 0))
    vertices.append((-1*lf, 1.2*math.sqrt(2)*r, 0))
    vc = []
    vc.append((-1/2*math.sqrt(2)*r, 1/2*math.sqrt(2)*r, 0))
    vc.append((0, r, 0))
    vc_old = vc.copy()
    for i in vc_old:
        j = (i[1], i[0]*-1, i[2])
        vc.append(j)
    vc_old = vc.copy()
    for i in vc_old:
        j = (i[0]*-1, i[1]*-1, i[2])
        vc.append(j)
    vc_old = vc.copy()
    for i in vc_old:
        j = (i[0]*(d/2)/r, i[1]*(d/2)/r, i[2])
        vc.append(j)
    for i in vc:
        vertices.append(i)
    vertices_old = vertices.copy()
    for i in vertices_old:
        j = (i[0], i[1], w)
        vertices.append(j)
    return (vertices)
vertices = (defineVertices(d,r,h,lf,lb,w))

#now for the 20 blocks
def defineBlocks():
    blockVs = []
    blockVs.append((47,32,33,48,15,0,1,16))
    blockVs.append((48,33,34,49,16,1,2,17))
    blockVs.append((49,34,35,50,17,2,3,18))
    blockVs_old = blockVs.copy()
    for i in range(len(blockVs_old)):
        k = blockVs[i]
        if i%3==0:
            j = ((k[0]+4-16, k[1]+4, k[2]+4, k[3]+2, k[4]+4-16, k[5]+4, k[6]+4, k[7]+2))
        else:
            j = ((k[0]+2, k[1]+4, k[2]+4, k[3]+2, k[4]+2, k[5]+4, k[6]+4, k[7]+2))
        blockVs.append(j)
    blockVs_old = blockVs.copy()
    for i in range(len(blockVs_old)):
        k = blockVs[i]
        if i%3==0:
            if i == 0:
                j = ((k[0]+8-16, k[1]+8, k[2]+8, k[3]+4, k[4]+8-16, k[5]+8, k[6]+8, k[7]+4))
            else:
                j = ((k[0]+8, k[1]+8, k[2]+8, k[3]+4, k[4]+8, k[5]+8, k[6]+8, k[7]+4))
        else:
            if i == 5:
                j = ((k[0]+4, k[1]+8, k[2]+8, k[3]+4-8, k[4]+4, k[5]+8, k[6]+8, k[7]+4-8))
            else:
                j = ((k[0]+4, k[1]+8, k[2]+8, k[3]+4, k[4]+4, k[5]+8, k[6]+8, k[7]+4))
        blockVs.append(j)
    blockC = (56, 48, 49, 57, 24, 16, 17, 25)
    for i in range(8):
        k = blockC
        if i == 7:
            blockVs.append((k[0]+i, k[1]+i, k[2]+i-8, k[3]+i-8, k[4]+i, k[5]+i, k[6]+i-8, k[7]+i-8))
        else:
            blockVs.append((k[0]+i, k[1]+i, k[2]+i, k[3]+i, k[4]+i, k[5]+i, k[6]+i, k[7]+i))

    blockCs = []
    blockCs.append((hCells, lfCells, wCells))
    blockCs.append((hCells, circCells, wCells))
    blockCs.append((hCells, circCells, wCells))
    blockCs.append((lbCells, hCells, wCells))
    blockCs.append((lbCells, circCells, wCells))
    blockCs.append((lbCells, circCells, wCells))
    blockCs_old = blockCs.copy()
    for i in range(len(blockCs_old)):
        k = blockCs_old[i]
        if i==0:
            j = ((k[0], int(k[1]*lbCells/lfCells), k[2]))
        elif i > 2:
            j = ((int(k[0]*lfCells/lbCells), k[1], k[2]))
        else:
            j = ((k[0], k[1], k[2]))
        blockCs.append(j)
    for i in range(8):
        blockCs.append((radialCells, circCells, wCells))

    blockGs = []
    blockGs.append((hGrading, 1/lfGrading, wGrading))
    blockGs.append((hGrading, circGrading, wGrading))
    blockGs.append((hGrading, circGrading, wGrading))
    blockGs.append((lbGrading, 1/hGrading, wGrading))
    blockGs.append((lbGrading, circGrading, wGrading))
    blockGs.append((lbGrading, circGrading, wGrading))
    blockGs_old = blockGs.copy()
    for i in range(len(blockGs_old)):
        k = blockGs_old[i]
        if i==0:
            j = ((k[0], k[1]*lfGrading/lbGrading, k[2]))
        elif i > 2:
            j = ((k[0]*lfGrading/lbGrading, k[1], k[2]))
        else:
            j = ((k[0], k[1], k[2]))
        blockGs.append(j)
    for i in range(8):
        blockGs.append((radialGrading, circGrading, wGrading))

    return (blockVs, blockCs, blockGs)
blocks = (defineBlocks())

#now for the edges, anything that isn't a straight line needs one other point prescribed
#use an angle theta
#that is, 32 arcs
def defineEdges(r, d, w):
    theta = math.pi/8
    s = math.sin(theta)
    c = math.cos(theta)
    edges = []
    edges.append((16, 17, (-s*r, c*r, 0)))
    edges.append((17, 18, (s*r, c*r, 0)))
    edges.append((18, 19, (c*r, s*r, 0)))
    edges.append((19, 20, (c*r, -s*r, 0)))
    edges_old = edges.copy()
    for i in range(len(edges_old)):
        k = edges_old[i]
        if i == 3:
            j = (k[0]+4, k[1]+4-8, (-1*k[2][0], -1*k[2][1], k[2][2]))
        else:
            j = (k[0]+4, k[1]+4, (-1*k[2][0], -1*k[2][1], k[2][2]))
        edges.append(j)
    edges_old = edges.copy()
    for i in range(len(edges_old)):
        k = edges_old[i]
        j = (k[0]+8, k[1]+8, (k[2][0]*(d/2)/r, k[2][1]*(d/2)/r, k[2][2]))
        edges.append(j)
    edges_old = edges.copy()
    for i in range(len(edges_old)):
        k = edges_old[i]
        j = (k[0]+32, k[1]+32, (k[2][0], k[2][1], k[2][2]+w))
        edges.append(j)

    return(edges)
edges = (defineEdges(r, d, w))

#boundaries are defined by faces, which are in turn defined by vertices
def defineBoundaries():
    boundaries = []

    #inlet
    bInlet = []
    bInlet.append((0,32,47,15))
    bInlet.append((15,47,46,14))
    for i in range(2):
        k = bInlet[1]
        j = i+1
        bInlet.append((k[0]-j, k[1]-j, k[2]-j, k[3]-j))
    boundaries.append(("inlet","patch", bInlet))

    #outlet
    bOutlet = []
    bOutlet.append((4,36,37,5))
    for i in range(3):
        k = bOutlet[0]
        j = i+1
        bOutlet.append((k[0]+j, k[1]+j, k[2]+j, k[3]+j))
    boundaries.append(("outlet","patch", bOutlet))

    #top
    bTop = []
    bTop.append((0,32,33,1))
    for i in range(3):
        k = bTop[0]
        j = i+1
        bTop.append((k[0]+j, k[1]+j, k[2]+j, k[3]+j))
    boundaries.append(("top","symmetryPlane", bTop))

    #bottom
    bBottom = []
    bBottom.append((8,40,41,9))
    for i in range(3):
        k = bBottom[0]
        j = i+1
        bBottom.append((k[0]+j, k[1]+j, k[2]+j, k[3]+j))
    boundaries.append(("bottom","symmetryPlane", bBottom))

    #cylinder
    bCyl = []
    bCyl.append((24,56,57,25))
    for i in range(7):
        k = bCyl[0]
        j = i+1
        if j==7:
            bCyl.append((k[0]+j, k[1]+j, k[2]+j-8, k[3]+j-8))
        else:
            bCyl.append((k[0]+j, k[1]+j, k[2]+j, k[3]+j))
    boundaries.append(("cylinder","wall", bCyl))

    return(boundaries)
boundaries = (defineBoundaries())

#now for formatting
with open("./blockMeshDict", "w") as text_file:
    text_file.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMesDict;\n}\n\nconvertToMeters " + str(scaling) + ";\n\n")
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
    text_file.write(");\n\n")
    text_file.write("edges\n(\n\n")
    for i in range(len(edges)):
        k = edges[i]
        text_file.write("arc " + str(k[0]) + " " + str(k[1]) + " (" + str(k[2][0]) + " " + str(k[2][1]) + " " + str(k[2][2]) + ")\n")
    text_file.write("\n);\n\n")
    text_file.write("boundary\n(")
    for i in range(len(boundaries)):
        k = boundaries[i]
        text_file.write("\n\n\t" + k[0] + "\n\t{\n\t\ttype " + k[1] + ";\n\t\tfaces\n\t\t(\n")
        for j in k[2]:
            text_file.write("\t\t\t(" + str(j[0]) + " " + str(j[1]) + " " + str(j[2]) + " " + str(j[3]) + ")\n")
        text_file.write("\t\t);\n\t}")
    text_file.write("\n\n);")
