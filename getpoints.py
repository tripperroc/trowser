import shapefile
import json


sf = shapefile.Reader("ZillowNeighborhoods-NY.shp")
shapes = sf.shapes()
data = list()

for i in range(0,len(shapes)):
    points = shapes[i].points
    pointsdata = list()
    for point in points:
        pointsdata.append({"lat": point[1], "lon": point[0]})
    record = dict()
    record["points"] = pointsdata
    record["city"] = sf.records()[i][2]
    record["neighborhood"] = sf.records()[i][3]
    if record["city"] == "Rochester":
        data.append(record)

f = open("points.json","w")
f.write(json.dumps(data))
