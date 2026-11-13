# Hafta 02: Aylık Rapor #1, Ekim 2026

Soru: Ekim 2026'da fiyatı hacim mi taşıdı, maliyet mi?

## Ana bulgular

- Ekim 2026 PTF'si 59,3 USD/MWh ile son dört Ekim'in en düşüğü. Tüketim en yüksek, termik santrallere kalan yük en düşük (hidro payı %29, Ekim 2025: %11).
- Eylül → Ekim 2026: termik yük azaldığı için hacim fiyatı 2,4 USD aşağı çekti, ama aynı yükte fiyat 3,0 USD yükseldi (eğri kayması).
- Sekiz olası neden test edildi. Güçlü olanlar: ithal kömür hazır kapasitesinin düşmesi (9,3 → 8,1 GW, ay sonunda 5,9 GW) ve spot gazın %14 pahalanması. BOTAŞ tarifesi, kur ve dış ticaret açıklamıyor.
- Akşam saatlerinin %27'sinde PTF tavanda (Eylül: %3).

## Sınırlar

- Arz eğrisi gerçekleşen saatlerden kestirildi; termik yük yaklaşık bir büyüklüktür.
- Ekim 2025 kıyası nicel verilmedi (fiyat tavanı 3.400 → 4.500 TL değişti).
- Baraj doluluk geçmişi ve ithal kömür kapasite kaybının nedeni (bakım / arıza) doğrulanamadı.

## İçerik

- `notebooks/01_veri_cekme.ipynb`: PTF, üretim, tüketim, SMF, sistem yönü, GİP
- `notebooks/02_analiz.ipynb`: ay kartı, arz eğrisi, ayrıştırma, neden testleri
- `notebooks/03_ek_veri.ipynb`: emre amade kapasite, arıza-bakım bildirimleri, spot gaz, baraj doluluk
- `kaynak/botas_tarife.csv`: BOTAŞ elektrik üretim amaçlı gaz tarifesi (resmi tarifelerden derlendi)
- `rapor/`: PDF rapor ve LinkedIn metni
