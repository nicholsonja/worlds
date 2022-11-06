INPUT_TEMPLATE_FILE = "path-template.xml"
OUTPUT_WORLD_FILE = "path_world.xml"

MODEL_TEMPLATE = """
      <model name='MODEL-NAME'>
        <scale>1 1 1</scale>
        <pose>MODEL-X MODEL-Y 0 0 -0 MODEL-YAW</pose>
        <velocity>0 0 0 0 -0 0</velocity>
        <acceleration>0 -0 0 0 -0 0</acceleration>
        <wrench>0 -0 0 0 -0 0</wrench>
      </model>
"""

INCLUDE_TEMPLATE = """
    <model name='MODEL-NAME'>
      <static>1</static>
      <include>
        <uri>model:///home/user/worlds/models/line</uri>
	  </include>
    </model>
"""

INCLUDE_END_TEMPLATE = """
    <model name='MODEL-NAME'>
      <static>1</static>
      <include>
        <uri>model:///home/user/worlds/models/end_line</uri>
	  </include>
    </model>
"""
