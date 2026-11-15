@echo off
REM ===========================================================================================
REM  Munger V2 - Ahold Delhaize (empresa de reserva) - informes anuales 2016-2018 (14-nov-2026)
REM  La carpeta tiene los informes 2019-2025; para la Historia de 10 anos faltan 2016, 2017 y 2018.
REM  Fuente: web oficial de Ahold Delhaize (media.aholddelhaize.com, enlaces de sus paginas de
REM  informes anuales). Incluye el folleto oficial de 2018 reexpresado por la NIIF 16 (la NIIF 16
REM  entra en 2019). Guarda en KONINKLIJKE AHOLD DELHAIZE\descargas_2026 con HUELLAS.txt.
REM  Borra lo que no sea un PDF de verdad. No modifica nada mas.
REM ===========================================================================================
setlocal
set "DESTINO=C:\Users\jluis\Desktop\IDEAS DE INVERSION JOSE LUIS\INFORMACION ECONOMICA EMPRESAS\KONINKLIJKE AHOLD DELHAIZE\descargas_2026"
if not exist "%DESTINO%" mkdir "%DESTINO%"
cd /d "%DESTINO%"
set "UA=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
echo Descargando el informe anual 2016...
curl -L --fail -A "%UA%" -o "AD_annual-report-2016.pdf" "https://media.aholddelhaize.com/media/ycfni1cc/ahold-delhaize-annual-report-2016.pdf"
echo Descargando el informe anual 2017...
curl -L --fail -A "%UA%" -o "AD_annual-report-2017.pdf" "https://media.aholddelhaize.com/media/wsafdah4/annual-report-2017.pdf"
echo Descargando el informe anual 2018...
curl -L --fail -A "%UA%" -o "AD_annual-report-2018.pdf" "https://media.aholddelhaize.com/media/jr2l1zc2/annual-report-2018.pdf"
echo Descargando el folleto de 2018 reexpresado por la NIIF 16...
curl -L --fail -A "%UA%" -o "AD_2018-restatement-booklet-IFRS16.pdf" "https://www.aholddelhaize.com/media/8952/2018-restatement-booklet-ifrs-16-dated-march-25-2019.pdf"
echo Comprobando que son PDF de verdad (no paginas web)...
for %%F in (AD_*.pdf) do (
  findstr /m /b "%%PDF" "%%F" >nul || (echo   %%F NO es un PDF: se borra & del "%%F")
)
echo Calculando huellas SHA-256...
if exist HUELLAS.txt del HUELLAS.txt
for %%F in (AD_*.pdf) do (
  echo %%F>> HUELLAS.txt
  certutil -hashfile "%%F" SHA256 | findstr /v "hash CertUtil" >> HUELLAS.txt
)
echo.
echo Terminado. Archivos en: %DESTINO%
pause
