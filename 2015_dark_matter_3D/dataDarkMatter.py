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
    # create a new 'XML PolyData Reader'
    ds14_scivis_0128_e4_dt04_0 = XMLPolyDataReader(FileName=[fileName])
    ds14_scivis_0128_e4_dt04_0.PointArrayStatus = ['DarkMatter_Phi']

    # create a new 'Gaussian Resampling'
    gaussianResampling2 = GaussianResampling(Input=ds14_scivis_0128_e4_dt04_0)
    gaussianResampling2.ResampleField = ['POINTS', 'DarkMatter_Phi']
    gaussianResampling2.ResamplingGrid = [100, 100, 100] #[200, 200, 200]
    gaussianResampling2.GaussianSplatRadius = 0.01
    gaussianResampling2.ScaleSplats = 0
    gaussianResampling2.EllipticalSplats = 0
    gaussianResampling2.FillVolumeBoundary = 0
    gaussianResampling2.FillValue = 1.0
    gaussianResampling2.SplatAccumulationMode = 'Sum'

    # create a new 'TTK ScalarFieldSmoother'
    tTKScalarFieldSmoother1 = TTKScalarFieldSmoother(Input=gaussianResampling2)
    tTKScalarFieldSmoother1.ScalarField = 'SplatterValues'

    # create a new 'Tetrahedralize'
    tetrahedralize1 = Tetrahedralize(Input=tTKScalarFieldSmoother1)
    
    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tetrahedralize1, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #tTKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', 'DarkMatter_Phi']
    
    res = tTKArrayEditor1
    
    return res
    
def processDataset():
  allFiles = os.listdir("./nonProcessed/")
  allFiles.sort()
  
  timeSteps = ["0.0200", "0.0300", "0.0400", "0.0500", "0.0600", "0.0700", "0.0800", "0.0900", "0.1000", "0.1100", "0.2700", "0.2800", "0.2900", "0.3000", "0.3100", "0.3200", "0.3300", "0.3400", "0.3500", "0.3600", "0.5900", "0.6000", "0.6100", "0.6200", "0.6300", "0.6400", "0.6500", "0.6600", "0.6700", "0.6800", "0.9100", "0.9200", "0.9300", "0.9400", "0.9500", "0.9600", "0.9700", "0.9800", "0.9900", "1.0000"]
  clusterID = [0] * 10 + [1] * 10 + [2] * 10 + [3] * 10
  
  data = []
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    
    metaData = {}
    metaData["TimeStep"] = timeSteps[i]
    metaData["ClusterID"] = clusterID[i]
    metaData["Dim."] = "3D"
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

