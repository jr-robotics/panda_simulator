from interactive_markers.interactive_marker_server import *
from interactive_markers.menu_handler import *
from visualization_msgs.msg import *
from geometry_msgs.msg import Quaternion


class RvizMarkers():

    def makeBox(self, msg):
        marker = Marker()

        marker.type = Marker.CUBE
        marker.scale.x = msg.scale * 0.05
        marker.scale.y = msg.scale * 0.05
        marker.scale.z = msg.scale * 0.05
        marker.color.r = 0.5
        marker.color.g = 0.5
        marker.color.b = 0.5
        marker.color.a = 1.0

        return marker

    def makeBoxControl(self, msg):
        control = InteractiveMarkerControl()
        control.always_visible = True
        control.markers.append(self.makeBox(msg))
        msg.controls.append(control)
        return control

    def makeMarker(self, fixed, interaction_mode, position, orientation, show_6dof=False):
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = 'base'
        int_marker.pose.position = position

        init_orientation = Quaternion(
            orientation[1], orientation[2], orientation[3], orientation[0])

        int_marker.pose.orientation = init_orientation

        int_marker.scale = 0.5

        int_marker.name = 'marker'
        int_marker.description = 'Marker Control'

        # insert a box
        self.makeBoxControl(int_marker)
        int_marker.controls[0].interaction_mode = interaction_mode

        if fixed:
            int_marker.name += '_fixed'
            int_marker.description += '\n(fixed orientation)'

        if interaction_mode != InteractiveMarkerControl.NONE:
            control_modes_dict = {
                InteractiveMarkerControl.MOVE_3D: 'MOVE_3D',
                InteractiveMarkerControl.ROTATE_3D: 'ROTATE_3D',
                InteractiveMarkerControl.MOVE_ROTATE_3D: 'MOVE_ROTATE_3D'}
            int_marker.name += '_' + control_modes_dict[interaction_mode]
            int_marker.description = '3D Control'
            if show_6dof:
                int_marker.description += ' + 6-DOF controls'
            int_marker.description += '\n' + \
                control_modes_dict[interaction_mode]

        if show_6dof:
            def _create_control(x: int = 0, y: int = 0, z: int = 0, w: int = 0, control_name: str = '', interaction_mode=InteractiveMarkerControl.ROTATE_AXIS) -> InteractiveMarkerControl:
                control = InteractiveMarkerControl()
                control.orientation.x = x
                control.orientation.y = y
                control.orientation.z = z
                control.orientation.w = w
                control.name = control_name
                control.interaction_mode = interaction_mode
                if fixed:
                    control.orientation_mode = InteractiveMarkerControl.FIXED
                return control

            control = _create_control(
                x=0, y=0, z=0, w=1, control_name='rotate_x', interaction_mode=InteractiveMarkerControl.ROTATE_AXIS)
            int_marker.controls.append(control)

            control = InteractiveMarkerControl()
            control.orientation = init_orientation

            control.name = 'move_x'
            control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
            if fixed:
                control.orientation_mode = InteractiveMarkerControl.FIXED
            int_marker.controls.append(control)

            control = _create_control(x=0, y=1, z=0, w=1, control_name='rotate_z', interaction_mode=InteractiveMarkerControl.ROTATE_AXIS)
            int_marker.controls.append(control)

            control = _create_control(x=0, y=1, z=0, w=1, control_name='move_z', interaction_mode=InteractiveMarkerControl.MOVE_AXIS)
            int_marker.controls.append(control)

            control = _create_control(x=0, y=0, z=1, w=1, control_name='rotate_y', interaction_mode=InteractiveMarkerControl.ROTATE_AXIS)
            int_marker.controls.append(control)

            control = _create_control(x=0, y=0, z=1, w=1, control_name='move_y', interaction_mode=InteractiveMarkerControl.MOVE_AXIS)
            int_marker.controls.append(control)

        return int_marker
