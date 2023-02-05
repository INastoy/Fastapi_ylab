import uuid

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from apps.menu.crud import SubmenuCRUD
from apps.menu.schemas import BaseSchema, SubmenuSchema

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenu'])


@router.get(
    '/',
    response_model=list[SubmenuSchema],
    status_code=HTTP_200_OK,
    summary='Список подменю',
)
async def get_submenus(menu_id: uuid.UUID, submenu: SubmenuCRUD = Depends()):
    """Возвращает список всех подменю с количеством всех блюд"""
    return await submenu.get_all(menu_id)


@router.get(
    '/{submenu_id}',
    response_model=SubmenuSchema,
    status_code=HTTP_200_OK,
    summary='Получить подменю',
)
async def get_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SubmenuCRUD = Depends()):
    """Возвращает указанное подменю с количеством всех блюд"""
    return await submenu.get_by_id(submenu_id, menu_id)


@router.post(
    '/',
    response_model=SubmenuSchema,
    status_code=HTTP_201_CREATED,
    summary='Создать подменю',
)
async def create_submenu(menu_id: uuid.UUID, submenu_data: BaseSchema, submenu: SubmenuCRUD = Depends()):
    """Создает новое меню"""
    return await submenu.create(submenu_data, menu_id)


@router.delete('/{submenu_id}', status_code=HTTP_200_OK, summary='Удалить подменю')
async def delete_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SubmenuCRUD = Depends()):
    """Удаляет указанное меню"""
    return await submenu.delete(submenu_id, menu_id)


@router.patch('/{submenu_id}', response_model=SubmenuSchema, summary='Изменить подменю')
async def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu_data: BaseSchema,
    submenu: SubmenuCRUD = Depends(),
):
    """Обновляет указанное меню"""
    return await submenu.update(submenu_id, submenu_data, menu_id)
