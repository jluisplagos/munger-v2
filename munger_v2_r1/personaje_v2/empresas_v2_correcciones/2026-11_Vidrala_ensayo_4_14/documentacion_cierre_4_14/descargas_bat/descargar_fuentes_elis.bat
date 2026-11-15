@echo off
REM ===========================================================================================
REM  Munger V2 - Elis - descarga de las fuentes oficiales que faltan (14-nov-2026)
REM  Guarda los archivos en la carpeta ELIS\descargas_2026 (la carpeta ELIS ya esta compartida con
REM  la sesion) y escribe HUELLAS.txt con el SHA-256 de cada archivo. No modifica nada mas.
REM  Requiere Windows 10 o posterior (curl y certutil vienen con Windows).
REM ===========================================================================================
setlocal
set "DESTINO=C:\Users\jluis\Desktop\IDEAS DE INVERSION JOSE LUIS\INFORMACION ECONOMICA EMPRESAS\ELIS\descargas_2026"
if not exist "%DESTINO%" mkdir "%DESTINO%"
cd /d "%DESTINO%"
set "UA=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

echo Descargando el informe financiero semestral 2026 (ingles y frances)...
curl -L --fail -A "%UA%" -o "Elis_2026_half-year_financial_report_EN.pdf" "https://fr.elis.com/sites/fr.elis.com/files/2026/07/30/Elis%%20-%%202026%%20half-year%%20financial%%20report_0.pdf"
curl -L --fail -A "%UA%" -o "Elis_Rapport_financier_semestriel_2026_FR.pdf" "https://fr.elis.com/sites/fr.elis.com/files/2026/07/30/Elis%%20-%%20Rapport%%20financier%%20semestriel%%202026.pdf"

echo Descargando la presentacion de resultados del primer semestre de 2026...
curl -L --fail -A "%UA%" -o "Elis_H1_2026_results_presentation.pdf" "https://fr.elis.com/sites/fr.elis.com/files/2026/07/29/Elis%%20-%%20H1%%202026%%20results%%20presentation.pdf"

echo Descargando el comunicado de resultados anuales 2025...
curl -L --fail -A "%UA%" -o "Elis_Resultats_annuels_2025_communique.pdf" "https://fr.elis.com/sites/fr.elis.com/files/2026/03/12/20260311%%20-%%20Elis%%20-%%20R%%C3%%A9sultats%%20annuels%%202025_0.pdf"

echo Descargando el comunicado de resultados del primer semestre de 2026 (pagina web)...
curl -L --fail -A "%UA%" -o "Elis_H1_2026_results_comunicado.html" "https://www.globenewswire.com/news-release/2026/07/29/3335442/0/en/Elis-H1-2026-results.html"

echo Descargando los resultados de la conversion de las OCEANE 2029 (pagina web)...
curl -L --fail -A "%UA%" -o "Elis_OCEANE_2029_resultados_conversion.html" "https://mfn.se/all/a/elis/elis-announces-the-results-of-the-conversion-and-exchange-period-for-its-2029-oceanes-5b2a8d04"

echo Descargando el ajuste del ratio de conversion de las OCEANE 2029 (pagina web)...
curl -L --fail -A "%UA%" -o "Elis_OCEANE_2029_ajuste_ratio.html" "https://live.euronext.com/en/products/equities/company-news/2026-05-27-elis-adjustment-conversion-ratio-oceane-2029"

echo Descargando la lista de comunicados de Elis en Euronext (para localizar la declaracion de acciones al 30-09-2026)...
curl -L --fail -A "%UA%" -o "Elis_comunicados_Euronext.html" "https://live.euronext.com/en/listview/company-press-release/201058"

echo Calculando huellas SHA-256...
if exist HUELLAS.txt del HUELLAS.txt
for %%F in (*.pdf *.html) do (
  echo %%F>> HUELLAS.txt
  certutil -hashfile "%%F" SHA256 | findstr /v "hash CertUtil" >> HUELLAS.txt
)
echo.
echo Terminado. Archivos en: %DESTINO%
echo Si alguna descarga ha fallado, aparece arriba un error de curl; el resto sigue siendo valido.
pause
