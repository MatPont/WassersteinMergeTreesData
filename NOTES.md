# (2018) Asteroid Impact (3D) 
Extents=[300, 300, 300]

## Preprocessing:
- TTKScalarFieldSmoother (iterationNumber=1)

## Ground Truth (temporal subsampling):
Run: yA31
TimeStep  ClusterID
01141     0
03429     0
05700     0 
07920     0 
09782     0 
13306     1
16317     1 
18124     1 
19599     1 
21255     1 
28649     2
31737     2 
34654     2 
37273     2 
39476     2
44229     3 
45793     3 
47190     3 
48557     3 
49978     3

## Ground Truth (clustering):
ClusterID is defined according the third character of run name (asteroid diameter).
The timestep selected is the last one of the run.
Run   TimeStep  ClusterID
yA11  34883     0
yA31  49978     1
yA32  220062    1
yB11  37894     0
yB31  46521     1
yC11  30975     1
yC31  48663     0


# (2017) Cloud processes (2D) (.vtu)
Extents=[1430,1557,1]

## Preprocessing:
- TTKScalarFieldSmoother (iterationNumber=10)

## Ground Truth:
TimeStep  ClusterID
0         0
5         0
10        0
15        0
500       1
505       1
510       1
515       1
1000      2
1005      2
1010      2
1015      2


# (2016) Viscous fingering (3D)

## Preprocessing:
- GaussianResampling (resamplingGrid=[50, 50, 50] ; GaussianSplatRadius=0.1 ; GaussianExponentFactor=-5 ; ScaleSplats=1 ; ScaleFactor=1; EllipticalSplats=1 ; EllipticalEccentricity=2.5 ; FillVolumeBoundary=1 ; FillValue=0 ; **SplatAccumulationMode=sum** ; EmptyCellValue=0)

## Ground Truth:
ClusterID is defined according the resolution parameter.
The timestep selected is the last one of the run.
Resolution  Run TimeStep  ClusterID
020         1   120       0
020         3   120       0
020         4   120       0
020         5   120       0
020         6   120       0
030         1   120       1
030         2   120       1
030         3   120       1
030         4   120       1
030         5   120       1
044         1   120       2
044         2   120       2
044         3   120       2
044         4   120       2
044         5   120       2


# (2015) Dark matter (3D)

## Preprocessing:
- GaussianResampling (**resamplingGrid=[100, 100, 100]** ; **GaussianSplatRadius=0.01** ; GaussianExponentFactor=-5 ; **ScaleSplats=0** ; **EllipticalSplats=0** ; **FillVolumeBoundary=0** ; **SplatAccumulationMode=sum** ; EmptyCellValue=0)
- TTKScalarFieldSmoother (iterationNumber=1)

## Ground Truth:
TimeStep  ClusterID
0.0200    0
0.0300    0
0.0400    0
0.0500    0
0.0600    0
0.0700    0
0.0800    0
0.0900    0
0.1000    0
0.1100    0
0.2700    1
0.2800    1
0.2900    1
0.3000    1
0.3100    1
0.3200    1
0.3300    1
0.3400    1
0.3500    1
0.3600    1
0.5900    2
0.6000    2
0.6100    2
0.6200    2
0.6300    2
0.6400    2
0.6500    2
0.6600    2
0.6700    2
0.6800    2
0.9100    3
0.9200    3
0.9300    3
0.9400    3
0.9500    3
0.9600    3
0.9700    3
0.9800    3
0.9900    3
1.0000    3
>>>>>>> 9d8f6d83bf78ea16deadd4ed1dcc4d17991acc74


# (2014) Volcanic Eruptions (2D)

## Preprocessing:
- ResampleToImage (dimensions=[500, 500, 1])
<<<<<<< HEAD
- TTKTopologicalSimplification (threshold=0.5 -- )
=======
- TTKTopologicalSimplification (threshold=0.5 (~0.5% of the maximum persistence over all members) )

## Ground Truth:
Modality: AIRS
TimeStep  ClusterID
150_am    0
150_pm    0
151_am    0 
151_pm    0 
156_am    1 
156_pm    1
157_am    1
157_pm    1
164_am    2
164_pm    2
165_am    2 
165_pm    2
>>>>>>> 9d8f6d83bf78ea16deadd4ed1dcc4d17991acc74


# (2008) Ionization front (2D)

## Preprocessing:
- ResampleToImage (dimensions=[600, 248, 1])
- TTKScalarFieldNormalizer

## Ground Truth:
TimeStep  ClusterID
0025      0
0026      0
0027      0
0028      0
0075      1
0076      1
0077      1
0078      1
0125      2
0126      2
0127      2
0128      2
0175      3
0176      3
0177      3
0178      3


# (2008) Ionization front (3D)

## Preprocessing:
- ResampleToImage (dimensions=[300, 124, 124])
- TTKScalarFieldNormalizer

## Ground Truth:
Same as Ionization front (2D)


# (2006) Earthquake (3D)

## Preprocessing:
- ResampleToImage (dimensions=[375, 188, 50])
- TTKTopologicalSimplification (threshold=0.0025 (~0.06% of the maximum persistence over all members) )

## Ground Truth:
TimeStep  ClusterID
002700    0
002900    0
003100    0
003300    0
007700    1
007900    1
008100    1
008300    1
011700    2
011900    2
012100    2
012300    2


# (2004) Isabel (3D) ; Starting Vortex (2D) ; Sea Surface Height (2D) ; Vortex Street (2D)

## Preprocessing:
No preprocessing from data given by [Vidal et al., 2019]

## Ground Truth:
Same as [Vidal et al., 2019]
