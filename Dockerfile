FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /TODOLIST

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

# COPY backend/ ./backend/

EXPOSE 8000

RUN python backend/manage.py migrate --run-syncdb

# WORKDIR /backend

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]