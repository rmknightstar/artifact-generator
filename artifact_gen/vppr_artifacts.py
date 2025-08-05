from . import artifact_utils as au
import json
from IPython.display import display_markdown, display_html

def generate_artifacts(year, month, vppr_root, ig_template, artifact_list=["evite", "linkedin", "IG1","IG2"] ):
 #TODO: Fix indentation
 fmt_map=dict()
 au.VPPR = vppr_root
 artifacts=json.load(open(f"{au.VPPR}/artifacts.json"))
 officers=json.load(open(f"{au.VPPR}/officers.json"))
 fmt_map["ig_template"] = ig_template

 au.yyyymm=f"{year}/{str(month).zfill(2)}"
 fmt_map["formatted_date"] = au.second_wed_formated(year,month)
 venue=json.load(open(f"{au.VPPR}/{au.yyyymm}/venue.json"))
 for artifact in artifact_list:

  for outer in officers:
    for inner in officers[outer]:
      fmt_map[f"{outer}_{inner}"]=officers[outer][inner]

  for outer in artifacts:
    if outer == "artifacts":
      for inner in artifacts[outer][artifact]["var"]:
        fmt_map[inner]=artifacts[outer][artifact]["var"][inner]
    else:
      for inner in artifacts[outer]:
        fmt_map[f"{outer}_{inner}"]=artifacts[outer][inner]

  for inner in venue:
    fmt_map[f"venue_{inner}"]=venue[inner]

  print(json.dumps(fmt_map,indent=2))

  xelems=list()
  for element in artifacts["artifacts"][artifact]["elements"]:
    xelem=dict()
    for field in element:
      xelem[field]=str(element[field]).format(**fmt_map)
    xelems.append(xelem)

  xartifact={
      "base": artifacts["artifacts"][artifact]["base"].format(**fmt_map),
      "elements": xelems
  }
  print(json.dumps(xartifact,indent=2))

  im=au.process_artifact(xartifact)

  display_markdown(f"# {artifact}", raw=True)
  display(im)
  im.save(f"{au.VPPR}/{au.yyyymm}/{artifact}.png")

