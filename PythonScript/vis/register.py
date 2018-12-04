import vis
import vtk
# ------------
# vis_register
# ------------
gReposObjDisp = {}

def register(ren,objName):
    global gReposObjDisp
        
    try:
        gReposObjDisp[objName]
        if ren[0] in gReposObjDisp[objName]:
            raise ValueError("ERROR: "+ objName+ " already exists in ren " + ren[0])
        else:
            gReposObjDisp[objName].append(ren[0])
    except:
        gReposObjDisp[objName] = {ren[0]}
    return
        
# --------------
# vis_unregister
# --------------
def unregister(ren, objName):
    global gReposObjDisp
    try:
        gReposObjDisp[objName]
    except:
        raise ValueError("ERROR: object not registered!")
        
    if ren[0] not in gReposObjDisp[objName]:
        raise ValueError("ERROR: object not registered in "+ren[0])
    else:
        gReposObjDisp[objName].remove(ren[0])
        if not gReposObjDisp[objName]:
            del gReposObjDisp[objName]
    return 