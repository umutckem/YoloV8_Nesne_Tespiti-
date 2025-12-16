# 🪑⌨️ YOLOv8 Chair & Keyboard Detector

Sandalye ve klavye nesnelerini tespit etmek için YOLOv8 makine öğrenmesi modelini kullanan masaüstü uygulaması.

---

## 📋 İçindekiler

- [Proje Açıklaması](#proje-açıklaması)
- [Teknolojiler](#teknolojiler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Dosya Yapısı](#dosya-yapısı)
- [Model Eğitimi](#model-eğitimi)
- [Proje Detayları](#proje-detayları)

---

## 🎯 Proje Açıklaması

Bu proje, YOLOv8 (You Only Look Once) nesne tespiti modelini kullanarak resimlerdeki **sandalye** ve **klavye** nesnelerini otomatik olarak tespit eder. PyQt5 arayüzüyle kullanıcı dostu bir masaüstü uygulaması sağlar.

### Özellikler:
- 🖼️ Kolayca görsel seçimi
- 🔍 Gerçek zamanlı nesne tespiti
- 💾 Tespit edilmiş görselleri kaydetme
- 📊 Eğitim metrikleri ve grafikler

---

## 🛠️ Teknolojiler

| Teknoloji | Kullanım |
|-----------|----------|
| **Python 3.x** | Programlama dili |
| **YOLOv8** | Nesne tespiti modeli (Ultralytics) |
| **PyQt5** | Masaüstü GUI arayüzü |
| **OpenCV (cv2)** | Görüntü işleme |
| **NumPy** | Sayısal hesaplamalar |

---

## 📦 Kurulum

### Ön Koşullar
- Python 3.8 veya üzeri
- pip paket yöneticisi

### Gerekli Paketleri Yükleme

```bash
pip install ultralytics PyQt5 opencv-python numpy
```

### Model Dosyasını Hazırlama

Eğitilmiş model dosyası (`best.pt`) projenin ana dizininde olmalıdır:

```
GUI/
├── gui_app.py
├── best.pt          ← Model burada olmalı
└── Uygulama_2.ipynb
```

Model dosyası `runs/chair_keyboard/weights/` dizininden kopyalanabilir.

---

## 🚀 Kullanım

### Uygulamayı Başlatma

```bash
python gui_app.py
```

### Adımlar:

1. **🖼️ Görsel Seç** - Görsel seçme penceresinden bir resim dosyası seçin (JPG, JPEG, PNG)
2. **🔍 Test Et** - Seçili resim üzerinde nesne tespiti çalıştırın
3. **💾 Kaydet** - Tespit edilen nesnelerin etiketlendiği resmi kaydedin

---

## 📁 Dosya Yapısı

```
GUI/
├── gui_app.py              # Ana uygulama dosyası
├── best.pt                 # Eğitilmiş YOLO modeli
├── Uygulama_2.ipynb        # Jupyter notebook (model eğitimi)
├── README.md               # Bu dosya
└── runs/
    └── chair_keyboard/
        ├── args.yaml               # Model eğitim parametreleri
        ├── results.csv             # Eğitim sonuçları
        ├── results.png             # Eğitim grafikleri
        ├── confusion_matrix.png    # Karmaşıklık matrisi
        ├── confusion_matrix_normalized.png
        ├── BoxF1_curve.png         # F1 eğrisi
        ├── BoxPR_curve.png         # Precision-Recall eğrisi
        ├── BoxP_curve.png          # Precision eğrisi
        ├── BoxR_curve.png          # Recall eğrisi
        ├── labels.jpg              # Veri seti etiketleri
        ├── train_batch*.jpg        # Eğitim batch örnekleri
        ├── val_batch*.jpg          # Doğrulama batch örnekleri
        └── weights/
            ├── best.pt             # En iyi model
            └── last.pt             # Son eğitim checkpoint
```

---

## 🧠 Model Eğitimi

Model eğitimi `Uygulama_2.ipynb` Jupyter notebook'unda gerçekleştirilmiştir.

### Eğitim Süreci:

1. **Veri Seti Hazırlığı** - Sandalye ve klavye görüntüleri ile `data.yaml` oluşturma
2. **Model Yükleme** - YOLOv8 nano (yolov8n) modelini indirme
3. **Eğitim** - 50 epoch ile modeli eğitme
4. **Doğrulama** - Modelin performansını test etme

### Eğitim Parametreleri:
```yaml
epochs: 50
imgsz: 640
batch: 16
device: GPU (CUDA) / CPU
```

### Sınıflar:
- `0: chair` (Sandalye)
- `1: keyboard` (Klavye)

---

## 🎨 Arayüz Özellikleri

### Tema
- **Koyu Mod** - Göz dostu tasarım
- **Modern Stilizasyon** - PyQt5 QSS (Qt Style Sheet) ile özelleştirilmiş

### Bileşenler
- **Orijinal Görüntü Paneli** - Seçilen resim gösterilir
- **Tespit Edilen Görüntü Paneli** - Nesneler etiketlenmiş resim gösterilir
- **Kontrol Düğmeleri** - Görsel seçimi, test, kaydetme işlemleri

### Mesajlar
- Hata mesajları (Model bulunamadı, format hatası vb.)
- Bilgi mesajları (Başarılı kayıt vb.)
- Uyarı mesajları (Test edilmemiş, seçim yapılmamış vb.)

---

## 📊 Model Performansı

Eğitim sonuçları `runs/chair_keyboard/` dizininde bulunmaktadır:

- **results.csv** - Eğitim ve doğrulama metrikleri
- **Grafikleri:**
  - Precision, Recall, F1 Score eğrileri
  - Karmaşıklık matrisi
  - Eğitim batch örnekleri

---

## 👤 Proje Bilgileri

- **Geliştirici:** Umutcan Kemahlı
- **Okul Numarası:** 2212721050
- **GitHub:** [YoloV8_Nesne_Tespiti](https://github.com/umutckem/YoloV8_Nesne_Tespiti-.git)

---

## 📝 Notlar

- Model dosyası ilk çalışmada otomatik kontrol edilir
- GPU varsa otomatik olarak CUDA kullanılır, yoksa CPU'da çalışır
- Paneller pencere boyutu değiştiğinde otomatik olarak yeniden ölçeklendirilir
- Test etmeden önce mutlaka bir görüntü seçilmesi gerekir

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## Proje Data Set

https://drive.google.com/drive/folders/1UAToG9RRDO_Uf4YAiCoQBmF64IKaNEnV?usp=sharing

---

<img width="1004" height="638" alt="Ekran görüntüsü 2025-12-17 005725" src="https://github.com/user-attachments/assets/c757b27f-a514-4ec7-bf02-f40803302a16" />

<img width="1001" height="635" alt="Ekran görüntüsü 2025-12-17 005746" src="https://github.com/user-attachments/assets/2023b365-5108-4b05-929d-c37b81570bdb" />






**Son Güncelleme:** 2025 | YOLOv8 Nesne Tespiti Projesi
