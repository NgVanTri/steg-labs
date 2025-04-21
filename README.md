Các bạn sử dụng câu lệnh này để tải bài lab về máy :
imodule https://github.com/NgVanTri/steg-labs/raw/refs/heads/main/stego-basic-hide_bipolar_eh.tar
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip
RUN pip3 install pycryptodome pwntools pyinstaller
