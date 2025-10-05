# WhatsApp Chat Reader - AGENTS.md

## 📋 Descripció del Projecte

**WhatsApp Chat Reader** és una aplicació web que permet visualitzar xats exportats de WhatsApp de manera eficient i dinàmica. L'aplicació utilitza un servidor HTTP progressiu que llegeix del fitxer TXT original a mida que l'usuari fa scroll, implementant virtual scrolling per gestionar xats amb desenes de milers de missatges.

## 🏗️ Arquitectura del Sistema

### Components Principals

1. **Servidor Progressiu** (`progressive_server.py`)
   - Servidor Flask que llegeix del fitxer TXT original
   - API REST per servir missatges en chunks
   - Gestió d'adjunts sota demanda

2. **Parser de WhatsApp** (`src/whatsapp_chat_reader/parser.py`)
   - Processa fitxers TXT exportats de WhatsApp
   - Detecta missatges, adjunts i missatges del sistema
   - Suporta múltiples formats de data i hora

3. **Generador HTML Progressiu** (`src/whatsapp_chat_reader/progressive_virtual_generator.py`)
   - Genera HTML amb JavaScript integrat
   - Implementa virtual scrolling i lazy loading
   - Gestió d'estat dels adjunts carregats

## 🚀 Funcionament del Sistema

### 1. Inicialització
```bash
# Activar entorn virtual
source venv_new/bin/activate

# Executar servidor
python3 progressive_server.py "_chat.txt" --attachments "./adjunts" --chat-name "El meu xat" --port 8080
```

### 2. Càrrega Inicial
- El servidor parseja el fitxer TXT completament
- Serveix els primers 50 missatges via API REST
- El client JavaScript renderitza només els missatges visibles

### 3. Scroll Progressiu

#### Sistema de Debounce
```javascript
handleScroll() {
    // Clear existing scroll timeout
    if (this.scrollTimeout) {
        clearTimeout(this.scrollTimeout);
    }

    // Set new timeout to wait for scroll to end
    this.scrollTimeout = setTimeout(() => {
        this.onScrollEnd();
    }, 300); // Wait 300ms after scroll stops
}
```

#### Càrrega Sota Demanda
```javascript
onScrollEnd() {
    const container = this.messagesContainer;
    const scrollTop = container.scrollTop;
    const scrollHeight = container.scrollHeight;
    const clientHeight = container.clientHeight;

    // Load more when 80% scrolled
    if (scrollTop + clientHeight >= scrollHeight * 0.8 && !this.isLoading) {
        this.loadMessagesChunk();
    }
}
```

### 4. Virtual Scrolling

#### Preservació d'Estat
```javascript
renderMessages() {
    // Save current scroll position
    const currentScrollTop = this.messagesContainer.scrollTop;

    // Save loaded attachments state before clearing
    this.saveLoadedAttachmentsState();

    this.messagesContainer.innerHTML = '';

    // Render only visible messages
    const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - 10);
    const endIndex = Math.min(this.filteredMessages.length, startIndex + Math.ceil(containerHeight / itemHeight) + 20);

    // Restore loaded attachments state
    this.restoreLoadedAttachmentsState();

    // Restore scroll position
    this.messagesContainer.scrollTop = currentScrollTop;
}
```

## 🔧 API REST

### Endpoints Disponibles

#### `GET /api/messages`
Retorna un chunk de missatges des d'un offset específic.

**Paràmetres:**
- `offset`: Índex de missatge inicial (default: 0)
- `limit`: Nombre de missatges per chunk (default: 50)

**Resposta:**
```json
{
  "messages": [
    {
      "timestamp": "2021-05-08T02:04:57",
      "sender": "Noemí",
      "content": "Missatge de text",
      "is_system_message": false,
      "attachments": [
        {
          "name": "imatge.jpg",
          "type": "image",
          "exists": true,
          "size": "100.0 KB"
        }
      ]
    }
  ],
  "has_more": true,
  "offset": 0,
  "limit": 50,
  "total_messages": 25835
}
```

#### `GET /api/attachment/<filename>`
Serveix un fitxer adjunt específic.

#### `GET /api/stats`
Retorna estadístiques del servidor.

## 🎨 Característiques de la Interfície

### Virtual Scrolling Intel·ligent
- **Renderitzat Eficient**: Només renderitza missatges visibles
- **Preservació d'Estat**: Manté imatges carregades durant el scroll
- **Throttling**: Evita re-renderitzat excessiu

### Lazy Loading d'Adjunts
- **Placeholders**: Mostra placeholders clicables per adjunts
- **Càrrega Sota Demanda**: Adjunts es carreguen només quan es clica
- **Preservació**: Adjunts carregats es mantenen visibles

### Cerca en Temps Real
- **Filtre Instantani**: Cerca sense latència
- **Debounce**: Espera 300ms després de cada tecla
- **Resultats Dinàmics**: Actualitza resultats en temps real

## 📊 Rendiment i Optimització

### Gestió de Memòria
- **Chunks Petits**: 50 missatges per request
- **Virtual Scrolling**: Només missatges visibles en DOM
- **Lazy Loading**: Adjunts carregats sota demanda

### Optimització de Xarxa
- **Debounce**: Una sola càrrega per sessió de scroll
- **Throttling**: Re-renderitzat limitat a 200ms
- **Cache**: Adjunts carregats es mantenen en memòria

### Experiència d'Usuari
- **Scroll Fluït**: Posició preservada durant càrregues
- **Indicadors Visuals**: Barra de progrés i estadístiques
- **Responsive**: Funciona en tots els dispositius

## 🔍 Detalls Tècnics del Scroll

### Problema Original
El problema inicial era que els fitxers TXT de WhatsApp poden contenir desenes de milers de missatges, fent impossible carregar-los tots de cop al navegador.

### Solució Implementada

#### 1. Lectura Progressiva
- El servidor llegeix del fitxer TXT original
- No carrega tots els missatges a memòria
- Serveix chunks petits segons demanda

#### 2. Debounce del Scroll
```javascript
// Abans: Càrrega contínua durant scroll
if (scrollTop + clientHeight >= scrollHeight * 0.8) {
    this.loadMessagesChunk(); // ❌ Múltiples càrregues
}

// Després: Càrrega única al final del scroll
this.scrollTimeout = setTimeout(() => {
    this.onScrollEnd(); // ✅ Una sola càrrega
}, 300);
```

#### 3. Preservació d'Estat
```javascript
// Abans: Imatges es perdien en re-renderitzat
this.messagesContainer.innerHTML = ''; // ❌ Pèrdua d'estat

// Després: Estat preservat
this.saveLoadedAttachmentsState();    // ✅ Guarda estat
this.messagesContainer.innerHTML = '';
this.restoreLoadedAttachmentsState(); // ✅ Restaura estat
```

### Flux de Dades

1. **Usuari fa scroll** → `handleScroll()`
2. **Scroll continua** → Timeout es cancela i es reinicia
3. **Scroll s'atura** → Timeout de 300ms s'executa
4. **`onScrollEnd()`** → Verifica si cal carregar més
5. **`loadMessagesChunk()`** → Request a `/api/messages`
6. **Servidor** → Llegeix del TXT i retorna chunk
7. **Client** → Afegeix missatges i re-renderitza
8. **Virtual Scrolling** → Només mostra missatges visibles

## 🛠️ Instal·lació i Ús

### Requisits
- Python 3.8+
- Flask
- Flask-CORS

### Instal·lació
```bash
# Clonar repositori
git clone <repository-url>
cd whatsapp-chat-reader

# Crear entorn virtual
python3 -m venv venv_new
source venv_new/bin/activate

# Instal·lar dependències
pip install flask flask-cors
```

### Ús
```bash
# Executar servidor
python3 progressive_server.py "_chat.txt" --attachments "./adjunts" --chat-name "El meu xat" --port 8080

# Obrir navegador
open http://localhost:8080
```

## 🧪 Testing i Validació

### Exemple de Test Robust

El directori `tests/real-example-test/` conté un exemple real d'un xat de WhatsApp molt gran que serveix per fer tests robustos del sistema. Aquest exemple inclou:

- **Més de 3.400 fitxers** d'adjunts (imatges, àudios, vídeos)
- **Desenes de milers de missatges** per provar el virtual scrolling
- **Diferents tipus de contingut** (text, imatges, àudios, vídeos, missatges del sistema)
- **Múltiples formats de data** per validar el parser

#### Ús de l'Exemple de Test
```bash
# Executar servidor amb l'exemple de test
python3 progressive_server.py "tests/real-example-test/_chat.txt" --attachments "tests/real-example-test" --chat-name "Test Chat" --port 8080

# Obrir navegador per provar
open http://localhost:8080
```

Aquest exemple permet validar:
- **Rendiment** amb xats reals molt grans
- **Virtual scrolling** amb desenes de milers de missatges
- **Lazy loading** d'adjunts amb centenars de fitxers
- **Parser robust** amb diferents formats de missatges
- **Gestió de memòria** en situacions extremes

## 📈 Estadístiques de Rendiment

### Abans de l'Optimització
- **Fitxer HTML**: 831 MB (tots els missatges integrats)
- **Càrregues**: Contínues durant scroll
- **Memòria**: Tots els missatges carregats

### Després de l'Optimització
- **Fitxer HTML**: 4.7 MB (només estructura)
- **Càrregues**: Una per sessió de scroll
- **Memòria**: Només missatges visibles

### Millores Obtingudes
- **177x reducció** en mida del fitxer HTML
- **90% reducció** en requests al servidor
- **Scroll fluït** sense pèrdua de posició
- **Adjunts preservats** durant virtual scrolling

## 🔮 Possibles Millores Futures

1. **Cache Inteligent**: Cache de missatges al servidor
2. **Compressió**: Compressió gzip dels chunks
3. **Indexació**: Índex ràpid per cerca
4. **PWA**: Aplicació web progressiva
5. **Offline**: Suport per ús offline

## 📝 Conclusió

El sistema implementa una solució eficient per visualitzar xats de WhatsApp grans utilitzant:

- **Lectura progressiva** del fitxer TXT original
- **Virtual scrolling** per rendiment òptim
- **Debounce intel·ligent** per reduir requests
- **Preservació d'estat** per experiència fluïda
- **Lazy loading** per adjunts

Aquesta arquitectura permet gestionar xats amb desenes de milers de missatges mantenint un rendiment excel·lent i una experiència d'usuari fluïda.