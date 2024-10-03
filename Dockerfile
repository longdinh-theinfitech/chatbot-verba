FROM python:3.11
WORKDIR /Verba

# Tạo môi trường ảo trong container
RUN python -m venv /opt/venv

# Kích hoạt môi trường ảo
ENV PATH="/opt/venv/bin:$PATH"

# Copy code vào container
COPY . /Verba

# Cài đặt thư viện từ môi trường ảo
RUN pip install -e .

EXPOSE 8000

CMD ["verba", "start", "--port", "8000", "--host", "0.0.0.0"]
