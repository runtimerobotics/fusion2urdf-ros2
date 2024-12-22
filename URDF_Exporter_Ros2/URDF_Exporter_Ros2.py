#Author-syuntoku14
#Description-Generate URDF file from Fusion 360

import adsk, adsk.core, adsk.fusion, traceback
import os
import sys
from .utils import utils
from .core import Link, Joint, Write

"""
# length unit is 'cm' and inertial unit is 'kg/cm^2'
# If there is no 'body' in the root component, maybe the corrdinates are wrong.
"""

# joint effort: 100
# joint velocity: 100
# supports "Revolute", "Rigid" and "Slider" joint types

# I'm not sure how prismatic joint acts if there is no limit in fusion model

def run(context):
    ui = None
    success_msg = 'Successfully created URDF file'
    msg = success_msg

    try:
        # --------------------
        # initialize
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Fusion 360 -> ROS 2 URDF'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return

        root = design.rootComponent  # root component
        components = design.allComponents

        # set the names
        robot_name = root.name.split()[0]
        package_name = robot_name + '_description'

        # Show welcome message
        welcome_msg = ("Welcome to the Fusion 'Fusion 360 -> ROS 2 URDF Script' plugin.\n"
                       "\n"
                       "This tool generates a robot_description package along with launch files for visualizing your robot in Rviz and spawning the model in Gazebo Sim.\n"
                       "\n"
                       "It has been tested with ROS 2 Jazzy and Gazebo Harmonic, as well as ROS 2 Humble with both Gazebo Classic and Gazebo Sim.\n\n"
                       "\n"
                       "Press OK to continue or Cancel to quit.")
        if ui.messageBox(welcome_msg, title, adsk.core.MessageBoxButtonTypes.OKCancelButtonType) != adsk.core.DialogResults.DialogOK:
            return

        # Show folder browse message
        browse_msg = "Press Ok to browse the folder for saving the ROS package, cancel to quit."
        if ui.messageBox(browse_msg, title, adsk.core.MessageBoxButtonTypes.OKCancelButtonType) != adsk.core.DialogResults.DialogOK:
            return

        # Browse folder
        save_dir = utils.file_dialog(ui)
        if save_dir == False:
            ui.messageBox('Fusion 360 -> ROS 2 URDF was canceled', title)
            return 0

        save_dir = save_dir + '/' + package_name
        try:
            os.mkdir(save_dir)
        except:
            pass

        # Ask for Gazebo version
        gazebo_msg = "Are you using Gazebo 11? Press Yes for Gazebo 11, No for Gazebo Sim."
        if ui.messageBox(gazebo_msg, title, adsk.core.MessageBoxButtonTypes.YesNoButtonType) == adsk.core.DialogResults.DialogYes:
            generate_urdf_gazebo11(save_dir)
        else:
            generate_urdf_gazebo_sim(save_dir)

        ui.messageBox(success_msg, title)

    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{str(e)}', title)

def generate_urdf_gazebo11(save_dir):
    # Function to generate URDF for Gazebo 11
    pass

def generate_urdf_gazebo_sim(save_dir):
    # Function to generate URDF for Gazebo Sim
    pass
