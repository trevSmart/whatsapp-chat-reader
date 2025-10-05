# WhatsApp Chat Reader

Una eina professional per processar xats exportats de WhatsApp i generar documents HTML amb els adjunts integrats.

## Descripció

Aquesta aplicació processa els fitxers de text exportats de WhatsApp i genera un document HTML interactiu que mostra:

- Tots els missatges del xat amb timestamps i remitents
- Adjunts integrats (imatges, vídeos, àudios, documents)
- Enllaços clicables per URLs
- Interfície moderna i responsive
- Estadístiques del xat

## Instal·lació

### Des del codi font

```bash
git clone <repository-url>
cd whatsapp-chat-reader
pip install -e .
```

### Desenvolupament

```bash
# Instal·lar dependències de desenvolupament
pip install -r requirements-dev.txt
pip install -e .

# Executar tests
make test

# Executar linting
make lint

# Formatar codi
make format
```

## Ús

### Com a script

```bash
python whatsapp_chat_reader.py chat.txt
```

### Com a comanda instal·lada

```bash
whatsapp-chat-reader chat.txt --output mi_xat.html --open
```

### Opcions avançades

```bash
whatsapp-chat-reader chat.txt --output mi_xat.html --chat-name "Xat amb Noemí" --attachments-dir ./adjunts --open
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
whatsapp-chat-reader chat.txt

# Especificar el nom del xat i obrir-lo
whatsapp-chat-reader chat.txt --chat-name "Xat familiar" --open

# Utilitzar un directori diferent per als adjunts
whatsapp-chat-reader chat.txt --attachments-dir ./media

# Generar amb un nom personalitzat
whatsapp-chat-reader chat.txt --output conversa_2021.html --chat-name "Conversa 2021"
```

## Estructura del projecte

```
whatsapp-chat-reader/
├── src/
│   └── whatsapp_chat_reader/
│       ├── __init__.py
│       ├── parser.py              # Parser per processar els missatges
│       ├── html_generator.py      # Generador de documents HTML
│       └── whatsapp_chat_reader.py # Script principal
├── tests/
│   ├── __init__.py
│   └── test_whatsapp_chat_reader.py
├── examples/
│   ├── exemple_chat.txt
│   └── exemple_chat.html
├── docs/
├── pyproject.toml                 # Configuració del projecte
├── setup.py                       # Setup script (compatibilitat)
├── requirements.txt               # Dependències bàsiques
├── requirements-dev.txt          # Dependències de desenvolupament
├── pytest.ini                    # Configuració de pytest
├── Makefile                      # Tasques de desenvolupament
├── .gitignore                    # Fitxers a ignorar per git
└── README.md                     # Aquesta documentació
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

## Desenvolupament

### Configuració del entorn

```bash
# Clonar el repositori
git clone <repository-url>
cd whatsapp-chat-reader

# Crear entorn virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instal·lar en mode desenvolupament
make install-dev
```

### Tasques disponibles

```bash
make help          # Mostra totes les tasques disponibles
make test          # Executa els tests
make test-cov      # Executa tests amb cobertura
make lint          # Executa linting
make format        # Formata el codi
make check         # Executa linting i tests
make clean         # Neteja fitxers temporals
make build         # Construeix el paquet
make example       # Executa l'exemple
```

### Executar tests

```bash
# Tests bàsics
python -m pytest tests/

# Amb cobertura
python -m pytest tests/ --cov=whatsapp_chat_reader --cov-report=html

# Usant Makefile
make test-cov
```

## API

### Ús programàtic

```python
from whatsapp_chat_reader import WhatsAppParser, HTMLGenerator

# Parsejar un xat
parser = WhatsAppParser()
messages = parser.parse_chat_file("chat.txt")

# Trobar adjunts
attachment_map = parser.find_attachment_files(messages, "./adjunts")

# Generar HTML
generator = HTMLGenerator()
html_content = generator.generate_html(messages, attachment_map, "Nom del Xat")

# Escriure el fitxer
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

## Característiques

- **Integració completa**: Tots els adjunts es mostren directament al document
- **Interfície moderna**: Disseny inspirat en WhatsApp amb estils CSS moderns
- **Responsive**: Funciona bé en dispositius mòbils i escriptori
- **Enllaços clicables**: URLs automàticament convertides a enllaços
- **Estadístiques**: Informació sobre missatges, adjunts i participants
- **Codificació robusta**: Suport per diferents codificacions de text
- **Sense dependències**: Utilitza només la biblioteca estàndard de Python
- **Estructura professional**: Segueix les millors pràctiques de Python

## Limitacions

- Els fitxers grans poden fer el document HTML molt pesant
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

### Process de contribució

1. Fork el repositori
2. Crea una branca per la teva feature (`git checkout -b feature/nova-feature`)
3. Commit els teus canvis (`git commit -am 'Afegeix nova feature'`)
4. Push a la branca (`git push origin feature/nova-feature`)
5. Obre un Pull Request

## Llicència

Aquest projecte està sota la llicència MIT. Veure el fitxer LICENSE per més detalls.

## Changelog

### v1.0.0
- Versió inicial
- Parser per xats de WhatsApp
- Generador HTML amb adjunts integrats
- Suport per imatges, vídeos, àudios i documents
- Interfície responsive
- Tests unitaris
- Documentació completa
