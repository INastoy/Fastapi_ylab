import uuid

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from apps.menu.crud import MenuCRUD
from apps.menu.schemas import BaseSchema, MenuSchema

router = APIRouter(prefix='/menus', tags=['menu'])


@router.get('/', response_model=list[MenuSchema], status_code=HTTP_200_OK, summary='Список меню')
async def get_menus(menu: MenuCRUD = Depends()):
    """Возвращает список всех меню с количеством всех подменю и блюд"""
    return await menu.get_all()


@router.get(
    '/{menu_id}',
    response_model=MenuSchema,
    status_code=HTTP_200_OK,
    summary='Получить меню',
)
async def get_menu(menu_id: uuid.UUID, menu: MenuCRUD = Depends()):
    """Возвращает меню с количеством всех подменю и блюд"""
    return await menu.get_by_id(menu_id)


@router.post('/', response_model=MenuSchema, status_code=HTTP_201_CREATED, summary='Создать меню')
async def create_menu(menu_data: BaseSchema, menu: MenuCRUD = Depends()):
    """Создает новое меню"""
    return await menu.create(menu_data)


@router.delete('/{menu_id}', status_code=HTTP_200_OK, summary='Удалить меню')
async def delete_menu(menu_id: uuid.UUID, menu: MenuCRUD = Depends()):
    """Удаляет указанное меню"""
    return await menu.delete(menu_id)


@router.patch('/{menu_id}', response_model=MenuSchema, summary='Обновить меню')
async def update_menu(menu_id: uuid.UUID, menu_data: BaseSchema, menu: MenuCRUD = Depends()):
    """Обновляет указанное меню"""
    return await menu.update(menu_id, menu_data)


@router.post(
    '/menus/fill',
    status_code=HTTP_201_CREATED,
    summary='Заполняет базу тестовыми данными',
)
async def fill_menus(menu: MenuCRUD = Depends()):
    """Создает тестовые меню, подменю и блюда на основе .json файла"""
    return await menu.create_example(file_path='core/example_db_filler.json')


@router.post(
    '/menus/gen_excel',
    status_code=HTTP_202_ACCEPTED,
    summary='Сгенерировать .xlsx файл с меню',
)
async def gen_excel(menu: MenuCRUD = Depends()):
    """Генерирует пример заполненного меню с подменю и блюдами.
    При вызове возвращает id, по которому можно получить файл через эндпоинт get_excel
    """
    return await menu.gen_excel()


@router.get(
    '/menus/get_excel',
    response_class=FileResponse,
    status_code=HTTP_200_OK,
    summary='Скачать Меню.xlsx',
)
async def get_excel(file_id: uuid.UUID):
    """Возвращает Excel файл с текущим меню, подменю и блюдами.
    Для получения файла требуется получить file_id в энпоинте gen_excel"""
    return FileResponse(path=f'{file_id}.xlsx', media_type='multipart/form-data', filename='Меню.xlsx')
