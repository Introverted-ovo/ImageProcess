import sys
from functools import partial

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtGui import QTransform, QPainter, QColor, QPixmap

#包含的ui页面
import MainWindow
from increase_image import Ui_Form
from image_beautify import Ui_image_beautify
#包含算法
import ImageProcessing,region_grow
from PyQt5.QtWidgets import *

from MyLabel import MyLabel


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口UI
        self.ui = MainWindow.Ui_mainWindow()
        self.ui.setupUi(self)  # 将主窗口UI设置为当前窗口
        # 改变窗口大小
        self.resize(1600, 900)

        # 图像增强子窗口
        self.child_window = QWidget()
        self.child_image_increase = Ui_Form()
        self.child_image_increase.setupUi(self.child_window)
        # 人像美颜子窗口
        self.child_window1 = QWidget()
        self.child_image_beautify = Ui_image_beautify()
        self.child_image_beautify.setupUi(self.child_window1)

        # 实例化方法类
        self.image_processor = ImageProcessing.ImageProcessor()
        # 打开图片
        self.ui.pushButton.clicked.connect(partial(self.image_processor.open_image,  self.ui.label))
        # 保存图片
        self.ui.pushButton_2.clicked.connect(partial(self.image_processor.save_image,  self.ui.label))
        # 摄像头抓取图片
        self.ui.pushButton_4.clicked.connect(partial(self.image_processor.camera_open_image,  self.ui.label))
        # 退出程序
        self.ui.pushButton_3.clicked.connect(self.image_processor.program_exit)
        # 顺时针旋转
        self.ui.action0_0.triggered.connect(partial(self.image_processor.rotate, 90, self.ui.label))
        # 顺时针旋转
        self.ui.action00.triggered.connect(partial(self.image_processor.rotate, -90, self.ui.label))
        # 对称
        self.ui.action1_12.triggered.connect(partial(self.image_processor.transform_image, self.ui.label, 1))
        # 平移
        self.ui.action1.triggered.connect(partial(self.image_processor.translate_scale_start, self.ui.label))
        self.ui.action2_3.triggered.connect(partial(self.image_processor.translate_scale_end, self.ui.label))
        # 裁剪
        self.ui.action1_10.triggered.connect(partial(self.image_processor.image_crop, self.ui.label))
        # 显示直方图
        self.ui.action0.triggered.connect(partial(self.image_processor.scale_histogram, self.ui.label))
        # 灰度化
        self.ui.actiontu.triggered.connect(partial(self.image_processor.rgb_gray, self.ui.label))
        # RGB转SHI
        self.ui.action1_97.triggered.connect(partial(self.image_processor.rgb_hsi, self.ui.label))
        # 图像加噪（高斯噪声）
        self.ui.action1_16.triggered.connect(partial(self.image_processor.show_gaussian, self.ui))
        self.ui.spinBox.valueChanged.connect(partial(self.image_processor.add_gaussian_noise, self.ui.label,self.ui))
        self.ui.spinBox_3.valueChanged.connect(partial(self.image_processor.add_gaussian_noise, self.ui.label,self.ui))
        # 图像加噪（椒盐噪声）
        self.ui.action2_4.triggered.connect(partial(self.image_processor.show_pepper, self.ui))
        self.ui.doubleSpinBox.valueChanged.connect(partial(self.image_processor.add_pepper_noise, self.ui.label,self.ui))
        self.ui.doubleSpinBox_3.valueChanged.connect(partial(self.image_processor.add_pepper_noise, self.ui.label,self.ui))
        # 图像加噪（泊松噪声）
        self.ui.action3_2.triggered.connect(partial(self.image_processor.add_bs_noise, self.ui.label))
        # 图像加噪（speckle噪声）
        self.ui.action4.triggered.connect(partial(self.image_processor.add_speckle_noise, self.ui.label))
        # 去噪（均值去噪）
        self.ui.action1_25.triggered.connect(partial(self.image_processor.show_average_noise, self.ui))
        self.ui.spinBox_4.valueChanged.connect(partial(self.image_processor.denoise_average, self.ui.label,self.ui))
        self.ui.spinBox_5.valueChanged.connect(partial(self.image_processor.denoise_average, self.ui.label,self.ui))
        # 去噪（中值去噪）
        self.ui.action1_24.triggered.connect(partial(self.image_processor.show_median_noise, self.ui))
        self.ui.spinBox_6.valueChanged.connect(partial(self.image_processor.denoise_median, self.ui.label,self.ui))
        # 去噪（高斯去噪）
        self.ui.action1_32.triggered.connect(partial(self.image_processor.show_gaussian_noise, self.ui))
        self.ui.spinBox_7.valueChanged.connect(partial(self.image_processor.denoise_gaussian, self.ui.label,self.ui))
        self.ui.spinBox_8.valueChanged.connect(partial(self.image_processor.denoise_gaussian, self.ui.label,self.ui))
        self.ui.spinBox_9.valueChanged.connect(partial(self.image_processor.denoise_gaussian, self.ui.label, self.ui))
        # 去噪（双边滤波）
        self.ui.action1_36.triggered.connect(partial(self.image_processor.show_bilateral_noise, self.ui))
        self.ui.spinBox_12.valueChanged.connect(partial(self.image_processor.denoise_bilateral, self.ui.label,self.ui))
        self.ui.spinBox_10.valueChanged.connect(partial(self.image_processor.denoise_bilateral, self.ui.label,self.ui))
        self.ui.spinBox_11.valueChanged.connect(partial(self.image_processor.denoise_bilateral, self.ui.label, self.ui))
        # 直接拼接
        self.ui.action1_98.triggered.connect(partial(self.image_processor.zhijiepinjie0, self.ui.label))
        # 加权拼接
        self.ui.action1_99.triggered.connect(partial(self.image_processor.jiaquanpinjie0, self.ui.label))


        # 直方图均衡化
        self.ui.action1_40.triggered.connect(partial(self.image_processor.histogram_equalization, self.ui.label))
        # 图像增强
        self.ui.action2_2.triggered.connect(self.child_window.show)
        self.child_image_increase.horizontalSlider.valueChanged.connect(partial(self.image_processor.increase_image, self.child_image_increase.horizontalSlider,self.child_image_increase.horizontalSlider_2,self.child_image_increase.horizontalSlider_3,self.child_image_increase.horizontalSlider_4, self.ui.label))# 亮度调整
        self.child_image_increase.horizontalSlider_2.valueChanged.connect(partial(self.image_processor.increase_image, self.child_image_increase.horizontalSlider,self.child_image_increase.horizontalSlider_2,self.child_image_increase.horizontalSlider_3,self.child_image_increase.horizontalSlider_4, self.ui.label))# 亮度调整
        self.child_image_increase.horizontalSlider_3.valueChanged.connect(partial(self.image_processor.increase_image, self.child_image_increase.horizontalSlider,self.child_image_increase.horizontalSlider_2,self.child_image_increase.horizontalSlider_3,self.child_image_increase.horizontalSlider_4, self.ui.label))# 亮度调整
        self.child_image_increase.horizontalSlider_4.valueChanged.connect(partial(self.image_processor.increase_image, self.child_image_increase.horizontalSlider,self.child_image_increase.horizontalSlider_2,self.child_image_increase.horizontalSlider_3,self.child_image_increase.horizontalSlider_4, self.ui.label))# 亮度调整
        # 拼图
        self.ui.action1_94.triggered.connect(partial(self.image_processor.pintu, self.ui.label))
        # 图像腐蚀
        self.ui.action1_3.triggered.connect(partial(self.image_processor.show_erode, self.ui))
        self.ui.spinBox_2.valueChanged.connect(partial(self.image_processor.erode_image, self.ui.label,self.ui))
        # 图像膨胀
        self.ui.action1_4.triggered.connect(partial(self.image_processor.show_dilate, self.ui))
        self.ui.spinBox_13.valueChanged.connect(partial(self.image_processor.dilate_image, self.ui.label,self.ui))
        # 图像开操作
        self.ui.action1_5.triggered.connect(partial(self.image_processor.show_opened, self.ui))
        self.ui.spinBox_14.valueChanged.connect(partial(self.image_processor.opened_image, self.ui.label,self.ui))
        # 图像闭操作
        self.ui.action1_6.triggered.connect(partial(self.image_processor.show_closed, self.ui))
        self.ui.spinBox_15.valueChanged.connect(partial(self.image_processor.closed_image, self.ui.label,self.ui))
        # 图像梯度操作
        self.ui.action1_7.triggered.connect(partial(self.image_processor.show_gradient, self.ui))
        self.ui.spinBox_16.valueChanged.connect(partial(self.image_processor.gradient_image, self.ui.label,self.ui))
        # 图像顶帽操作
        self.ui.actiondi.triggered.connect(partial(self.image_processor.show_tophat, self.ui))
        self.ui.spinBox_17.valueChanged.connect(partial(self.image_processor.tophat_image, self.ui.label,self.ui))
        # 图像黑帽操作
        self.ui.action1_8.triggered.connect(partial(self.image_processor.show_blackhat, self.ui))
        self.ui.spinBox_18.valueChanged.connect(partial(self.image_processor.blackhat_image, self.ui.label,self.ui))
        # 伪彩色增强
        self.ui.action1_96.triggered.connect(partial(self.image_processor.wei_cai_se, self.ui.label))
        # 假色彩增强
        self.ui.action1_91.triggered.connect(self.child_window.show)

        # 边缘检测
        self.ui.action1_54.triggered.connect(partial(self.image_processor.edge_dectect, self.ui.label))
        # 轮廓检测
        self.ui.action1_80.triggered.connect(partial(self.image_processor.gontour_dectect, self.ui.label))
        # 直线检测
        self.ui.action1_82.triggered.connect(partial(self.image_processor.LSD_line_dectect, self.ui.label))
        # 圆形检测
        self.ui.action1_86.triggered.connect(partial(self.image_processor.Circles_dectect, self.ui.label))
        # 二值分割（边缘检测）
        self.ui.action1_23.triggered.connect(partial(self.image_processor.show_edge_dectect2, self.ui))
        self.ui.spinBox_20.valueChanged.connect(partial(self.image_processor.edge_dectect2, self.ui.label,self.ui))
        self.ui.spinBox_21.valueChanged.connect(partial(self.image_processor.edge_dectect2, self.ui.label,self.ui))
        # 二值分割（阈值分割）
        self.ui.action1_55.triggered.connect(partial(self.image_processor.show_threshold, self.ui))
        self.ui.spinBox_22.valueChanged.connect(partial(self.image_processor.threshold, self.ui.label,self.ui))
        self.ui.spinBox_23.valueChanged.connect(partial(self.image_processor.threshold, self.ui.label,self.ui))
        # 二值分割（区域生长）
        self.ui.action1_65.triggered.connect(partial(self.image_processor.region_growing, self.ui))
        # 人像美颜
        self.ui.action1_73.triggered.connect(self.child_window1.show)
        self.child_image_beautify.horizontalSlider.valueChanged.connect(partial(self.image_processor.beautify, self.child_image_beautify.horizontalSlider,self.child_image_beautify.horizontalSlider_3,self.ui.label))
        self.child_image_beautify.horizontalSlider_3.valueChanged.connect(partial(self.image_processor.beautify, self.child_image_beautify.horizontalSlider,self.child_image_beautify.horizontalSlider_3,self.ui.label))
        # self.child_image_beautify.pushButton.clicked.connect(partial(self.image_processor.shoulian, self.ui.label))




        # mask掩膜
#        self.ui.action1_28.triggered.connect(partial(self.image_processor.mask_img, self.ui.label))
        # 加框
        self.ui.action1_87.triggered.connect(partial(self.image_processor.border_img, self.ui.label, 1))
        self.ui.action1_88.triggered.connect(partial(self.image_processor.border_img, self.ui.label, 2))
        self.ui.action1_89.triggered.connect(partial(self.image_processor.border_img, self.ui.label, 3))
        self.ui.action1_90.triggered.connect(partial(self.image_processor.border_img, self.ui.label, 4))
        # 浮雕效果
        self.ui.action1_38.triggered.connect(partial(self.image_processor.apply_emboss_effect, self.ui.label))
        # 凸透镜效果
        self.ui.action1_39.triggered.connect(partial(self.image_processor.tutoujing, self.ui.label))
        # 素描效果
        self.ui.action1_46.triggered.connect(partial(self.image_processor.sumiao, self.ui.label))
        # 毛玻璃效果
        self.ui.action1_48.triggered.connect(partial(self.image_processor.maoboli, self.ui.label))
        # 怀旧效果
        self.ui.action1_49.triggered.connect(partial(self.image_processor.huaijiu, self.ui.label))
        # 卡通效果
        self.ui.action1_53.triggered.connect(partial(self.image_processor.cartoon, self.ui.label))
        # 流年效果
        self.ui.action1_50.triggered.connect(partial(self.image_processor.liunian, self.ui.label, 10))
        # 油漆效果
        self.ui.action1_52.triggered.connect(partial(self.image_processor.youqi, self.ui.label))
        # 光照效果
        self.ui.action1_51.triggered.connect(partial(self.image_processor.guangzhao, self.ui.label, 150))

        # 水彩效果
        self.ui.action1_42.triggered.connect(partial(self.image_processor.shuicai, self.ui.label))
        # 油画效果
        self.ui.action1_41.triggered.connect(partial(self.image_processor.youhua, self.ui.label))
        # 彩铅效果
        self.ui.action1_45.triggered.connect(partial(self.image_processor.caiqian, self.ui.label))



        # 超分辨率
        self.ui.action1_85.triggered.connect(partial(self.image_processor.show_supper, self.ui))
        self.ui.doubleSpinBox_2.valueChanged.connect(partial(self.image_processor.supper, self.ui.label,self.ui))
        # 倒影图制作
        self.ui.action1_95.triggered.connect(partial(self.image_processor.transform_image, self.ui.label, 0))
        # 老照片修复
        self.ui.action1_71.triggered.connect(partial(self.image_processor.oldphoto, self.ui.label))


        # 人脸识别（图片）
        self.ui.action1_69.triggered.connect(partial(self.image_processor.tp_FaceTec, self.ui.label))
        # 人脸识别（视频）
        self.ui.action1_70.triggered.connect(self.image_processor.sp_FaceTec)



    def keyPressEvent(self, event):
        # 捕获键盘事件
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # 当按下回车键时，替换图片
            if self.image_processor.count == 1:
                self.image_processor.new_label1.setParent(None)
                self.image_processor.new_label1.deleteLater()
                self.ui.label.show()
                pixmap = QPixmap("cropped_image.jpg")
                self.ui.label.setPixmap(pixmap)
                self.image_processor.count = 0
            else:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
