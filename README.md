# WhatsApp Chat Reader

Una eina per processar xats exportats de WhatsApp i generar documents HTML amb els adjunts integrats.

## Descripció

Aquesta aplicació processa els fitxers de text exportats de WhatsApp i genera un document HTML interactiu que mostra:

- Tots els missatges del xat amb timestamps i remitents
- Adjunts integrats (imatges, vídeos, àudios, documents)
- Enllaços clicables per URLs
- Interfície moderna i responsive
- Estadístiques del xat

## Instal·lació

### Instal·lació del paquet (recomanat)

```bash
git clone <repository-url>
cd whatsapp-chat-reader
pip install -e .
```

Després de la instal·lació, pots executar:

```bash
whatsapp-chat-reader chat.txt
```

### Ús sense instal·lació

Si no vols instal·lar el paquet, pots executar els scripts directament:

```bash
git clone <repository-url>
cd whatsapp-chat-reader
PYTHONPATH=src python3 -m whatsapp_chat_reader.main chat.txt
```

O usar el servidor progressiu amb el script fàcil:

```bash
./server.sh chat.txt --chat-name "El meu xat" --port 8080
```

### Script d'execució fàcil

Hem creat un script intel·ligent que gestiona automàticament les dependències:

- **`./server.sh`**: Prova primer amb entorn virtual, després amb instal·lació global

### Servidor Progressiu (Opcional)

Per utilitzar el servidor progressiu amb xats molt grans, cal instal·lar Flask:

```bash
pip install flask flask-cors
```

O simplement usa el script fàcil que ho gestiona automàticament.

## Ús

### Ús amb servidor progressiu (recomanat per xats grans)

**Opció 1: Script fàcil (recomanat)**
```bash
./server.sh chat.txt --chat-name "El meu xat" --port 8080
```

**Opció 2: Manual amb entorn virtual**
```bash
source venv_new/bin/activate
python progressive_server.py chat.txt --chat-name "El meu xat" --port 8080
```

**Opció 3: Manual amb detecció automàtica d'adjunts**
```bash
python progressive_server.py chat.txt --attachments ./adjunts --chat-name "El meu xat" --port 8080
```

**Opció 4: Ús mínim (port per defecte 5000)**
```bash
./server.sh chat.txt
```

> **Nota**: En macOS, el port 5000 pot estar ocupat per AirPlay. Si tens problemes, usa un port diferent com `--port 8080`.

El servidor detecta automàticament el directori d'adjunts al mateix nivell que el fitxer TXT, així que normalment no cal especificar `--attachments`.

### Ús bàsic (generador HTML estàtic)

Si has instal·lat el paquet:

```bash
whatsapp-chat-reader chat.txt
```

O sense instal·lar:

```bash
PYTHONPATH=src python3 -m whatsapp_chat_reader.main chat.txt
```

Això generarà un fitxer `chat.html` al mateix directori que el fitxer del xat.

### Opcions avançades

```bash
whatsapp-chat-reader chat.txt --output mi_xat.html --chat-name "Xat amb Noemí" --open
```

O sense instal·lar:

```bash
PYTHONPATH=src python3 -m whatsapp_chat_reader.main chat.txt --output mi_xat.html --chat-name "Xat amb Noemí" --open
```

#### Paràmetres disponibles:

- `chat_file`: Fitxer del xat exportat de WhatsApp (obligatori)
- `--output`, `-o`: Nom del fitxer HTML de sortida
- `--attachments-dir`, `-a`: Directori amb els adjunts (per defecte: mateix directori que el xat)
- `--chat-name`, `-n`: Nom del xat per mostrar al document HTML
- `--open`: Obrir el document HTML generat al navegador

### Exemples d'ús

```bash
# Processar un xat amb el nom per defecte (amb paquet instal·lat)
whatsapp-chat-reader chat.txt

# O sense instal·lar
PYTHONPATH=src python3 -m whatsapp_chat_reader.main chat.txt

# Especificar el nom del xat i obrir-lo
whatsapp-chat-reader chat.txt --chat-name "Xat familiar" --open

# Utilitzar un directori diferent per als adjunts
whatsapp-chat-reader chat.txt --attachments-dir ./media

# Generar amb un nom personalitzat
whatsapp-chat-reader chat.txt --output conversa_2021.html --chat-name "Conversa 2021"

# Usar servidor progressiu per xats grans (recomanat)
python progressive_server.py chat.txt --attachments ./adjunts --chat-name "Xat gran" --port 8080
```

## Format dels xats de WhatsApp

L'aplicació processa xats exportats amb el format estàndard de WhatsApp:

```
[8/5/21 2:04:57] Noemí: Els missatges i les trucades estan xifrats d'extrem a extrem...
[8/5/21 16:38:19] Marc: ‎<adjunt: 00000003-PHOTO-2021-05-08-16-38-19.jpg>
[8/5/21 16:39:00] Marc: Casi a sagrada família
```

### Adjunts

Els adjunts es detecten automàticament pel patró `‎<adjunt: nom_del_fitxer>` i es busquen al directori especificat.

## Tipus de fitxers suportats

### Imatges
- JPG, JPEG, PNG, GIF, BMP, WebP, SVG
- S'integren directament al document HTML

### Vídeos
- MP4, AVI, MOV, MKV, WebM, 3GP
- Reproductor de vídeo integrat

### Àudios
- MP3, WAV, OGG, M4A, AAC, FLAC
- Reproductor d'àudio integrat

### Documents
- PDF, DOC, DOCX, TXT, i altres
- Enllaç de descàrrega

## Estructura del projecte

```
whatsapp-chat-reader/
├── src/
│   └── whatsapp_chat_reader/
│       ├── __init__.py                        # Mòdul principal
│       ├── parser.py                          # Parser per processar els missatges
│       ├── html_generator.py                  # Generador de documents HTML
│       ├── progressive_virtual_generator.py   # Generador HTML progressiu amb virtual scrolling
│       └── main.py                            # Script principal
├── progressive_server.py                      # Servidor Flask per lectura progressiva
├── requirements.txt                           # Dependències
├── setup.py                                   # Configuració del paquet
└── README.md                                  # Aquesta documentació
```

## Servidor Progressiu per Xats Grans

Per xats amb desenes de milers de missatges, utilitza el servidor progressiu:

```bash
# Instal·lar dependències
pip install flask flask-cors

# Executar servidor
python3 progressive_server.py "chat.txt" --attachments "./adjunts" --chat-name "El meu xat" --port 8080
```

El servidor progressiu ofereix:
- **Lectura progressiva**: Només carrega els missatges necessaris
- **Virtual scrolling**: Rendiment òptim amb milers de missatges
- **Càrrega sota demanda**: Adjunts carregats quan es necessiten
- **API REST**: Endpoints per accedir a missatges i adjunts
- **Cerca en temps real**: Filtratge instantani de missatges

Obre el navegador a `http://localhost:8080` per veure el xat.

## Proves amb Exemple Real

El projecte inclou un exemple real de test amb més de 25.000 missatges i 3.400 adjunts:

```bash
# Executar tests automàtics
./test_real_example.sh

# O manualment amb pytest
python3 -m pytest tests/test_real_example.py -v

# O executar el servidor amb l'exemple
python3 progressive_server.py "tests/real-example-test/_chat.txt" \
    --attachments "tests/real-example-test" \
    --chat-name "Test Chat" \
    --port 8080
```

## Característiques

- **Integració completa**: Tots els adjunts es mostren directament al document
- **Interfície moderna**: Disseny inspirat en WhatsApp amb estils CSS moderns
- **Responsive**: Funciona bé en dispositius mòbils i escriptori
- **Enllaços clicables**: URLs automàticament convertides a enllaços
- **Estadístiques**: Informació sobre missatges, adjunts i participants
- **Codificació robusta**: Suport per diferents codificacions de text
- **Servidor progressiu**: Per xats molt grans amb virtual scrolling

## Limitacions

- Els fitxers grans poden fer el document HTML molt pesat
- Alguns navegadors poden tenir límits de mida per documents HTML
- Els adjunts es codifiquen en base64, cosa que augmenta la mida del document

## Solució de problemes

### El parser no detecta correctament les dates
Assegura't que el format de data al fitxer del xat sigui `dd/mm/yy` o `dd/mm/yyyy`.

### Els adjunts no es troben
Verifica que els noms dels fitxers d'adjunts coincideixin exactament amb les referències al xat.

### Problemes de codificació
Si hi ha caràcters estranys, l'aplicació intentarà diferents codificacions automàticament.

## Contribucions

Les contribucions són benvingudes! Si trobes errors o tens suggeriments per millorar l'aplicació, si us plau obre un issue o pull request.

## Llicència

Aquest projecte està sota la llicència MIT. Veure el fitxer LICENSE per més detalls.
