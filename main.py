import streamlit as st
import os
import shutil
from engine import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz # Metin benzerliği için kütüphane
from PIL import Image

# 1. Klasör Yapısını Otomatik Oluştur
folders = ['database', 'uploads', 'violations']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

st.set_page_config(page_title="Market AI Pro", layout="wide")
st.title("🛒 Hibrit Ürün Karşılaştırma ve Stok Kontrolü")

# Yan Menü: Veritabanı Özeti
st.sidebar.header("Depo Durumu")
db_images = os.listdir("database")
st.sidebar.write(f"Sistemde kayıtlı ürün sayısı: {len(db_images)}")

# Ana Ekran: Dosya Yükleme ve Metin Girişi
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    uploaded_file = st.file_uploader("Ürün fotoğrafını seçin...", type=["jpg", "png", "jpeg"])
with col_input2:
    user_input_name = st.text_input("Ürün adını girin (Opsiyonel):", placeholder="Örn: Eti Burçak")

if uploaded_file is not None:
    # Geçici kaydet
    temp_path = os.path.join("uploads", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    c_left, c_right = st.columns([1, 2])
    
    with c_left:
        st.image(uploaded_file, caption="Sorgulanan Ürün", use_container_width=True)

    with st.spinner('Hibrit analiz yapılıyor (Görsel + Metin)...'):
        target_vec = get_embedding(temp_path).reshape(1, -1)
        db_path = "database"
        results = []
        
        if len(os.listdir(db_path)) == 0:
            st.info("Veritabanı boş. İlk ürünü ekleyebilirsiniz.")
        else:
            for img_name in os.listdir(db_path):
                current_img_path = os.path.join(db_path, img_name)
                
                # A. GÖRSEL SKOR
                db_vec = get_embedding(current_img_path).reshape(1, -1)
                visual_score = cosine_similarity(target_vec, db_vec)[0][0]
                
                # B. METİN SKORU (Dosya adı ve Kullanıcı girişi kıyası)
                clean_db_name = os.path.splitext(img_name)[0]
                if user_input_name:
                    # Kullanıcı isim girdiyse hem girilenle hem dosya adıyla bak
                    text_score = fuzz.token_sort_ratio(user_input_name.lower(), clean_db_name.lower()) / 100
                else:
                    text_score = visual_score # İsim girilmediyse görseli baz al
                
                # C. HİBRİT SKOR (%60 Görsel, %40 Metin)
                hybrid_score = (visual_score * 0.6) + (text_score * 0.4)
                results.append((img_name, visual_score, text_score, hybrid_score, current_img_path))
            
            # Hibrit skora göre sırala
            results.sort(key=lambda x: x[3], reverse=True)

    with c_right:
        if results:
            top_name, v_s, t_s, h_s, top_path = results[0]
            
            st.subheader("Analiz Özeti")
            # Durum Belirleme
            if h_s > 0.88:
                st.error(f"⚠️ STOKTA MEVCUT: %{h_s*100:.1f} benzerlik ile bu ürün zaten var.")
            elif h_s > 0.60:
                st.warning(f"🧐 BENZER ÜRÜN: %{h_s*100:.1f} benzerlik. Varyant (Çilekli/Vanilyalı) olabilir.")
            else:
                st.success(f"✅ YENİ ÜRÜN: Sistemde benzer bir ürün bulunamadı.")
                
                new_name = st.text_input("Kaydedilecek Ürün Adı:", value=uploaded_file.name)
                if st.button("Veritabanına Kaydet"):
                    shutil.copy(temp_path, os.path.join("database", new_name))
                    st.balloons()
                    st.rerun()

            st.divider()
            
            # Galeri Kısmı
            st.write("🔍 **En Yakın 3 Eşleşme (Görsel & Metin Detaylı)**")
            cols = st.columns(3)
            for idx, (name, v_score, t_score, h_score, path) in enumerate(results[:3]):
                with cols[idx]:
                    st.image(path, use_container_width=True)
                    st.caption(f"**{name}**")
                    st.caption(f"Görsel: %{v_score*100:.0f} | Metin: %{t_score*100:.0f}")
                    st.write(f"**Hibrit: %{h_score*100:.1f}**")