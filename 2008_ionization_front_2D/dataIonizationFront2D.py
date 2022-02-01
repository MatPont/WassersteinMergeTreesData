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
import pandas as pd

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

def generate(fileName, metaData):
    # create a new 'Legacy VTK Reader'
    multifield0 = LegacyVTKReader(FileNames=[fileName])

    # create a new 'Resample To Image'
    resampleToImage1 = ResampleToImage(Input=multifield0)
    resampleToImage1.SamplingDimensions = [600, 248, 1]
    #resampleToImage1.SamplingDimensions = [300, 124, 124]
    resampleToImage1.UseInputBounds = 1

    # create a new 'TTK ScalarFieldNormalizer'
    tTKScalarFieldNormalizer1 = TTKScalarFieldNormalizer(Input=resampleToImage1)
    tTKScalarFieldNormalizer1.ScalarField = 'density'

    # create a new 'Tetrahedralize'
    tetrahedralize1 = Tetrahedralize(Input=tTKScalarFieldNormalizer1)

    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tetrahedralize1, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #TKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', 'density']
    
    res = tTKArrayEditor1
    
    return res
    
def processDataset():
  allFiles = os.listdir("./nonProcessed/")
  allFiles.sort()
  
  timeSteps = ["0025", "0026", "0027", "0028", "0075", "0076", "0077", "0078", "0125", "0126", "0127", "0128", "0175", "0176", "0177", "0178"]
  clusterID = [0] * 4 + [1] * 4 + [2] * 4 + [3] * 4
  
  data = []
  
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
    
    data.append([outFileName, metaData["TimeStep"], metaData["ClusterID"], metaData["Dim."], metaData["Generation"]])
    
  df = pd.DataFrame(data, columns = ["FILE", "TimeStep", "ClusterID", "Dim.", "Generation"])
  df.to_csv("data.csv", index=None)
    
# ----------------------------------------------------------------

if __name__ == "__main__":
    processDataset()

