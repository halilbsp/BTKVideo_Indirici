# 🎓 BTK Akademi Course Downloader 📥

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff) ![C#](https://custom-icon-badges.demolab.com/badge/C%23-%23239120.svg?logo=cshrp&logoColor=white)

**BTK Akademi** üzerindeki kursları, video kalitesinden ödün vermeden yerel diskinize indirmeyi sağlayan, modern arayüze sahip bir masaüstü uygulamasıdır. 🚀

Bu proje, **Python**'un güçlü scraping yeteneklerini (yt-dlp & ffmpeg) 🐍, **C# WPF**'in modern ve kullanıcı dostu arayüzü 💻 ile birleştiren hibrit bir yapıdadır.

![Ekran Görüntüsü](https://iili.io/fRkJtVf.png)




## ✨ Özellikler

* 🎨 **Modern UI:** WPF ile hazırlanmış, **Light/Dark 🌙/☀️** tema desteği sunan şık arayüz.
* 🔑 **Token Girişi:** Yetki gerektiren kurslar için kolay `Authorization Token` desteği.
* 📦 **Akıllı İndirme:** Kurs müfredatını tarar, bölümleri klasörler 📂, videoları ise sıralı şekilde isimlendirerek 🎞️ indirir.
* 📊 **Canlı Takip:** İndirme durumunu anlık **Progress Bar** üzerinden izleyin.
* 📝 **Detaylı Log:** Arka planda çalışan Python işlemlerini anlık olarak ekrana yansıtır.
* 🛡️ **Hata Yakalama:** Eksik dosya veya geçersiz token durumlarında kullanıcı dostu uyarılar verir.



## 🛠️ Gereksinimler (Prerequisites)

Projeyi sorunsuz çalıştırmak için bilgisayarınızda aşağıdakilerin yüklü olması gerekir:

1.  🐍 **Python 3.x:** [Python İndir](https://www.python.org/downloads/) (Kurulum sırasında **"Add to PATH"** kutucuğunu işaretlemeyi unutmayın!)
2.  👾 **.NET 8.0 Runtime:** [Windows Desktop Runtime İndir](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Ayrıca Python için gerekli kütüphaneyi terminalde şu komutla yükleyin:
```bash
pip install requests
```


## ⚙️ Kurulum (Installation)
Uygulamanın çalışabilmesi için ffmpeg ve yt-dlp araçlarına ihtiyacı vardır. Lisans kuralları gereği bu dosyalar projeye dahil edilmemiştir, lütfen aşağıdaki adımları takip edin:

1.**Projeyi İndirin**
Bu repoyu bilgisayarınıza klonlayın veya ZIP olarak indirip klasöre çıkartın.

2. **Araçları İndirin**
Aşağıdaki linklerden gerekli .exe dosyalarını indirin:
```bash
  📥 yt-dlp: GitHub Release Sayfası (yt-dlp.exe dosyasını indirin)
  
  🎞️ ffmpeg: Gyan.dev FFmpeg Builds (ffmpeg-release-essentials.zip içindeki bin klasöründen ffmpeg.exe dosyasını alın)
```
3. **Dosyaları Yerleştirin**
İndirdiğiniz yt-dlp.exe ve ffmpeg.exe dosyalarını, uygulamanın .exe dosyasının bulunduğu klasöre (genellikle bin/Debug/net8.0-windows/) kopyalayın.

  * 📂 Klasör Yapınız Şöyle Görünmeli:
```bash
    BtkDownloader/
    │
    ├── 🚀 BtkDownloader.exe    (Uygulama)
    ├── 📄 main.py              (Python Scripti)
    ├── ⚙️ yt-dlp.exe           <-- Buraya atılacak
    └── ⚙️ ffmpeg.exe           <-- Buraya atılacak

```

 ## 📖 Nasıl Kullanılır?
1. 🔍 **Kurs ID'sini Bulun:** Kurs sayfasındaki URL'den ID numarasını alın (Örn: `.../details/14301` -> ID: `14301`).
2. 🍪 **Token'ı Kapın:**
   * Tarayıcıda `F12` tuşuna basıp **Network** (Ağ) sekmesine gidin.
   * Sayfayı yenileyip (`F5`) herhangi bir isteği yakalayın.
   * `Request Headers` içindeki **Authorization** (Bearer...) değerini kopyalayın.
3. 🖱️ **Uygulamaya Girin:** ID ve Token'ı yapıştırın, indirme klasörünü 📂 seçin.
4. ▶️ **Başlatın:** Arkanıza yaslanın, gerisini programa bırakın. ☕

## ⚠️ Yasal Uyarı
Bu proje tamamen eğitim ve kişisel gelişim amaçlı 🎓 geliştirilmiştir. İndirilen içeriklerin tüm telif hakları BTK Akademi'ye ve ilgili eğitmenlere aittir. İçeriklerin izinsiz paylaşılması veya ticari kullanımı yasaktır. Lütfen emeğe saygı gösterelim. 🙏


### 👨‍💻 Geliştirici Ekibi 

Bu proje, aşağıdaki ekip tarafından iş birliği ile geliştirilmiştir:

* 🐍 **Halil BAŞPINAR (Python):**  [Halil](https://github.com/halilbsp)
* 🎨 **Selahattin Eyüp ALTAŞ (C# WPF):**  [Mikleo18](https://github.com/Mikleo18)
* 🕷️ **Hüseyin GENCAN:**  [Hüseyin](https://github.com/AmourHG)

*Mehmet Akif Ersoy Üniversitesi - Bilişim Sistemleri ve Teknolojileri*


