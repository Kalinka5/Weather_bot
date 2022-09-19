from aiogram.utils import executor
from create_bot import dp

from handlers import client
# , admin
client.register_handlers_client(dp)

# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
