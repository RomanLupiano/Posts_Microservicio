# Servicio de Publicaciones
Este repositorio contiene el servicio de publicaciones de una red social simple. El servicio maneja las publiciones y likes de los usuarios.


#### Pasos a seguir
1. python -m venv env
2. source ./env/bin/activate
3. pip install -r requirements.txt
4. cd Posts/
5. uvicorn main:app --reload



### Framework y herramientas utilizados 🛠️
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Requests](https://pypi.org/project/requests/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Typing](https://docs.python.org/3/library/typing.html)
- [Peewee](http://docs.peewee-orm.com/en/latest/) -> SQLite
