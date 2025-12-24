from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        table_price VARCHAR(255) NULL,
        product_price VARCHAR(255) NULL,
        all_price VARCHAR(255) NULL,
        hour_table_night VARCHAR(255) NULL,
        hour_table_day VARCHAR(255) NULL,
        benefit BIGINT NULL,
        damage BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_billard(self):
        sql = """
        CREATE TABLE IF NOT EXISTS billiard (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(255) NOT NULL,
        start_time varchar(255) NOT NULL,
        finish_time varchar(255) NULL,
        other varchar(255) NULL,
        price varchar(255) NULL,
        telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_product(self):
        sql = """
        CREATE TABLE IF NOT EXISTS product (
        id SERIAL PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        table_name VARCHAR(255) NULL,
        waiting_person varchar(255) NULL,
        product_number varchar(255) NULL,
        product_price varchar(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_nakladnoy(self):
        sql = """
        CREATE TABLE IF NOT EXISTS nakladnoy (
        id SERIAL PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        have_product INTEGER NOT NULL,
        original_price BIGINT,
        sell_price BIGINT
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, table_price, product_price, all_price, hour_table_night, hour_table_day, benefit, damage):
        sql = "INSERT INTO users (full_name, username, telegram_id, table_price, product_price, all_price, hour_table_night, hour_table_day, benefit, damage) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) returning *"
        return await self.execute(sql, full_name, username, telegram_id, table_price, product_price, all_price, hour_table_night, hour_table_day, benefit, damage, fetchrow=True)


    async def add_billiard(self, table_name, start_time, finish_time, other, price, telegram_id):
        sql = "INSERT INTO billiard (table_name, start_time, finish_time, other, price, telegram_id) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, table_name, start_time, finish_time, other, price, telegram_id, fetchrow=True)
    
    async def add_product(self,product_name, table_name, waiting_person, product_number, product_price):
        sql = "INSERT INTO product (product_name, table_name, waiting_person, product_number, product_price) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, product_name, table_name, waiting_person, product_number, product_price, fetchrow=True)
    
    async def add_nakladnoy(self,product_name, have_product, original_price, sell_price):
        sql = "INSERT INTO nakladnoy (product_name, have_product, original_price, sell_price) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, product_name, have_product, original_price, sell_price, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)
    
    async def select_all_billiard(self):
        sql = "SELECT * FROM billiard"
        return await self.execute(sql, fetch=True)
    
    async def select_all_products(self):
        sql = "SELECT * FROM product"
        return await self.execute(sql, fetch=True)
    
    async def select_all_nakladnoy(self):
        sql = "SELECT * FROM nakladnoy"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_billiard(self, **kwargs):
        sql = "SELECT * FROM billiard WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_product(self, **kwargs):
        sql = "SELECT * FROM product WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_nakladnoy(self, **kwargs):
        sql = "SELECT * FROM nakladnoy WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)
    
    async def count_billiard(self):
        sql = "SELECT COUNT(*) FROM billiard"
        return await self.execute(sql, fetchval=True)
    
    async def count_nakladnoy(self):
        sql = "SELECT COUNT(*) FROM nakladnoy"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
    
    async def update_user_table(self, table_price, telegram_id):
        sql = "UPDATE Users SET table_price=$1 WHERE telegram_id=$2"
        return await self.execute(sql, table_price, telegram_id, execute=True)
    
    async def update_user_all_price(self, table_price, telegram_id):
        sql = "UPDATE Users SET all_price=$1 WHERE telegram_id=$2"
        return await self.execute(sql, table_price, telegram_id, execute=True)
    
    async def update_user_product(self, product_price, telegram_id):
        sql = "UPDATE Users SET product_price=$1 WHERE telegram_id=$2"
        return await self.execute(sql, product_price, telegram_id, execute=True)
    
    async def update_user_benefit(self, benefit, telegram_id):
        sql = "UPDATE Users SET benefit=$1 WHERE telegram_id=$2"
        return await self.execute(sql, benefit, telegram_id, execute=True)
    
    async def update_user_damage(self, damage, telegram_id):
        sql = "UPDATE Users SET damage=$1 WHERE telegram_id=$2"
        return await self.execute(sql, damage, telegram_id, execute=True)
    
    async def select_products_by_table(self, table_name):
        sql = "SELECT * FROM product WHERE table_name=$1"
        return await self.execute(sql, table_name, fetch=True)


    async def update_product_number(self, product_number, id):
        sql = "UPDATE product SET product_number=$1 WHERE id=$2"
        return await self.execute(sql, product_number, id, execute=True)
    
    async def update_product_price(self, product_price, id):
        sql = "UPDATE product SET product_price=$1 WHERE id=$2"
        return await self.execute(sql, product_price, id, execute=True)
    
    async def update_nakladnoy_have(self, have_product, product_name):
        sql = "UPDATE nakladnoy SET have_product=$1 WHERE product_name=$2"
        return await self.execute(sql, have_product, product_name, execute=True)
    
    async def delete_billiard(self, table_name, telegram_id=None):
        sql = """
        DELETE FROM billiard 
        WHERE table_name = $1 
        AND (telegram_id = $2)
        """
        return await self.execute(sql, table_name, telegram_id, execute=True)
    
    async def delete_product(self, table_name, product_name):
        sql = """
        DELETE FROM product
        WHERE table_name = $1 AND product_name = $2
        """
        await self.execute(sql, table_name, product_name, execute=True)

    async def delete_product_for_id(self, ID):
        sql = """
        DELETE FROM product
        WHERE id = $1
        """
        await self.execute(sql, ID, execute=True)

    
    
    async def delete_nakladnoy(self, product_name: str):
        sql = "DELETE FROM nakladnoy WHERE product_name=$1"
        return await self.execute(sql, product_name, execute=True)


    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
