Vagrant.configure("2") do |config|
  config.vm.box = "almalinux/9"
  config.vm.hostname = "alma"

  # Проброс портов: SSH и метрики на хост
  config.vm.network :forwarded_port, guest: 22,   host: 10022, host_ip: "127.0.0.1"
  config.vm.network :forwarded_port, guest: 8080, host: 18080, host_ip: "127.0.0.1"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.cpus = 2
  end
end
