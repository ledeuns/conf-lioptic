import sys
import os
from datetime import datetime
import yaml
import jinja2

def ComputeIntercoPfx(svlan):
  """ Generates a 100.64/10 prefix based on the svlan-id
      Output if svlan=1001 : 100.67.233
  """
  byte1 = 100
  byte2 = 64 + int(svlan/256)
  byte3 = svlan%256
  return str(byte1)+"."+str(byte2)+"."+str(byte3)
  
def PrintConfig(genlist):
  templateLoader = jinja2.FileSystemLoader(searchpath="/")
  templateEnv = jinja2.Environment(loader=templateLoader)
  TEMPLATE_FILE = os.getcwd()+"/conf-lioptic.jinja"
  template = templateEnv.get_template(TEMPLATE_FILE)
  templateVars = {}
  for v in genlist:
    templateVars.update(v)
  templateVars["interco4_prefix"] = ComputeIntercoPfx(templateVars["svlan"])
  templateVars["datetime"] = datetime.now().strftime("%d/%m/%y %H:%M")
  outputText = template.render( templateVars )
  print (outputText)

input = yaml.load(open('conf-lioptic.yaml'))
if (sys.argv[1:]):
  PrintConfig(input[sys.argv[1:][0]])
else:
  for i in input:
    PrintConfig(input[i])
