# Flashcard Generator

Flashcard Generator è un'applicazione desktop professionale sviluppata in Python per facilitare l'apprendimento mnemonico attraverso mazzi di carte personalizzabili. Il software è progettato con un'architettura modulare e segue le migliori pratiche di ingegneria del software, inclusi il type hinting e un sistema di logging strutturato.

## Caratteristiche Tecniche

*   **Architettura**: Modulare (Separazione tra UI, Logica di Export e Database).
*   **Interfaccia Grafica**: Sviluppata con CustomTkinter per un'esperienza utente moderna in modalità scura.
*   **Gestione Dati**: Utilizzo di SQLite con integrità referenziale e query parametrizzate.
*   **Visualizzazione**: Grafici dinamici integrati tramite Matplotlib per il tracciamento delle performance.
*   **Esportazione**: Generazione di documenti PDF A4 con layout a due colonne (Fronte/Retro) tramite ReportLab e immagini PNG tramite Pillow.

## Requisiti di Sistema

Il software richiede Python 3.x e le librerie grafiche di sistema per Tkinter.

### Dipendenze
Le librerie Python necessarie sono elencate nel file requirements.txt e includono:
*   customtkinter
*   reportlab
*   pillow
*   matplotlib

## Installazione e Avvio

1. Installare le dipendenze di sistema (esempio per Fedora):
   ```bash
   sudo dnf install python3-tkinter python3-pillow-tk python3-matplotlib-tk
   ```

2. Installare i pacchetti Python necessari:
   ```bash
   pip install -r requirements.txt
   ```

3. Eseguire l'applicazione:
   ```bash
   python3 flashcard_app/main.py
   ```

## Struttura del Progetto

*   `flashcard_app/main.py`: Punto di ingresso dell'applicazione.
*   `flashcard_app/database.py`: Gestore della persistenza dei dati.
*   `flashcard_app/ui/`: Componenti dell'interfaccia grafica.
*   `flashcard_app/export/`: Moduli per la generazione di PDF e immagini.
*   `flashcard_app/assets/`: Risorse grafiche e configurazioni del tema.

## Licenza

Questo progetto è distribuito sotto Licenza MIT. Consultare il file LICENSE per ulteriori dettagli.
