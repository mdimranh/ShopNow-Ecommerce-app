# ShopNow Ecommerce app
![developer](https://img.shields.io/badge/Developed%20By%20%3A-Md%20Imran%20Hossain-red)
--
## Tech Stack

**Client:** HTML, CSS, Bootstrap, Javascript, Jquery

**Server:** Python, Django, Django-Rest-Framework

## Demo Shop

**Shop**:
http://shopnowbd.herokuapp.com

### Admin:
**username**: ```admin@gmail.com```<br/>
**password**: ```admin```<br/>
**link**: http://shopnowbd.herokuapp.com/control

## Run Locally

Clone the project

```bash
  git clone https://https://github.com/mdimranh/ShopNow-Ecommerce-app.git
```

Go to the project directory

```bash
  cd ecomapp
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```
Now click here
http://localhost:8000


## API Reference

#### Registration

```http
  POST /api/registration
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `first_name` | `string` | **Required** |
| `last_name` | `string` | **Required** |
| `email` | `email` | **Required** |
| `password` | `string` | **Required** |

#### Login

```http
  POST /api/token
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `email` | **Required** |
| `password` | `string` | **Required** |

#### ShopCart

```http
  POST /api/myshopcart
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `Header` | `Bearer access` |
