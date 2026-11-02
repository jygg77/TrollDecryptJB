# TrollDecryptJB

Audit tecnico e build dimostrativa rootless isolata; non include funzioni di decrittazione o hook dell'app originale.

## Cosa fa

- Compila un'app UIKit standalone (TrollDecryptAuditDemo) in rootless iOS usando Theos.
- Applica la compilazione con make clean package FINALPACKAGE=1.
- Verifica il DEB generato e documenta l'esito in evidence.txt.

## Cosa NON fa

- Non compila né copia sorgenti originali, hook, daemon, helper, entitlements privati o codice di decrittazione.
- Il risultato è solo una dimostrazione tecnica del processo di build rootless.

## Build manuale

```bash
git clone --recursive https://github.com/theos/theos
# Installare gli SDK necessari in $THEOS/sdks
make clean package FINALPACKAGE=1
dpkg-deb -I TrollDecryptAuditDemo_*.deb
dpkg-deb -c TrollDecryptAuditDemo_*.deb
```
