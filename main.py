from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import psycopg2


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

numbers = [
    {
        "id": 1,
        "name": "Artur",
        "phone_number": "8 995 886 10-43"
     },
    {
        "id": 2,
        "name": "Sonia",
        "phone_number": "8 993 636 10-53"
    },
]

@app.get("/")
def main_proceed():
    return "Главная страница справочника"


@app.get("/numbers", tags=["Номера"], summary="Получить список всех номеров")
def read_numbers():
    return numbers


@app.get("/numbers/{number_id}", tags=["Номера"], summary="Получить информацию о конкретном номере")
def read_number(number_id: int):
    for number in numbers:
        if number["id"] == number_id:
            return number
    raise HTTPException(status_code=404, detail="Номер не найден")


class NewNumber(BaseModel):
    name: str
    phone_number: str


@app.post("/numbers", tags=["Номера"])
def create_number(new_number: NewNumber):
    numbers.append(
        {
            "id": len(numbers) + 1,
            "name": new_number.name,
            "phone_number": new_number.phone_number
        })
    return {"success": True, "message": "Номер успешно добавлен"}




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)