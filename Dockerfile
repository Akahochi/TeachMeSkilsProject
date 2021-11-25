FROM python:3.10.0-alpine3.14

WORKDIR /app/

ENV PYTHONDONTVRITEBYTECODE 1

#Requirements for postgresql
RUN apk update && apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Requirements for Pillow
RUN apk add jprg-dev zlib-dev freatype-dev lcms2-dev openjpeg-dev tiff-dav tel-dev

# Install requirements
RUN pip install --upgradw pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/some_site/

#CMD ["python", "manage.py", "runserver"]
ENTRYPOINT ["python", "manage.py"]
