

# 🛒 Hibrit Ürün Arama Motoru (ResNet50 + OCR)

Bu proje, market ürünlerini veya tekstil ürünlerini (kazak, gömlek vb.) hem **görsel benzerlik** hem de **üzerlerindeki metinler** üzerinden tanımlayan gelişmiş bir hibrit arama motorudur.

Standart görsel arama motorları sadece renklere odaklandığı için beyaz bir süt kutusu ile beyaz bir peynir paketini karıştırabilir. Bu sistem, **ResNet50** ile görselin derin özelliklerini çıkarırken **EasyOCR** ile ürün üzerindeki yazıları okuyarak bu sorunu aşar.

## ✨ Öne Çıkan Özellikler

* **Yüksek Hassasiyetli CNN:** ResNet50 mimarisi kullanılarak 2048 boyutlu derin özellik vektörü çıkarma.
* **OCR Entegrasyonu:** EasyOCR kütüphanesi ile ambalaj üzerindeki marka, ürün adı ve tip bilgilerini otomatik tanımlama.
* **Hibrit Skorlama Algoritması:** %70 görsel benzerlik ve %30 metin benzerliği ağırlıklı akıllı sıralama.
* **Hızlı Vektör Arama:** Facebook AI (Faiss) kütüphanesi ile milisaniyeler içinde binlerce ürün arasında tarama.
* **Modern Kontrol Paneli:** Bootstrap 5 ve FontAwesome ile zenginleştirilmiş kullanıcı dostu arayüz.

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python 3.x, Flask, SQLite
* **Yapay Zeka:** TensorFlow (ResNet50), EasyOCR
* **Vektör Veritabanı:** Faiss (Facebook AI Similarity Search)
* **Frontend:** HTML5, CSS3, Bootstrap 5



