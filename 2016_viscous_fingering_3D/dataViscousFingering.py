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
    # create a new 'XML Unstructured Grid Reader'
    a025vtu = XMLUnstructuredGridReader(FileName=[fileName])
    a025vtu.PointArrayStatus = ['concentration', 'velocity']

    # create a new 'Gaussian Resampling'
    gaussianResampling1 = GaussianResampling(Input=a025vtu)
    gaussianResampling1.ResampleField = ['POINTS', 'concentration']
    gaussianResampling1.SplatAccumulationMode = 'Sum'

    # create a new 'Tetrahedralize'
    tetrahedralize1 = Tetrahedralize(Input=gaussianResampling1)
    
    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tetrahedralize1, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #tTKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', 'concentration']
    
    res = tTKArrayEditor1
    
    return res    
  
def processDataset():
  allFiles = os.listdir("./nonProcessed/")
  allFiles.sort()
  
  runNames = ["0.22"] * 5 + ["0.33"] * 5 + ["0.44"] * 5
  runIDs = ["01", "03", "04", "05", "06"] + ["01", "02", "03", "04", "05"] * 2
  clusterID = [0] * 5 + [1] * 5 + [3] * 5
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    
    metaData = {}
    metaData["TimeStep"] = "120"
    metaData["RunName"] = runNames[i]
    metaData["RunID"] = runIDs[i]
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

