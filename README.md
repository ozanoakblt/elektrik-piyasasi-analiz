# Türkiye Elektrik Piyasası: Haftalık Analiz Serisi

Türkiye elektrik piyasasını EPİAŞ Şeffaflık Platformu verisiyle her hafta tek bir soru üzerinden inceleyen açık bir analiz serisi. Her hafta bir öncekinin üzerine kurulur; kod, grafikler, rapor ve yöntem notları burada.

> Bu çalışmalar kişisel çalışmamdır; çalıştığım kurumu veya müşterilerini temsil etmez. Yatırım, ticaret ya da hukuki tavsiye değildir. Sonuçlar ilişkidir, nedensellik iddiası taşımaz.

## Seri

Müfredatın tamamı: [`docs/Mufredat.pdf`](docs/Mufredat.pdf) (6 modül, 24 hafta).

| Hafta | Soru | Rapor | Kod |
|---|---|---|---|
| 01 | Elektriğin saati ve mevsimi: PTF günün saatine, ayına ve üretim karışımına göre nasıl değişiyor? | [Carousel](hafta_01/carousel/Hafta01_Carousel.pdf) | [notebooks](hafta_01/notebooks) |
| 02 | Aylık Rapor #1, Ekim 2026: fiyatı hacim mi taşıdı, maliyet mi? | [Rapor](hafta_02/rapor/Hafta02_Ekim2026_Rapor.pdf) | [notebooks](hafta_02/notebooks) |
| 03 | Bir MWh'nin yolculuğu: elektriğin ne kadarı PTF'den fiyatlanıyor? | [Rapor](hafta_03/rapor/Hafta03_MWh_Yolculugu.pdf) | [notebooks](hafta_03/notebooks) |
| 04 | Merit order'ı veriden kurmak: GÖP arz-talep eğrileri | Yakında | |

## Veri

- Kaynak: EPİAŞ Şeffaflık Platformu API (kişisel hesapla), Open-Meteo, BOTAŞ tarifeleri, DSİ.
- **EPİAŞ verisi bu repoda yoktur.** Her haftanın `01_veri_cekme.ipynb` dosyası veriyi kendi EPİAŞ hesabınızla indirir. Kaynakların kullanım koşullarına uymak kullanıcının sorumluluğundadır.
- Kullanıcı adı ve şifre koda yazılmaz; çalıştırma anında sorulur ya da `EPIAS_USER` / `EPIAS_PASS` ortam değişkenlerinden okunur.
- Hafta 3'ten itibaren API çağrıları açık kaynak [`eptr2`](https://github.com/tideseed/eptr2) paketiyle yapılır.

## Çalıştırma

```
pip install -r requirements.txt
```

Notebook'lar yerelde haftalık klasörlerle (`Hafta_01/`, `Hafta_02/`, ...) yan yana çalışacak şekilde yazıldı; sonraki haftalar önceki haftanın işlenmiş tablosunu `../Hafta_0X/02_islenmis/` yolundan okur. Her haftada önce `01_veri_cekme`, sonra `02_analiz` çalıştırılır.

## Yöntem ilkeleri

- Fiyatlar USD bazında ve aynı ay karşılaştırmasıyla kıyaslanır; nominal TL düzeyleri yıllar arasında doğrudan karşılaştırılmaz.
- Her iddia veriyle test edilir; test edilemeyen yazılmaz ya da "test edilemedi" diye belirtilir.
- Olası nedenler tek tek elenir; sonuçlar olağanüstü dönemler çıkarılarak tekrarlanır.
- Her raporun son sayfasında yöntem ve sınırlar yer alır.
