#import os
#import math
import ctypes
import sys

if sys.platform == "darwin":
    ext = "dylib"
elif sys.platform == "linux2":
    ext = "so"
elif sys.platform == "win32" or sys.platform =="cygwin":
    ext = "dll"
else:
    raise ValueError("System unrecognized")

if sys.version_info < (3,0):
    myDll=ctypes.PyDLL('lib_simvascular_solid.' + ext)
    myDll.initpySolid()
    import pySolid as Solid
    myDll=ctypes.PyDLL('lib_simvascular_polydata_solid.' + ext)
    myDll.initpySolidPolydata()
    import pySolidPolydata as SolidPolyData
    myDll=ctypes.PyDLL('lib_simvascular_repository.' + ext)
    myDll.initpyRepository()
    import pyRepository as Repository
    myDll=ctypes.PyDLL('lib_simvascular_mesh.' + ext)
    myDll.initpyMeshObject()
    import pyMeshObject as MeshObject
    myDll=ctypes.PyDLL('lib_simvascular_tetgen_mesh.' + ext)
    myDll.initpyMeshTetgen()
    import pyMeshTetgen as MeshTetGen
    myDLL=ctypes.PyDLL('lib_simvascular_utils.' + ext)
    myDLL.initpyMath()
    import pyMath as Math
    myDll=ctypes.PyDLL('lib_simvascular_segmentation.' + ext)
    myDll.initpyContour()
    myDll.initpyThresholdContour()
    myDll.initpylevelSetContour()
    myDll.initpyPolygonContour()
    myDll.initpyCircleContour()
    myDll.initpySplinePolygonContour()
    import pyContour as Contour
    import pyThresholdContour as ThresholdContour
    import pylevelSetContour as LevelSetContour
    import pyCircleContour as CircleContour
    import pyPolygonContour as PolygonContour
    import pySplinePolygonContour as SplinePolygonContour
    myDll=ctypes.PyDLL('lib_simvascular_vmtk_utils.' + ext)
    myDll.initpyVMTKUtils()
    import pyVMTKUtils as VMTKUtils
    myDll=ctypes.PyDLL('lib_simvascular_opencascade_solid.' + ext)
    myDll.initpySolidOCCT()
    import pySolidOCCT as SolidOCCT
    myDll=ctypes.PyDLL('lib_simvascular_mmg_mesh.' + ext)
    myDll.initpyMeshUtil()
    import pyMeshUtil as MeshUtil
    myDll=ctypes.PyDLL('lib_simvascular_itk_lset.' + ext)
    myDll.initpyItkls()
    import pyItkls as Itkls
    myDll=ctypes.PyDLL('lib_simvascular_adaptor.' + ext)
    myDll.initpyMeshAdapt()
    import pyMeshAdapt as MeshAdapt
    myDll=ctypes.PyDLL('lib_simvascular_tetgen_adaptor.' + ext)
    myDll.initpyTetGenAdapt()
    import pyTetGenAdapt as TetGenAdapt
    myDll=ctypes.PyDLL('lib_simvascular_geom.' + ext)
    myDll.initpyGeom()
    import pyGeom as Geom
    myDll=ctypes.PyDLL('lib_simvascular_image.' + ext)
    myDll.initpyImage()
    import pyImage as Image
    myDll=ctypes.PyDLL('lib_simvascular_path.' + ext)
    myDll.initpyPath()
    import pyPath as Path
    myDll=ctypes.PyDLL('liborg_sv_pythondatanodes.' + ext)
    myDll.initpyGUI()
    import pyGUI as GUI
else:
    myDll=ctypes.PyDLL('lib_simvascular_solid.' + ext)
    func=myDll.PyInit_pySolid
    func.restype = ctypes.py_object
    Solid = func()
    myDll=ctypes.PyDLL('lib_simvascular_polydata_solid.' + ext)
    func=myDll.PyInit_pySolidPolydata
    func.restype = ctypes.py_object
    SolidPolyData=func()
    myDll=ctypes.PyDLL('lib_simvascular_repository.' + ext)
    func=myDll.PyInit_pyRepository
    func.restype = ctypes.py_object
    Repository=func()
    myDll=ctypes.PyDLL('lib_simvascular_mesh.' + ext)
    func=myDll.PyInit_pyMeshObject
    func.restype = ctypes.py_object
    MeshObject=func()
    myDll=ctypes.PyDLL('lib_simvascular_tetgen_mesh.' + ext)
    func=myDll.PyInit_pyMeshTetgen
    func.restype = ctypes.py_object
    MeshTetgen=func()
    myDLL=ctypes.PyDLL('lib_simvascular_utils.' + ext)
    func=myDLL.PyInit_pyMath
    func.restype = ctypes.py_object
    Math=func()
    myDll=ctypes.PyDLL('lib_simvascular_segmentation.' + ext)
    func=myDll.PyInit_pyContour
    func.restype = ctypes.py_object
    Contour=func()
    func=myDll.PyInit_pyThresholdContour
    func.restype = ctypes.py_object
    ThresholdContour=func()
    func=myDll.PyInit_pylevelSetContour
    func.restype = ctypes.py_object
    LevelSetContour=func()
    func=myDll.PyInit_pyPolygonContour
    func.restype = ctypes.py_object
    PolygonContour=func()
    func=myDll.PyInit_pyCircleContour
    func.restype = ctypes.py_object
    CircleContour=func()
    func=myDll.PyInit_pySplinePolygonContour
    func.restype = ctypes.py_object
    SplinePolygonContour=func()
    myDll=ctypes.PyDLL('lib_simvascular_vmtk_utils.' + ext)
    func=myDll.PyInit_pyVMTKUtils
    func.restype = ctypes.py_object
    VMTKUtils=func()
    myDll=ctypes.PyDLL('lib_simvascular_opencascade_solid.' + ext)
    func=myDll.PyInit_pySolidOCCT
    func.restype = ctypes.py_object
    SolidOCCT=func()
    myDll=ctypes.PyDLL('lib_simvascular_mmg_mesh.' + ext)
    func=myDll.PyInit_pyMeshUtil
    func.restype = ctypes.py_object
    MeshUtil=func()
    myDll=ctypes.PyDLL('lib_simvascular_itk_lset.' + ext)
    func=myDll.PyInit_pyItkls
    func.restype = ctypes.py_object
    Itkls=func()
    myDll=ctypes.PyDLL('lib_simvascular_adaptor.' + ext)
    func=myDll.PyInit_pyMeshAdapt
    func.restype = ctypes.py_object
    MeshAdapt=func()
    myDll=ctypes.PyDLL('lib_simvascular_tetgen_adaptor.' + ext)
    func=myDll.PyInit_pyTetGenAdapt
    func.restype = ctypes.py_object
    TetGenAdapt=func()
    myDll=ctypes.PyDLL('lib_simvascular_geom.' + ext)
    func=myDll.PyInit_pyGeom
    func.restype = ctypes.py_object
    Geom=func()
    myDll=ctypes.PyDLL('lib_simvascular_image.' + ext)
    func=myDll.PyInit_pyImage
    func.restype = ctypes.py_object
    Image=func()
    myDll=ctypes.PyDLL('lib_simvascular_path.' + ext)
    func=myDll.PyInit_pyPath
    func.restype = ctypes.py_object
    Path=func()
    myDll=ctypes.PyDLL('liborg_sv_pythondatanodes.' + ext)
    func=myDll.PyInit_pyGUI
    func.restype = ctypes.py_object
    GUI=func()

    

