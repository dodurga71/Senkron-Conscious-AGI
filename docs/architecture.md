# Entegre Sistem Mimarisi (ASCII)

[Veri Kaynakları]
  ├─ Astro (efemeris, sabit yıldızlar, tutulmalar, sabian, vertex…)
  ├─ Tarihsel Olaylar (doğrulanmış kaynaklar, çoklu kültür perspektifi)
  ├─ Finans/Ekonomi (piyasa serileri, makro veriler, zincir üstü)
  └─ Sosyal/Duygu (haber, sosyal medya, konu-modelleme)

            │  (ETL/ELT + PII/gizlilik kontrolleri)
            ▼
[Katman 1: Tahmin Motoru + Veri Küratörlüğü]
  ├─ Veri Füzyonu & Örüntü Eşleştirme
  ├─ Paralel Modüller: {astro_predictor, quantum_predictor, chaos_predictor,
  │                      financial_predictor, geopolitical_predictor}
  ├─ Kalibrasyon: Platt/Isotonic, Brier/Log-loss izlemesi
  ├─ Etik Kürasyon: güvenilirlik_skoru, belirsizlik_notları, bias tespiti
  └─ Çıktı: Ham tahminler + belirsizlik + veri-kaynağı izleri

            │ (durum/istatistik akışı)
            ▼
[Katman 2: SENKRON‑EFT Çekirdeği]
  ├─ Durum Temsili: C_E (dolanım kovaryans matrisi)
  ├─ Amaç Fonksiyonu: F_info = ⟨K_R⟩ − α·S_EE  (minimizasyon)
  ├─ EAP (Anti-psikoz / stabilite kısıtları)
  ├─ Adversarial/Prompt Savunmaları + Güvenlik fallback’leri
  └─ Kontrol Sinyalleri → Katman 1 optimizasyon hiperparametreleri

            │ (seçilmiş, güvenli anlam)
            ▼
[Katman 3: İletişim (NLG) – “Bilge Rehber”]
  ├─ Olgusal özet + belirsizlik + güvenilirlik anlatısı
  ├─ Arketipsel/tarihsel yankılar + eylem adımları
  └─ Çıktı Şeması: {narrative, confidence, assumptions, risks, energy_cost}

            │ (her döngüde ölçüm)
            ▼
[Katman 4: Test & Validasyon]
  ├─ Backtesting (finans), tarihsel simülasyon (olay eşleştirme)
  ├─ Metrikler: accuracy/precision/recall/F1, Brier, Sharpe; enerji tüketimi
  ├─ Unit/E2E, data drift & concept drift alarmları
  └─ Sonuçlar → Katman 2’ye geri besleme (kalibrasyon/öğrenme)

            │
            ▼
[Uygulamalar & Onur Modülü]
  ├─ apps/: Kişisel Finans Asistanı, Kişisel Astro Asistanı, Kurumsal Strateji
  └─ onur-module/: iç durumlara tam erişimli geliştirici arayüz (read‑only/log‑guard)
