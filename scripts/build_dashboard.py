import json, os
D = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(D,"dashboard_data.json")))
tpl = open(os.path.join(D,"template.html")).read()
chartjs = open(os.path.join(D,"chart.umd.js")).read()
out = tpl.replace("__DASHBOARD_DATA__", json.dumps(data)).replace("__CHARTJS_INLINE__", chartjs)
outpath = os.path.join(D,"..","dashboard","Walmart_Dashboard.html")
open(outpath,"w").write(out)
print("Built:", len(out), "bytes ->", outpath)
