from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import role as crud_role
from app.schemas.role import RoleResponse
from app.security import require_role

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=list[RoleResponse])
def read_roles(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("administrator"))
):
    roles = crud_role.get_all_roles(db)
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
def read_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("administrator"))
):
    role = crud_role.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role