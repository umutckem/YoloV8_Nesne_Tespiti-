import sys
import os

import cv2
import numpy as np
from ultralytics import YOLO

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QSize


MODEL_PATH = "best.pt"


# --- QSS (Qt Style Sheet) ile Koyu Tema ---
DARK_MODE_QSS = """
QMainWindow {
    background-color: #2e2e2e; /* Ana arka plan */
    color: #f0f0f0;            /* Genel yazı rengi */
}

QLabel#ImagePanel {
    background-color: #3c3c3c;
    border: 2px dashed #5a5a5a; /* Daha belirgin çerçeve */
    border-radius: 10px;
    font-size: 16pt;
    color: #cccccc;
    min-height: 400px;
}

QPushButton {
    background-color: #0078d7; /* Mavi ton */
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    min-width: 150px;
}

QPushButton:hover {
    background-color: #005bb5; /* Hover rengi */
}

QPushButton:pressed {
    background-color: #004494;
}

QMessageBox {
    background-color: #3c3c3c;
    color: #f0f0f0;
}
"""
# --------------------------------------------


def cvimg_to_qpixmap(img_bgr):
    """OpenCV BGR numpy -> QPixmap (RGB)"""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w, ch = img_rgb.shape
    bytes_per_line = ch * w
    # QImage.Format_RGB888 daha genel kullanım için uygundur.
    qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ---------- Model Yükleme ----------
        if not os.path.exists(MODEL_PATH):
            QMessageBox.critical(
                self,
                "Model Bulunamadı",
                f"best.pt modeli bulunamadı.\n\nLütfen MODEL_PATH'i kontrol edin:\n{MODEL_PATH}"
            )
            sys.exit(1)

        # Cihaz belirleme (GPU varsa 'cuda', yoksa 'cpu')
        device = 'cuda' if YOLO.device == 'cuda' else 'cpu'
        self.model = YOLO(MODEL_PATH, task='detect')
        print(f"YOLO modeli yüklendi. Cihaz: {device}")


        # Seçilen ve etiketli görüntüler
        self.current_img_path = None
        self.current_img_bgr = None
        self.tagged_img_bgr = None

        self.original_pixmap = None
        self.tagged_pixmap = None

        self.init_ui()
        
        # İlk panel metnini başlangıçta göster
        self.label_original.setText("Bir Görsel Seçmek İçin Butona Basın.")
        self.label_tagged.setText("Henüz Test Edilmedi.")


    def init_ui(self):
        self.setWindowTitle("⚡ YOLOv8 Chair & Keyboard Detector")
        self.setMinimumSize(QSize(1000, 600))

        # --- Paneller (QLabel yerine QFrame/QLabel kombinasyonu tercih edilebilir) ---
        # QSS ile kolay stil verebilmek için objectName atıyoruz.
        self.label_original = QLabel("Original Image Panel")
        self.label_original.setObjectName("ImagePanel") # QSS için ID
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_original.setScaledContents(False) # Pixmap'i elle ölçekleyeceğiz

        self.label_tagged = QLabel("Tagged Image Panel")
        self.label_tagged.setObjectName("ImagePanel") # QSS için ID
        self.label_tagged.setAlignment(Qt.AlignCenter)
        self.label_tagged.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_tagged.setScaledContents(False)

        panel_layout = QHBoxLayout()
        panel_layout.addWidget(self.label_original)
        panel_layout.addWidget(self.label_tagged)

        # --- Butonlar ---
        btn_select = QPushButton("🖼️ Görsel Seç")
        btn_test = QPushButton("🔍 Test Et")
        btn_save = QPushButton("💾 Kaydet")
        
        # Signal/Slot bağlantıları
        btn_select.clicked.connect(self.select_image)
        btn_test.clicked.connect(self.test_image)
        btn_save.clicked.connect(self.save_image)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_select)
        buttons_layout.addWidget(btn_test)
        buttons_layout.addWidget(btn_save)
        buttons_layout.addStretch()

        # --- Ana Layout ---
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addLayout(panel_layout)
        main_layout.addLayout(buttons_layout)

        self.setCentralWidget(main_widget)

    # ------------------------------------------------
    #                 İŞLEVLER
    # ------------------------------------------------
    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Bir Görsel Seç",
            os.path.expanduser("~"), # Başlangıç klasörü kullanıcı ana dizini
            "Image Files (*.jpg *.jpeg *.png)"
        )
        if not file_path:
            return

        img = cv2.imread(file_path)
        if img is None:
            QMessageBox.warning(self, "Hata", "Görsel okunamadı! Lütfen dosya formatını kontrol edin.")
            return

        self.current_img_path = file_path
        self.current_img_bgr = img
        self.tagged_img_bgr = None  # Yeni seçimde eski etiketli görseli sil
        self.tagged_pixmap = None   # Etiketli pixmap'i de sil

        self.original_pixmap = cvimg_to_qpixmap(img)
        self.update_panels()

    def test_image(self):
        if self.current_img_path is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir görsel seçmelisiniz.")
            return

        # YOLOv8 inference
        try:
            # Modelin `path` yerine direk numpy array'i alması daha hızlı olabilir
            results = self.model(self.current_img_bgr, verbose=False) 
            result = results[0] 
            plotted_bgr = result.plot() 
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"YOLO model testi başarısız oldu:\n{e}")
            return

        self.tagged_img_bgr = plotted_bgr
        self.tagged_pixmap = cvimg_to_qpixmap(plotted_bgr)
        self.update_panels()

    def save_image(self):
        if self.tagged_img_bgr is None:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Kaydedilecek etiketli görüntü yok.\nÖnce 'Test Et' butonuna basınız."
            )
            return

        # Seçilen görselin adını temel alarak başlangıç dosya adı önerisi
        base_name = os.path.basename(self.current_img_path) if self.current_img_path else "image"
        default_save_name = f"tagged_{base_name}"
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Etiketli Görüntüyü Kaydet",
            default_save_name,
            "Image Files (*.jpg *.jpeg *.png)"
        )
        if not save_path:
            return

        # OpenCV BGR formatında kaydediyoruz
        success = cv2.imwrite(save_path, self.tagged_img_bgr)
        if success:
            QMessageBox.information(self, "✅ Başarılı", f"Görüntü kaydedildi:\n{save_path}")
        else:
            QMessageBox.warning(self, "❌ Hata", "Görüntü kaydedilemedi! Kayıt yolunu kontrol edin.")

    # ------------------------------------------------
    #           PANEL GÖRÜNÜMÜNÜ GÜNCELLEME
    # ------------------------------------------------
    def update_panels(self):
        # Orijinal Panel Güncelleme
        if self.original_pixmap is not None:
            # Panel boyutuna göre ölçekleme
            scaled_original = self.original_pixmap.scaled(
                self.label_original.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_original.setPixmap(scaled_original)
            self.label_original.setText("") # Resmi gösterince metni sil
        else:
            self.label_original.setText("Bir Görsel Seçmek İçin Butona Basın.")

        # Etiketli Panel Güncelleme
        if self.tagged_pixmap is not None:
            scaled_tagged = self.tagged_pixmap.scaled(
                self.label_tagged.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_tagged.setPixmap(scaled_tagged)
            self.label_tagged.setText("") # Resmi gösterince metni sil
        else:
             # Orijinal resim seçildiyse ama henüz test edilmediyse
            if self.original_pixmap is not None:
                self.label_tagged.setPixmap(QPixmap()) # Önceki resmi kaldır
                self.label_tagged.setText("Test Etmek İçin 'Test Et' Butonuna Basın.")
            else:
                self.label_tagged.setPixmap(QPixmap())
                self.label_tagged.setText("Henüz Test Edilmedi.")


    def resizeEvent(self, event):
        # Pencere boyutu değişince panelleri yeniden ölçekle
        self.update_panels()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Koyu temayı uygula
    app.setStyleSheet(DARK_MODE_QSS) 
    
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())