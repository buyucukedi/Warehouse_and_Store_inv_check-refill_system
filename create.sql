CREATE TABLE Store(
	id varchar(4) PRIMARY KEY,
    name varchar(20),
    address varchar(10) UNIQUE
);

CREATE TABLE Warehouse(
	id varchar(4) PRIMARY KEY,
    name varchar(20),
    address varchar(10) UNIQUE
);

CREATE TABLE Product(
	name varchar(20),
    brand varchar(20),
    price int,
    PRIMARY KEY(brand, name)
);

CREATE TABLE Sells(
	product_name varchar(20),
    product_brand varchar(20),
    store_id varchar(4),
    quantity int,
    PRIMARY KEY(product_brand, product_name, market_id),
    FOREIGN KEY(product_brand, product_name) REFERENCES Product(brand, name),
	FOREIGN KEY(store_id) REFERENCES Store(id)
);

CREATE TABLE Owns(
	product_name varchar(20),
    product_brand varchar(20),
    warehouse_id varchar(4),
    quantity int,
    PRIMARY KEY(product_brand, product_name, warehouse_id),
    FOREIGN KEY(product_brand, product_name) REFERENCES Product(brand, name),
	FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id)
);