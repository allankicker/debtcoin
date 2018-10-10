# debtcoin (la monnaie forcitycienne)

Ou piece dette en français.

## Principe

debtcoin est une base de données peer-to-peer sécurisée qui permets d'effectuer des reconnaissances de dettes d'un compte à un autre.
Les comptes sont identifiés par des clefs publiques, chaque propriétaire de compte détient la clef privée correspondante à la clef publique enregistrée dans la base de données.

Les règles de fonctionnement de debtcoin sont les suivantes :
- Un debtcoin vaut 1 euro à tout moment 
- Un debtcoin en circulation équivaut à un euro de dette. 
- Un paiement en debtcoin est une reconnaissance de dette, ce qui veut dire que si Alice paie 1 debtcoin à Bob, alors Bob détient une créhance de 1€ sur Alice, Le compte d'Alice est débiteur avec un solde de -1 debtcoin. Lorsque Alice rembourse 1€ à Bob, Bob paie 1 debtcoin à Alice. A la fin du processus, les comptes d'Alice et de Bob sont équilibrés : chacun détient 0 debtcoin. 
- Chaque compte peut créer une infinité de debtcoin étant donné qu'un debtcoin est une reconnaissance de dette. Libre à chacun de reconnaitre autant de dettes qu'il le souhaite vers autant de comptes qu'il le souhaite.
- Comme dans bitcoin, l'historique complet de toutes les transactions (le ledger aka livre de compte) est connu et partagé par tous les clients utilisateurs de debtcoin.
- Comme dans bitcoin, les utilisateurs participent eux-même au travail de validation et diffusion des transactions, via un client peer-to-peer.
- La validation d'une transaction consiste à vérifier que la signature est correcte, c'est à dire qu'Alice a bien signé la transaction de 1 debtcoin vers Bob avec sa propre clef privée.
- Une fois la transaction signée et diffusée, un problème de double dépense apparait : Imaginons qu'Alice a payée 1 debtcoin à Bob en signant et diffusant la transaction au réseau. Bob peut tout à fait re-diffuser la transaction comme si elle était nouvelle. Lorsque le réseau reçoit la 2ème transaction, il n'a aucun moyen de savoir si elle est légitime ou pas. Pour régler ce problème, chaque transaction contient un identifiant unique (UID) inséré et signé par le payeur. Pour un compte donné, le réseau n'intègre la transaction que si l'UID n'est pas déja présent dans la base de données. 


## Composants logiciels

Je vois 3 composants à créer :

### Service de stockage / diffusion des transactions

Il s'agit d'un client peer-to-peer en charge de :
- Traiter les transactions entrantes depuis le réseau et les intégrer à la base de données si elles sont valides,
- Traiter les requetes de mise à jour de la part du réseau (ex: un nouveau noeud à besoin de se mettre à jour, il envoie une requête aux autres noeuds pour récupérer l'historique des transactions),
- Diffuser vers les autres noeuds les transactions sortantes.

Pour ça, on aura besoin de :
- un protocole de communication utilisés par chacun des noeuds,
- une base de données et un client de base de données,
- un service HTTP pour communiquer avec les autres noeuds.

### backend de création / vérification des transactions

Un module en charge de réaliser les opérations cryptographiques nécessaires à :
- la vérification de la validité des transactions entrantes
- la création des transactions sortantes

### Interface ligne de commande pour payer et consulter son solde

Un petit executable à executer dans un terminal avec des options pour payer, consulter son solde, etc. Il sera capable d'intéragir avec un client peer-to-peer et avec le backend de création des transactions. 

## Limitations

- Les adresses des noeuds seront stockées en dur, ainsi que la liste des utilisateurs. 
- Pas de résistance au spam, etc. On tourne sur un réseau local et on se fait confiance. 

## Licence

debtcoin est open-source sous licence GPLv3.
