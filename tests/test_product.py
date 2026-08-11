def create_warehouse(client):
    response = client.post(
        "/warehouses/",
        json={
            "name": "Test Warehouse",
            "city": "Test City"
        }
    )

    assert response.status_code == 201

    return response.json()


def create_product(client, warehouse_id):
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "quantity": 0,
            "warehouse_id": warehouse_id
        }
    )

    assert response.status_code == 201

    return response.json()


def test_incoming_movement(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    response = client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 10
        }
    )

    assert response.status_code == 201

    movement = response.json()

    assert movement["product_id"] == product["id"]
    assert movement["movement_type"] == "IN"
    assert movement["quantity"] == 10


def test_outgoing_movement(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 10
        }
    )

    response = client.post(
        "/movements/out",
        json={
            "product_id": product["id"],
            "quantity": 4
        }
    )

    assert response.status_code == 201

    movement = response.json()

    assert movement["product_id"] == product["id"]
    assert movement["movement_type"] == "OUT"
    assert movement["quantity"] == 4

def test_outgoing_movement_not_enough_stock(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    response = client.post(
        "/movements/out",
        json={
            "product_id": product["id"],
            "quantity": 10
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough products in stock"


def test_movement_product_not_found(client):
    response = client.post(
        "/movements/in",
        json={
            "product_id": 999999,
            "quantity": 10
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_movement_invalid_quantity(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    response = client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 0
        }
    )

    assert response.status_code == 422


def test_get_movements(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 10
        }
    )

    response = client.get("/movements/")

    assert response.status_code == 200

    movements = response.json()

    assert len(movements) == 1
    assert movements[0]["product_id"] == product["id"]
    assert movements[0]["movement_type"] == "IN"
    assert movements[0]["quantity"] == 10


def test_get_movements_by_product(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 10
        }
    )

    response = client.get(
        f"/movements/?product_id={product['id']}"
    )

    assert response.status_code == 200

    movements = response.json()

    assert len(movements) == 1
    assert movements[0]["product_id"] == product["id"]

def test_transfer_product(client):
    source_warehouse = create_warehouse(client)

    destination_response = client.post(
        "/warehouses/",
        json={
            "name": "Destination Warehouse",
            "city": "Destination City"
        }
    )

    assert destination_response.status_code == 201

    destination_warehouse = destination_response.json()

    product = create_product(
        client,
        source_warehouse["id"]
    )

    # Добавляем 10 единиц товара
    response = client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 10
        }
    )

    assert response.status_code == 201

    # Перемещаем 4 единицы
    response = client.post(
        "/movements/transfer",
        json={
            "product_id": product["id"],
            "to_warehouse_id": destination_warehouse["id"],
            "quantity": 4
        }
    )

    assert response.status_code == 200

    # Проверяем остаток на исходном складе
    response = client.get(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200

    source_product = response.json()

    assert source_product["quantity"] == 6
    assert source_product["warehouse_id"] == source_warehouse["id"]

    # Проверяем товар на новом складе
    response = client.get(
        f"/products/?warehouse_id={destination_warehouse['id']}"
    )

    assert response.status_code == 200

    products = response.json()["items"]

    assert len(products) == 1

    destination_product = products[0]

    assert destination_product["name"] == product["name"]
    assert destination_product["quantity"] == 4
    assert destination_product["warehouse_id"] == destination_warehouse["id"]

    # Проверяем историю движений
    response = client.get("/movements/")

    assert response.status_code == 200

    movements = response.json()

    assert len(movements) == 3

    movement_types = {
        movement["movement_type"]
        for movement in movements
    }

    assert movement_types == {"IN", "OUT"}

    incoming_movements = [
        movement
        for movement in movements
        if movement["movement_type"] == "IN"
    ]

    outgoing_movements = [
        movement
        for movement in movements
        if movement["movement_type"] == "OUT"
    ]

    assert len(incoming_movements) == 2
    assert len(outgoing_movements) == 1

    assert outgoing_movements[0]["quantity"] == 4
    assert outgoing_movements[0]["product_id"] == product["id"]

    destination_incoming = [
        movement
        for movement in incoming_movements
        if movement["quantity"] == 4
    ]

    assert len(destination_incoming) == 1
    assert destination_incoming[0]["product_id"] == destination_product["id"]

def test_transfer_not_enough_stock(client):
    source_warehouse = create_warehouse(client)

    destination_response = client.post(
        "/warehouses/",
        json={
            "name": "Destination Warehouse",
            "city": "Destination City"
        }
    )

    assert destination_response.status_code == 201

    destination_warehouse = destination_response.json()

    product = create_product(
        client,
        source_warehouse["id"]
    )

    response = client.post(
        "/movements/transfer",
        json={
            "product_id": product["id"],
            "to_warehouse_id": destination_warehouse["id"],
            "quantity": 10
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough products in stock"


def test_transfer_same_warehouse(client):
    warehouse = create_warehouse(client)

    product = create_product(
        client,
        warehouse["id"]
    )

    response = client.post(
        "/movements/transfer",
        json={
            "product_id": product["id"],
            "to_warehouse_id": warehouse["id"],
            "quantity": 1
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Source and destination warehouses are the same"
    )


def test_transfer_does_not_change_stock_on_failure(client):
    source_warehouse = create_warehouse(client)

    destination_response = client.post(
        "/warehouses/",
        json={
            "name": "Destination Warehouse",
            "city": "Destination City"
        }
    )

    assert destination_response.status_code == 201

    destination_warehouse = destination_response.json()

    product = create_product(
        client,
        source_warehouse["id"]
    )

    # Добавляем 5 единиц
    response = client.post(
        "/movements/in",
        json={
            "product_id": product["id"],
            "quantity": 5
        }
    )

    assert response.status_code == 201

    # Пытаемся переместить 10 единиц,
    # хотя на складе есть только 5
    response = client.post(
        "/movements/transfer",
        json={
            "product_id": product["id"],
            "to_warehouse_id": destination_warehouse["id"],
            "quantity": 10
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough products in stock"

    # Проверяем, что исходный остаток не изменился
    response = client.get(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200

    source_product = response.json()

    assert source_product["quantity"] == 5

    # Проверяем, что товар на складе назначения не появился
    response = client.get(
        f"/products/?warehouse_id={destination_warehouse['id']}"
    )

    assert response.status_code == 200

    products = response.json()["items"]

    assert len(products) == 0

    # Проверяем историю движений
    response = client.get("/movements/")

    assert response.status_code == 200

    movements = response.json()

    # Должно остаться только первоначальное IN
    assert len(movements) == 1
    assert movements[0]["movement_type"] == "IN"
    assert movements[0]["quantity"] == 5

def test_transfer_invalid_quantity(client):
    source_warehouse = create_warehouse(client)

    destination_response = client.post(
        "/warehouses/",
        json={
            "name": "Destination Warehouse",
            "city": "Destination City"
        }
    )

    assert destination_response.status_code == 201

    destination_warehouse = destination_response.json()

    product = create_product(
        client,
        source_warehouse["id"]
    )

    # Проверяем quantity = 0
    response = client.post(
        "/movements/transfer",
        json={
            "product_id": product["id"],
            "to_warehouse_id": destination_warehouse["id"],
            "quantity": 0
        }
    )

    assert response.status_code == 422

    # Проверяем отрицательное количество
    response = client.post(
        "/movements/transfer",
        json={
            "product_id": product["id"],
            "to_warehouse_id": destination_warehouse["id"],
            "quantity": -5
        }
    )

    assert response.status_code == 422