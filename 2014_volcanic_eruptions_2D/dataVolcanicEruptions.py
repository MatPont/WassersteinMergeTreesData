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
import sys
import pandas as pd

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------
def generate(fileName, metaData):
    # create a new 'Legacy VTK Reader'
    volcano_2011_150_amvtk = LegacyVTKReader(FileNames=[fileName])
    
    sm = servermanager.Fetch(volcano_2011_150_amvtk)

    # create a new 'Resample To Image'
    resampleToImage1 = ResampleToImage(Input=volcano_2011_150_amvtk)
    resampleToImage1.SamplingDimensions = [500, 500, 1]
    resampleToImage1.UseInputBounds = 1

    # create a new 'Tetrahedralize'
    tetrahedralize2 = Tetrahedralize(Input=resampleToImage1)

    # create a new 'Warp By Scalar'
    warpByScalar1 = WarpByScalar(Input=tetrahedralize2)
    warpByScalar1.Scalars = ['POINTS', 'SO2']
    warpByScalar1.ScaleFactor = 10.0

    # create a new 'Tetrahedralize'
    tetrahedralize1 = Tetrahedralize(Input=warpByScalar1)

    # create a new 'TTK PersistenceDiagram'
    tTKPersistenceDiagram1 = TTKPersistenceDiagram(Input=tetrahedralize1)
    tTKPersistenceDiagram1.ScalarField = 'SO2'
    tTKPersistenceDiagram1.InputOffsetField = 'SO2'

    # create a new 'Threshold'
    threshold1 = Threshold(Input=tTKPersistenceDiagram1)
    threshold1.Scalars = ['CELLS', 'Persistence']
    threshold1.ThresholdRange = [0.5, 9999999.0]

    # create a new 'TTK TopologicalSimplification'
    tTKTopologicalSimplification1 = TTKTopologicalSimplification(Domain=tetrahedralize1,
        Constraints=threshold1)
    tTKTopologicalSimplification1.ScalarField = 'SO2'
    tTKTopologicalSimplification1.InputOffsetField = 'SO2'
    tTKTopologicalSimplification1.Vertexidentifierfield = 'CriticalType'
    tTKTopologicalSimplification1.OutputOffsetScalarField = ''

    # create a new 'TTK ArrayEditor'
    tTKArrayEditor1 = TTKArrayEditor(Target=tTKTopologicalSimplification1, Source=None)
    tTKArrayEditor1.TargetAttribute = 'Field Data'
    #tTKArrayEditor1.DataString = """ClusterID, 0
#myTest, 54"""
    metaDataString = ''.join([str(k)+","+str(metaData[k])+"\n" for k in metaData.keys()])
    tTKArrayEditor1.DataString = metaDataString
    tTKArrayEditor1.TargetArray = ['POINTS', 'SO2']
    
    res = tTKArrayEditor1

    return res
    
def processDataset():
  allFiles = os.listdir("./nonProcessed/")
  allFiles.sort()
  
  timeSteps = ["150_am", "150_pm", "151_am", "151_pm", "156_am", "156_pm", "157_am", "157_pm", "164_am", "164_pm", "165_am", "165_pm"]
  clusterID = [0] * 4 + [1] * 4 + [2] * 4
  
  data = []
  
  for i, myFile in enumerate(allFiles):
    print(i, "/", len(allFiles), ":", myFile)
    
    metaData = {}
    metaData["TimeStep"] = timeSteps[i]
    metaData["ClusterID"] = clusterID[i]
    metaData["Modality"] = "AIRS"
    metaData["Dim."] = "2D"
    metaData["Generation"] = "Acquired"
    
    res = generate("./nonProcessed/"+myFile, metaData)
    
    ext = ".vtu"
    outFileName = "./processed/"+myFile[:-4]+ext
    XMLUnstructuredGridWriter(FileName=outFileName, Input=res).UpdatePipeline()
    
    data.append([outFileName, metaData["TimeStep"], metaData["ClusterID"], metaData["Modality"], metaData["Dim."], metaData["Generation"]])
    
  df = pd.DataFrame(data, columns = ["FILE", "TimeStep", "ClusterID", "Modality", "Dim.", "Generation"])
  df.to_csv("data.csv", index=None)
    
# ----------------------------------------------------------------

if __name__ == "__main__":
    processDataset()

