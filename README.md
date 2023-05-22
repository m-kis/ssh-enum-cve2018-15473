# SSH User Enumeration Script

Ce script permet d'effectuer une énumération des utilisateurs SSH sur un système cible. Il utilise une technique de manipulation des paquets SSH pour déterminer quels noms d'utilisateurs sont valides.

## Utilisation

Le script peut être exécuté avec différentes options :

python ssh_user_enum.py <cible> [-p <port>] [-u <nom_utilisateur>] [-w <wordlist>]
  

- `<cible>` : L'adresse IP du système cible.
- `-p <port>` : (Facultatif) Le port du service SSH (par défaut : 22).
- `-u <nom_utilisateur>` : (Facultatif) Le nom d'utilisateur à vérifier.
- `-w <wordlist>` : (Facultatif) Le chemin vers une wordlist de noms d'utilisateurs.

## Prérequis

- Python 3.x
- Module Paramiko (installé automatiquement si manquant)

## Avertissement

Ce script utilise des techniques de manipulation de paquets SSH pour déterminer quels noms d'utilisateurs sont valides. Il est destiné à des fins éducatives et de test sur des systèmes où vous avez l'autorisation explicite d'effectuer de telles actions. L'utilisation de ce script sans autorisation appropriée peut être illégale. L'auteur et les contributeurs ne sont pas responsables de toute utilisation abusive ou illégale de ce script.

## Auteur

Ce script a été développé par M-KIS. Pour toute question ou commentaire, veuillez contacter contact@m-kis.fr
  
  
