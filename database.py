import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Inicializar el cliente de mongoDB
client = AsyncIOMotorClient(MONGODB_URL)

#Seleccionar la bae de datos (se creara automaticamente si no existe)

database = client.ambiente502

# Seleccionar la coleccion (se creara automaticamente si no existe)
collection = database.mesas

async def test_connection():
    try:
        # verificar la conexion al servidor de mongoDB
        await client.admin.command('ping')
        print("Conexión exitosa a MongoDB")

        doctest ={
            "nombre": "Cristoval",
            "edad": 19,
            "genero": "Masculino"
        }

        print("Insertando documento de prueba...")
        result = await collection.insert_one(doctest)
        print(f"Documento insertado con ID: {result.inserted_id}")

        datarequest = await collection.find_one({"_id": result.inserted_id})
        print(f"Documento recuperado: {datarequest}")
        

    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())        