import subprocess
import shutil
import os
import requests
import json
import argparse
import sys

# Başlangıçta boş tanımlıyoruz, main fonksiyonunda dolduracağız
AUTHORIZATION_TOKEN = ""

def check_dependencies():
    missing = []
    if shutil.which("ffmpeg") is None:
        missing.append("ffmpeg")
    
    if shutil.which("yt-dlp") is None:
        missing.append("yt-dlp")
        
    if missing:
        print(f"HATA: Aşağıdaki bağımlılıklar bulunamadı: {', '.join(missing)}")
        print("\nLütfen bu programları kurun ve PATH'inize ekleyin.")
        return False
    return True

def download_video(hls_url, output_filename, download_path):
    full_path = os.path.join(download_path, output_filename)
    print(f"STATUS:İndiriliyor: {output_filename}")
    
    try:
        # Anlık çıktıları C# tarafına iletmek için Popen kullanıyoruz
        process = subprocess.Popen(
            [
                "yt-dlp",
                "-f", "bestvideo+bestaudio/best",
                "-o", full_path,
                hls_url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # Çıktıyı bekle
        out, err = process.communicate()
        
        if process.returncode == 0:
            print(f"SUCCESS:Tamamlandı: {output_filename}")
            return True
        else:
            # yt-dlp bazen warningleri stderr'e yazar, her stderr hata değildir ama kontrol edelim
            print(f"ERROR:İndirme sırasında hata/uyarı: {err}")
            return False
            
    except Exception as e:
        print(f"ERROR:Kritik İndirme Hatası: {str(e)}")
        return False

def get_course_syllabus(course_id):
    url = f"https://www.btkakademi.gov.tr/api/service/v1/public/51/course/details/program/syllabus/{course_id}?language=tr"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR:Syllabus API hatası: {e}")
        return None

def start_course_delivery(course_id, program_id):
    # Global token değişkenini kullan
    url = f"https://www.btkakademi.gov.tr/api/service/v1/course/deliver/start/{course_id}"
    headers = {
        "Authorization": AUTHORIZATION_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"programId": program_id}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("remoteCourseReference")
    except requests.exceptions.RequestException as e:
        # 401 hatası token geçersiz demektir
        if hasattr(e, 'response') and e.response is not None and e.response.status_code == 401:
             print(f"ERROR:Yetkilendirme Hatası (Token geçersiz olabilir). ID: {course_id}")
        else:
             print(f"ERROR:Deliver start API hatası (course_id: {course_id}): {e}")
        return None

def get_hls_url(remote_course_reference):
    url = f"https://cinema8.com/api/v1/uscene/rawvideo/flavor/{remote_course_reference}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("hlsUrl")
    except requests.exceptions.RequestException as e:
        print(f"ERROR:Cinema8 API hatası (reference: {remote_course_reference}): {e}")
        return None

def sanitize_filename(filename):
    # Windows dosya isimlerinde yasaklı karakterleri temizle
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def main():
    # Windows konsolunda Türkçe karakter sorununu çözmek için
    sys.stdout.reconfigure(encoding='utf-8')

    # Argümanları tanımla
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, type=int, help="Kurs ID")
    parser.add_argument("--dir", required=True, type=str, help="İndirme Klasörü")
    parser.add_argument("--token", required=True, type=str, help="Auth Token")
    
    args = parser.parse_args()

    # Argümanları değişkenlere ata
    program_id = args.id
    download_dir = args.dir
    
    # Global token değişkenini güncelle
    global AUTHORIZATION_TOKEN
    AUTHORIZATION_TOKEN = args.token

    if not check_dependencies():
        exit(1)

    if not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
        except OSError as e:
            print(f"ERROR:Klasör oluşturulamadı: {e}")
            exit(1)
    
    print(f"INFO:Kurs müfredatı alınıyor (ID: {program_id})...")
    sys.stdout.flush() 
    
    syllabus_data = get_course_syllabus(program_id)
    if not syllabus_data:
        print("ERROR:Müfredat alınamadı! Kurs ID yanlış olabilir.")
        exit(1)
    
    all_courses = []
    for section in syllabus_data:
        section_title = section.get("title", "Bilinmeyen Bölüm")
        courses = section.get("courses", [])
        
        for course in courses:
            course["section_title"] = section_title
            all_courses.append(course)
    
    print(f"INFO:Toplam {len(all_courses)} video bulundu.")
    sys.stdout.flush()
    
    for idx, course in enumerate(all_courses, 1):
        course_id_item = course.get("id")
        course_title = course.get("title", "Bilinmeyen")
        section_title = course.get("section_title", "")
        
        # C# Progress Bar için format: PROGRESS:Mevcut/Toplam
        print(f"PROGRESS:{idx}/{len(all_courses)}")
        sys.stdout.flush()

        # Token ile video linkini al
        remote_ref = start_course_delivery(course_id_item, program_id)
        if not remote_ref:
            # Hata mesajı start_course_delivery içinde basılıyor
            continue
        
        hls_url = get_hls_url(remote_ref)
        if not hls_url:
            print(f"ERROR:HLS URL alınamadı: {course_title}")
            continue
        
        safe_title = sanitize_filename(course_title)
        safe_section = sanitize_filename(section_title)
        output_filename = f"{safe_section}_{safe_title}.mp4"
        
        # İndirmeyi başlat
        download_video(hls_url, output_filename, download_dir)
        sys.stdout.flush()

if __name__ == "__main__":
    main()