# 💰 Solana Discord Bot - SOL Mokėjimų Priėmimo Sistema

Automatinis Discord bota, kuris priima Solana (SOL) mokėjimus ir siunčia notifikacijas į Discord kanalą.

## ✨ Savybės

- ✅ Automatiškai klausoma Solana blockchain'o
- ✅ Realia laiku notifikacijos apie gautus SOL mokėjimus
- ✅ Transakcijų istorija saugoma lokalioje duomenų bazėje
- ✅ Lengvi Discord komandos: `!wallet`, `!balance`, `!transactions`
- ✅ Palaikomas devnet ir mainnet
- ✅ Automatinis mokėjimų paskirstymas (split)

## 📋 Reikalingiausios Dalys

Prieš pradedant, turėsite:

1. **Discord serveris** (kuriame jūs administratorius)
2. **Discord Bot Token** 
3. **Solana Wallet** (Phantom, Ledger, ar panašus)
4. **Python 3.8+**

---

## 🚀 Greitas Pradžia

### 1️⃣ Parsisiųsti Projektą

```bash
git clone https://github.com/rbc8n64wtp-netizen/solana-discord-bot.git
cd solana-discord-bot
```

### 2️⃣ Sukurti Virtualią Aplinką

```bash
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3️⃣ Instaliuoti Priklausomybes

```bash
pip install -r requirements.txt
```

### 4️⃣ Sukonfigūruoti `.env` Failą

Kopijuoti `.env.example` į `.env`:

```bash
cp .env.example .env
```

Redaguoti `.env` failą su savo duomenimis:

```
DISCORD_TOKEN=your_bot_token_here
SOLANA_WALLET_ADDRESS=9VjeJCg8rW5dKyPYU6SZDgiTcNNzfCjLy381WEGVjW2G
SOLANA_RPC_URL=https://api.devnet.solana.com
MIN_SOL_AMOUNT=0.1
NOTIFICATION_CHANNEL_ID=your_channel_id
SPLIT_WALLET_ADDRESS=wallet_kam_siusti_dali
SPLIT_PERCENTAGE=30
```

### 5️⃣ Paleisti Botą

```bash
python bot.py
```

Turėtumėte pamatyti:
```
✅ Bot prijungtas kaip BotName#1234
💰 Klausau Solana wallet: YOUR_ADDRESS
```

---

## ⚙️ Konfigūracija

### Discord Bot Setup

1. Eiti į [Discord Developer Portal](https://discord.com/developers/applications)
2. Spustelėti "New Application"
3. Eiti į "Bot" → "Add Bot"
4. Kopijuoti token ir įdėti į `.env` failą

### Discord Channel ID

1. Įjungti "Developer Mode" (Settings → Advanced → Developer Mode)
2. Dešiniu pelenu spustelėti kanalą ir "Copy Channel ID"
3. Įdėti į `.env` failą `NOTIFICATION_CHANNEL_ID`

### Solana Wallet

Galite naudoti:
- **Phantom Wallet** (parsisiųsti iš phantom.app)
- **Ledger** (hardware wallet)
- **Solflare** (web wallet)

### RPC Endpoints

- **Devnet (Bandymas):** `https://api.devnet.solana.com`
- **Testnet:** `https://api.testnet.solana.com`
- **Mainnet:** `https://api.mainnet-beta.solana.com`

### Payment Split (Paskirstymas)

Pridėti į `.env`:
```
# Wallet, kur siųsti dalį
SPLIT_WALLET_ADDRESS=another_wallet_address

# Kiek procentų siųsti (0-100)
SPLIT_PERCENTAGE=30
```

**Pavyzdys:**
- Gautas: 1 SOL
- Siąsti jums: 70% = 0.7 SOL
- Siąsti kitam: 30% = 0.3 SOL

---

## 📝 Discord Komandos

### `!wallet`
Parodyti Solana wallet adresą, kuriame priimami SOL

```
!wallet
```

### `!balance`
Patikrinti wallet balansą

```
!balance
```

### `!transactions`
Pamatyti paskutines 10 transakcijų

```
!transactions
```

### `!split`
Matyti paskirstymo nustatymus

```
!split
```

---

## 🌐 Deployment (24/7 Veikimas)

### Replit (REKOMENDUOJAMAS)

1. Eiti į [Replit.com](https://replit.com)
2. Spustelėti "Create" → "Import from GitHub"
3. Įklijuoti repo URL: `https://github.com/rbc8n64wtp-netizen/solana-discord-bot.git`
4. Redaguoti `.env` failą Replit'e
5. Spustelėti "Run"
6. Bot veiks 24/7! ✅

### Railway.app

1. Eiti į [Railway.app](https://railway.app)
2. Spustelėti "New Project"
3. Pasirinkti "Deploy from GitHub"
4. Pasirinkti šią repozitoriją
5. Nustatyti `.env` kintamuosius
6. Palesti

---

## 💳 Kaip Veikia Payment Split

**Scenarijus:**
1. Žmogus siųsta 1 SOL į bot wallet
2. Bot automatiškai:
   - Gauna transakcija į blockchain'ą
   - Patikrina kiekį
   - Paskirstytas pagal `SPLIT_PERCENTAGE`
   - Siųsta jums ir kitam wallet'ui

**Pavyzdys su 30% split:**

```
Gautas SOL: 1.0
Jūsų wallet: 0.7 SOL (70%)
Kito wallet: 0.3 SOL (30%)
```

---

## 🔒 Saugumas

⚠️ **SVARBU:**

- **Niekada nedelei savo private key** viešoje vietoje
- **Niekada nedelei .env failą** GitHub'e (naudok `.gitignore`)
- Naudoti tik **public wallet address** botui
- Regulariai tikrinti transakcijas `transactions.json` failą
- Bot turi turėti **readonly** prieigą prie wallet'o

---

## 🐛 Trikčių Šalinimas

### Bot neprijungiamas
```
❌ KLAIDA: Nėra DISCORD_TOKEN
```
**Sprendimas:** Patikrinti `.env` failą, ar `DISCORD_TOKEN` yra teisingas

### Bot nemato transakcijų
1. Patikrinti, ar `SOLANA_WALLET_ADDRESS` teisingas
2. Patikrinti, ar `NOTIFICATION_CHANNEL_ID` teisingas
3. Patikrinti, ar bot turi leidimą į kanalą
4. Naudoti devnet bandymams

### Klaida su Solana RPC
```
ConnectionError: Failed to connect to endpoint
```
**Sprendimas:** Patikrinti `SOLANA_RPC_URL` - gali būti nepasiekiamas

### Paskirstymas neverikia
1. Patikrinti `SPLIT_WALLET_ADDRESS` formato
2. Patikrinti `SPLIT_PERCENTAGE` (0-100)
3. Patikrinti, ar pakankamas balanso

---

## 📊 Transakcijų Istorija

Visos transakcijos saugomos `transactions.json` failą:

```json
{
  "3kZKJqS9...": {
    "amount": 0.5,
    "timestamp": "2024-01-15 14:30:45",
    "status": "success",
    "split": {
      "you": 0.35,
      "other": 0.15
    }
  }
}
```

---

## 🎓 Mokymo Medžiaga

- [Discord.py Dokumentacija](https://discordpy.readthedocs.io/)
- [Solana Python SDK](https://github.com/michaelhly/solana-py)
- [Solana Dokumentacija](https://docs.solana.com/)
- [Solana Explorer](https://explorer.solana.com/) - Tikrinti transakcijas

---

## 📞 Pagalba

Jei kažkas neveikia:
1. Patikrinti Discord Developer Portal
2. Patikrinti `.env` failą
3. Patikrinti bot privilegijas
4. Naudoti `python -m pdb bot.py` debuigavimui
5. Peržiūrėti logs terminale

---

## 📜 Licencija

MIT License - Laisvai naudoti

---

## ⚠️ Atsakomybė

- Šis bota yra **viešai testuoti**
- **Blockchain transakcijos VISUOMET matoma** - tai Solana blockchain'o tikslas
- Atsakyti reguliacija ir mokesčiai!
- Naudok tik **legaliems tikslams**

---

**Sėkmės! 🚀💰**

Jeigu turite klausimų - kurkite issues GitHub'e arba skaitykite dokumentaciją!
