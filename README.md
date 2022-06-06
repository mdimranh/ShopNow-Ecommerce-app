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

### Registration

```http
  POST /api/registration
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `first_name` | `string` | **Required** |
| `last_name` | `string` | **Required** |
| `email` | `email` | **Required** |
| `password` | `string` | **Required** |

### Login

```http
  POST /api/token
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `email` | **Required** |
| `password` | `string` | **Required** |

```http
  POST /api/resfresh
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required** |

### ShopCart

```http
  GET /api/myshopcart
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, get from /api/token'" | **Required** |

### Wishlist

```http
  GET /api/wishlist
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/wishlist/delete/<int:id>[product id]
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

### Product

```http
  GET /api/products
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/product/<int:id>
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/products/new-product
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `date_range` | `int`[no of days] | **Required** |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/products/hot-product
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/products/recently-view
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `no_of_product` | `int` | **Required** |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/products/best-sold
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `date_range` | `int`[no of days] | **Required** |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/products/latest-sold
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `no_of_product` | `int` | **Required** |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/products/product-carousel
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

### Category

```http
  GET /api/categories
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |

```http
  GET /api/category/<int:id> [category id]
```

| Parameter | Type/Value     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` [Header] | "Bearer 'access key, from /api/token'" | **Required** |
