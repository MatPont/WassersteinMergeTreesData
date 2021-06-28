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
import sys
import os

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

def generate(fileName, metaData):
    cloud0vtu = XMLUnstructuredGridReader(FileName=[fileName])
    cloud0vtu.PointArrayStatus = ['ccb']

    """# create a new 'Cell Data to Point Data'
    cellDatatoPointData1 = CellDatatoPointData(Input=cloud0vtu)
    cellDatatoPointData1.ProcessAllArrays = 0
    cellDatatoPointData1.CellDataArraytoprocess = ['ccb']

    # create a new 'Tetrahedralize'
    tetrahedralize1 = Tetrahedralize(Input=cellDatatoPointData1)

    # create a new 'TTK ScalarFieldSmoother'
    tTKScalarFieldSmoother1 = TTKScalarFieldSmoother(Input=tetrahedralize1)
    tTKScalarFieldSmoother1.ScalarField = 'ccb'
    tTKScalarFieldSmoother1.IterationNumber = 10"""
    
    tTKScalarFieldSmoother1 = cloud0vtu
    
    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tTKScalarFieldSmoother1, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #tTKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', 'ccb']
    
    res = tTKArrayEditor1
    
    return res
    
def processDataset():
  allFiles = os.listdir("./nonProcessed/")
  allFiles.sort()
  
  timeSteps = ["0", "5", "10", "15", "500", "505", "510", "515", "1000", "1005", "1010", "1015"]
  clusterID = [0] * 4 + [1] * 4 + [2] * 4
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    
    metaData = {}
    metaData["TimeStep"] = timeSteps[i]
    metaData["ClusterID"] = clusterID[i]
    metaData["Dim."] = "2D"
    metaData["Generation"] = "Simulation"
    
    res = generate("./nonProcessed/"+myFile, metaData)
    
    ext = ".vtu"
    outFileName = "./processed/"+myFile[:-4]+ext
    XMLUnstructuredGridWriter(FileName=outFileName, Input=res).UpdatePipeline()
    
# ----------------------------------------------------------------

if __name__ == "__main__":
    processDataset()

