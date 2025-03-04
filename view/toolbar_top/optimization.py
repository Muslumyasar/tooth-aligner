from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QAction,
    QSizePolicy
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from constant.enums import PanelMode
from controller.bite_contact_controller import reset_bite_contact
from controller.segmentation_controller import set_selected_arch, set_selected_label
from controller.step_controller import update_transform_arch
from controller.summary_controller import get_studi_model_summary_pts, get_summary_flat_pts
from optimization.de_optimization import start_de

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton

def create_optimization_menu(self, parent_layout):
    self.container_tool_btn = QWidget()
    self.container_tool_btn_layout = QHBoxLayout()
    self.container_tool_btn.setLayout(self.container_tool_btn_layout)
    
    self.btn_de_optimization = ToolTopButton("DE Optimization",'icons/teeth-segmentation.png','icons/teeth-segmentation-colors.png',True)
    # self.btn_de_optimization.setObjectName('btn_toolbar_tool_segmentation')
    self.btn_de_optimization.clicked.connect(lambda e: click_btn_de_optimization(self,e))
    # self.btn_de_optimization.toggled.connect(lambda e: toggle_btn_de_optimization(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_de_optimization)
    
    
    section = ToolbarTopSection("Optimization",self.container_tool_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)


def click_btn_de_optimization(self, e):
    error_opt = 30
    step_i = 1
    while(step_i<12):
    # while(error_opt > 1):
        self.btn_addmin_step_aligner.btn_increase.click()
        print("step_i",step_i)
        step_i+=1
        new_models, error_opt = start_de(self.models, get_summary_flat_pts(self), get_studi_model_summary_pts(self))
        print("eror", error_opt)
        for i in range(len(self.models)):
            self.models[i].mesh = new_models[i].mesh.clone()
            self.models[i].right_left_vec = new_models[i].right_left_vec
            self.models[i].forward_backward_vec = new_models[i].forward_backward_vec
            self.models[i].upward_downward_vec = new_models[i].upward_downward_vec
            self.models[i].gingiva=new_models[i].gingiva
            self.models[i].teeth=new_models[i].teeth
            update_transform_arch(self,self.step_model.get_current_step())
        # self.btn_addmin_step_aligner.btn_increase.click()
    self.btn_de_optimization.setChecked(False)
    # self.model_plot.add(new_models[0].mesh)
    # self.model_plot.add(new_models[1].mesh)
    # self.model_plot.render()