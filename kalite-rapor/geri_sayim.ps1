$Host.UI.RawUI.WindowTitle = "Veri toplama - geri sayim"
# Bu pencere acik oldugu surece bilgisayarin uykuya gecmemesini iste (ekran yine kapanabilir).
# Ayar degistirmez; pencere kapaninca istek kendiliginden biter.
Add-Type -Namespace Uyku -Name Engel -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
[void][Uyku.Engel]::SetThreadExecutionState([uint32]"0x80000001")   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
$cache = "C:\Users\ALPTEK~1\AppData\Local\Temp\claude\3277f1e1c3eb6939\9afdeac4-3302-4312-8507-8157b956a04b\scratchpad\kbu_cache"
$toplam = 14912
$gecmis = New-Object System.Collections.Generic.List[object]
while ($true) {
    $n = (Get-ChildItem -Path $cache -Filter "course_*.html" -File).Count
    $simdi = Get-Date
    $gecmis.Add([pscustomobject]@{ t = $simdi; n = $n })
    while ($gecmis.Count -gt 40) { $gecmis.RemoveAt(0) }   # son ~20 dakika
    $calisiyor = [bool](Get-Process -Name py, python -ErrorAction SilentlyContinue)
    Clear-Host
    Write-Host ""
    Write-Host "  KARABUK BILGI PAKETI - VERI TOPLAMA" -ForegroundColor Cyan
    Write-Host ""
    $yuzde = [math]::Round(100 * $n / $toplam, 1)
    $dolu = [int][math]::Floor($yuzde / 2.5)
    Write-Host ("  [" + ("#" * $dolu) + ("." * (40 - $dolu)) + "]  %" + $yuzde)
    Write-Host ""
    Write-Host ("  Inen ders     : {0:N0} / {1:N0}" -f $n, $toplam)
    Write-Host ("  Kalan ders    : {0:N0}" -f ($toplam - $n))
    if ($gecmis.Count -ge 3) {
        $ilk = $gecmis[0]
        $dk = ($simdi - $ilk.t).TotalMinutes
        $hiz = ($n - $ilk.n) / [math]::Max($dk, 0.01)
        if ($hiz -gt 0) {
            $kalanDk = ($toplam - $n) / $hiz
            $ks = [timespan]::FromMinutes($kalanDk)
            Write-Host ("  Hiz           : {0:N0} ders / dakika" -f $hiz)
            Write-Host ("  Kalan sure    : {0} saat {1} dakika" -f [int][math]::Floor($ks.TotalHours), $ks.Minutes) -ForegroundColor Yellow
            Write-Host ("  Tahmini bitis : {0:HH:mm}" -f $simdi.AddMinutes($kalanDk)) -ForegroundColor Green
        } else {
            Write-Host "  Hiz           : son dakikalarda yeni ders inmedi" -ForegroundColor Red
        }
    } else {
        Write-Host "  Kalan sure    : hesaplaniyor (1-2 dakika)..."
    }
    Write-Host ""
    $log = "C:\Users\ALPTEK~1\AppData\Local\Temp\claude\3277f1e1c3eb6939\9afdeac4-3302-4312-8507-8157b956a04b\scratchpad\topla3.log"
    $bitti = (Test-Path $log) -and (Select-String -Path $log -Pattern "^BITTI" -Quiet)
    if ($bitti -and -not $calisiyor) {
        Write-Host "  BITTI! Veri dosyasi yazildi." -ForegroundColor Green
        Write-Host "  Bilgisayar 2 dakika icinde KAPANACAK. Iptal icin: Baslat > 'cmd' yaz > shutdown /a" -ForegroundColor Yellow
        shutdown.exe /s /t 120 /c "Veri toplama bitti. Bilgisayar 2 dakika icinde kapanacak. Iptal: shutdown /a"
        break
    }
    Write-Host "  Bitince       : bilgisayar KENDINI KAPATACAK (2 dk uyari ile)" -ForegroundColor Yellow
    if (-not $calisiyor) { Write-Host "  UYARI: toplama programi calismiyor gorunuyor." -ForegroundColor Red }
    Write-Host "  Uyku engeli   : ACIK (bu pencere acikken bilgisayar uyumaz)" -ForegroundColor Green
    Write-Host ("  Son guncelleme: {0:HH:mm:ss}  (30 sn'de bir yenilenir; bu pencereyi kapatmak toplamayi durdurmaz ama uyku engelini kaldirir)" -f $simdi) -ForegroundColor DarkGray
    Start-Sleep -Seconds 30
}
[void][Uyku.Engel]::SetThreadExecutionState([uint32]"0x80000000")   # uyku engelini kaldir
Read-Host "Kapatmak icin Enter"
