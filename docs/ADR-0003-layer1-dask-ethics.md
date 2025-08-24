# ADR-0003: Katman-1 Dask + Etik Kürasyon
## Karar
- JSON akışları Dask Bag ile parçalı işlenecek.
- Minimum sahalar: {id, ts}; eksikler elenir.
- Normalizasyon: min-max (0..1) alan bazında; NaN/None korunur.
## Gerekçeler
- IO ve cpu-bound iş yüklerinde ölçeklenebilirlik.
- Etik/güvenilirlik kuralları için merkezi “kurasyon” katmanı.
