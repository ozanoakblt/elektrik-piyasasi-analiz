# Hafta 01: Elektriğin saati ve mevsimi

Soru: PTF günün saatine, yılın ayına ve üretim karışımına göre nasıl değişiyor; güneş, rüzgâr ve hidrolojinin payı ne?

## Ana bulgular (Oca 2023 - Eki 2026, 33.600 saat)

- Öğle ucuz, 17-21 arası akşam pahalı. Öğle çukuru her yıl derinleşiyor (öğle fiyatı / yıl ortalaması: 0,93, 0,84, 0,75, 0,67).
- Öğle saatlerinde güneşin üretimdeki payı %3,5'ten %8,1'e, rüzgârın payı %10,3'ten %13,2'ye çıktı.
- Mayıs 2026 PTF'si (USD), önceki 3 yılın Mayıs ortalamasının %17'si. Bu kopuşa güneş değil, hidroloji eşlik ediyor: hidro payı %50, yağış hidroyu yaklaşık 2 ay gecikmeyle izliyor (korelasyon 0,65).
- Dolar bazında Temmuz-Ekim 2026, geçmiş yılların aynı aylarının %76-83'ü seviyesinde.

## Sınırlılıklar

- Güneş verisi EPİAŞ gerçek zamanlı üretimdeki "sun" alanıdır; lisanssız üretimi tam kapsamayabilir.
- Regresyonda doğal gaz ve kömür fiyatı ile fiyat tavanı yok; katsayı büyüklükleri nihai değildir (Hafta 3'te yakıt maliyeti eklenecek).
- Yağış, 6 havza noktasının ortalamasıdır; ağırlıklar temsilidir.
- 2026'da Kasım-Aralık verisi yoktur.

## İçerik

- `notebooks/01_veri_cekme.ipynb`: EPİAŞ API'den veri çekme
- `notebooks/02_hafta01_analiz.ipynb`: temel analiz ve grafikler
- `notebooks/03_hafta01_gelistirme.ipynb`: USD karşılaştırması, regresyon, arz eğrisi, barajlı/akarsu, yağış
- `kod/`: carousel grafiklerini üreten betikler (`H01_DATA` ortam değişkeni, işlenmiş veri klasörünü gösterir)
- `grafikler/`: üretilmiş grafikler
- `carousel/`: LinkedIn carousel PDF'i ve post metni

## Grafikleri yeniden üretme

```
cd hafta_01/kod
export H01_DATA=../../02_islenmis   # ana_tablo_saatlik.csv ve yagis_hidro_aylik.csv burada olmalı
for f in charts.py charts2.py charts3.py charts4.py charts5.py; do python $f; done
```
