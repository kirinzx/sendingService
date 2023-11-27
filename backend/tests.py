import requests
from datetime import datetime, timedelta

domen = "http://127.0.0.1:8000/"

def check_client():
    def check_create():
        print("СОЗДАНИЕ!")
        print("Создание. Ниже должны быть статусы 201")
        for i in range(0,20):
            response = requests.post(url=domen+"client/",json={
                "phone_number": 79998887700 + i,
                "mob_operator_code": "999",
                "tag": "customer",
                "timezone": "Europe/Moscow"
            })
            print(response.status_code)

        for i in range(0,20):
            response = requests.post(url=domen+"client/",json={
                "phone_number": 71118887700 + i,
                "mob_operator_code": "111",
                "tag": "seller",
                "timezone": "Europe/Moscow"
            })

            print(response.status_code)

        print("Тест на ошибки. Снизу должны быть статусы 400")

        response = requests.post(url=domen+"client/",json={
            "phone_number": 71118887700,
            "mob_operator_code": "111",
            "tag": "seller",
            "timezone": "Europe/Moscow"
        })

        print(response.status_code, response.text)

        response = requests.post(url=domen+"client/",json={
            "phone_number": 71111887700,
            "mob_operator_code": "112",
            "tag": "seller",
            "timezone": "Europe/Moscow"
        })

        print(response.status_code, response.text)

        response = requests.post(url=domen+"client/",json={
            "phone_number": 71121887700,
            "mob_operator_code": "111",
            "tag": "seller",
            "timezone": "Europe/Moscow"
        })

        print(response.status_code, response.text)

        response = requests.post(url=domen+"client/",json={
            "phone_number": 77777771122,
            "mob_operator_code": "777",
            "tag": "seller",
            "timezone": "smth"
        })

        print(response.status_code, response.text)

    def check_delete():
        print("УДАЛЕНИЕ")
        print("Удаление. ниже должны быть статусы 204")
        response = requests.delete(url=domen+'client/79998887700')

        print(response.status_code)

        response = requests.delete(url=domen+'client/79998887701')

        print(response.status_code)

        print("Проверка на ошибки. Снизу должны быть статусы 404")

        response = requests.delete(url=domen+'client/0')

        print(response.status_code)

        response = requests.delete(url=domen+'client/79598887701')

        print(response.status_code)

    def check_update():
        print("Обновление")
        print("Снизу должны быть статусы 200")
        response = requests.patch(url=domen+'client/79998887702',data={
            "tag": "broker",
            "timezone": "Europe/Samara"
        })

        print(response.status_code)

        response = requests.patch(url=domen+'client/79998887702',data={
            "phone_number": 79998887701,
        })

        print(response.status_code)

        response = requests.patch(url=domen+'client/79998887701',data={
            "phone_number": 70008887701,
            "mob_operator_code": "000"
        })

        print(response.status_code)

        print("Проверка на ошибки. Снизу должны быть статусы 400")

        response = requests.patch(url=domen+'client/70008887701',data={
            "phone_number": 79998887701,
        })

        print(response.status_code, response.text)

        response = requests.patch(url=domen+'client/70008887701',data={
            "mob_operator_code": "999",
        })

        print(response.status_code, response.text)

        response = requests.patch(url=domen+'client/70008887701',data={
            "tag": "broker",
            "timezone": "1"
        })

        print(response.status_code, response.text)
    
    print("КЛИЕНТ")
    print("-------------------------------------------------")
    check_create()
    print("-------------------------------------------------")
    check_delete()
    print("-------------------------------------------------")
    check_update()
    print("-------------------------------------------------")

def check_sending():
    def check_create():
        print("Создание")
        print("Ниже должны быть статусы 201")
        
        response = requests.post(domen+"sending/",json={
            'start_date': (datetime.utcnow() + timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M"),
            'message_text': 'Тест 1!',
            'client_filter': {
                    'tag': 'customer',
                    'mob_operator_code': None
                },
            'end_date': (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
        })
        print(response.status_code)

        response = requests.post(domen+"sending/",json={
            'start_date': (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"),
            'message_text': 'Тест 2!',
            'client_filter': {
                    'tag': None,
                    'mob_operator_code':"000"
                },
            'end_date': (datetime.utcnow() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
        })
        print(response.status_code)

        response = requests.post(domen+"sending/",json={
            'start_date': (datetime.utcnow() + timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M"),
            'message_text': 'Тест 3!',
            'client_filter': {
                    'tag': None,
                    'mob_operator_code': None
                },
            'end_date': (datetime.utcnow() + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M"),
        })
        print(response.status_code)

        print("Проверка на ошибки. Ниже должны быть статусы 400")

        response = requests.post(domen+"sending/",json={
            'start_date': (datetime.utcnow() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M"),
            'message_text': 'Ошибочный тест!',
            'client_filter': {
                    'tag': 'broker',
                    'mob_operator_code': None
                },
            'end_date': (datetime.utcnow() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M"),
        })
        print(response.status_code, response.text)

        response = requests.post(domen+"sending/",json={
            'start_date': (datetime.utcnow() - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M"),
            'message_text': 'Ошибочный тест!',
            'client_filter': {
                    'tag': 'broker',
                    'mob_operator_code': None
                },
            'end_date': (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"),
        })
        print(response.status_code, response.text)

    def check_delete():
        print("Удаление")
        print("Ожидаем 204")
        response = requests.delete(domen+"sending/1")
        print(response.status_code)
        print("Ожидаем 404")
        response = requests.delete(domen+"sending/125125")
        print(response.status_code, response.text)

    def check_update():
        """
        Вот с такими данными создавалась рассылка с id 3
        json={
            'start_date': (datetime.utcnow() + timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M"),
            'message_text': 'Тест 3!',
            'client_filter': {
                    'tag': None,
                    'mob_operator_code': None
                },
            'end_date': (datetime.utcnow() + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M"),
        }
        """
        print("Обновление")
        print("Ниже должны быть статусы 200")
        
        response = requests.patch(domen+"sending/3",json={
            'message_text': 'Перетест!',
        })
        print(response.status_code)

        response = requests.patch(domen+"sending/3",json={
            'client_filter': {
                "tag": "customer",
                'mob_operator_code': None
            }
        })
        print(response.status_code)

        response = requests.patch(domen+"sending/3",json={
            "start_date": (datetime.utcnow() + timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M")
        })
        print(response.status_code)

        response = requests.patch(domen+"sending/3",json={
            "end_date": (datetime.utcnow() + timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M")
        })
        print(response.status_code)

        print("Проверка на ошибки. Ниже должны быть статусы 400")

        response = requests.patch(domen+"sending/3",json={
            "start_date": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        })
        print(response.status_code, response.text)

        response = requests.patch(domen+"sending/3",json={
            "end_date": (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        })
        print(response.status_code, response.text)

    def check_get():
        print("Получение")
        print("Общая статистика по рассылкам")
        response = requests.get(domen+"sending/")

        print(response.text)

        print("Подробная статистика")

        response = requests.get(domen+"sending/2")

        print(response.text)

    print("РАССЫЛКИ")
    print("-------------------------------------------------")
    check_create()
    print("-------------------------------------------------")
    check_delete()
    print("-------------------------------------------------")
    check_update()
    print("-------------------------------------------------")
    check_get()
    print("-------------------------------------------------")


def main():
    check_client()
    check_sending()

main()