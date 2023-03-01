from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hello_world():
    """
        this is the hello world and goes to swagger an host/docs
    :return:
    """
    return "hello world"
