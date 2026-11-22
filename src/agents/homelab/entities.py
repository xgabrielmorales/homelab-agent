from typing import Literal

from pydantic import BaseModel, Field


class DailyReport(BaseModel):
    status: Literal["ok", "atencion", "critico"] = Field(
        description=(
            "'ok' si nada requiere acción, 'atencion' si hay algo que revisar sin urgencia y "
            "'critico' si algo está caído o a punto de fallar."
        ),
    )
    summary: str = Field(
        description=(
            "Reporte en Markdown para una notificación del celular: viñetas cortas, lo más "
            "importante primero, máximo 1500 caracteres."
        ),
    )
