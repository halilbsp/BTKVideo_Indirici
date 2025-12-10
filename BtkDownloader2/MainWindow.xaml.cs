using System.Diagnostics;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace BtkDownloader
{
    public partial class MainWindow : Window
    {
        private bool isDarkTheme = false;

        public MainWindow()
        {
            InitializeComponent();
        }

        // 1. Klasör Seçme İşlemi
        private void BtnSelectFolder_Click(object sender, RoutedEventArgs e)
        {
            // .NET Core/5/6+ WPF projelerinde Microsoft.Win32.OpenFolderDialog kullanılabilir
            var dialog = new Microsoft.Win32.OpenFolderDialog();
            if (dialog.ShowDialog() == true)
            {
                txtFolderPath.Text = dialog.FolderName;
            }
        }

        // 2. Başlat Butonu
        private async void BtnStart_Click(object sender, RoutedEventArgs e)
        {
            string courseId = txtCourseId.Text;
            string outputDir = txtFolderPath.Text;

            // XAML'e eklediğimiz txtToken kutusundan veriyi alıyoruz
            string token = txtToken.Text.Trim();

            if (string.IsNullOrEmpty(courseId) || string.IsNullOrEmpty(outputDir) || string.IsNullOrEmpty(token))
            {
                MessageBox.Show("Lütfen Kurs ID, Klasör ve Token alanlarını doldurun.");
                return;
            }

            // Kullanıcı "Bearer " yazmayı unuttuysa biz ekleyelim
            if (!token.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase))
            {
                token = "Bearer " + token;
            }

            btnStart.IsEnabled = false;
            txtLogs.Clear();
            Log("İşlem başlatılıyor...");

            // Token'ı fonksiyona iletiyoruz
            await RunPythonScript(courseId, outputDir, token);

            btnStart.IsEnabled = true;
            Log("İşlem bitti.");
        }

        // 2. PYTHON ÇALIŞTIRMA FONKSİYONU 
        private async Task RunPythonScript(string id, string path, string token)
        {
            await Task.Run(() =>
            {
                try
                {
                    ProcessStartInfo start = new ProcessStartInfo();
                    start.FileName = "python";

                    // HATA BURADA ÇÖZÜLÜYOR:
                    // Python'a --token argümanını ekleyerek gönderiyoruz.
                    // Token içinde boşluklar olduğu için (Bearer ...) tırnak içine (\" \") alıyoruz.
                    start.Arguments = $"main.py --id {id} --dir \"{path}\" --token \"{token}\"";

                    start.UseShellExecute = false;
                    start.RedirectStandardOutput = true;
                    start.RedirectStandardError = true;
                    start.CreateNoWindow = true;
                    start.StandardOutputEncoding = System.Text.Encoding.UTF8;

                    using (Process process = Process.Start(start))
                    {
                        while (!process.StandardOutput.EndOfStream)
                        {
                            string line = process.StandardOutput.ReadLine();
                            if (!string.IsNullOrEmpty(line))
                            {
                                Dispatcher.Invoke(() => ParseOutput(line));
                            }
                        }

                        string err = process.StandardError.ReadToEnd();
                        if (!string.IsNullOrEmpty(err))
                            Dispatcher.Invoke(() => Log("PYTHON ERROR: " + err));

                        process.WaitForExit();
                    }
                }
                catch (Exception ex)
                {
                    Dispatcher.Invoke(() => Log($"KRİTİK HATA: {ex.Message}"));
                }
            });
        }

       

        // 4. Python Çıktısını İşleme (Log ve Progress)
        private void ParseOutput(string line)
        {
            if (line.StartsWith("PROGRESS:"))
            {
                // Format: PROGRESS:5/45
                try
                {
                    string[] parts = line.Split(':')[1].Split('/');
                    double current = double.Parse(parts[0]);
                    double total = double.Parse(parts[1]);
                    progressBar.Maximum = total;
                    progressBar.Value = current;
                    lblStatus.Text = $"İndiriliyor: {current} / {total}";
                }
                catch { }
            }
            else if (line.StartsWith("INFO:"))
            {
                Log("[BİLGİ] " + line.Substring(5));
            }
            else if (line.StartsWith("STATUS:"))
            {
                Log("[DURUM] " + line.Substring(7));
            }
            else
            {
                Log(line);
            }
        }

        private void Log(string message)
        {
            txtLogs.AppendText($"{DateTime.Now:HH:mm:ss} - {message}\n");
            txtLogs.ScrollToEnd();
        }

        // 5. Light/Dark Theme Değiştirme
        private void ToggleTheme_Click(object sender, RoutedEventArgs e)
        {
            isDarkTheme = !isDarkTheme;

            if (isDarkTheme)
            {
                // Koyu Tema
                ToggleTheme.Content = "☀️";
                this.Resources["WindowBackgroundBrush"] = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#1E1E1E"));
                this.Resources["TextBrush"] = new SolidColorBrush(Colors.White);
                this.Resources["CardBackgroundBrush"] = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#252526"));
                this.Resources["BorderBrush"] = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#3E3E42"));
            }
            else
            {
                ToggleTheme.Content = "🌙";
                this.Resources["WindowBackgroundBrush"] = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#F5F5F5"));
                this.Resources["TextBrush"] = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#333333"));
                this.Resources["CardBackgroundBrush"] = new SolidColorBrush(Colors.White);
                this.Resources["BorderBrush"] = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#DDDDDD"));
            }
        }
    }
}