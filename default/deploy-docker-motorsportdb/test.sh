#!/bin/bash
docker rm -f deploy-motorsportdb 2>/dev/null || true

docker run -d --name deploy-motorsportdb --network host debian:bookworm bash -c "
  set -eux;

  apt-get clean;
  rm -rf /var/lib/apt/lists/*;
  apt-get update;

  for i in 1 2 3; do
    dpkg --configure -a || true;
    apt-get install -f -y || true;
    sleep 2;
  done;

  apt-get install -y git acl wget apache2 php libapache2-mod-php;

  rm -rf /var/www/html;
  mkdir -p /var/www;
  cd /var/www;
  git clone -b in-dev https://github.com/Motorsport-DB/website html;
  cd html;
  git clone https://github.com/Motorsport-DB/races;
  git clone https://github.com/Motorsport-DB/teams;
  git clone https://github.com/Motorsport-DB/drivers;

  setfacl -R -m u:www-data:rwX .;
  setfacl -dR -m u:www-data:rwX .;
  chmod -R u+rwX .;

  echo 'ServerName localhost' >> /etc/apache2/apache2.conf;

  # Modifier Apache pour écouter sur le port 8043 au lieu de 80
  sed -i 's/Listen 80/Listen 8043/' /etc/apache2/ports.conf
  sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8043>/' /etc/apache2/sites-available/000-default.conf

  apt-get update;
  apt-get install -y wget;
  wget -q https://github.com/grafana/k6/releases/download/v0.48.0/k6-v0.48.0-linux-amd64.deb;
  dpkg -i k6-v0.48.0-linux-amd64.deb || apt-get install -f -y;

  apache2ctl -D FOREGROUND
"

echo "⏳ Attente que apache démarre dans le container..."
until docker exec deploy-motorsportdb pgrep apache2 > /dev/null 2>&1; do
  sleep 2
done
echo "✅ Apache est prêt."

echo "🚀 Container déployé et accessible sur le port 8043."
