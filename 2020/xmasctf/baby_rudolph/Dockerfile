FROM debian:10-slim
RUN apt-get update && apt-get install -y qemu-system-arm
COPY ./kernel /root/kernel
COPY ./rootfs /root/rootfs
EXPOSE 8000/tcp

CMD ["/usr/bin/qemu-system-aarch64", "-M", "virt", "-cpu", "cortex-a57", "-m", "128", "-kernel", "/root/kernel", "-initrd", "/root/rootfs", "-nographic", "-serial", "mon:stdio", "-append", "console=ttyAMA0 FLAG=\"XMAS{This_is_Flag!!}\"", "-netdev", "user,id=n1,hostfwd=tcp::8000-:8000", "-device", "virtio-net-pci,netdev=n1"]


