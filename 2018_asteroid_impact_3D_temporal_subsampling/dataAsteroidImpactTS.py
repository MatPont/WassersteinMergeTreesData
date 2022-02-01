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
import pandas as pd

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XML Image Data Reader'
def generate(fileName, metaData):
    pv_insitu = XMLImageDataReader(FileName=[fileName])
    pv_insitu.CellArrayStatus = ['vtkGhostType']
    pv_insitu.PointArrayStatus = ['prs', 'tev', 'v02', 'v03', 'vtkValidPointMask', 'vtkGhostType']
    scalar = 'tev'

    # create a new 'Calculator'
    calculator2 = Calculator(Input=pv_insitu)
    calculator2.ResultArrayName = 'scalar'
    calculator2.Function = 'tev+v02+v03'
    scalar = 'scalar'
    pv_insitu = calculator2

    # create a new 'TTK ScalarFieldSmoother'
    tTKScalarFieldSmoother1 = TTKScalarFieldSmoother(Input=pv_insitu)
    tTKScalarFieldSmoother1.ScalarField = scalar
    
    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tTKScalarFieldSmoother1, Source=None)
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
  
  timeSteps = ["01141", "03429", "05700", "07920", "09782", "13306", "16317", "18124", "19599", "21255", "28649", "31737", "34654", "37273", "39476", "44229", "45793", "47190", "48557", "49978"]
  clusterID = [0] * 5 + [1] * 5 + [2] * 5 + [3] * 5
  
  data = []
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    
    metaData = {}
    metaData["TimeStep"] = timeSteps[i]
    metaData["RunName"] = "yA31"
    metaData["ClusterID"] = clusterID[i]
    metaData["Dim."] = "3D"
    metaData["Generation"] = "Simulation"
    
    res = generate("./nonProcessed/"+myFile, metaData)
    
    ext = ".vtu"
    outFileName = "./processed/"+myFile[:-4]+ext
    XMLUnstructuredGridWriter(FileName=outFileName, Input=res).UpdatePipeline()
    
    data.append([outFileName, metaData["TimeStep"], metaData["RunName"], metaData["ClusterID"], metaData["Dim."], metaData["Generation"]])
    
  df = pd.DataFrame(data, columns = ["FILE", "TimeStep", "RunName", "ClusterID", "Dim.", "Generation"])
  df.to_csv("data.csv", index=None)
    
# ----------------------------------------------------------------

if __name__ == "__main__":
    processDataset()

