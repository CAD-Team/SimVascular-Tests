import vis
import vtk
# -------------------
# ::vis::deleteWindow
# -------------------
def deleteWindow(window, ren):
    
  #@c Delete window displaying single renderer
  #@a window: window to be destroyed
  #@a ren: renderer to be destroyed

  # clear all displayed objects
  vis.img.imgRmAll(ren)
  vis.poly.polyRmAll(ren)
  vis.actor.actorRmAll(ren)

  # delete generic interactors
  try:
      delattr(vis, "genericInteractor_"+ren[0])
      delattr(vis, "genericInteractorStyle_"+ren[0])
  except:
      print("No genericInteractor or genericInteractorStyle found")
      
  del window
  del ren


# ---------------
# ::vis::initTKgr
# ---------------
#Initialize the vtk render window
def initRen(title):
    renId = 1
    renWin = [None]*2
    renWin[0] = title
    renWin[1] = vtk.vtkRenderWindow()
    
    ren = [None]*2
    ren[0] = "%s_ren%d" % (renWin[0], renId)
    ren[1] = vtk.vtkRenderer()
    renWin[1].AddRenderer(ren[1])
    ren[1].SetBackground(0,0,0)
    
    
    # add generic interactors
    try:
      delattr(vis, "genericInteractor_"+ren[0])
      delattr(vis, "genericInteractorStyle_"+ren[0])
    except:
      pass
      
    genericInteractor = [None]*2
    genericInteractorStyle = [None]*2
    
    genericInteractor[0] =  "iren_"+ren[0]
    genericInteractorStyle[0] = "irenStyle_"+ren[0]
    
    genericInteractor[1] = vtk.vtkRenderWindowInteractor()
    genericInteractorStyle[1] = vtk.vtkInteractorStyleSwitch()
    
    genericInteractorStyle[1].SetCurrentStyleToTrackballCamera()
    genericInteractor[1].SetInteractorStyle(genericInteractorStyle[1])
    
    genericInteractor[1].SetRenderWindow(renWin[1])
    
    setattr(vis, ren[0],ren)
    setattr(vis, renWin[0],renWin)
    setattr(vis, genericInteractor[0], genericInteractor)
    setattr(vis, genericInteractorStyle[0], genericInteractorStyle)

    return ren

    
    


#proc ::vis::deletePickedActor {ren} {
#
#  #@author Nathan Wilson
#  #@c Deletes the currently selected actor from the renderer
#  #@a ren: renderer
#
#  ::vis::tkDeselectPickedActor
#  ::vis::actorRm $::vis::tkvars(PickedAssemblyRenderer) $::vis::tkvars(PickedAssembly)
#
#}