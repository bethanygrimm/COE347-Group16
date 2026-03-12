import math


scaling = 1.0

d = 1.0          # cylinder diameter
r = 2.0          # radius of the intermediate outer circle around cylinder
h = 15.0         # half-height of the domain
lf = 10.0        # inlet distance upstream of cylinder center
lb = 25.0        # outlet distance downstream of cylinder center
w = 0.1          # spanwise thickness

wCells = 1
wGrading = 1
circCells = 48
circGrading = 1
radialCells = 48
radialGrading = 1
lfCells = 80
lfGrading = 1
lbCells = 200
lbGrading = 1
hCells = 120
hGrading = 1


def defineVertices(d, r, h, lf, lb, w):
    vertices = []
    vertices.append((-1 * lf, h, 0))
    vertices.append((-1 / 2 * math.sqrt(2) * r, h, 0))
    vertices.append((0, h, 0))
    vertices.append((1 / 2 * math.sqrt(2) * r, h, 0))
    vertices.append((lb, h, 0))
    vertices.append((lb, 1 / 2 * math.sqrt(2) * r, 0))
    vertices.append((lb, 0, 0))
    vertices.append((lb, -1 / 2 * math.sqrt(2) * r, 0))
    vertices.append((lb, -1 * h, 0))
    vertices.append((1 / 2 * math.sqrt(2) * r, -1 * h, 0))
    vertices.append((0, -1 * h, 0))
    vertices.append((-1 / 2 * math.sqrt(2) * r, -1 * h, 0))
    vertices.append((-1 * lf, -1 * h, 0))
    vertices.append((-1 * lf, -1 / 2 * math.sqrt(2) * r, 0))
    vertices.append((-1 * lf, 0, 0))
    vertices.append((-1 * lf, 1 / 2 * math.sqrt(2) * r, 0))
    vc = []
    vc.append((-1 / 2 * math.sqrt(2) * r, 1 / 2 * math.sqrt(2) * r, 0))
    vc.append((0, r, 0))
    vc_old = vc.copy()
    for i in vc_old:
        vc.append((i[1], -i[0], i[2]))
    vc_old = vc.copy()
    for i in vc_old:
        vc.append((-i[0], -i[1], i[2]))
    vc_old = vc.copy()
    for i in vc_old:
        vc.append((i[0] * (d / 2) / r, i[1] * (d / 2) / r, i[2]))
    for i in vc:
        vertices.append(i)
    vertices_old = vertices.copy()
    for i in vertices_old:
        vertices.append((i[0], i[1], w))
    return vertices


def defineBlocks():
    blockVs = []
    blockVs.append((47, 32, 33, 48, 15, 0, 1, 16))
    blockVs.append((48, 33, 34, 49, 16, 1, 2, 17))
    blockVs.append((49, 34, 35, 50, 17, 2, 3, 18))
    blockVs_old = blockVs.copy()
    for i in range(len(blockVs_old)):
        k = blockVs[i]
        if i % 3 == 0:
            j = (k[0] + 4 - 16, k[1] + 4, k[2] + 4, k[3] + 2, k[4] + 4 - 16, k[5] + 4, k[6] + 4, k[7] + 2)
        else:
            j = (k[0] + 2, k[1] + 4, k[2] + 4, k[3] + 2, k[4] + 2, k[5] + 4, k[6] + 4, k[7] + 2)
        blockVs.append(j)
    blockVs_old = blockVs.copy()
    for i in range(len(blockVs_old)):
        k = blockVs[i]
        if i % 3 == 0:
            if i == 0:
                j = (k[0] + 8 - 16, k[1] + 8, k[2] + 8, k[3] + 4, k[4] + 8 - 16, k[5] + 8, k[6] + 8, k[7] + 4)
            else:
                j = (k[0] + 8, k[1] + 8, k[2] + 8, k[3] + 4, k[4] + 8, k[5] + 8, k[6] + 8, k[7] + 4)
        else:
            if i == 5:
                j = (k[0] + 4, k[1] + 8, k[2] + 8, k[3] + 4 - 8, k[4] + 4, k[5] + 8, k[6] + 8, k[7] + 4 - 8)
            else:
                j = (k[0] + 4, k[1] + 8, k[2] + 8, k[3] + 4, k[4] + 4, k[5] + 8, k[6] + 8, k[7] + 4)
        blockVs.append(j)
    blockC = (56, 48, 49, 57, 24, 16, 17, 25)
    for i in range(8):
        k = blockC
        if i == 7:
            blockVs.append((k[0] + i, k[1] + i, k[2] + i - 8, k[3] + i - 8, k[4] + i, k[5] + i, k[6] + i - 8, k[7] + i - 8))
        else:
            blockVs.append((k[0] + i, k[1] + i, k[2] + i, k[3] + i, k[4] + i, k[5] + i, k[6] + i, k[7] + i))

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
        if i == 0:
            j = (k[0], int(k[1] * lbCells / lfCells), k[2])
        elif i > 2:
            j = (int(k[0] * lfCells / lbCells), k[1], k[2])
        else:
            j = (k[0], k[1], k[2])
        blockCs.append(j)
    for _ in range(8):
        blockCs.append((radialCells, circCells, wCells))

    blockGs = []
    blockGs.append((hGrading, 1 / lfGrading, wGrading))
    blockGs.append((hGrading, circGrading, wGrading))
    blockGs.append((hGrading, circGrading, wGrading))
    blockGs.append((lbGrading, 1 / hGrading, wGrading))
    blockGs.append((lbGrading, circGrading, wGrading))
    blockGs.append((lbGrading, circGrading, wGrading))
    blockGs_old = blockGs.copy()
    for i in range(len(blockGs_old)):
        k = blockGs_old[i]
        if i == 0:
            j = (k[0], k[1] * lfGrading / lbGrading, k[2])
        elif i > 2:
            j = (k[0] * lfGrading / lbGrading, k[1], k[2])
        else:
            j = (k[0], k[1], k[2])
        blockGs.append(j)
    for _ in range(8):
        blockGs.append((radialGrading, circGrading, wGrading))

    return blockVs, blockCs, blockGs


def defineEdges(r, d, w):
    theta = math.pi / 8
    s = math.sin(theta)
    c = math.cos(theta)
    edges = []
    edges.append((16, 17, (-s * r, c * r, 0)))
    edges.append((17, 18, (s * r, c * r, 0)))
    edges.append((18, 19, (c * r, s * r, 0)))
    edges.append((19, 20, (c * r, -s * r, 0)))
    edges_old = edges.copy()
    for i in range(len(edges_old)):
        k = edges_old[i]
        if i == 3:
            j = (k[0] + 4, k[1] + 4 - 8, (-k[2][0], -k[2][1], k[2][2]))
        else:
            j = (k[0] + 4, k[1] + 4, (-k[2][0], -k[2][1], k[2][2]))
        edges.append(j)
    edges_old = edges.copy()
    for i in range(len(edges_old)):
        k = edges_old[i]
        edges.append((k[0] + 8, k[1] + 8, (k[2][0] * (d / 2) / r, k[2][1] * (d / 2) / r, k[2][2])))
    edges_old = edges.copy()
    for i in range(len(edges_old)):
        k = edges_old[i]
        edges.append((k[0] + 32, k[1] + 32, (k[2][0], k[2][1], k[2][2] + w)))
    return edges


def defineBoundaries():
    boundaries = []

    bInlet = []
    bInlet.append((0, 32, 47, 15))
    bInlet.append((15, 47, 46, 14))
    for i in range(2):
        k = bInlet[1]
        j = i + 1
        bInlet.append((k[0] - j, k[1] - j, k[2] - j, k[3] - j))
    boundaries.append(("inlet", "patch", bInlet))

    bOutlet = []
    bOutlet.append((4, 36, 37, 5))
    for i in range(3):
        k = bOutlet[0]
        j = i + 1
        bOutlet.append((k[0] + j, k[1] + j, k[2] + j, k[3] + j))
    boundaries.append(("outlet", "patch", bOutlet))

    bTop = []
    bTop.append((0, 32, 33, 1))
    for i in range(3):
        k = bTop[0]
        j = i + 1
        bTop.append((k[0] + j, k[1] + j, k[2] + j, k[3] + j))
    boundaries.append(("top", "symmetryPlane", bTop))

    bBottom = []
    bBottom.append((8, 40, 41, 9))
    for i in range(3):
        k = bBottom[0]
        j = i + 1
        bBottom.append((k[0] + j, k[1] + j, k[2] + j, k[3] + j))
    boundaries.append(("bottom", "symmetryPlane", bBottom))

    bCyl = []
    bCyl.append((24, 56, 57, 25))
    for i in range(7):
        k = bCyl[0]
        j = i + 1
        if j == 7:
            bCyl.append((k[0] + j, k[1] + j, k[2] + j - 8, k[3] + j - 8))
        else:
            bCyl.append((k[0] + j, k[1] + j, k[2] + j, k[3] + j))
    boundaries.append(("cylinder", "wall", bCyl))

    return boundaries


def write_block_mesh_dict(filename="blockMeshDict"):
    vertices = defineVertices(d, r, h, lf, lb, w)
    blocks = defineBlocks()
    edges = defineEdges(r, d, w)
    boundaries = defineBoundaries()

    with open(filename, "w", encoding="utf-8") as text_file:
        text_file.write("FoamFile\n{\n\tversion\t2.0;\n\tformat\tascii;\n\tclass\tdictionary;\n\tobject\tblockMeshDict;\n}\n\nconvertToMeters " + str(scaling) + ";\n\n")
        text_file.write("vertices\n(\n")
        for idx, v in enumerate(vertices):
            text_file.write(f"\t({v[0]} {v[1]} {v[2]}) // {idx}\n")
        text_file.write(");\n\nblocks\n(\n")
        for i in range(len(blocks[0])):
            text_file.write("\thex (" + " ".join(str(x) for x in blocks[0][i]) + ") (" + " ".join(str(x) for x in blocks[1][i]) + ") simpleGrading (" + " ".join(str(x) for x in blocks[2][i]) + ")\n")
        text_file.write(");\n\nedges\n(\n")
        for e in edges:
            text_file.write(f"\tarc {e[0]} {e[1]} ({e[2][0]} {e[2][1]} {e[2][2]})\n")
        text_file.write(");\n\nboundary\n(\n")
        for name, btype, faces in boundaries:
            text_file.write(f"\t{name}\n\t{{\n\t\ttype {btype};\n\t\tfaces\n\t\t(\n")
            for face in faces:
                text_file.write("\t\t\t(" + " ".join(str(x) for x in face) + ")\n")
            text_file.write("\t\t);\n\t}\n")
        text_file.write(");\n\nmergePatchPairs\n(\n);\n")


if __name__ == "__main__":
    write_block_mesh_dict()
