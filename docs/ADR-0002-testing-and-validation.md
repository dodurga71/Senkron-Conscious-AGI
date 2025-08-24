# ADR-0002: Test, Backtesting ve Enerji Ölçümü Planı

## Kapsam
- Birim testleri (pytest)
- Entegrasyon: e2e demo
- Backtesting: veri füzyonu → tahmin → metrikler
- Enerji/performans: zaman ve (mümkünse) sistem ölçümleri

## Metrikler
- Doğruluk/MAE/MAPE (probleme göre seçilir)
- Kalibrasyon kontrolü (ileride Brier/Platt)
- Enerji: başlangıçta zaman tabanlı ölçümler (CPU zamanı). Gerektiğinde psutil entegrasyonu.

## Çıktılar
- ./coverage.xml (CI artifact)
- ./outputs/ ve ./logs/ (e2e artifact)
