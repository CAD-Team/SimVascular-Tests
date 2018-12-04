import vtk
import vis
def actorRM(ren, actor):
    if(ren[1].GetActors().IsItemPresent(actor[1])):
        ren[1].RemoveActor(actor[1])
    vis.renfun.render(ren)
    return
    
def actor2DRm(ren, actor):
    if(ren[1].GetActors2D().IsItemPresent(actor[1])):
        ren[1].RemoveActor2D(actor[1])
    vis.renfun.render(ren)
    return
    
def actorRmAll(ren):
    actorAll = ren[1].GetActors()
    for i in range(0,actorAll.GetNumberOfItems()):
        ren[1].RemoveActor2D(actorAll.GetNextActor())
    vis.renfun.render(ren)
    return