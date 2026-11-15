@echo off
REM ===========================================================================================
REM  Munger V2 - Viscofan - boletin oficial de cotizacion de la Bolsa de Madrid del 3-nov-2026 (v2, 14-nov-2026)
REM  Fuente del precio de cierre de Viscofan (celda C37 = 54,70 EUR). La v1 usaba la direccion antigua, que ahora
REM  redirige a la portada de BME Exchange: esta usa la nueva (/descargas/boletines/madrid/...). Seccion 16: precios
REM  del mercado continuo; seccion 9: precios por nombre corto. Borra los archivos falsos de la v1.
REM  Guarda en VISCOFAN SA\descargas_2026 y escribe HUELLAS_PRECIO.txt. No modifica nada mas.
REM ===========================================================================================
setlocal
set "DESTINO=C:\Users\jluis\Desktop\IDEAS DE INVERSION JOSE LUIS\INFORMACION ECONOMICA EMPRESAS\VISCOFAN SA\descargas_2026"
if not exist "%DESTINO%" mkdir "%DESTINO%"
cd /d "%DESTINO%"
del /q "BMadrid_boletin_20261103_seccion_*.pdf" 2>nul
set "UA=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
set "BASE=https://www.bolsasymercados.es/descargas/boletines/madrid/2026/11/03"
for %%S in (16 9) do (
  echo Descargando la seccion %%S del boletin del 3-nov-2026...
  curl -L --fail -A "%UA%" -o "BMadrid_boletin_20261103_seccion_%%S.pdf" "%BASE%/1_%%S_0_20261103.pdf"
)
echo Comprobando que son PDF de verdad (no paginas web)...
for %%F in (BMadrid_boletin_20261103_*.pdf) do (
  findstr /m /b "%%PDF" "%%F" >nul || (echo   %%F NO es un PDF: se borra & del "%%F")
)
echo Calculando huellas SHA-256...
if exist HUELLAS_PRECIO.txt del HUELLAS_PRECIO.txt
for %%F in (BMadrid_boletin_20261103_*.pdf) do (
  echo %%F>> HUELLAS_PRECIO.txt
  certutil -hashfile "%%F" SHA256 | findstr /v "hash CertUtil" >> HUELLAS_PRECIO.txt
)
echo.
echo Terminado. Archivos en: %DESTINO%
pause
