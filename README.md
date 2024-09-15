# SMAKOLYK

### A site that helps to manage catering services

## Installation


### Requirements
    
- `Docker`
- `Docker-Compose`
- `Git`

### I. Clone the repository:
```bash
git clone https://github.com/iamnovichek/smakolyk.git
```

### II. Go to the `smakolyk/` directory:
```bash
cd smakolyk
```

### III. Provide all required environment variables
#### a) Create `.env` file or run the following command
```bash
mv .env.example .env
```

#### b) Provide all missing values where there is `#`:
##### (How and where to obtain `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` it will be explained at the end of this documentation)
```
# DB settings
DB_PORT=5432
DB_HOST=postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST_AUTH_METHOD=md5
# Django settings
SECRET_KEY=#
# SMTP settings
EMAIL_HOST_USER=#
EMAIL_HOST_PASSWORD=#
# Site management settings
ACCOUNTANT=#
ORDERS_RECEIVER=#
# Celery
CELERY_BROKER_IP=redis
```

# !!!WARNING!!!
## You WON'T be able to make your orders on weekend due to the website logic. If you want to do so, follow steps below.

### 1. Go to `apps/smakolyk/views.py`
### 2. Comment out these lines of code (114 and 115):

```python
if self.is_weekend():
    return redirect("smakolyk:weekend")
```
### IV. Now you can run build script
```bash
docker-compose up -d --build
```

## Additional info like "How and where to obtain `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`"

## 1) How and where to obtain `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`?
### a) You must have Google account
### b) Go to `https://myaccount.google.com/`
### c) Then go to security
### d) Write `Application passwords` (or whatever account language you have set) and go to
### e) Just create a new one
### f) Now save the password Google provided you and assign it to `EMAIL_HOST_PASSWORD`
### g) For `EMAIL_HOST_USER` you should set your Google account email address

## 2) How and where to obtain `ACCOUNTANT` and `ORDERS_RECEIVER`?
### - You can prive the same address you gave for `EMAIL_HOST_USER`
