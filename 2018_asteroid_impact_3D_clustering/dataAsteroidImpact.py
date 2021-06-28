# state file generated using paraview version 5.7.0

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# trace generated using paraview version 5.7.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
import os

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XML Image Data Reader'
def generate(fileName, metaData):
    pv_insitu = XMLImageDataReader(FileName=[fileName])
    pv_insitu.CellArrayStatus = ['vtkGhostType']
    pv_insitu.PointArrayStatus = ['prs', 'tev', 'v02', 'v03', 'vtkValidPointMask', 'vtkGhostType']
    scalar = 'tev'
    
    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=pv_insitu, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #tTKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', scalar]
    
    res = tTKArrayEditor1

    return res

def processDataset():
  allFiles = os.listdir("./nonProcessed/")
  allFiles.sort()
  
  timeSteps = ["34883", "49978", "220062", "37894", "46521", "30975", "48663"]
  runNames = ["yA11", "yA31", "yA32", "yB11", "yB31", "yC11", "yC31"]
  clusterID = [0, 1, 1, 0, 1, 0, 1] # third character of runName (1 or 3)
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    
    metaData = {}
    metaData["TimeStep"] = timeSteps[i]
    metaData["RunName"] = runNames[i]
    metaData["ClusterID"] = clusterID[i]
    metaData["Dim."] = "3D"
    metaData["Generation"] = "Simulation"
    
    res = generate("./nonProcessed/"+myFile, metaData)
    
    ext = ".vtu"
    outFileName = "./processed/"+myFile[:-4]+ext
    XMLUnstructuredGridWriter(FileName=outFileName, Input=res).UpdatePipeline()
    
# ----------------------------------------------------------------

if __name__ == "__main__":
    processDataset()

