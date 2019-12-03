# Campaign Service

## Setup a connection with the panel

## Use with Docker Compose

This project is based on Django and depends on `Redis` and `PostgreSQL`

```
  acdc:
    image: lotrekagency/acdc:latest
    env_file:
      - ./envs/acdc.env
    restart: unless-stopped
```

Variables you need to set are:

- SECRET_KEY: The secret Key for the app
- STATIC_URL: The static url for the app
- ENVIRONMENT: environment (DEVELOPMENT, STAGING, PRODUCTION)

- REDIS_HOST: Redis Host
- DB_HOST: PostgreSQL Database Host
- POSTGRES_USER: PostgreSQL DB user
- POSTGRES_PASSWORD: PostgreSQL DB Password
- POSTGRES_DB: PostgreSQL DB name

## Try creating an order

http://localhost:8000/api/deepdata/baldiflex/orders/

```
{
  "externalid": "3246315233",
  "source": "1",
  "email": "alice@example.com",
  "userid": "3246315233",
  "acceptsMarketing": "1",
  "orderNumber": "1057",
  "orderProducts": [
    {
      "externalid": "PROD12345",
      "name": "Pogo Stick",
      "price": "4900",
      "quantity": "1",
      "category": "Toys"
    },
    {
      "externalid": "PROD23456",
      "name": "Skateboard",
      "price": "3000",
      "quantity": "1",
      "category": "Toys"
    }
  ],
  "orderUrl": "https://example.com/orders/3246315233",
  "orderDate": "2016-09-13T17:41:39-04:00",
  "shippingMethod": "UPS Ground",
  "totalPrice": "9111",
  "currency": "USD"
}
```


# Try creating an abandoned cart

http://localhost:8000/api/deepdata/baldiflex/abandoned_cart/

```
{
  "externalcheckoutid": "3246315233",
  "source": "1",
  "email": "alice@example.com",
  "userid": "3246315233",
  "acceptsMarketing": "1",
  "orderProducts": [
    {
      "externalid": "PROD12345",
      "name": "Pogo Stick",
      "price": "4900",
      "quantity": "1",
      "category": "Toys",
      "description": "The most advanced Pogo Stick ever created!",
      "productUrl": "https://example.com/products/pogo-stick",
      "imageUrl": "https://example.com/products/pogo-stick.jpg"
    },
    {
      "externalid": "PROD23456",
      "name": "Skateboard",
      "price": "3000",
      "quantity": "1",
      "category": "Toys",
      "description": "Do a kick flip!",
      "productUrl": "https://example.com/products/skateboard",
      "imageUrl": "https://example.com/products/skateboard.jpg"
    }
  ],
  "orderUrl": "https://example.com/orders/3246315233",
  "externalCreatedDate": "2016-09-13T17:41:39-04:00",
  "externalUpdatedDate": "2016-09-14T13:20:17-04:00",
  "abandonedDate": "2016-09-13T17:41:39-04:00",
  "totalPrice": "9111",
  "currency": "USD"
}
```
