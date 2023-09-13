# migong backend

## Get started

### environment setting

```
cd ..
python3 -m pip install virtualenv
virtualenv venv --python=python3.11
source /venv/bin/activate
```

### package install

```
pip install -r requirements.txt
```

### server start

```
python3 manage.py migrate
python3 manage.py runserver
```

## spec

boto3 : python 용 aws sdk
django-storages : 장고에서 저장소 사용
