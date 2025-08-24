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
## Mermaid Diyagramı

```mermaid
flowchart TB
  subgraph Sources[Veri Kaynakları]
    A1[Astro]
    A2[Tarihsel]
    A3[Finans/Ekonomi]
    A4[Sosyal/Duygu]
  end

  subgraph L1[Katman 1: Tahmin Motoru + Veri Küratörlüğü]
    L1A[Çoklu Veri Füzyonu]
    L1B[Paralel Modüller]
    L1C[Kalibrasyon]
    L1D[Etik Kürasyon]
  end

  subgraph L2[Katman 2: SENKRON-EFT Çekirdeği]
    L2A[C_E Durum Temsili]
    L2B[F_info Minimizasyonu]
    L2C[EAP Stabilite & Güvenlik]
  end

  subgraph L3[Katman 3: İletişim (NLG)]
    L3A[Bilge Rehber Anlatı]
  end

  subgraph L4[Katman 4: Test & Validasyon]
    L4A[Backtesting/Simülasyon]
    L4B[Metrikler & Enerji]
  end

  A1-->L1A
  A2-->L1A
  A3-->L1A
  A4-->L1A
  L1A-->L1B-->L1C-->L1D-->L2A-->L2B-->L3A
  L2C-->L1B
  L4A-->L1B
  L4B-->L2B
  L3A-->|çıktılar|EndUser[(Uygulamalar)]

