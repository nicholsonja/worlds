INPUT_TEMPLATE_FILE = "path-template.xml"
INPUT_MAZE_TEMPLATE_FILE = "maze-template.xml"
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

INCLUDE_BOX_TEMPLATE = """
    <model name='MODEL-NAME'>
      <static>1</static>
      <include>
        <uri>model:///home/user/worlds/models/MODEL-BOX</uri>
	  </include>
    </model>
"""

MODEL_BOX_TEMPLATE = """
      <model name='MODEL-NAME'>
        <scale>1 1 1</scale>
        <pose>MODEL-X MODEL-Y .25 0 -0 MODEL-YAW</pose>
        <velocity>0 0 0 0 -0 0</velocity>
        <acceleration>0 -0 0 0 -0 0</acceleration>
        <wrench>0 -0 0 0 -0 0</wrench>
      </model>
"""


GROUND_MODEL = """
<model name='ground_plane'>
      <static>1</static>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>100</mu>
                <mu2>50</mu2>
              </ode>
              <torsional>
                <ode/>
              </torsional>
            </friction>
            <contact>
              <ode/>
            </contact>
            <bounce/>
          </surface>
          <max_contacts>10</max_contacts>
        </collision>
        <visual name='visual'>
          <cast_shadows>0</cast_shadows>
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/Grey</name>
            </script>
          </material>
        </visual>
        <self_collide>0</self_collide>
        <enable_wind>0</enable_wind>
        <kinematic>0</kinematic>
      </link>
    </model>
    """

GROUND_INCLUDE = """
<model name='ground_plane'>
        <pose>0 0 0 0 -0 0</pose>
        <scale>1 1 1</scale>
        <link name='link'>
          <pose>0 0 0 0 -0 0</pose>
          <velocity>0 0 0 0 -0 0</velocity>
          <acceleration>0 0 0 0 -0 0</acceleration>
          <wrench>0 0 0 0 -0 0</wrench>
        </link>
      </model>
      """
