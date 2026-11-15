@echo off
REM ===========================================================================================
REM  Munger V2 - Elis - declaracion oficial del numero de acciones y derechos de voto (14-nov-2026)
REM  Hace falta para comprobar Analisis!C55 (acciones) y C41 (capitalizacion) del expediente Elis:
REM  el revisor independiente encontro que C55 usa la media diluida de 2025 (259,08 M) y no las
REM  acciones vigentes tras la recompra y la conversion de las OCEANE (7-oct-2026).
REM  Guarda los archivos en ELIS\descargas_2026_acciones y escribe HUELLAS.txt (SHA-256).
REM  No modifica nada mas. Requiere Windows 10 o posterior (curl y certutil vienen con Windows).
REM ===========================================================================================
setlocal
set "DESTINO=C:\Users\jluis\Desktop\IDEAS DE INVERSION JOSE LUIS\INFORMACION ECONOMICA EMPRESAS\ELIS\descargas_2026_acciones"
if not exist "%DESTINO%" mkdir "%DESTINO%"
cd /d "%DESTINO%"
set "UA=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

echo Descargando la declaracion de acciones y derechos de voto a 31-10-2026 (pagina web, 12-nov-2026)...
curl -L --fail -A "%UA%" -o "Elis_acciones_derechos_voto_31-10-2026.html" "https://www.globenewswire.com/news-release/2026/11/12/3401906/0/en/elis-disclosure-of-the-number-of-shares-forming-the-capital-and-of-the-total-number-of-voting-rights-as-of-31-10-2026.html"

echo Descargando el PDF adjunto de esa declaracion...
curl -L --fail -A "%UA%" -o "Elis_acciones_derechos_voto_31-10-2026.pdf" "https://ml-eu.globenewswire.com/Resource/Download/069e702d-074b-4e1f-bfed-27c7f4d0e60b"

echo Descargando la declaracion a 30-09-2026 (pagina web, para contrastar el mes anterior)...
curl -L --fail -A "%UA%" -o "Elis_acciones_derechos_voto_30-09-2026.html" "https://www.globenewswire.com/news-release/2026/10/14/3380822/0/en/elis-disclosure-of-the-number-of-shares-forming-the-capital-and-of-the-total-number-of-voting-rights-as-of-30-09-2026.html"

echo Comprobando que el PDF es un PDF de verdad...
findstr /m /b "%%PDF" "Elis_acciones_derechos_voto_31-10-2026.pdf" >nul 2>&1
if errorlevel 1 (
  echo AVISO: el archivo .pdf descargado no empieza por %%PDF; puede ser una pagina web. Las paginas .html siguen siendo validas.
)

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
