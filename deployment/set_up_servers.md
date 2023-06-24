## Server Set Up

#### Clone the Repository
```commandline
git clone https://github.com/ntua/apistresstesting.git
```

#### Set Up Docker
```commandline
sudo apt-get update -y
sudo apt-get install ca-certificates curl gnupg -y

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo docker run hello-world
```

#### Set Up Python
```commandline
sudo apt install zsh -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sudo apt-get install make -y
sudo apt install python3.10-venv -y
```

```commandline
sudo PYTHONPATH="${PYTHONPATH}:/home/alexk/apistresstesting" venv/bin/python3 ./architectures/serialised_rmq.py
```

```commandline
sudo docker compose -f deployment/docker-compose-.yml up -d
```

```commandline
http://10.3.2.71:3001 : Grafana
http://10.3.2.72:8080 : RedPanda
http://10.3.2.73:8080 : DB
http://10.3.2.74:9090 : Prometheus
http://api.diem-platform.com: API
```
