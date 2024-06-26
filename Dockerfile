# Install dependencies
FROM python:3.12 AS dependency
WORKDIR /app

# Install CMake
RUN apt-get update && apt-get install -y cmake

# Install dlib and face_recognition as a separate step for caching
RUN pip install --user dlib
RUN pip install --user face_recognition

COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY resources resources
COPY static static
COPY templates templates
COPY app.py .
COPY face_to_encoding.py .
COPY inference.py .
COPY requirements.txt .
COPY train.py .
COPY models.py .

# Build runtime image
FROM python:3.12 AS run
COPY --from=dependency /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV SERVER_PORT=443
WORKDIR /app
COPY --from=dependency /app .
CMD ["python","app.py"]