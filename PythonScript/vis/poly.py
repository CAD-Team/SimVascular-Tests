import vis
import vtk
import Repository
# -----------
# ::vis::poly
# -----------
def poly(ren,obj):
    #@c Display a vtkPolyData object in the given renderer
    #@a ren: renderer
    #@a obj: object name
    vis.poly.polyRm(ren,obj)
    tag = "%s_%s" % (ren[0],obj[0])
    Map = [None]*2
    Map[0] = "p_map_"+tag
    Map[1] = vtk.vtkPolyDataMapper()
    Map[1].SetInputData(obj[1])
    #Map[1].ScalarVisibilityOff()
    
    act = [None]*2
    act[0] = "p_act_"+tag
    act[1] = vtk.vtkActor()
    act[1].SetMapper(Map[1])
    act[1].GetProperty().SetColor(1,0,0)
    vis.renfun.renAddActor(ren,act)
    vis.renfun.render(ren)
    
    setattr(vis,Map[0], Map)
    setattr(vis,act[0],act)
    return act

# ----------
# vis_pRepos
# ----------
# Grab a given vtkPolyData object from the repository, and render it in the given rendering window.
def pRepos(ren,objName):
    tag = "%s_%s" % (ren[0],objName)
    
    try:
        vis.register(ren,objName)
    except:
        vis.poly.polyRm(ren,objName)
        vis.register(ren,objName)
        
    vtkName = Repository.ExportToVtk(objName)
    Map = [None]*2
    Map[0] = "p_map_"+tag
    Map[1] = vtk.vtkPolyDataMapper()
    Map[1].SetInputData(vtkName)
    Map[1].ScalarVisibilityOff()
    
    act = [None]*2
    act[0] = "p_act_"+tag
    act[1] = vtk.vtkActor()
    act[1].SetMapper(Map[1])
    act[1].GetProperty().SetColor(1,0,0)
    
    vis.renfun.renAddActor(ren,act)
    vis.renfun.render(ren)
    
    setattr(vis,Map[0], Map)
    setattr(vis,act[0],act)
    return act
    
# -------------------
# ::vis::polyGetActor
# -------------------

def polyGetActor(ren, obj):
  #@a ren: renderer
  #@a obj: object name
  #@r actor object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
        
    name ='p_act_'+tag
    return getattr(vis,name)


# ---------------
# ::vis::polyNorm
# ---------------
def polyNorm(ren,obj):
    #@c Add vtkPolyDataNormals to the vtkPolyData viewing pipeline.
    #@note there is no proc to perform the reverse operation (i.e. remove
    #@note the normals).  This is because the caller can presumably just
    #@note turn off normal-based properties via the actor's vtkProperty.
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
        objName = obj[0]
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
        objName = obj
    else:
        raise ValueError("Argument type unsupported.")
    nrm = [None]*2
    
    try:
        Map = getattr(vis,"p_map_"+tag)
    except:
        raise ValueError(objName + " not currently being displayed in " + ren[0])
        
    act = getattr(vis,"p_act_"+tag)
    nrm[0] = "p_nrm_" + tag
    
    nrm[1] = vtk.vtkPolyDataNormals()
    nrm[1].SetInputDataObject(Map[1].GetInput())
    Map[1].SetInputDataObject(nrm[1].GetOutput())
    nrm[1].Update()
    
    setattr(vis,Map[0], Map)
    setattr(vis,act[0],act)
    setattr(vis,nrm[0],nrm)
    return act

# -------------
# ::vis::polyRm
# -------------
def polyRm(ren,obj):
    #@c Remove the poly from the given renderer
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")

    try:
        act = getattr(vis,"p_act_"+tag)
    except:
        return
            
    #if {$act == $::vis::tkvars(PickedAssembly)} {
    #  ::vis::tkDeselectPickedActor
    #}
    
    try:
        vis.poly.polyUnshow(ren,obj)
    except:
        pass
        
    delList = ["p_grayscaleLUT_" + tag,"p_blueToRedLUT_" + tag,"p_nrm_" + 
    tag,"p_map_" + tag,"p_act_" + tag,"p_lmap_" + tag,"p_labels_" + tag]
    
    for i in delList:
        try:
            delattr(vis, i)
        except:
            pass
                
    vis.renfun.render(ren)
    return
    

# ----------------
# ::vis::polyRmAll
# ----------------
def polyRmAll(ren):
    #@c Remove all polys from renderer
    #@a ren: renderer
    vis.poly.polyUnshowAll(ren)
    
    delList = ["p_grayscaleLUT_" + ren[0],"p_blueToRedLUT_" + ren[0],"p_nrm_" + 
    ren[0],"p_map_" + ren[0],"p_act_" +ren[0],"p_lmap_" + ren[0],"p_labels_" + ren[0]]
    dic = dir(vis)
    for i in delList:
        for j in dic:
            if i in j:
                delattr(vis,j)
    
    vis.renfun.render(ren)
    return


# ---------------
# ::vis::polyShow
# ---------------
# Note that Renderer::AddActor should only add an actor if it is not
# already present.
def polyShow(ren,obj):
    #@c Show object in renderer
    #@a ren: renderer
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    vis.poly.polyUnshow(ren,obj)
    actor = getattr(vis, "p_act_"+tag)
    ren[1].AddActor(actor[1])
    vis.renfun.render(ren)
    return



# -----------------
# ::vis::polyUnshow
# -----------------
def polyUnshow(ren,obj):
    #@c Remove actor from renderer
    #@a ren: renderer
    #@a obj: object name
    try:
        vis.poly.polyUnshowIds(ren,obj)
    except:
        pass
        
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
        
    actor = getattr(vis, "p_act_"+tag)
    
    if (ren[1].GetActors().IsItemPresent(actor[1])>0):
        ren[1].RemoveActor(actor[1])
        
    vis.renfun.render(ren)
    return


# --------------------
# ::vis::polyUnshowAll
# --------------------
#
def polyUnshowAll(ren):
    #@c Remove all poly actors from renderer
    #@a ren: renderer
    
    dic = dir(vis)
    tag = "p_labels_" + ren[0]
    
    for i in dic:
        if tag in i:
            actor = getattr(vis,i)
            vis.actor.actor2DRm(ren,actor)
            
    tag = "p_act_" + ren[0]
    
    for i in dic:
        if tag in i:
            actor = getattr(vis,i)
            vis.actor.actorRM(ren,actor) 

# ----------------------
# ::vis::polyShowScalars
# ----------------------
def polyShowScalars(ren,obj):
    #@c Show scalar values on poly in renderer in grayscale
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    lookupGrayscale = [None]*2
    lookupGrayscale[0] = "p_grayscaleLUT_"+tag
    lookupGrayscale[1] = vtk.vtkWindowLevelLookupTable()
    lookupGrayscale[1].SetWindow(1023)
    lookupGrayscale[1].SetLevel(512)
    lookupGrayscale[1].SetWindow(0.5)
    lookupGrayscale[1].SetLevel(0.5)
    lookupGrayscale[1].SetHueRange(0.,0.)
    lookupGrayscale[1].SetSaturationRange(0.,0.)
    lookupGrayscale[1].SetValueRange(0.,1.)
    lookupGrayscale[1].SetNumberOfColors(16384)
    lookupGrayscale[1].Build()
    
    act = polyGetActor(ren,obj)
    act[1].GetMapper().SetLookupTable(lookupGrayscale[1])
    act[1].GetMapper().ScalarVisibilityOn()
    
    Range = act[1].GetMapper().GetInput().GetPointData().GetScalars().GetRange()
    act[1].GetMapper().SetScalarRange(Range[0],Range[1])
    vis.renfun.render(ren)
    
    setattr(vis,act[0],act)
    setattr(vis,lookupGrayscale[0],lookupGrayscale)
    return
    

# ---------------------------
# ::vis::polyShowColorScalars
# ---------------------------
def polyShowColorScalars(ren, obj):

    #@c Show scalar values on poly in renderer in color
    #@a ren: renderer
    #@a obj: object name

    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    lookupColor = [None]*2
    lookupColor[0] = "p_blueToRedLUT_"+tag
    lookupColor[1] = vtk.vtkLookupTable()
    lookupColor[1].SetHueRange(0.6667 ,0.0)
    lookupColor[1].SetSaturationRange(1.,1.)
    lookupColor[1].SetValueRange(1.,1.)
    lookupColor[1].SetAlphaRange(1.,1.)
    lookupColor[1].SetNumberOfColors(16384)
    lookupColor[1].Build()
    
    act = polyGetActor(ren,obj)
    act[1].GetMapper().SetLookupTable(lookupColor[1])
    act[1].GetMapper().ScalarVisibilityOn()
    
    Range = act[1].GetMapper().GetInput().GetPointData().GetScalars().GetRange()
    act[1].GetMapper().SetScalarRange(Range[0],Range[1])
    vis.renfun.render(ren)
    
    setattr(vis,act[0],act)
    setattr(vis,lookupColor[0],lookupColor)
    return 


# ------------------
# ::vis::polyShowIds
# ------------------
def polyShowIds(ren,obj):

  #@c Show the point ids of a given poly object in renderer
  #@a ren: renderer
  #@a obj: object name
  if isinstance(obj,list):
      tag = "%s_%s" % (ren[0],obj[0])
  elif isinstance(obj,str):
      tag = "%s_%s" % (ren[0],obj)
  else:
      raise ValueError("Argument type unsupported.")
        
  try:
      vis.poly.polyUnshowIds(ren,obj)
  except:
      pass
      
  lmap = [None]*2
  lmap[0] = "p_lmap_"+tag
  labels = [None]*2
  labels[0] = "p_labels_"+tag
  
  lmap[1] = vtk.vtkLabeledDataMapper()
  lmap[1].SetLabelModeToLabelIds()
  if isinstance(obj,list):
        lmap[1].SetInputDataObject(obj[1])
  else:
        vtkPoly = Repository.ExportToVtk(obj)
        lmap[1].SetInputDataObject(vtkPoly)
  lmap[1].SetLabelFormat("%g")
  
  labels[1] = vtk.vtkActor2D()
  labels[1].SetMapper(lmap[1])
  ren[1].AddActor2D(labels[1])
  vis.renfun.render(ren)
  
  setattr(vis,lmap[0],lmap)
  setattr(vis,labels[0],labels)
  return   

# ----------------------
# ::vis::polyShowCellIds
# ----------------------
def polyShowCellIds(ren,obj):

  #@c Show the cell ids of a given poly object in a renderer
  #@a ren: renderer
  #@a obj: object name
  if isinstance(obj,list):
      tag = "%s_%s" % (ren[0],obj[0])
  elif isinstance(obj,str):
      tag = "%s_%s" % (ren[0],obj)
  else:
      raise ValueError("Argument type unsupported.")
  
  try:
      vis.poly.polyUnshowCellIds(ren,obj)
  except:
      pass
    
  lmap = [None]*2
  lmap[0] = "p_lmapc_"+tag
  labels = [None]*2
  labels[0] = "p_labelsc_"+tag  
  ids = [None]*2
  ids[0] = "p_cellids_"+tag
  
  filt = vtk.vtkCellCenters()
  if isinstance(obj,list):
        filt.SetInputDataObject(obj[1])
  else:
        vtkPoly = Repository.ExportToVtk(obj)
        filt.SetInputDataObject(vtkPoly)
  filt.Update()
  ids[1] = filt.GetOutput()
  
  lmap[1] = vtk.vtkLabeledDataMapper()
  lmap[1].SetLabelModeToLabelIds()
  lmap[1].SetInputDataObject(ids[1])
  lmap[1].SetLabelFormat("%g")
  labels[1] = vtk.vtkActor2D()
  labels[1].SetMapper(lmap[1])
  ren[1].AddActor2D(labels[1])
  
  vis.renfun.render(ren)
  setattr(vis,lmap[0],lmap)
  setattr(vis,labels[0],labels)
  return 


# ---------------------------
# ::vis::polyShowScalarValues
# ---------------------------
def polyShowScalarValues(ren,obj):

  #@c Show the scalar values for object in renderer
  #@a ren: renderer
  #@a obj: object name
  if isinstance(obj,list):
      tag = "%s_%s" % (ren[0],obj[0])
  elif isinstance(obj,str):
      tag = "%s_%s" % (ren[0],obj)
  else:
      raise ValueError("Argument type unsupported.")
  
  try:
      vis.poly.polyUnshowScalarValues(ren,obj)
  except:
      pass
      
  lmap = [None]*2
  lmap[0] = "p_lmap_"+tag
  labels = [None]*2
  labels[0] = "p_labels_"+tag  
  
  lmap[1] = vtk.vtkLabeledDataMapper()
  lmap[1].SetLabelModeToLabelScalars()
  if isinstance(obj,list):
        lmap[1].SetInputDataObject(obj[1])
  else:
        vtkPoly = Repository.ExportToVtk(obj)
        lmap[1].SetInputDataObject(vtkPoly)
  lmap[1].SetLabelFormat("%g")
  
  labels[1] = vtk.vtkActor2D()
  labels[1].SetMapper(lmap[1])
  ren[1].AddActor2D(labels[1])
  
  vis.renfun.render(ren)
  setattr(vis,lmap[0],lmap)
  setattr(vis,labels[0],labels)
  return


# --------------------
# ::vis::polyUnshowIds
# --------------------
def polyUnshowIds(ren,obj):
    #@c Remove the point ids from the poly in renderer
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    
    lmap = getattr(vis,"p_lmap_"+tag)
    labels = getattr(vis,"p_labels_"+tag)
    
    if (ren[1].GetActors2D().IsItemPresent(labels[1])>0):
        ren[1].RemoveActor2D(labels[1])
        
    vis.renfun.render(ren)
    setattr(vis,lmap[0],lmap)
    setattr(vis,labels[0],labels)
    return
    

# ------------------------
# ::vis::polyUnshowCellIds
# ------------------------
def polyUnshowCellIds(ren,obj):
  #@c Remove the cell ids from the poly in renderer
  #@a ren: renderer
  #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    
    lmap = getattr(vis,"p_lmapc_"+tag)
    labels = getattr(vis,"p_labelsc_"+tag)
  
    if (ren[1].GetActors2D().IsItemPresent(labels[1])>0):
        ren[1].RemoveActor2D(labels[1])
    
    vis.renfun.render(ren)
    setattr(vis,lmap[0],lmap)
    setattr(vis,labels[0],labels)
    return


# -----------------------------
# ::vis::polyUnshowScalarValues
# -----------------------------
def polyUnshowScalarValues(ren,obj):
    
  #@c Remove the scalar values of object from renderer
  #@a ren: renderer
  #@a obj: object name
    vis.poly.polyUnshowIds(ren,obj)
    return



# ---------------------------
# ::vis::polyDisplayWireframe
# ---------------------------
def polyDisplayWireframe(ren,obj):
    #@c Display object as wireframe
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    actor = getattr(vis, "p_act_"+tag)
    
    actor[1].GetProperty().SetRepresentationToWireframe()
    vis.renfun.render(ren)
    return



# ------------------------
# ::vis::polyDisplayPoints
# ------------------------
def polyDisplayPoints(ren,obj):
    #@c Display object as points
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
        
    actor = getattr(vis, "p_act_"+tag)
    
    actor[1].GetProperty().SetRepresentationToPoints()

    vis.renfun.render(ren)
    return

# -------------------------
# ::vis::polyDisplaySurface
# -------------------------
def polyDisplaySurface(ren,obj):

    #@c Display object as surface
    #@a ren: renderer
    #@a obj: object name
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    actor = getattr(vis, "p_act_"+tag)
    
    actor[1].GetProperty().SetRepresentationToSurface()
    
    vis.renfun.render(ren)
    return


# -------------------------
# ::vis::polyGetScalarRange
# -------------------------
def polyGetTableRange(ren,obj):
    
    #@c Get the scalar range
    #@a ren: renderer
    #@a obj: image object
    
    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    mapper = getattr(vis,"p_map_"+tag)

    return mapper[1].GetScalarRange()


# -------------------------
# ::vis::polySetScalarRange
# -------------------------
def polySetScalarRange(ren,Min,Max,obj):
    
    #@c Set the scalar range
    #@a ren:  renderer
    #@a obj: image object
    #@a min: minimum value
    #@a max: maximum value
    if (Min>=Max):
        return

    if isinstance(obj,list):
        tag = "%s_%s" % (ren[0],obj[0])
    elif isinstance(obj,str):
        tag = "%s_%s" % (ren[0],obj)
    else:
        raise ValueError("Argument type unsupported.")
    mapper = getattr(vis,"p_map_"+tag)
    
    mapper[1].SetScalarRange(Min,Max)
    return
    
