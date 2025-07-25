# 📚 Documentation Complète des APIs Client - MyWitti

## 🎯 Vue d'ensemble

Cette documentation présente toutes les APIs disponibles pour développer un site client complet pour l'application MyWitti. L'application est un système de récompenses pour épargnants qui permet aux clients de gagner des jetons et de les échanger contre des récompenses.

### 🔗 Base URL
```
http://127.0.0.1:5000
```

### 🔐 Authentification
Toutes les APIs client nécessitent une authentification JWT. Le token doit être inclus dans le header `Authorization` :
```
Authorization: Bearer {votre_token_jwt}
```

---

## 🔑 1. AUTHENTIFICATION

### 1.1 Connexion Client
**Endpoint :** `POST /accounts/login`

**Headers :**
```
Content-Type: application/json
```

**Body (JSON) :**
```json
{
    "identifiant": "user_test",
    "password": "password123"
}
```

**Réponse attendue :**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Codes de statut :**
- `200` : Connexion réussie
- `401` : Identifiants invalides
- `500` : Erreur serveur

### 1.2 Déconnexion Client
**Endpoint :** `POST /customer/logout`

**Headers :**
```
Authorization: Bearer {token}
```

**Réponse attendue :**
```json
{
    "msg": "Déconnexion réussie"
}
```

---

## 📊 2. DASHBOARD ET PROFIL

### 2.1 Tableau de bord client
**Endpoint :** `GET /customer/{customer_code}/dashboard`

**Headers :**
```
Authorization: Bearer {token}
```

**Exemple d'URL :** `GET /customer/user_test/dashboard`

**Réponse attendue :**
```json
{
    "category": "Executive",
    "jetons": 500,
    "percentage": 44.44,
    "short_name": "Test",
    "tokens_to_next_tier": 500,
    "last_transactions": [
        {
            "date": "2025-06-27",
            "amount": "200",
            "type": "Bonus fidélité"
        },
        {
            "date": "2025-06-25",
            "amount": "100",
            "type": "Achat carte cadeau"
        }
    ]
}
```

**Explication des champs :**
- `category` : Catégorie du client (Eco Premium, Executive, Executive+, First Class)
- `jetons` : Nombre total de jetons
- `percentage` : Pourcentage de progression dans la catégorie actuelle
- `tokens_to_next_tier` : Jetons nécessaires pour passer à la catégorie suivante
- `last_transactions` : 5 dernières transactions

### 2.2 Profil client
**Endpoint :** `GET /customer/{customer_code}/profile`

**Exemple d'URL :** `GET /customer/user_test/profile`

**Réponse attendue :**
```json
{
    "first_name": "User",
    "short_name": "Test",
    "agency": "RGK",
    "jetons": 500,
    "category": "Executive",
    "percentage": 44.44,
    "tokens_to_next_tier": 500
}
```

### 2.3 Historique des transactions
**Endpoint :** `GET /customer/{customer_code}/transactions`

**Paramètres optionnels :**
- `period`: `week`, `month`, `year` (défaut: `month`)

**Exemple d'URL :** `GET /customer/user_test/transactions?period=month`

**Réponse attendue :**
```json
{
    "transactions": [
        {
            "date": "2025-06-27 14:30:00",
            "amount": "200",
            "type": "Deposit"
        },
        {
            "date": "2025-06-25 10:15:00",
            "amount": "100",
            "type": "Purchase"
        }
    ],
    "total_transactions": 2,
    "period_start": "2025-06-01",
    "period_end": "2025-06-30",
    "trends": {
        "deposit_percentage": 50.0,
        "withdrawal_percentage": 50.0
    }
}
```

**Types de transactions :**
- `Deposit` : Dépôt/Ajout de jetons
- `Withdrawal` : Retrait de jetons
- `Purchase` : Achat de récompense
- `Reward` : Récompense/Bonus

### 2.4 Notifications client
**Endpoint :** `GET /customer/{customer_code}/notifications`

**Exemple d'URL :** `GET /customer/user_test/notifications`

**Réponse attendue :**
```json
{
    "msg": "Notifications récupérées avec succès",
    "notifications": [
        {
            "id": 1,
            "message": "Bienvenue sur la plateforme MyWitti !",
            "created_at": "2025-06-21 10:00:00"
        },
        {
            "id": 2,
            "message": "Votre commande #123 a été validée",
            "created_at": "2025-06-26 14:30:00"
        }
    ]
}
```

---

## 🎁 3. RÉCOMPENSES ET ACHATS

### 3.1 Liste des récompenses disponibles
**Endpoint :** `GET /lot/rewards`

**Réponse attendue :**
```json
[
    {
        "id": 1,
        "title": "Carte cadeau 5000 FCFA",
        "tokens_required": 50,
        "image_url": "/static/uploads/gift-card.jpg",
        "category": "Eco Premium",
        "quantity_available": 100
    },
    {
        "id": 2,
        "title": "Carte cadeau 10000 FCFA",
        "tokens_required": 100,
        "image_url": "/static/uploads/gift-card.jpg",
        "category": "Executive",
        "quantity_available": 50
    },
    {
        "id": 3,
        "title": "Smartphone Samsung",
        "tokens_required": 1500,
        "image_url": "/static/uploads/smartphone.jpg",
        "category": "Executive +",
        "quantity_available": 10
    }
]
```

### 3.2 Gestion des favoris

#### 3.2.1 Ajouter/Retirer des favoris
**Endpoint :** `POST /lot/rewards/{reward_id}/favorite`

**Exemple d'URL :** `POST /lot/rewards/1/favorite`

**Body (JSON) :**
```json
{}
```

**Réponse attendue (ajout) :**
```json
{
    "msg": "Récompense ajoutée aux favoris"
}
```

**Réponse attendue (retrait) :**
```json
{
    "msg": "Récompense retirée des favoris"
}
```

#### 3.2.2 Liste des favoris
**Endpoint :** `GET /lot/favorites`

**Réponse attendue :**
```json
{
    "count": 2,
    "items": [
        {
            "id": 1,
            "title": "Carte cadeau 5000 FCFA",
            "tokens_required": 50,
            "category": "Eco Premium",
            "image_url": "/static/uploads/gift-card.jpg"
        },
        {
            "id": 2,
            "title": "Carte cadeau 10000 FCFA",
            "tokens_required": 100,
            "category": "Executive",
            "image_url": "/static/uploads/gift-card.jpg"
        }
    ]
}
```

### 3.3 Gestion du panier

#### 3.3.1 Ajouter au panier
**Endpoint :** `POST /lot/cart`

**Body (JSON) :**
```json
{
    "reward_id": 1,
    "quantity": 2
}
```

**Réponse attendue :**
```json
{
    "msg": "Carte cadeau 5000 FCFA ajoutée au panier",
    "quantity": 2,
    "total_tokens": 100
}
```

#### 3.3.2 Voir le panier
**Endpoint :** `GET /lot/cart`

**Réponse attendue :**
```json
{
    "jetons_disponibles": 500,
    "jetons_requis": 100,
    "achat_possible": true,
    "transactions": [
        {
            "id": 1,
            "title": "Carte cadeau 5000 FCFA",
            "quantity": 2,
            "tokens_required_per_item": 50,
            "total_tokens": 100,
            "image_url": "/static/uploads/gift-card.jpg",
            "transaction_id": "550e8400-e29b-41d4-a716-446655440000"
        }
    ],
    "notifications": []
}
```

#### 3.3.3 Passer une commande
**Endpoint :** `POST /lot/place-order`

**Body (JSON) :**
```json
{}
```

**Réponse attendue :**
```json
{
    "id": "order-550e8400-e29b-41d4-a716-446655440000",
    "customer": "User Test",
    "contact": "N/A",
    "date": "2025-06-28",
    "heure": "14:30:00",
    "amount": 100,
    "items": [
        {
            "reward_id": 1,
            "title": "Carte cadeau 5000 FCFA",
            "tokens_required_per_item": 50,
            "total_tokens": 100,
            "image_url": "/static/uploads/gift-card.jpg"
        }
    ]
}
```

---

## 📋 4. FAQ

### 4.1 Liste des FAQ
**Endpoint :** `GET /faq`

**Réponse attendue :**
```json
{
    "msg": "FAQ récupérées avec succès",
    "faqs": [
        {
            "id": 1,
            "question": "Comment fonctionne le système de jetons ?",
            "answer": "Les jetons sont des points que vous gagnez en utilisant nos services. Vous pouvez les échanger contre des récompenses."
        },
        {
            "id": 2,
            "question": "Comment passer une commande ?",
            "answer": "Allez dans la section \"Lots\" et sélectionnez l'article de votre choix. Ajoutez-le au panier et validez votre commande."
        },
        {
            "id": 3,
            "question": "Comment contacter le support ?",
            "answer": "Vous pouvez nous contacter via l'onglet \"Support\" ou par téléphone au +2250710922213."
        }
    ]
}
```

---

## 📊 5. SONDAGES

### 5.1 Liste des sondages actifs
**Endpoint :** `GET /survey/surveys`

**Réponse attendue :**
```json
{
    "msg": "Sondages récupérées avec succès",
    "surveys": [
        {
            "id": 1,
            "title": "Satisfaction générale",
            "description": "Comment évaluez-vous votre expérience sur notre plateforme ?",
            "is_active": true,
            "created_at": "2025-06-01 10:00:00"
        }
    ]
}
```

### 5.2 Détails d'un sondage
**Endpoint :** `GET /survey/surveys/{survey_id}`

**Exemple d'URL :** `GET /survey/surveys/1`

**Réponse attendue :**
```json
{
    "msg": "Détails du sondage récupérés avec succès",
    "survey": {
        "id": 1,
        "title": "Satisfaction générale",
        "description": "Comment évaluez-vous votre expérience sur notre plateforme ?",
        "is_active": true,
        "created_at": "2025-06-01 10:00:00"
    },
    "options": [
        {
            "id": 1,
            "option_text": "Très mal",
            "option_value": 1
        },
        {
            "id": 2,
            "option_text": "Mal",
            "option_value": 2
        },
        {
            "id": 3,
            "option_text": "Moyen",
            "option_value": 3
        },
        {
            "id": 4,
            "option_text": "Bien",
            "option_value": 4
        },
        {
            "id": 5,
            "option_text": "Très bien",
            "option_value": 5
        }
    ]
}
```

### 5.3 Répondre à un sondage
**Endpoint :** `POST /survey/surveys/{survey_id}/respond`

**Exemple d'URL :** `POST /survey/surveys/1/respond`

**Body (JSON) :**
```json
{
    "option_id": 5
}
```

**Réponse attendue :**
```json
{
    "message": "Réponse enregistrée avec succès"
}
```

---

## 🆘 6. SUPPORT

### 6.1 Informations de contact
**Endpoint :** `GET /support/contact`

**Réponse attendue :**
```json
{
    "phone": "+2250710922213",
    "whatsapp": "+2250710922213",
    "email": "misterjohn0798@gmail.com",
    "default_message": "Bonjour, j'ai besoin d'aide avec l'application."
}
```

### 6.2 Créer une demande de support
**Endpoint :** `POST /support/request`

**Body (JSON) :**
```json
{
    "subject": "Problème de connexion",
    "description": "Je n'arrive pas à me connecter à mon compte depuis hier",
    "request_type": "Assistance"
}
```

**Types de demande autorisés :**
- `Reclamation`
- `Assistance`
- `Autre`

**Réponse attendue :**
```json
{
    "message": "Demande de support créée avec succès",
    "request_id": 1
}
```

---

## 👥 7. SYSTÈME DE PARRAINAGE

### 7.1 Inviter un ami
**Endpoint :** `POST /customer/invite`

**Body (JSON) :**
```json
{
    "email": "ami@example.com"
}
```

**Réponse attendue :**
```json
{
    "message": "Invitation envoyée",
    "referral_link": "http://127.0.0.1:5000/accounts/refer/550e8400-e29b-41d4-a716-446655440000"
}
```

### 7.2 Mes parrainages
**Endpoint :** `GET /customer/my-referrals`

**Réponse attendue :**
```json
{
    "referrals": [
        {
            "referral_link": "http://127.0.0.1:5000/accounts/refer/550e8400-e29b-41d4-a716-446655440000",
            "referred_email": "ami@example.com",
            "status": "pending",
            "created_at": "2025-06-28T14:30:00"
        }
    ],
    "total_referrals": 1,
    "pending_count": 1,
    "accepted_count": 0,
    "rewarded_count": 0
}
```

**Statuts possibles :**
- `pending` : En attente
- `accepted` : Accepté
- `rewarded` : Récompensé

---

## 🏆 8. SYSTÈME DE CATÉGORIES

### 8.1 Catégories disponibles
L'application utilise un système de 4 catégories basé sur le nombre de jetons :

| Catégorie | Code | Jetons minimum | Jetons maximum |
|-----------|------|----------------|----------------|
| Eco Premium | A | 0 | 100 |
| Executive | B | 100 | 1,000 |
| Executive + | C | 1,000 | 3,000 |
| First Class | D | 3,000 | ∞ |

### 8.2 Calcul de progression
- **Pourcentage** : Position dans la catégorie actuelle
- **Jetons pour le niveau suivant** : Jetons nécessaires pour passer à la catégorie supérieure

---

## 🔒 9. SÉCURITÉ ET GESTION D'ERREURS

### 9.1 Codes de statut HTTP
- `200` : Succès
- `201` : Créé avec succès
- `400` : Requête invalide
- `401` : Non authentifié
- `403` : Accès interdit
- `404` : Ressource non trouvée
- `500` : Erreur serveur interne

### 9.2 Gestion des erreurs
Toutes les APIs retournent des messages d'erreur cohérents :

```json
{
    "message": "Description de l'erreur"
}
```

### 9.3 Validation des données
- **Email** : Format email valide requis
- **Jetons** : Doit être un nombre positif
- **Quantités** : Doit être supérieur à 0
- **Types de demande** : Doit être dans la liste autorisée

---

## 📱 10. EXEMPLES D'UTILISATION COMPLETS

### 10.1 Flux complet d'achat
```javascript
// 1. Connexion
const loginResponse = await fetch('/accounts/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        identifiant: 'user_test',
        password: 'password123'
    })
});
const { access_token } = await loginResponse.json();

// 2. Récupération du dashboard
const dashboardResponse = await fetch('/customer/user_test/dashboard', {
    headers: { 'Authorization': `Bearer ${access_token}` }
});
const dashboard = await dashboardResponse.json();

// 3. Liste des récompenses
const rewardsResponse = await fetch('/lot/rewards', {
    headers: { 'Authorization': `Bearer ${access_token}` }
});
const rewards = await rewardsResponse.json();

// 4. Ajouter au panier
const cartResponse = await fetch('/lot/cart', {
    method: 'POST',
    headers: { 
        'Authorization': `Bearer ${access_token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        reward_id: 1,
        quantity: 2
    })
});

// 5. Voir le panier
const viewCartResponse = await fetch('/lot/cart', {
    headers: { 'Authorization': `Bearer ${access_token}` }
});
const cart = await viewCartResponse.json();

// 6. Passer la commande
const orderResponse = await fetch('/lot/place-order', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${access_token}` }
});
const order = await orderResponse.json();
```

### 10.2 Gestion des notifications
```javascript
// Récupération des notifications
const notificationsResponse = await fetch('/customer/user_test/notifications', {
    headers: { 'Authorization': `Bearer ${access_token}` }
});
const notifications = await notificationsResponse.json();

// Affichage du nombre de notifications non lues
const unreadCount = notifications.notifications.length;
```

---

## 🛠️ 11. DÉVELOPPEMENT FRONTEND

### 11.1 Structure recommandée
```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   ├── Rewards/
│   │   ├── Cart/
│   │   ├── Profile/
│   │   └── Support/
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── storage.js
│   ├── pages/
│   │   ├── Login.js
│   │   ├── Dashboard.js
│   │   ├── Rewards.js
│   │   └── Profile.js
│   └── utils/
│       ├── constants.js
│       └── helpers.js
```

### 11.2 Service API recommandé
```javascript
// services/api.js
class ApiService {
    constructor() {
        this.baseURL = 'http://127.0.0.1:5000';
        this.token = localStorage.getItem('token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(this.token && { 'Authorization': `Bearer ${this.token}` })
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Erreur API');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Méthodes d'authentification
    async login(identifiant, password) {
        const data = await this.request('/accounts/login', {
            method: 'POST',
            body: JSON.stringify({ identifiant, password })
        });
        this.setToken(data.access_token);
        return data;
    }

    async logout() {
        await this.request('/customer/logout', { method: 'POST' });
        localStorage.removeItem('token');
        this.token = null;
    }

    // Méthodes dashboard
    async getDashboard(customerCode) {
        return await this.request(`/customer/${customerCode}/dashboard`);
    }

    async getProfile(customerCode) {
        return await this.request(`/customer/${customerCode}/profile`);
    }

    // Méthodes récompenses
    async getRewards() {
        return await this.request('/lot/rewards');
    }

    async addToCart(rewardId, quantity = 1) {
        return await this.request('/lot/cart', {
            method: 'POST',
            body: JSON.stringify({ reward_id: rewardId, quantity })
        });
    }

    async getCart() {
        return await this.request('/lot/cart');
    }

    async placeOrder() {
        return await this.request('/lot/place-order', {
            method: 'POST'
        });
    }
}

export default new ApiService();
```

---

## 📋 12. CHECKLIST DE DÉVELOPPEMENT

### 12.1 Fonctionnalités essentielles
- [ ] Page de connexion
- [ ] Dashboard avec statistiques
- [ ] Catalogue des récompenses
- [ ] Système de panier
- [ ] Historique des transactions
- [ ] Gestion des notifications
- [ ] Page de profil
- [ ] Système de parrainage
- [ ] FAQ
- [ ] Sondages
- [ ] Support client

### 12.2 Fonctionnalités avancées
- [ ] Filtrage des récompenses par catégorie
- [ ] Recherche de récompenses
- [ ] Système de favoris
- [ ] Notifications push
- [ ] Mode hors ligne
- [ ] Partage sur réseaux sociaux

### 12.3 Tests recommandés
- [ ] Tests d'authentification
- [ ] Tests de navigation
- [ ] Tests d'achat complet
- [ ] Tests de gestion d'erreurs
- [ ] Tests de responsive design
- [ ] Tests de performance

---

## 📞 13. SUPPORT ET CONTACT

Pour toute question technique ou support :
- **Téléphone :** +2250710922213
- **WhatsApp :** +2250710922213
- **Email :** misterjohn0798@gmail.com

---

## 📄 14. LICENCE ET CONDITIONS

Cette documentation est fournie à des fins de développement uniquement. L'utilisation des APIs doit respecter les conditions générales de l'application MyWitti.

---

*Documentation mise à jour le : 28/06/2025*
*Version : 1.0*
