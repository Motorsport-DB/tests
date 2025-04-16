docker rm -f deploy-motorsportdb || true

docker run -d -p 8043:80 -v /var/run/docker.sock:/var/run/docker.sock --name deploy-motorsportdb debian:bookworm bash -c "
  apt-get update && \
  apt-get install -y apache2 php libapache2-mod-php git && \
  mkdir -p /var/www && \
  cd /var/www && \
  rm -rf html && \
  git clone https://github.com/Motorsport-DB/website html && \
  cd html && \
  git clone https://github.com/Motorsport-DB/races && \
  git clone https://github.com/Motorsport-DB/teams && \
  git clone https://github.com/Motorsport-DB/drivers && \
  echo 'Déploiement réussi !' && \
  echo 'ServerName localhost' >> /etc/apache2/apache2.conf && \
  apache2ctl -D FOREGROUND"