from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import APIRouter, Query, Path, HTTPException, Body
from starlette.responses import JSONResponse

from api.responses.detail import DetailResponse

router = APIRouter()


class NameIn(BaseModel):
    name: str


@router.get("/", response_model=DetailResponse)
def hello_world():
    """
    this is the hello world and goes to swagger an host/docs
    """
    return DetailResponse(message="hello world")


@router.get("/hello", response_model=DetailResponse)
def send_data_query(name: str = Query(..., title="Name", description="the Name")):
    return DetailResponse(message=f"hello {name}")


@router.post("hello/name", response_model=DetailResponse)
def send_data_body(name: NameIn = Body(...)):
    """
    Response with Hello name, where name is user provided
    """
    return DetailResponse(message=f"hello {name}")


@router.post("hello/{name}", response_model=DetailResponse)
# we cant pass Model in path
def send_data_path(name: str = Path(..., name="path param", description="description")):
    """
    Response with Hello name, where name is user provided in query param
    """
    return DetailResponse(message=f"hello {name}")


@router.delete(
    "/delete/{name}",
    response_model=DetailResponse,
    responses={401: {"model": DetailResponse}},
)
def delete_data(name: str = Path(...)):
    if name == "admin":
        # this is terrible >.<
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder(DetailResponse(message="can't delete admin")),
        )
    return DetailResponse(message="ok")


@router.get("/error")
def get_error_http():
    raise HTTPException(status_code=404, detail="not found")
