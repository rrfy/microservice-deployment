Коротко: ниже пошаговый README в формате Markdown для развёртывания с нуля на Ubuntu‑хосте: установка VirtualBox, Vagrant, Ansible и Docker, клонирование репозитория, подъём ВМ через Vagrant, получение SSH‑параметров, запуск плейбука Ansible для сборки образа и старта контейнера, а также проверка метрик и основные советы по отладке.[1][2][3][4]

### Описание

Гайд разворачивает сервис из репозитория rrfy/microservice-deployment локально на хосте без предустановленного VirtualBox, Vagrant, Ansible и Docker, создаёт ВМ через Vagrant/VirtualBox, настраивает проброс портов для SSH и метрик, доставляет сервис с помощью Ansible, собирает Docker‑образ и запускает контейнер, после чего метрики доступны по 18080 на хосте и 8080 внутри ВМ.[3][4]

## Установка инструментов на хост

- Установить Vagrant с официальной страницы установки для Linux/Ubuntu, затем проверить версию командой vagrant --version.
- Установить Ansible на Ubuntu, выполнив sudo apt install ansible; проверить ansible --version.
- Установить Docker Engine на Ubuntu по официальной инструкции Docker и убедиться, что демон запущен (systemctl status docker).
- Установить VirtualBox и убедиться, что доступна настройка NAT Port Forwarding для проброса портов к ВМ.

## Получение кода проекта

- Склонировать репозиторий с файлами проекта на хосте: git clone git@github.com:rrfy/microservice-deployment.git и перейти в каталог проекта, где уже лежат все нужные файлы.

## Подъём виртуальной машины (Vagrant + VirtualBox)

- Vagrantfile в проекте должен описывать бокс AlmaLinux/Ubuntu с пробросом портов: 22→10022 для SSH и 8080→18080 для метрик, что обеспечивает доступ Ansible и проверку сервиса с хоста по 127.0.0.1:18080.
- Поднять ВМ командой vagrant up, чтобы Vagrant скачал образ бокса и создал ВМ в VirtualBox с NAT и forwarded_port согласно Vagrantfile.
- Получить фактические SSH‑параметры ВМ: vagrant ssh-config, из этого вывода нужны HostName, Port, User и IdentityFile для Ansible inventory.

## Конфигурация Ansible инвентори

- Создать или обновить inventory и внести параметры подключения из vagrant ssh-config, например:  
  ```
  [vm]
  alma ansible_host=127.0.0.1 ansible_port=10022 ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/alma/virtualbox/private_key
  ```
- Проверить инвентори: ansible-inventory -i inventory --list, чтобы убедиться, что Ansible видит группу и хост корректно.
- Запустить Ansible playbook из корня проекта командой
```
ansible-playbook -i inventory playbook.yml
```
- Метрики для Prometheus находятся на хостовой машине по адрессу http://127.0.0.1:18080/metrics
