from sqlmodel import Session
from app.core.database import engine
from app.models.modelos import Categoria, Plato


def run_seed():
    with Session(engine) as session:

        # Categorías
        categorias_nombres = ["Comidas", "Bebidas", "Postres"]

        categorias = []
        for nombre in categorias_nombres:
            cat = Categoria(nombre=nombre)
            session.add(cat)
            categorias.append(cat)

        session.commit()

        # Listas de platos
        comidas = [
            "Hamburguesa clásica",
            "Pollo frito",
            "Sándwich de lomito",
            "Pasta carbonara",
            "Tacos mixtos",
            "Lasagna",
            "Salchipapa",
            "Churrasco",
            "Pizza personal",
            "Ensalada César"
        ]

        bebidas = [
            "Coca Cola",
            "Agua mineral",
            "Jugo de naranja",
            "Limonada",
            "Té helado",
            "Café americano",
            "Café latte",
            "Batido de chocolate",
            "Refresco de maracuyá",
            "Sprite"
        ]

        postres = [
            "Helado de vainilla",
            "Torta de chocolate",
            "Flan casero",
            "Brownie",
            "Cheesecake",
            "Gelatina",
            "Pie de limón",
            "Tres leches",
            "Cupcake",
            "Alfajor"
        ]

        precios_demo = {
            "Comidas": 25,
            "Bebidas": 8,
            "Postres": 12
        }

        # Crear platos
        for cat in categorias:
            if cat.nombre == "Comidas":
                lista = comidas
            elif cat.nombre == "Bebidas":
                lista = bebidas
            else:
                lista = postres

            for nombre_plato in lista:
                session.add(
                    Plato(
                        nombre=nombre_plato,
                        precio_venta=precios_demo[cat.nombre],
                        categoria_id=cat.id
                    )
                )

        session.commit()
        print("Seed realizado.")


if __name__ == "__main__":
    run_seed()
