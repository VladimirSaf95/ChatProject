from fixture.helper_base import HelperBase
from fixture.api_client import APIClient
import pytest
import os
import time

def test_show_chat_messages(app,api_client):
    helper_base = HelperBase(app)

    # Проверка если чат открыт
    if helper_base.check_chatbutton_existence() is False:
        #Кликаем на иконку закрытие чата
        helper_base.clickchatbutton()

    #Получаем айди сообщения отправленного ранее
    event_id = os.environ.get("EVENT_ID_A")

    # Проверка, что event_id был получен в предыдущем тесте
    if event_id is None:
        responseA = api_client.sendmessages(response_b=False)
        event_id = os.environ.get("EVENT_ID_A")

    time.sleep(3)

    # Проверить наличие элемента с соответствующим id
    elements = helper_base.find_elements_by_id(f"message_{event_id}")
    assert elements, f"Сообщение с ID {event_id} не найдено."


