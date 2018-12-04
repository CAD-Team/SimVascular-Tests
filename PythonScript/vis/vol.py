import vis
import vtk
import Repository

# ------------
# vis_volRepos
# ------------
def vis_volRepos(ren, objName):
    if Repository.Exists(objName)==0:
        raise ValueError("ERROR:  Object does not exist.")
        return
    if Repository.Type(objName) != "StructuredPts":
        raise TypeError("Incorrect object type.")
        return
    caster = [None]*2
    opacityTransferFunction = [None]*2
    colorTransferFunction = [None]*2
    gradientTransferFunction = [None]*2
    volumeProperty = [None]*2
    volumeMapper = [None]*2
    compositeFunction = [None]*2
    outline = [None]*2
    outlineMapper = [None]*2
    outlineProperty = [None]*2
    lod = [None]*2
    
    caster[0] = "vis_vol_caster_"+objName
    opacityTransferFunction[0] = "vis_vol_opacityTransferFunction_"+objName
    colorTransferFunction[0] = "vis_vol_colorTransferFunction_"+objName
    gradientTransferFunction[0] = "vis_vol_gradientTransferFunction_"+objName
    volumeProperty[0] = "vis_vol_volumeProperty_"+objName
    volumeMapper[0] = "vis_vol_volumeMapper_"+objName
    compositeFunction[0] = "vis_vol_compositeFunction_"+objName
    outline[0] = "vis_vol_outline_"+objName
    outlineMapper[0] = "vis_vol_outlineMapper_"+objName
    outlineProperty[0] = "vis_vol_outlineProperty_"+objName
    lod[0] = "vis_vol_lod_" + objName
    
    caster[1] = vtk.vtkImageCast()
    caster[1].SetOutputScalarTypeToUnsignedShort()
    caster[1].SetInputDataObject(Repository.ExportToVtk(objName))
    caster[1].Update()
    
    # Create transfer functions for opacity and color
    opacityTransferFunction[1] = vtk.vtkPiecewiseFunction()
    opacityTransferFunction[1].AddPoint(0,0.)
    opacityTransferFunction[1].AddPoint(80,0.)
    opacityTransferFunction[1].AddPoint(128,0.5)
    opacityTransferFunction[1].AddPoint(150,0.9)
    opacityTransferFunction[1].AddPoint(350,1.0)
    
    colorTransferFunction[1] = vtk.vtkColorTransferFunction()
    colorTransferFunction[1].AddRGBPoint(0,0,0,0)
    colorTransferFunction[1].AddRGBPoint(350,1,1,1)
    
    gradientTransferFunction[1] = vtk.vtkPiecewiseFunction()
    gradientTransferFunction[1].AddPoint(0,1.0)
    gradientTransferFunction[1].AddPoint(1,1.0)
    gradientTransferFunction[1].AddPoint(255,1.0)
    gradientTransferFunction[1].AddPoint(512,1.0)
    
    # Create properties, mappers, volume actors, and ray cast function
    volumeProperty[1] = vtk.vtkVolumeProperty()
    volumeProperty[1].SetColor(colorTransferFunction[1])
    volumeProperty[1].SetScalarOpacity(opacityTransferFunction[1])
    volumeProperty[1].SetGradientOpacity(gradientTransferFunction[1])
    volumeProperty[1].SetInterpolationTypeToLinear()
    
    volumeMapper[1] = vtk.vtkSmartVolumeMapper()
    volumeMapper[1].SetInputDataObject(caster[1].GetOutput())
    
    lod[1] = vtk.vtkVolume()
    lod[1].SetProperty(volumeProperty[1])
    lod[1].SetMapper(volumeMapper[1])
    
    ren[1].AddViewProp(lod[1])
    
    setattr(vis, caster[0], caster)
    setattr(vis, opacityTransferFunction[0], opacityTransferFunction)
    setattr(vis, colorTransferFunction[0], colorTransferFunction)
    setattr(vis, gradientTransferFunction[0], gradientTransferFunction)
    setattr(vis, volumeProperty[0], volumeProperty)
    setattr(vis, volumeMapper[0], volumeMapper)
    setattr(vis, compositeFunction[0], compositeFunction)
    setattr(vis, outline[0], outline)
    setattr(vis, outlineMapper[0], outlineMapper)
    setattr(vis, outlineProperty[0], outlineProperty)
    setattr(vis, lod[0], lod)
    vis.renfun.render(ren)
    return lod
    
# ---------
# vis_volRm
# ---------
def vis_volRm(ren, objName):
    
    caster = getattr(vis, 'vis_vol_caster_'+objName)
    opacityTransferFunction = getattr(vis, 'vis_vol_opacityTransferFunction_'+objName)
    colorTransferFunction = getattr(vis, 'vis_vol_colorTransferFunction_'+objName)
    gradientTransferFunction = getattr(vis, 'vis_vol_gradientTransferFunction_'+objName)
    volumeProperty = getattr(vis, 'vis_vol_volumeProperty_'+objName)
    volumeMapper = getattr(vis, 'vis_vol_volumeMapper_'+objName)
    compositeFunction = getattr(vis, 'vis_vol_compositeFunction_'+objName)
    outline = getattr(vis, 'vis_vol_outline_'+objName)
    outlineMapper = getattr(vis, 'vis_vol_outlineMapper_'+objName)
    outlineProperty = getattr(vis, 'vis_vol_outlineProperty_'+objName)
    lod = getattr(vis, 'vis_vol_lod_'+objName)
    
    if (ren[1].GetViewProps().IsItemPresent(lod[1])>0):
        ren[1].RemoveViewProp(lod[1])
        delattr(vis,caster[0])
        delattr(vis,opacityTransferFunction[0])
        delattr(vis,colorTransferFunction[0])
        delattr(vis,gradientTransferFunction[0])
        delattr(vis,volumeProperty[0])
        delattr(vis,volumeMapper[0])
        delattr(vis,compositeFunction[0])
        delattr(vis,outline[0])
        delattr(vis,outlineMapper[0])
        delattr(vis,outlineProperty[0])
    vis.renfun.render(ren)
    
    return
    
    
# ---------------------------------
# vis_volSetOpacityTransferFunction
# ---------------------------------
def vis_volSetOpacityTransferFunction(ren, objName, values):
    #@c Change opacity transfer function.
    #@a ren: Render Window.
    #@a objName:  Repository StructuredPoints object.
    #@a values: Python n by 2 list of scalar - opacity pairs.
  
    lod = getattr(vis, 'vis_vol_lod_'+objName)
    opacityTransferFunction = getattr(vis, 'vis_vol_opacityTransferFunction_'+objName)
    
    opacityTransferFunction.RemoveAllPoints()
    opacityTransferFunction.PrepareForNewData()
    
    if len(values)==0:
        return
        
    for i in range (0, len(values)):
        if len(values[i])!=2:
            print("Warning:  incorrect scalar-opacity pair %i. Ignored." %i)
        else:
            opacityTransferFunction.AddPoint(values[i][0], values[i][1])
    
    vis.renfun.render(ren)
    return

