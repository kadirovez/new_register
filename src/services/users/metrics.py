
import psutil

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import PlainTextResponse

from src.utils.get_active_login_sessions import get_active_login_sessions
from src.utils.get_active_users import get_active_users


async def get_all_data(
        db: AsyncSession
):

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    network = psutil.net_io_counters()
    active_login_sessions = await get_active_login_sessions(db=db)
    active_users = await get_active_users(db=db)

    return PlainTextResponse(
        f"""
active_users {active_users}
cpu_usage_percent {cpu}
memory_usage_percent {memory}
network_megabytes_sent {network.bytes_sent / 1024 ** 2:.2f}
network_megabytes_received {network.bytes_recv / 1024 ** 2:.2f}
active_login_sessions {active_login_sessions}
"""
    )
