from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routes import cart
from app.logger import setup_logger

logger = setup_logger(__name__)

# Create all tables in the database based on our models
# In production you'd use Alembic migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shopping Cart API",
    description="E-commerce shopping cart management API",
    version="1.0.0",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Catches ALL Pydantic validation errors (422).
    Logs them without exposing sensitive data.
    """
    # Build a safe summary of what went wrong
    error_summary = []
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"])
        error_summary.append(f"{field}: {error['msg']}")

    logger.warning(
        "Validation error on %s %s — %s",
        request.method,
        request.url.path,
        "; ".join(error_summary)
    )

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


# Register the cart router
app.include_router(cart.router)


@app.get("/")
def health_check():
    """Simple health check endpoint."""
    return {"status": "running", "message": "Shopping Cart API is live"}