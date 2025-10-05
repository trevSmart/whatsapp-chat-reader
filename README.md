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

No cal instal·lar dependències externes per l'aplicació bàsica. L'aplicació utilitza només mòduls de la biblioteca estàndard de Python.

```bash
git clone <repository-url>
cd whatsapp-chat-reader
```

### Servidor Progressiu (Opcional)

Per utilitzar el servidor progressiu amb xats molt grans, cal instal·lar Flask:

```bash
pip install flask flask-cors
```

## Ús

### Ús bàsic

```bash
python whatsapp_chat_reader.py chat.txt
```

Això generarà un fitxer `chat.html` al mateix directori que el fitxer del xat.

### Opcions avançades

```bash
python whatsapp_chat_reader.py chat.txt --output mi_xat.html --chat-name "Xat amb Noemí" --open
```

#### Paràmetres disponibles:

- `chat_file`: Fitxer del xat exportat de WhatsApp (obligatori)
- `--output`, `-o`: Nom del fitxer HTML de sortida
- `--attachments-dir`, `-a`: Directori amb els adjunts (per defecte: mateix directori que el xat)
- `--chat-name`, `-n`: Nom del xat per mostrar al document HTML
- `--open`: Obrir el document HTML generat al navegador

### Exemples d'ús

```bash
# Processar un xat amb el nom per defecte
python whatsapp_chat_reader.py chat.txt

# Especificar el nom del xat i obrir-lo
python whatsapp_chat_reader.py chat.txt --chat-name "Xat familiar" --open

# Utilitzar un directori diferent per als adjunts
python whatsapp_chat_reader.py chat.txt --attachments-dir ./media

# Generar amb un nom personalitzat
python whatsapp_chat_reader.py chat.txt --output conversa_2021.html --chat-name "Conversa 2021"
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
├── whatsapp_chat_reader.py    # Script principal
├── whatsapp_parser.py         # Parser per processar els missatges
├── html_generator.py          # Generador de documents HTML
├── requirements.txt           # Dependències (només biblioteca estàndard)
└── README.md                 # Aquesta documentació
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
